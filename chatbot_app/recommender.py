import re

from dataclasses import dataclass

from typing import Optional, List, Dict

from django.db.models import Q


# --------- DOMAIN: keywords -----------

CATEGORY_KEYWORDS = {
    "office": ["office", "work", "formal", "meeting", "corporate"],
    "party":  ["party", "wedding", "reception", "night", "club"],
    "casual": ["casual", "daily", "home", "comfortable", "regular"],
    "sports": ["sports", "gym", "workout", "fitness", "running"],
}

PRODUCT_TYPES = [
    "dress", "kurta", "top", "tshirt", "jeans", "skirt", "lehenga", "gown", "co-ord", "coordset", "jumpsuit"
]

COLORS = ["black","white","blue","red","pink","green","beige","brown","grey","gray","purple","yellow","orange","maroon","navy",'mustard yellow']

MATERIALS = ["cotton","silk","linen","polyester","denim","rayon","georgette","chiffon","satin","wool","crepe"]


# This is like a “result object” that stores what we understood from user sentence.

@dataclass
class ParsedQuery:
    intent: Optional[str] = None
    max_price: Optional[int] = None
    min_price: Optional[int] = None
    color: Optional[str] = None
    material: Optional[str] = None
    product_type: Optional[str] = None
    raw: str = ""


def _detect_intent(text: str) -> Optional[str]:

    t = text.lower()

    for intent, keys in CATEGORY_KEYWORDS.items():

        if any(k in t for k in keys):

            return intent
        
    return None


def _detect_price(text: str):
   

    t = text.lower()

    max_m = re.search(r"(under|below|less than)\s*(\d+)", t)

    min_m = re.search(r"(above|more than|over)\s*(\d+)", t)

    max_price = int(max_m.group(2)) if max_m else None

    min_price = int(min_m.group(2)) if min_m else None

    return min_price, max_price


def _detect_color(text: str) -> Optional[str]:

    t = text.lower()

    for c in COLORS:

        if c in t:

            return c
        
    return None


def _detect_material(text: str) -> Optional[str]:

    t = text.lower()

    for m in MATERIALS:

        if m in t:

            return m
        
    return None


def _detect_product_type(text: str) -> Optional[str]:

    t = text.lower()

    for p in PRODUCT_TYPES:

        if p in t:
            
            return "co-ord" if p in ["coordset", "co-ord"] else p
        
    return None


def parse_user_query(message: str) -> ParsedQuery:


    # ensures message is not None, removes extra spaces.
    msg = (message or "").strip()

    # calls all helper functions
    intent = _detect_intent(msg)

    min_price, max_price = _detect_price(msg)

    color = _detect_color(msg)

    material = _detect_material(msg)

    product_type = _detect_product_type(msg)

    return ParsedQuery(
        intent=intent,
        min_price=min_price,
        max_price=max_price,
        color=color,
        material=material,
        product_type=product_type,
        raw=msg
    )


def style_tips_for_product(product, intent: Optional[str] = None) -> List[str]:
    
    # Creates an empty list.
    tips: List[str] = []
    
    # Gets the product name from DB: product.name
    name = (product.name or "").lower()

    color = (product.color or "").lower()

    material = (product.material or "").lower()

    # Intent-based
    if intent == "office":
        tips += [
            "Pair with loafers or block heels for a clean formal look.",
            "Carry a structured tote bag and minimal jewelry (studs + watch).",
            "Layer with a blazer or long shrug for a professional finish."
        ]
    elif intent == "party":
        tips += [
            "Add statement earrings and a clutch to elevate the outfit.",
            "Wear heels/strappy sandals and go for a sleek hairstyle.",
            "Add a bold lipstick or winged eyeliner for a party-ready look."
        ]
    elif intent == "casual":
        tips += [
            "Style with sneakers or flats for comfort.",
            "Add a sling bag and light accessories (hoops/bracelet).",
            "Keep makeup minimal and hair open or in a messy bun."
        ]
    elif intent == "sports":
        tips += [
            "Wear trainers and keep accessories minimal.",
            "Go for a ponytail/bun; add a cap if needed.",
            "Choose breathable layers and a lightweight bag."
        ]

    # Material-based
    if "cotton" in material or "linen" in material:
        tips.append("Cotton/linen looks best with simple accessories and natural makeup.")
    if "silk" in material or "satin" in material:
        tips.append("Silk/satin looks premium—style with heels and metallic accessories.")

    # Color-based
    if "black" in color:
        tips.append("Black pairs beautifully with gold/silver jewelry and bold lipstick.")
    if "white" in color or "beige" in color:
        tips.append("Light shades look great with nude heels and pastel bags.")
    if "red" in color:
        tips.append("Keep accessories neutral so red remains the highlight.")

    # Type hints
    if "kurta" in name:
        tips.append("Complete with palazzo/straight pants and juttis; add a dupatta for elegance.")
    if "dress" in name: 
        tips.append("Add a belt to define the waist; a denim jacket also works nicely.")
   
    # Deduplicate
    seen = set()

    result = []

    for t in tips:

        if t not in seen:

            seen.add(t)

            result.append(t)

    return result[:6]


def recommend_products(ProductModel, parsed: ParsedQuery, limit: int = 6):
    """
    Recommendation Engine:
    - Filters by intent/category, price range, color/material if fields exist
    - Also does simple text match on name/description
    """
    qs = ProductModel.objects.all()

    # Category/intent filter (assumes FK category with name)
    # If your model differs, adjust this line.
    if parsed.intent:
        qs = qs.filter(category__name__icontains=parsed.intent)

    # Price range (assumes field: price)
    if parsed.min_price is not None:
        qs = qs.filter(price__gte=parsed.min_price)
    if parsed.max_price is not None:
        qs = qs.filter(price__lte=parsed.max_price)

    # Optional: color/material fields
    if parsed.color and hasattr(ProductModel, "color"):
        qs = qs.filter(color__icontains=parsed.color)

    if parsed.material and hasattr(ProductModel, "material"):
        qs = qs.filter(material__icontains=parsed.material)

    if parsed.product_type and hasattr(ProductModel, "product_type"):
        qs = qs.filter(product_type__icontains=parsed.product_type)

    # NLP-ish: match remaining keywords in name/description
    words = [w for w in parsed.raw.lower().split() if len(w) > 2]
    if words:
        q = Q()
        for w in words:
            if hasattr(ProductModel, "description"):
                q &= (Q(name__icontains=w) | Q(description__icontains=w))
            else:
                q &= Q(name__icontains=w)
        qs = qs.filter(q)

    return qs.order_by("-id")[:limit]
