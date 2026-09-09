import pytest


pytestmark = pytest.mark.integration


def test_list_services_public(client):
    response = client.get("/api/v1/services/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_service_not_found(client):
    response = client.get("/api/v1/services/9999")

    assert response.status_code == 404


def test_admin_can_create_service(client, admin_auth):
    response = client.post(
        "/api/v1/admin/services",
        headers=admin_auth,
        json={
            "name": "Website Development",
            "description": "Custom website development service",
            "price": 50000,
            "is_active": True,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Website Development"
    assert data["price"] == "50000.00"
    assert data["is_active"] is True


def test_customer_cannot_create_service(client, customer_auth):
    response = client.post(
        "/api/v1/admin/services",
        headers=customer_auth,
        json={
            "name": "Unauthorized Service",
            "description": "Should not be created",
            "price": 1000,
            "is_active": True,
        },
    )

    assert response.status_code == 403


def test_admin_can_update_service(client, admin_auth):
    create_response = client.post(
        "/api/v1/admin/services",
        headers=admin_auth,
        json={
            "name": "Old Service",
            "description": "Old description",
            "price": 10000,
            "is_active": True,
        },
    )

    service_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/admin/services/{service_id}",
        headers=admin_auth,
        json={
            "name": "Updated Service",
            "price": 15000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Service"
    assert data["price"] == "15000.00"


def test_admin_can_deactivate_service(client, admin_auth):
    create_response = client.post(
        "/api/v1/admin/services",
        headers=admin_auth,
        json={
            "name": "Temporary Service",
            "description": "Temporary",
            "price": 5000,
            "is_active": True,
        },
    )

    service_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/admin/services/{service_id}",
        headers=admin_auth,
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/api/v1/services/{service_id}"
    )

    assert get_response.status_code == 200
    assert get_response.json()["is_active"] is False