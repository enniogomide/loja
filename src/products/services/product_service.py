from core.middleware.exceptions import BusinessValidationError
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
        if "quantity" not in product_data or "price" not in product_data:
            raise BusinessValidationError(
                message='Dados incompletos para criar o produto: '
                'é necessário "Nome", "quantidade" e "preço"',
                code=400
            )

        if int(product_data["quantity"]) < 0:
            raise BusinessValidationError(
                message='Quantidade não pode ser zero e nem negativa',
                code=400
            )
        if float(product_data["price"]) < 0:
            raise BusinessValidationError(
                message='Preço não pode ser zero e nem negativo',
                code=400
            )

        return self.repository.create(product_data)

    def update_product(self, **data):
        return self.repository.update(**data)

    def delete_product(self, product_id):
        return self.repository.delete(product_id)

    def get_latest_products(self, limit=10):
        return self.repository.get_latest_products(limit)
