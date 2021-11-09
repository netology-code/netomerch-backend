import pytest


def test_admin_page_available(client):
    response = client.get("/admin/")
    assert response.status_code == 302

    response = client.get("/admin/", follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_login(admin_client, admin_user):
    response = admin_client.get("/admin/")
    assert response.status_code == 200
    assert admin_user.username in response.rendered_content
