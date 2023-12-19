# request.py

class Request:
    def __init__(self, id, client_name, client_email, client_phone, service, item, description, status):
        self.id = id
        self.client_name = client_name
        self.client_email = client_email
        self.client_phone = client_phone
        self.service = service
        self.item = item
        self.description = description
        self.status = status


    def __str__(self):
        return f"Request(id={self.id}, client_name={self.client_name}, client_email={self.client_email}, " \
               f"client_phone={self.client_phone}, service={self.service}, item={self.item}, " \
               f"description={self.description}, status={self.status})"