class Supplier:
    def __init__(self, id, name, contact_person, phone, email):
        self.id = id
        self.name = name
        self.contact_person = contact_person
        self.phone = phone
        self.email = email
    
    def __repr__(self):
        return f"Supplier( id={self.id}, name='{self.name}')"