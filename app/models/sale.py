class Sale:
    def __init__(self, id, drug_id, quantity, sale_price, sale_date):
        self.id = id
        self.drug_id = drug_id
        self.quantity = quantity
        self.sale_price = sale_price
        self.sale_date = sale_date
    
    def __repr__(self):
        return f"Sale( id={self.id}, drug_id={self.drug_id}, quantity={self.quantity})"