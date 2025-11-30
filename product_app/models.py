from django.db import models

from django.utils.text import slugify


class CategoryModel(models.Model):

    name = models.CharField(max_length=100, unique=True)

    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):

        return self.name


class ProductModel(models.Model):

    SIZE_CHOICES = [
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
        ("3XL", "3XL"),
        ("4XL", "4XL"),
    ]

    name = models.CharField(max_length=200)

    slug = models.SlugField(unique=True, blank=True)

    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.TextField()

    image = models.ImageField(upload_to='products/')

    stock = models.PositiveIntegerField(default=0)

    sizes_available = models.CharField(max_length=50, help_text="Use comma separated values e.g. XS,S,M")

    material = models.CharField(max_length=100, blank=True, null=True)

    color = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):

        if not self.slug:

            base_slug = slugify(self.name)

            slug = base_slug

            counter = 1

            while ProductModel.objects.filter(slug=slug).exists():

                slug = f"{base_slug}-{counter}"

                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def get_sizes_list(self):
    
            if not self.sizes_available:

                return []
            
            return [s.strip() for s in self.sizes_available.split(",") if s.strip()]


    def __str__(self):

        return self.name
    

# get_sizes_list() converts that string into a Python list:

# ["XS", "S", "M", "L", "XL"]

# This list is what you use in the template to build the <select> options
    

