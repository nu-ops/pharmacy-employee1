class Drug:
    def __init__(self, id, name, atc_code, description, price, discount_price, quantity, image_path, created_at):
        self.id = id
        self.name = name
        self.atc_code = atc_code
        self.description = description
        self.price = price
        self.discount_price = discount_price
        self.quantity = quantity
        self.image_path = image_path
        self.created_at = created_at
    
    def __repr__(self):
        return f"Drug(id={self.id}, name='{self.name}', price={self.price}, quantity={self.quantity})"