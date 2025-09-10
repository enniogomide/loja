import uuid
from datetime import datetime

import pytest
import pytz

from products.models import Product
from products.repositories.product_repository import ProductRepository
from tests.factories import product_to_create, products_to_create


@pytest.mark.django_db
class TestProductRepository:
    @pytest.fixture
    def repository(self):
        return ProductRepository()

    @pytest.fixture
    def created_product(self, repository):
        product = product_to_create()
        return repository.create(product)

    @pytest.fixture
    def created_products(self, repository):
        products = products_to_create()
        created_products = [repository.create(product) for product in products]
        return created_products

    def test_get_all(self, repository, created_products):
        seven = 7
        assert len(created_products) == seven
        products = repository.get_all()
        assert products.count() == seven
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

    def test_get_by_id_exists(self, repository, created_product):
        product = repository.get_by_id(created_product.id)
        assert product is not None
        assert product.name == created_product.name
        assert product.quantity == created_product.quantity
        assert product.price == created_product.price
        assert product.is_active is True
        assert product.created_at == created_product.created_at
        assert product.updated_at == created_product.updated_at

    def test_get_by_id_not_exists(self, repository):
        product = repository.get_by_id(999)
        assert product is None

    def test_create_product(
        self,
        repository,
    ):
        product_new = {"name": "New Product", "price": 20.00, "quantity": 100}
        product = repository.create(product_new)
        total_products = 1
        assert product.id is not None
        assert product.name == product_new["name"]
        assert product.price == product_new["price"]
        assert product.quantity == product_new["quantity"]
        current_time_utc = datetime.now(pytz.UTC)
        assert product.created_at < current_time_utc
        assert product.updated_at < current_time_utc
        assert Product.objects.count() == total_products

    def test_update_product_exists(self, repository, created_product):
        updated = repository.get_by_id(created_product.id)
        updated.name = "Updated Product"
        updated.price = 15.0
        updated.quantity = 350
        products = repository.update(data_to_update=updated.to_update())
        assert products[0]["id"] == created_product.id
        assert products[0]["name"] == updated.name
        assert products[0]["quantity"] == updated.quantity
        assert products[0]["price"] == updated.price
        current_time_utc = datetime.now(pytz.UTC)
        assert updated.created_at == created_product.created_at
        assert products[0]["updated_at"] < current_time_utc
        assert products[0]["updated_at"] > created_product.created_at

    def test_update_product_not_exists(self, repository, created_product):
        created_product.id = uuid.uuid4()
        updated = repository.update(data_to_update=created_product.to_update())
        assert not updated

    def test_delete_product_exists(self, repository, created_product):
        result = repository.delete(created_product.id)
        total_products = 0
        assert result is True
        assert Product.objects.count() == total_products

    def test_delete_product_not_exists(self, repository):
        result = repository.delete(uuid.uuid4())
        assert result is False

    def test_get_latest_products(self, repository, created_products):
        # Create multiple products

        latest = repository.get_latest_products(2)
        assert latest.count() == 2
        assert latest[0].name == created_products[6].name
        assert latest[1].name == created_products[5].name
