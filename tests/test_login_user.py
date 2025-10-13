import allure
import pytest
import requests
from data import LOGIN_USER_URL

@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_existing_user_success(self, registered_user):
        with allure.step("Отправить запрос на логин"):
            response = requests.post(LOGIN_USER_URL, json={
                "email": registered_user["email"],
                "password": registered_user["password"]
            })

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] == True

    @pytest.mark.parametrize("email,password", [
        ("nonexistent@user.com", "wrongpassword"),
        ("", "password123"),
        ("test@test.com", ""),
        ("", "")
    ])
    @allure.title("Ошибка при входе с неверными данными")
    def test_login_with_invalid_credentials_error(self, email, password):
        with allure.step("Отправить запрос на логин с неверными данными"):
            response = requests.post(LOGIN_USER_URL, json={
                "email": email,
                "password": password
            })

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] == False
        assert "message" in response_data