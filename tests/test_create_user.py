import allure
import pytest
import requests
from data import REGISTER_USER_URL


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, user_data):
        with allure.step("Отправить запрос на создание пользователя"):
            response = requests.post(REGISTER_USER_URL, json=user_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] == True
        assert "accessToken" in response_data

    @allure.title("Ошибка при создании пользователя с существующим email")
    def test_create_existing_user_error(self, registered_user):
        with allure.step("Отправить запрос на создание пользователя с существующим email"):
            response = requests.post(REGISTER_USER_URL, json=registered_user)

        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] == False
        assert "message" in response_data

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title("Ошибка при создании пользователя без обязательного поля")
    def test_create_user_without_required_field_error(self, user_data, missing_field):
        test_data = user_data.copy()
        test_data[missing_field] = ""

        with allure.step(f"Отправить запрос на создание пользователя без поля {missing_field}"):
            response = requests.post(REGISTER_USER_URL, json=test_data)

        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] == False
        assert "message" in response_data