import allure
import requests
from data import CREATE_ORDER_URL

@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Успешное создание заказа с авторизацией")
    def test_create_order_with_auth_success(self, registered_user, ingredients_data):
        response = requests.post(CREATE_ORDER_URL,
                                 json={"ingredients": ingredients_data},
                                 headers={"Authorization": registered_user["token"]}
                                 )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] == True
        assert "order" in response_data

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, ingredients_data):
        response = requests.post(CREATE_ORDER_URL, json={"ingredients": ingredients_data})

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] == True
        assert "order" in response_data

    @allure.title("Ошибка при создании заказа без ингредиентов")
    def test_create_order_without_ingredients_error(self, registered_user):
        response = requests.post(CREATE_ORDER_URL,
                                 json={"ingredients": []},
                                 headers={"Authorization": registered_user["token"]}
                                 )

        assert response.status_code == 400
        response_data = response.json()
        assert response_data["success"] == False

    @allure.title("Ошибка при создании заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash_error(self, registered_user):
        response = requests.post(CREATE_ORDER_URL,
                                 json={"ingredients": ["invalid_hash_1", "invalid_hash_2"]},
                                 headers={"Authorization": registered_user["token"]}
                                 )

        assert response.status_code == 500