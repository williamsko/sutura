from django.contrib.auth.models import User
from apps.customer.models import Customer, ProofType, Proofs, Favoris
from pymongo import MongoClient
from gridfs import GridFS
from apps.utils.exceptions import ProofStorageException
import logging

FORMAT = '%(levelname)s %(asctime)-15s %(name)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)


def retreive_customer_by_email(email: str):
    return User.objects.get(email=email)


def retreive_customer_by_identifier(identifier: str):
    return Customer.objects.get(identifier=identifier)


def retreive_customer_by_username(username: str):
    return User.objects.get(username=username)


def create_user(names, username, email, password) -> User:
    user = User()
    user.email = email
    user.username = username
    user.first_name = ' '.join(names[:-1])
    user.last_name = names[-1]
    user.set_password(password)
    user.save()
    return user


def create_customer(user, address=None):
    customer = Customer()
    customer.address = address
    customer.user = user
    customer.save()
    return customer


def retreive_all_customers():
    return Customer.objects.all()


def check_customer_password(username, password):
    user = retreive_customer_by_username(username)
    return user.check_password(password)


def get_customer(username: str) -> Customer:
    return Customer.objects.get(user__username=username)


def store_proof(customer, proof_type, proof_content):
    db = MongoClient().sutura_files
    fs = GridFS(db)
    return fs.put(proof_content)


def create_proof(customer, proof_type, proof_content):

    proof_type = ProofType.objects.get(short_name=proof_type)

    proof = Proofs()
    proof.customer = customer
    proof.type = proof_type
    proof.file_object = store_proof(customer, proof_type, proof_content)
    logger.debug(proof.file_object)
    proof.save()


def retreive_all_proofs():
    return Proofs.objects.all()


def retreive_all_proof_types():
    return ProofType.objects.all()


def retreive_all_favoris():
    return Favoris.objects.all()


def add_product_to_customer_favoris(customer, product):
    if not _check_if_product_is_favoris_of_customer(customer, product):
        favoris = Favoris()
        favoris.customer = customer
        favoris.product = product
        favoris.save()


def _check_if_product_is_favoris_of_customer(customer, product):
    return Favoris.objects.filter(customer=customer, product=product).count() > 0
