# from django.shortcuts import render

# # Create your views here.
# from django.http import JsonResponse
# from django.views.decorators.http import require_POST
# from django.views.decorators.csrf import csrf_exempt

# from product_app.models import ProductModel
# from .recommender import parse_user_query, recommend_products, style_tips_for_product


# @csrf_exempt
# @require_POST
# def chat_ask(request):
#     message = request.POST.get("message", "").strip()
#     if not message:
#         return JsonResponse({"reply": "Type something like: 'office wear under 1500' 😊", "products": []})

#     parsed = parse_user_query(message)
#     products_qs = recommend_products(ProductModel, parsed, limit=6)

#     products = []
#     for p in products_qs:
#         products.append({
#             "id": p.id,
#             "name": p.name,
#             "price": str(p.price),
#             "image": p.image.url if p.image else None,
#             "detail_url": f"/product/{p.slug}/",   # ✅ best for your model (slug exists)
#             "styling_tips": style_tips_for_product(p, intent=parsed.intent),
#         })

#     reply = "Here are some matches from our store 👇" if products else "No match found. Try: 'party wear red dress under 2000'."

#     return JsonResponse({
#         "reply": reply,
#         "understood": {
#             "intent": parsed.intent,
#             "min_price": parsed.min_price,
#             "max_price": parsed.max_price,
#             "color": parsed.color,
#             "material": parsed.material,
#             "product_type": parsed.product_type,
#         },
#         "products": products
#     })


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from product_app.models import ProductModel
from .recommender import parse_user_query, recommend_products, style_tips_for_product


@csrf_exempt
@require_POST
def chat_ask(request):
    try:
        message = request.POST.get("message", "").strip()

        if not message:
            return JsonResponse({
                "reply": "Type something like: 'office wear under 1500' 😊",
                "products": []
            })

        parsed = parse_user_query(message)
        products_qs = recommend_products(ProductModel, parsed, limit=6)

        products = []
        for p in products_qs:
            products.append({
                "id": p.id,
                "name": p.name,
                "price": str(p.price),
                "image": p.image.url if getattr(p, "image", None) else None,
                "detail_url": f"/product/{p.slug}/" if getattr(p, "slug", None) else "#",
                "styling_tips": style_tips_for_product(p, intent=parsed.intent),
            })

        reply = (
            "Here are some matches from our store 👇"
            if products else
            "No match found. Try: 'party wear red dress under 2000'."
        )

        return JsonResponse({
            "reply": reply,
            "understood": {
                "intent": parsed.intent,
                "min_price": parsed.min_price,
                "max_price": parsed.max_price,
                "color": parsed.color,
                "material": parsed.material,
                "product_type": parsed.product_type,
            },
            "products": products
        })

    except Exception as e:
        print("CHATBOT ERROR:", str(e))
        return JsonResponse({
            "reply": f"Server error: {str(e)}",
            "products": []
        }, status=500)