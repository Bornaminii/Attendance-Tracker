import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_health(api_client):
    response = api_client.get("/api/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_manage_check():
    call_command("check")
