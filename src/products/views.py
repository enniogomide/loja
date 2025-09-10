from django.http import JsonResponse
# from django.views.generic import ListView, DetailView
from django.views import View
from django.shortcuts import render

from .models import Product
from .services.product_service import ProductService


class ProductListView(View):
    def get(self, request):
        service = ProductService()
        template_name = "products/list.html"
        products = service.get_all_products()
        data = [{"name": p.name, "price": str(p.price)} for p in products]
        return render(request, template_name, data)
        # return JsonResponse(data, safe=False)

    def post(self, request):
        service = ProductService()
        product = service.create_product(request.POST.dict())
        return JsonResponse({"id": product.id, "name": product.name}, status=201)


class ProductDetailView(View):
    def get(self, request, product_id):
        service = ProductService()
        template_name = "products/detail.html"
        product = service.get_product_by_id(product_id)
        if product:
            data = {"name": product.name, "price": str(product.price)}
            return render(request, template_name, data)
            # return JsonResponse()
        return JsonResponse({"error": "Product not found"}, status=404)

    def put(self, request, product_id):
        service = ProductService()
        data = request.PUT.dict()  # Nota: Django não suporta request.PUT nativamente; use um parser ou request.POST.
        product = service.update_product(product_id, data)
        if product:
            return JsonResponse({"message": "Updated successfully"})
        return JsonResponse({"error": "Product not found"}, status=404)

    def delete(self, request, product_id):
        service = ProductService()
        if service.delete_product(product_id):
            return JsonResponse({"message": "Deleted successfully"})
        return JsonResponse({"error": "Product not found"}, status=404)
