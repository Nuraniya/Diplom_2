import pytest
import requests
from data import REGISTER_USER_URL, DELETE_USER_URL, GET_INGREDIENTS_URL
from generators import generate_user_data

@pytest.fixture
def user_data():
    return generate_user_data()

@pytest.fixture
def registered_user(user_data):
    response = requests.post(REGISTER_USER_URL, json=user_data)
    token = response.json()["accessToken"]
    user_data["token"] = token
    yield user_data
    requests.delete(DELETE_USER_URL, headers={"Authorization": token})

@pytest.fixture
def ingredients_data():
    response = requests.get(GET_INGREDIENTS_URL)
    ingredients = response.json()["data"]
    return [ingredient["_id"] for ingredient in ingredients[:2]]