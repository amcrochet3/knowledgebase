from django.urls import reverse
import pytest
from django.test import Client

client = Client()

pytestmark = pytest.mark.django_db
ASSET_TYPE_URL = reverse("asset-type-list")
TOPIC_AREA_URL = reverse("topic-area-list")


def test_asset_type(asset_type):
    response = client.get(ASSET_TYPE_URL)
    assert response.json()[0]["name"] == asset_type.name


def test_topic_area(topic_area):
    response = client.get(TOPIC_AREA_URL)
    assert response.json()[0]["name"] == topic_area.name