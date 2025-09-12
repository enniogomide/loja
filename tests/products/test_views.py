import json

import pytest
from django.test import Client, RequestFactory

from products.models import Product
from products.views import ProductDetailView, ProductListView
from tests.factories import product_to_create, products_to_create


@pytest.mark.django_db
class TestProductListView:
    @pytest.fixture
    def view(self):
        return ProductListView()

    @pytest.fixture
    def rf(self):
        return RequestFactory()

    @pytest.fixture
    def client(self):
        return Client()

    @pytest.fixture
    def created_product(self):
        product = product_to_create()
        return Product.objects.create(**product)

    @pytest.fixture
    def created_products(self):
        products = products_to_create()
        created_products = [Product.objects.create(**product) for product in products]
        return created_products

    @pytest.fixture
    def sample_product(self):
        return Product.objects.create(name="Test Product", price=10.00)

    def test_get_returns_all_products(self, rf, created_products):
        request = rf.get('/products/')
        response = ProductListView.as_view()(request)
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data) == len(created_products)
        for item, prod in zip(data, created_products):
            assert item['name'] == prod.name
            assert float(item['price']) == prod.price
            assert item['quantity'] == prod.quantity
            assert item['is_active'] == prod.is_active
            assert item['created_at'] == prod.created_at.strftime(
                '%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            assert item['updated_at'] == prod.updated_at.strftime(
                '%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            assert item['id'] == str(prod.id)

    def test_post_creates_new_product(self, client):
        data = {'name': 'New Product', 'price': '20.00', 'quantity': 5}
        request = client.post('/products/', data)
        response = ProductListView.as_view()(request)

        assert response.status_code == 201
        response_data = json.loads(response.content)
        assert response_data['name'] == 'New Product'
        assert Product.objects.count() == 1

    def test_post_invalid_data_missing_attributes(self, client):
        # Missing required field
        data = {'name': 'New Product'}
        response = client.post('/products/', data)

        # This will depend on how you handle errors in your service
        assert response.status_code == 400
        assert "Dados incompletos para criar o produto" in response.json()['error']


@pytest.mark.django_db
class TestProductDetailView:
    @pytest.fixture
    def view(self):
        return ProductDetailView()

    @pytest.fixture
    def rf(self):
        return RequestFactory()

    @pytest.fixture
    def sample_product(self):
        return Product.objects.create(name="Test Product", price=10.00)

    def test_get_existing_product(self, rf, sample_product):
        request = rf.get(f'/products/{sample_product.id}/')
        response = ProductDetailView.as_view()(request, product_id=sample_product.id)

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['name'] == 'Test Product'

    def test_get_nonexistent_product(self, rf):
        request = rf.get('/products/999/')
        response = ProductDetailView.as_view()(request, product_id=999)

        assert response.status_code == 404
        data = json.loads(response.content)
        assert data['error'] == 'Product not found'

    def test_put_updates_existing_product(self, rf, sample_product):
        # Note: Django's RequestFactory doesn't support PUT data natively
        # We need to handle this manually
        data = {'name': 'Updated Product', 'price': '15.00'}
        request = rf.put(
            f'/products/{sample_product.id}/',
            data=json.dumps(data),
            content_type='application/json'
        )

        # For PUT data, we need to add it to the request manually
        request.PUT = data

        response = ProductDetailView.as_view()(request, product_id=sample_product.id)

        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['message'] == 'Updated successfully'

        # Verify the product was actually updated
        sample_product.refresh_from_db()
        assert sample_product.name == 'Updated Product'
        assert sample_product.price == 15.00

    def test_put_nonexistent_product(self, rf):
        data = {'name': 'Updated Product'}
        request = rf.put(
            '/products/999/',
            data=json.dumps(data),
            content_type='application/json'
        )
        request.PUT = data

        response = ProductDetailView.as_view()(request, product_id=999)

        assert response.status_code == 404
        data = json.loads(response.content)
        assert data['error'] == 'Product not found'

    def test_delete_existing_product(self, rf, sample_product):
        request = rf.delete(f'/products/{sample_product.id}/')
        response = ProductDetailView.as_view()(request, product_id=sample_product.id)

        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['message'] == 'Deleted successfully'
        assert Product.objects.count() == 0

    def test_delete_nonexistent_product(self, rf):
        request = rf.delete('/products/999/')
        response = ProductDetailView.as_view()(request, product_id=999)

        assert response.status_code == 404
        data = json.loads(response.content)
        assert data['error'] == 'Product not found'
