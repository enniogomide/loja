import pytest

from products.models import Product


@pytest.mark.django_db
class TestProductModel:
    def test_check_for_product_attributes_and_creation(self):
        product = Product.objects.create(
            name="Teclado",
            quantity=200,
            price=150.00)
        assert hasattr(product, 'created_at')
        assert hasattr(product, 'updated_at')
        assert hasattr(product, 'is_active')
        assert product.name == "Teclado"
        assert product.quantity == 200
        assert product.price == 150.00
        assert str(product) == "Teclado"
