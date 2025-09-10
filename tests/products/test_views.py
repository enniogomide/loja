import pytest
from django.urls import reverse

from products.models import Product


@pytest.mark.django_db
def test_product_list_view(client):
    Product.objects.create(name="Tênis", price=199.90, quantity=5)
    url = reverse("product-list")
    response = client.get(url)
    assert response.status_code == 200
    assert "Tênis" in response.content.decode()
