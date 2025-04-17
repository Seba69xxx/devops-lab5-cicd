from fastapi.testclient import TestClient
import sys
import os
import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

try:
    from src.main import app
except ImportError as e:
    print(f"Не удалось импортировать 'app' из 'src.main'. Ошибка: {e}")
    raise ImportError(f"Не удалось импортировать 'app' из 'src.main'. Проверьте PYTHONPATH и структуру проекта. Ошибка: {e}") from e

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
    assert isinstance(response_data, int), f"Ожидался int (ID пользователя), получено: {type(response_data)}"
    assert response_data > 0, "Ожидался положительный ID пользователя"

def test_create_user_with_invalid_email():
    conflicting_user_data = {
        'name': 'Another Ivan',
        'email': existing_user_1_email, 
    }
    response = client.post("/api/v1/user", json=conflicting_user_data)
    assert response.status_code == 409

def test_delete_user():
    user_to_delete_data = {
        'name': 'User ToDelete',
        'email': 'delete.me@example.com'
    }
    create_response = client.post("/api/v1/user", json=user_to_delete_data)
    assert create_response.status_code == 201, "Не удалось создать пользователя для теста удаления"
    user_id_created = create_response.json()
    assert isinstance(user_id_created, int), "Создание пользователя не вернуло ID"
    email_to_delete = user_to_delete_data['email']
    delete_response = client.delete("/api/v1/user", params={'email': email_to_delete})
    assert delete_response.status_code == 204, f"Ожидался статус 204 при удалении, получен {delete_response.status_code}"
    get_response_check = client.get("/api/v1/user", params={'email': email_to_delete})
    assert get_response_check.status_code == 404, f"Ожидался статус 404 после удаления, получен {get_response_check.status_code}"
