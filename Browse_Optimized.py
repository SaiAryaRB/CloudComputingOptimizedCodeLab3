from products import dao


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @classmethod
    def load(cls, data):
        return cls(data['id'], data['name'], data['description'], data['cost'], data['qty'])

    def update_qty(self, qty: int):
        if qty < 0:
            raise ValueError('Quantity cannot be negative')
        self.qty = qty
        dao.update_qty(self.id, qty)


def list_products() -> list[Product]:
    products = dao.list_products()
    return [Product.load(product) for product in products]


def get_product(product_id: int) -> Product:
    product_data = dao.get_product(product_id)
    if product_data is None:
        raise ValueError(f'Product with ID {product_id} not found')
    return Product.load(product_data)


def add_product(product: Product):
    dao.add_product(product._dict_)  # Convert product to dictionary before adding