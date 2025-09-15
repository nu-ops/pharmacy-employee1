class Pharmacy:
    def __init__(self, id, address, city, phone):
        self.id = id
        self.address = address
        self.city = city
        self.phone = phone
    
    def __repr__(self):
        return f"Pharmacy( id={self.id}, address='{self.address}', city='{self.city}')"