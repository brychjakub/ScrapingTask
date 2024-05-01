class Product:
    def __init__(self, title, price, price_before_discount = None, availability = None, rating = None, number_of_ratings = None, url = None):
        self.title = title
        self.price = price
        self.price_before_discount = price_before_discount
        self.availability = availability
        self.rating = rating
        self.number_of_ratings = number_of_ratings
        self.url = url

    def __str__(self):
        return f"Title: {self.title}, Price: {self.price}, Price Before Discount: {self.price_before_discount if self.price_before_discount else 'N/A'}, Availability: {self.availability}, rating: {self.rating}, number_of_ratings: {self.number_of_ratings}, url: {self.url}"
