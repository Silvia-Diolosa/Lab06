from dataclasses import dataclass
from datetime import date

@dataclass
class Vendita:
    Retailer_code: int
    Product_number: int
    Order_method_code: int
    Date: date
    Quantity: int
    Unit_price: float
    Unit_sale_price: float


    # ricavo: campo non presente nel database, ma che aggiungo per comodità,
    # calcolandolo nel __post_init__(), ovverosia dopo che gli attributi principali sono già
    # stati popolati
    def __post_init__(self):
        """
        After initialization, it computes the "ricavo" of the sale as unit_sale_price * quantity.
        """
        self.ricavo: float = self.Unit_sale_price * self.Quantity

    def __str__(self):
        return f"Data: {self.Date}; Ricavo: {self.ricavo}; Retailer: {self.Retailer_code}; Product: {self.Product_number}"

    def __eq__(self, other):
        return (self.Retailer_code == other.retailer_code
                and self.Product_number == other.product_number
                and self.Order_method_code == other.order_method_code)

    def __hash__(self):
        return hash((self.Retailer_code, self.Product_number, self.Order_method_code))

    def __lt__(self, other):
        return self.ricavo < other.ricavo

