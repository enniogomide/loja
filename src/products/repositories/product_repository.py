from django.core.exceptions import ObjectDoesNotExist

from products.models import Product


class ProductRepository:
    @staticmethod
    def get_all():
        return Product.objects.all()

    @staticmethod
    def get_by_id(product_id):
        try:
            return Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(product):
        return Product.objects.create(
            name=product["name"],
            price=product["price"],
            quantity=product["quantity"],
        )

    @staticmethod
    def update(**kwargs):
        products = []
        for data_key, data_value in kwargs.items():
            if data_key == "data_to_update":
                product = ProductRepository.get_by_id(data_value["id"])
                if product:
                    for key, value in data_value.items():
                        if key != "id":
                            setattr(product, key, value)
                    product.save()
                    products.append(product.to_dict())
        return products

    @staticmethod
    def delete(product_id):
        product = ProductRepository.get_by_id(product_id)
        if product:
            product.delete()
            return True
        return False

    @staticmethod
    def get_latest_products(limit=10):
        return Product.objects.order_by("-created_at")[:limit]
