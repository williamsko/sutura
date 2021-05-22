import logging
from apps.customer.validator import CustomerValidator, CustomerLoginValidator, CustomerAddFavorisValidator
from marshmallow import ValidationError
from apps.customer import repository as customer_repository
from apps.product.repository import get_product_by_id
from django.contrib.auth.models import User
from apps.utils.exceptions import CustomerException, PayloadException, InternalException, ProductException
from apps.customer.models import Customer
from apps.product.models import Product

customer_validator = CustomerValidator()
customer_login_validator = CustomerLoginValidator()
customer_add_favoris_validator = CustomerAddFavorisValidator()

FORMAT = '%(levelname)s %(asctime)-15s %(name)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)


def new_customer(payload):
    _validate_customer_creation_payload(payload)

    full_name = payload.get('full_name')
    phone_number = payload.get('phone_number')
    email = payload.get('email')
    password = payload.get('password')

    try:
        customer_repository.retreive_customer_by_email(email)
        raise CustomerException('Cet utilisateur existe déjà')
    except User.DoesNotExist:
        pass

    names = full_name.split(' ')
    created_user = customer_repository.create_user(
        names, phone_number, email, password)

    customer = customer_repository.create_customer(created_user)
    return customer.json


def get_all_customers():
    return customer_repository.retreive_all_customers()


def get_all_proof_types():
    return customer_repository.retreive_all_proof_types()


def get_all_proofs():
    return customer_repository.retreive_all_proofs()


def get_all_favoris():
    return customer_repository.retreive_all_favoris()


def _validate_customer_creation_payload(payload):
    try:
        customer_validator.load(payload)
    except ValidationError as e:
        raise PayloadException(str(e))


def customer_login(payload):
    try:
        customer_login_validator.validate(payload)
    except ValidationError as e:
        raise PayloadException(str(e))

    phone_number = payload.get('phone_number')
    password = payload.get('password')

    try:
        login_result = customer_repository.check_customer_password(
            phone_number, password)
    except User.DoesNotExist:
        raise CustomerException('Utilisateur introuvable')
    except Exception as e:
        raise CustomerException(str(e))

    if login_result:
        customer = customer_repository.get_customer(phone_number)
        return customer.json
    raise CustomerException('Connexion impossible')


def add_proof_to_customer_account(identifier, proof_type, proof_content):
    try:
        customer = customer_repository.retreive_customer_by_identifier(
            identifier)
        customer_repository.create_proof(customer, proof_type, proof_content)
    except Customer.DoesNotExist:
        raise CustomerException('Client introuvable')
    except Exception as e:
        logger.error(e)
        raise InternalException('Enregistrement document impossible')
    return {}


def add_product_to_customer_favoris(payload):
    try:
        customer_add_favoris_validator.validate(payload)
    except ValidationError as e:
        raise PayloadException(str(e))

    identifier = payload.get('customer_identifier')
    product_id = payload.get('product_id')

    try:
        customer = customer_repository.retreive_customer_by_identifier(
            identifier)
        product = get_product_by_id(product_id)
        customer_repository.add_product_to_customer_favoris(customer, product)
    except Customer.DoesNotExist:
        raise CustomerException('Client introuvable')
    except Product.DoesNotExist:
        raise ProductException('Produit introuvable')
    except Exception:
        raise InternalException('Erreur Enregistrement Favoris')
    return {}


def get_customer_by_identifier(identifier):
    try:
        return customer_repository.retreive_customer_by_identifier(
            identifier)
    except Customer.DoesNotExist:
        raise CustomerException('Client introuvable')
