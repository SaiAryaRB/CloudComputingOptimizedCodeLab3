import json
from typing import List, Optional
from products import Product, get_product
from cart import dao


class Cart:
    """
    Represents a shopping cart with associated user information and products.
    """

    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> "Cart":
        """
        Load a Cart object from a dictionary.
        """
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[Product(**item) for item in data['contents']],
            cost=data['cost']
        )


def get_cart(username: str) -> List[Product]:
    """
    Retrieve the contents of the cart for a given username.

    Args:
        username (str): The username of the cart owner.

    Returns:
        List[Product]: List of product objects in the user's cart.
    """
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    try:
        products_in_cart = [
            get_product(product_id)
            for cart_detail in cart_details
            for product_id in json.loads(cart_detail['contents'])
        ]
        return products_in_cart
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Error processing cart contents for user '{username}': {e}")
        return []


def add_to_cart(username: str, product_id: int) -> None:
    """
    Add a product to the user's cart.

    Args:
        username (str): The username of the cart owner.
        product_id (int): The ID of the product to add.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int) -> None:
    """
    Remove a product from the user's cart.

    Args:
        username (str): The username of the cart owner.
        product_id (int): The ID of the product to remove.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str) -> None:
    """
    Delete the entire cart for the given username.

    Args:
        username (str): The username of the cart owner.
    """
    dao.delete_cart(username)
