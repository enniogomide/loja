from products.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def get_all_products(self):
        return self.repository.get_all()

    def get_product_by_id(self, product_id):
        product = self.repository.get_by_id(product_id)
        if not product:
            return None
        return product

    def create_product(self, product_data):
        if product_data["quantity"] < 0:
            raise ValueError("Estoque não pode ser negativo")
        return self.repository.create(product_data)

    def update_product(self, **data):
        return self.repository.update(**data)

    def delete_product(self, product_id):
        return self.repository.delete(product_id)

    def get_latest_products(self, limit=10):
        return self.repository.get_latest_products(limit)
