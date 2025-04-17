from fastapi.testclient import TestClient
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

try:
    from src.main import app
except ImportError as e:
    print(f"Не удалось импортировать 'app' из 'src.main'. Ошибка: {e}")
    print(f"Текущий sys.path: {sys.path}")
    raise ImportError(f"Не удалось импортировать 'app' из 'src.main'. Проверьте структуру проекта. Ошибка: {e}") from e

client = TestClient(app)

users_data = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]
existing_user_1_email = users_data[0]['email']
existing_user_1_data = users_data[0]

existing_user_2_id = users_data[1]['id']
existing_user_2_email = users_data[1]['email']


def test_get_existed_user():
    response = client.get("/api/v1/user", params={'email': existing_user_1_email})
    assert response.status_code == 200
    assert response.json() == existing_user_1_data

def test_get_unexisted_user():
    non_existent_email = "non.existent@example.com"
    response = client.get("/api/v1/user", params={'email': non_existent_email})
    assert response.status_code == 404

def test_create_user_with_valid_email():
    new_user_data = {
        'name': 'Anna Karenina',
        'email': 'a.k.karenina@novel.com',
    }
    response = client.post("/api/v1/user", json=new_user_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data['name'] == new_user_data['name']
    assert response_data['email'] == new_user_data['email']
    assert 'id' in response_data

def test_create_user_with_invalid_email():
    conflicting_user_data = {
        'name': 'Another Ivan',
        'email': existing_user_1_email,
    }
    response = client.post("/api/v1/user", json=conflicting_user_data)
    assert response.status_code == 409

def test_delete_user():
    user_id_to_delete = existing_user_2_id
    delete_url = f"/api/v1/user/{user_id_to_delete}"
    response = client.delete(delete_url)
    assert response.status_code == 200

    get_deleted_url = f"/api/v1/user/{user_id_to_delete}"
    response_check = client.get(get_deleted_url)
    assert response_check.status_code == 404
