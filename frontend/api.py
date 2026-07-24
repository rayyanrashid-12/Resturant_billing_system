import requests

BASE_URL = "http://127.0.0.1:8000"


def register(name, email, password, role):
    return requests.post(
        f"{BASE_URL}/user",
        json={
            "name": name,
            "email": email,
            "password": password,
            "role": role
        }
    )

def login(username, password):
    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": username,
            "password": password
        }
    )

    return response


def get_menu(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.get(
        f"{BASE_URL}/menu",
        headers=headers
    )


def create_menu(token, data):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.post(
        f"{BASE_URL}/menu",
        json=data,
        headers=headers
    )


def get_reports(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.get(
        f"{BASE_URL}/reports",
        headers=headers
    )

def create_order(token, customer_name):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.post(
        f"{BASE_URL}/orders",
        json={"customer_name": customer_name},
        headers=headers
    )

def update_menu(token, item_id, data):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.put(
        f"{BASE_URL}/menu/{item_id}",
        json=data,
        headers=headers
    )


def delete_menu(token, item_id):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.delete(
        f"{BASE_URL}/menu/{item_id}",
        headers=headers
    )



def create_order(token, customer_name):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.post(
        f"{BASE_URL}/orders",
        json={
            "customer_name": customer_name
        },
        headers=headers
    )


def get_orders(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.get(
        f"{BASE_URL}/orders",
        headers=headers
    )


def add_item_to_order(token, order_id, menu_item_id, quantity):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.post(
        f"{BASE_URL}/orders/{order_id}/items",
        json={
            "menu_item_id": menu_item_id,
            "quantity": quantity
        },
        headers=headers
    )

def get_bill(token, order_id):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.get(
        f"{BASE_URL}/bill/{order_id}",
        headers=headers
    )