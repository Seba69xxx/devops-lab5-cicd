from fastapi.testclient import TestClient
import sys
import os
import pytest # Импортируем pytest для возможного использования маркеров или фикстур в будущем

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

# existing_user_2_id = users_data[1]['id'] # Эта переменная больше не нужна напрямую для теста удаления
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
    # --- ИСПРАВЛЕНИЕ 1: Проверяем, что ответ - это ID (целое число) ---
    assert isinstance(response_data, int), f"Ожидался int (ID пользователя), получено: {type(response_data)}"
    assert response_data > 0, "Ожидался положительный ID пользователя"
    # --- Конец ИСПРАВЛЕНИЯ 1 ---

def test_create_user_with_invalid_email():
    conflicting_user_data = {
        'name': 'Another Ivan',
        'email': existing_user_1_email,
    }
    response = client.post("/api/v1/user", json=conflicting_user_data)
    assert response.status_code == 409

def test_delete_user():
    # --- ИСПРАВЛЕНИЕ 2: Сначала создаем пользователя, чтобы точно знать, что он есть ---
    user_to_delete_data = {
        'name': 'User ToDelete',
        'email': 'delete.me@example.com'
    }
    create_response = client.post("/api/v1/user", json=user_to_delete_data)
    assert create_response.status_code == 201, "Не удалось создать пользователя для теста удаления"
    user_id_to_delete = create_response.json()
    assert isinstance(user_id_to_delete, int), "Создание пользователя не вернуло ID для теста удаления"
    # --- Конец части создания ---

    # Теперь удаляем только что созданного пользователя
    delete_url = f"/api/v1/user/{user_id_to_delete}"
    response = client.delete(delete_url)
    # Проверяем статус ответа на удаление
    assert response.status_code == 200, f"Ожидался статус 200 при удалении, получен {response.status_code}"

    # Проверяем, что пользователь действительно удален
    get_deleted_url = f"/api/v1/user/{user_id_to_delete}"
    response_check = client.get(get_deleted_url)
    # Ожидаем 404 после удаления
    assert response_check.status_code == 404, f"Ожидался статус 404 после удаления, получен {response_check.status_code}"
    # --- Конец ИСПРАВЛЕНИЯ 2 ---
