import pytest
from rest_framework.reverse import reverse


@pytest.fixture
def user_data(django_user_model):
    return django_user_model.objects.create_user(username="ravi", password="12345", first_name="Ravi",
                                                 last_name="Ranjan", email="ezekie.em@gmail.com",
                                                 phone=1234567890, location="TataNagar")


@pytest.mark.django_db
def test_registration_successful(client, django_user_model):
    url = reverse("registration")
    data = {"username": "ravi", "password": "12345", "first_name": "Ravi", "last_name": "Ranjan",
            "email": "ezekie.em@gmail.com", "phone": 1234567890, "location": "TataNagar"}
    response = client.post(url, data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_registration_unsuccess(client, django_user_model, user_data):
    url = reverse("registration")
    user_data.save()
    data = {"username": "ravi", "password": "12345", "first_name": "Ravi", "last_name": "Ranjan",
            "email": "ezekie.em@gmail.com", "phone": 1234567890, "location": "TataNagar"}
    response = client.post(url, data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_login_successful(client, django_user_model, user_data):
    user_data.save()
    url = reverse("loginapi")
    login_data = {"username": "ravi", "password": "12345"}
    response = client.post(url, login_data, content_type='application/json')
    assert response.status_code == 202


@pytest.mark.django_db
def test_unsuccessful_login_api(client, django_user_model):
    url = reverse("loginapi")
    login_data = {"username": "ravi", "password": "12345"}
    response = client.post(url, login_data, content_type='application/json')
    assert response.status_code == 400
