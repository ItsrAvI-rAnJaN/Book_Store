import pytest
from rest_framework.reverse import reverse

BOOK_URL = reverse("bookapi")


@pytest.fixture
def user_response(client, db):
    user_url = reverse("registration")
    data = {"username": "ravi", "password": "12345", "first_name": "Ravi", "last_name": "Ranjan",
            "email": "ezekie.em@gmail.com", "phone": 1234567890, "location": "TataNagar"}
    return client.post(user_url, data)


class Testbookapi:

    @pytest.mark.django_db
    def test_book_creation_successful(self, client, django_user_model, user_response):
        book_list = {"title": "hey", "author": "kali", "price": 200, "quantity": 10,
                     "user": user_response.data.get("data").get("id")}
        note_response = client.post(BOOK_URL, book_list)
        assert note_response.status_code == 201

    @pytest.mark.django_db
    def test_book_creation_unsuccessful_validation_error(self, client, django_user_model, user_response):
        book_list = {"title": "hey", "author": "kali", "price": 200, "quantity": 10,
                     "user": "abc"}
        note_response = client.post(BOOK_URL, book_list)
        assert note_response.status_code == 400

    @pytest.mark.django_db
    def test_book_retrieve_successful(self, client, user_response):
        book_list = {"title": "hey", "author": "kali", "price": 200, "quantity": 10,
                     "user": user_response.data.get("data").get("id")}
        note_response = client.post(BOOK_URL, book_list)
        note_user_id = {"user": note_response.data.get("data").get("user")}
        note_user_id_response = client.get(BOOK_URL, note_user_id, content_type='application/json')
        assert note_user_id_response.status_code == 200

    @pytest.mark.django_db
    def test_book_update_successful(self, client, user_response):
        book_list = {"title": "hey", "author": "kali", "price": 200, "quantity": 10,
                     "user": user_response.data.get("data").get("id")}
        book_response = client.post(BOOK_URL, book_list, content_type='application/json')
        book_id = book_response.data.get("data").get("id")
        new_note_data = {"id": book_id, "title": "hey", "author": "kali", "price": 200,
                         "quantity": 10,
                         "user": user_response.data.get("data").get("id")}
        update_response = client.put(BOOK_URL, new_note_data, content_type='application/json')
        assert update_response.status_code == 201

    @pytest.mark.django_db
    def test_book_update_unsuccessful(self, client, user_response):
        book_list = {"title": "hey", "author": "kali", "price": 200, "quantity": 10,
                     "user": user_response.data.get("data").get("id")}
        client.post(BOOK_URL, book_list, content_type='application/json')
        new_note_data = {"title": "hey", "author": "tod", "price": 200, "quantity": 10,
                         "user": user_response.data.get("data").get("id")}
        update_response = client.put(BOOK_URL, new_note_data, content_type='application/json')
        assert update_response.status_code == 400

    @pytest.mark.django_db
    def test_book_delete_successful(self, client, user_response):
        book_list = {"title": "hey", "author": "kali", "price": 200, "quantity": 10,
                     "user": user_response.data.get("data").get("id")}
        book_response = client.post(BOOK_URL, book_list)
        book_id = {"id": book_response.data.get("data").get("id")}
        delete_response = client.delete(BOOK_URL, book_id, content_type='application/json')
        assert delete_response.status_code == 200

    @pytest.mark.django_db
    def test_book_delete_unsuccessful_bad_request(self, client, user_response):
        book_list = {"title": "hey", "author": "kali", "price": 200, "quantity": 10,
                     "user": user_response.data.get("data").get("id")}
        client.post(BOOK_URL, book_list)
        book_id = {"id": "abc"}
        delete_response = client.delete(BOOK_URL, book_id, content_type='application/json')
        assert delete_response.status_code == 400
