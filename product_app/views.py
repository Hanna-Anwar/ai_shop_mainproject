from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.

from product_app.models import ProductModel,CategoryModel

from django.views.generic import ListView, DetailView

#listing in product entered in dashboard to frontend
class ProductListView(ListView):

    model = ProductModel

    template_name = "product_list.html"

    context_object_name = "products"

    def get_queryset(self):

        queryset = ProductModel.objects.filter(is_active=True)

        category_slug = self.request.GET.get("category")  # read ?category=slug from URL
        
        if category_slug:

            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
         
        # get cat_name,slug
        
        context["categories"] = CategoryModel.objects.all() 

        context["selected_category"] = self.request.GET.get("category")

        return context
    

#      Variable	                 Purpose
#     categories	            To show category buttons in UI
#    selected_category	         To highlight active category and know which is selected


class ProductDetailView(DetailView):

    model = ProductModel

    template_name = "product_detail.html"

    context_object_name = "product"

    slug_field = "slug"

    slug_url_kwarg = "slug"

# slug_url_kwarg = "slug" → take this value from kwargs["slug"]

# slug_field = "slug" → search in the model’s slug field

