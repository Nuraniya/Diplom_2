import allure
import requests
from data import LOGIN_USER_URL

@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_existing_user_success(self, registered_user):
        response = requests.post(LOGIN_USER_URL, json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        })

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] == True

    @allure.title("Ошибка при входе с неверным логином и паролем")
    def test_login_with_invalid_credentials_error(self):
        response = requests.post(LOGIN_USER_URL, json={
            "email": "nonexistent@user.com",
            "password": "wrongpassword"
        })

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] == False