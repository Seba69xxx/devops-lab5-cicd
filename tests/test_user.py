from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
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

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    pass

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    pass

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    pass

def test_delete_user():
    '''Удаление пользователя'''
    pass

import httpx
import pytest
from main import app # Убедитесь, что экземпляр вашего FastAPI приложения называется 'app' в main.py

# Базовый URL для тестового клиента
BASE_URL = "http://test"

# Существующий тест (для справки)
@pytest.mark.asyncio
async def test_get_existed_user():
    async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"user_id": 1, "username": "Alice"}

# --- TODO: Реализуйте следующие четыре теста ---

@pytest.mark.asyncio
async def test_get_non_existed_user():
    """Тест получения пользователя, которого не существует."""
    async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
        # Предполагаем, что пользователя с ID 999 нет в исходных данных
        response = await client.get("/users/999")
    # Согласно src/routers/user.py, получение несуществующего пользователя возвращает 404
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_user():
    """Тест создания нового пользователя."""
    new_user_data = {"username": "Charlie"}
    async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/users/", json=new_user_data)
    # Согласно src/routers/user.py, успешное создание возвращает 201
    assert response.status_code == 201
    # Тело ответа должно содержать данные нового пользователя, включая присвоенный ID
    # Предположим, что следующий ID будет 3 (если в исходных данных есть 1 и 2)
    # Примечание: Более надежный тест мог бы сначала получить всех пользователей, чтобы определить ожидаемый следующий ID
    response_data = response.json()
    assert response_data["username"] == "Charlie"
    assert "user_id" in response_data # Проверяем, был ли присвоен ID

@pytest.mark.asyncio
async def test_create_user_conflict():
    """Тест создания пользователя, чье имя уже существует."""
    # Alice уже существует в исходных данных
    existing_user_data = {"username": "Alice"}
    async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/users/", json=existing_user_data)
    # Согласно src/routers/user.py, создание пользователя с существующим именем возвращает 409
    assert response.status_code == 409

@pytest.mark.asyncio
async def test_delete_user():
    """Тест удаления существующего пользователя."""
    # Удалим Bob (user_id 2, предполагая исходные данные)
    user_id_to_delete = 2
    async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.delete(f"/users/{user_id_to_delete}")
    # Согласно src/routers/user.py, успешное удаление возвращает 200
    assert response.status_code == 200
    assert response.json() == {"message": f"User {user_id_to_delete} deleted"}

    # Опционально: Проверим, действительно ли пользователь удален
    async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
         response_check = await client.get(f"/users/{user_id_to_delete}")
    assert response_check.status_code == 404 # Теперь должен быть Not Found (Не найден)
