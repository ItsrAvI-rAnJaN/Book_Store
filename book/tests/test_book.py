import pytest
import json
from django.urls import reverse

url = reverse('bookapi')


@pytest.fixture
def get_token_header(django_user_model, client):
    user = django_user_model.objects.create_user(username='ravi', first_name="ravi", last_name="ranjan",
                                                 email='ezekie.em@gmail.com', password='12345', location='abc',
                                                 phone=1234567890, is_superuser=True)
    url = reverse('loginapi')
    data = {'username': 'ravi', 'password': '12345'}
    response = client.post(url, data, content_type="application/json")

    json_data = json.loads(response.content)
    token = json_data['data']
    header = {'HTTP_TOKEN': token, "content_type": "application/json"}
    return user, header


@pytest.fixture
def book_details(get_token_header):
    user, header = get_token_header
    return {
        "title": "hy",
        "author": "kali",
        "price": 500,
        "quantity": 20,
        "user": user.id}


@pytest.fixture
def book_update_data(client, get_token_header, book_details):
    user, header = get_token_header
    response = client.post(url, book_details, **header)
    json_data = json.loads(response.content)
    book_id = json_data['data']['id']
    return {'id': book_id,
            "title": "hey",
            "author": "kali",
            "price": 600,
            "quantity": 20}


@pytest.fixture
def book_delete_data(client, get_token_header, book_details):
    user, header = get_token_header
    response = client.post(url, book_details, **header)
    json_data = json.loads(response.content)
    book_id = json_data['data']['id']
    data = {'id': book_id}
    return data


class TestBooksAPI:

    @pytest.mark.django_db
    def test_response_as_create_book_successfully(self, client, get_token_header, book_details):
        user, header = get_token_header
        response = client.post(url, book_details, **header)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_response_as_create_book_unsuccessfully(self, client, get_token_header, book_details):
        response = client.post(url, book_details)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_get_books(self, client, get_token_header, book_details):
        user, header = get_token_header
        response = client.post(url, book_details, **header)
        assert response.status_code == 201
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_response_as_update_books_successfully(self, client, get_token_header, book_update_data):
        user, header = get_token_header
        response = client.put(url, book_update_data, **header)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_response_as_update_books_unsuccessfully(self, client, get_token_header, book_update_data):
        response = client.put(url, book_update_data, )
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_delete_books_successfully(self, client, get_token_header, book_delete_data):
        user, header = get_token_header
        response = client.delete(url, book_delete_data, **header)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_response_as_delete_books_unsuccessfully(self, client, get_token_header, book_delete_data):
        response = client.delete(url, book_delete_data)
        assert response.status_code == 400
