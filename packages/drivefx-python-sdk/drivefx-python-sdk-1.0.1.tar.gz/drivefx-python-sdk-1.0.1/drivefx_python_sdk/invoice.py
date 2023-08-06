import  requests
from drivefx_python_sdk.exceptions import DriveFxException
import json


class Product:
    def __init__(self, reference, designation, unit_price, unit_code="M", discount1=0, quantity=1, tax_included=True, tax_percentage=23, tax_region="PT" ):

        self.reference = reference
        self.designation = designation
        self.unit_price = unit_price
        self.unit_code = unit_code
        self.discount1 = discount1
        self.quantity = quantity
        self.tax_included = tax_included
        self.tax_percentage = tax_percentage
        self.tax_region = tax_region

    def to_dict(self):
        product_dict = {
            "reference": self.reference,
            "designation": self.designation,
            "unitCode": self.unit_code,
            "unitPrice": self.unit_price,
            "discount1": self.discount1,
            "quantity": self.quantity,
            "taxIncluded": self.tax_included,
            "taxPercentage": self.tax_percentage,
            "taxRegion": self.tax_region
        }
        return product_dict


class Costumer:
    def __init__(self, number, name, email, tax_number, address, postal_code, city, country="PT",):

        self.number = number
        self.name = name
        self.email = email
        self.tax_number = tax_number
        self.address = address
        self.postal_code = postal_code
        self.city = city
        self.country = country

    def to_dict(self):
        costumer_dict = {
            "number": self.number,
            "name": self.name,
            "address": self.address,
            "postalCode": self.postal_code,
            "city": self.city,
            "country": self.country,
            "email": self.email,
            "taxNumber": self.tax_number
        }
        return costumer_dict


class Invoice:

    def __init__(self, costumer: Costumer, products):
        self.costumer = costumer
        self.products = products

    def to_dict(self):
        invoice_dict = {
            "customer": self.costumer.to_dict(),
            "requestOptions": {
                "option": 1
            },
            "document": {
                "docType": 1
            },
            "products": [
                p.to_dict() for p in self.products
            ]
        }
        return invoice_dict


class InvoiceService:

    API = "https://api.drivefx.net/v3"

    def __init__(self, backend_url, app_id, user_code, password):
        self.backend_url = backend_url
        self.app_id = app_id
        self.user_code = user_code
        self.password = password
        self.token = None

    def auth(self):

        input = {
            "credentials": {
                "backendUrl": self.backend_url,
                "appId": self.app_id,
                "userCode": self.user_code,
                "password": self.password
            }
        }

        response = requests.post(f"{InvoiceService.API}/generateAccessToken", json=input)
        response_json = response.json()

        if response_json["code"] == 0:
            self.token = response_json["token"]
        else:
            raise DriveFxException(response_json["message"])

        return self.token

    def create_invoice(self, invoice: Invoice):

        token = self.auth()
        headers = {'Authorization': token}

        input = invoice.to_dict()

        response = requests.post(f"{InvoiceService.API}/createDocument", json=input, headers=headers)
        response_json = response.json()

        if response_json["code"] == 1:
            invoice = response_json
        else:
            raise DriveFxException(response_json["message"])

        return invoice

