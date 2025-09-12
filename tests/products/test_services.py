import uuid

import pytest

from products.models import Product
from products.services.product_service import ProductService
from tests.factories import product_to_create, products_to_create


@pytest.mark.django_db
class TestProductService:
    @pytest.fixture
    def service(self):
        return ProductService()

    @pytest.fixture
    def created_product(self, service):
        product = product_to_create()
        return service.create_product(product)

    @pytest.fixture
    def created_products(self, service):
        products = products_to_create()
        created_products = [service.create_product(product) for product in products]
        return created_products

    def test_get_all_products_in_the_db(self, service, created_products):
        seven = 7
        assert len(created_products) == seven
        products = service.get_all_products()
        encontrou_produto = False
        for product in created_products:
            if products.first().id == product.id:
                encontrou_produto = True
                assert products.first().id == product.id
                assert products.first().name == product.name
                assert products.first().quantity == product.quantity
                assert products.first().price == product.price
                assert products.first().is_active is True
                assert products.first().created_at == product.created_at
                assert products.first().updated_at == product.updated_at
        assert encontrou_produto is True

    def test_get_product_by_id_exists(self, service, created_product):
        product = service.get_product_by_id(created_product.id)
        assert product is not None
        assert product.name == created_product.name

    def test_get_product_by_id_not_exists(self, service):
        product = service.get_product_by_id(uuid.uuid4())
        assert product is None

    def test_create_product(self, service):
        data = {"name": "New Product", "price": '20.00', "quantity": '50'}
        product = service.create_product(data)
        assert product.id is not None
        assert product.name == data["name"]

    def test_update_product_exists(self, service, created_product):
        created_product.name = "Updated Product"
        created_product.price = 15.00
        updated = service.update_product(data_to_update=created_product.to_update())
        product_updated = Product(**updated[0])
        assert product_updated.name == created_product.name
        assert product_updated.quantity == created_product.quantity
        assert product_updated.price == created_product.price
        assert product_updated.id == created_product.id
        assert product_updated.is_active == created_product.is_active
        assert product_updated.created_at == created_product.created_at
        assert product_updated.updated_at >= created_product.updated_at

    def test_update_product_not_exists(self, service, created_product):
        zero = 0
        created_product.name = "Updated Product"
        created_product.price = 15.00
        created_product.id = uuid.uuid4()
        updated = service.update_product(data_to_update=created_product.to_update())
        assert len(updated) == zero

    def test_delete_product_exists(self, service, created_product):
        result = service.delete_product(created_product.id)
        assert result is True

    def test_delete_product_not_exists(self, service, created_product):
        result = service.delete_product(uuid.uuid4())
        assert result is False

    def test_get_latest_products(self, service, created_products):
        latest = service.get_latest_products(2)
        assert latest is not None
        assert latest[0].created_at >= latest[1].created_at
        assert latest.count() == 2
        assert latest[0].name == created_products[6].name
        assert latest[1].name == created_products[5].name
