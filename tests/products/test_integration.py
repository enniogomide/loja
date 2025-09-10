import pytest

from products.services.product_service import ProductService


@pytest.mark.django_db
def test_full_test_for_product():
    ProductService.create_product("Caderno", 15.00, 30)
    products = ProductService.get_all()
    assert any(p.name == "Caderno" for p in products)
