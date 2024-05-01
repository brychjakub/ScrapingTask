class Product:
    def __init__(self, title, price, price_before_discount=None, availability=None):
        self.title = title
        self.price = price
        self.price_before_discount = price_before_discount
        self.availability = availability  # New attribute

    def __str__(self):
        return f"Title: {self.title}, Price: {self.price}, Price Before Discount: {self.price_before_discount if self.price_before_discount else 'N/A'}, Availability: {self.availability}"
