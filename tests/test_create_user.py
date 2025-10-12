import allure
import requests
from data import REGISTER_USER_URL, DELETE_USER_URL


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, user_data):
        response = requests.post(REGISTER_USER_URL, json=user_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] == True
        assert "accessToken" in response_data

        requests.delete(DELETE_USER_URL, headers={"Authorization": response_data["accessToken"]})

    @allure.title("Ошибка при создании пользователя с существующим email")
    def test_create_existing_user_error(self, registered_user):
        response = requests.post(REGISTER_USER_URL, json=registered_user)

        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] == False

    @allure.title("Ошибка при создании пользователя без пароля")
    def test_create_user_without_password_error(self, user_data):
        user_data["password"] = ""
        response = requests.post(REGISTER_USER_URL, json=user_data)

        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] == False