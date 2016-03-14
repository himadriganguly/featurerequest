import factory
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Client, Product, FeatureRequest

class ClientFactory(factory.django.DjangoModelFactory):
	
	class Meta:
		model=Client
	
	name=factory.Sequence(lambda n: 'Client {0}'.format(n))


class ProductFactory(factory.django.DjangoModelFactory):
	
	class Meta:
		model=Product
	
	name=factory.Sequence(lambda n: 'Product {0}'.format(n))

class FeatureRequestFactory(factory.django.DjangoModelFactory):
	
	class Meta:
		model=FeatureRequest
		
	title=factory.Faker('text', max_nb_chars=20)
	desc=factory.Faker('text', max_nb_chars=400)
	priority=12345
	targetdate='2016-03-24'
	url=''
	client=factory.SubFactory(ClientFactory)
	productarea=factory.SubFactory(ProductFactory)

class UserFactory(factory.django.DjangoModelFactory):
    """
    Creates a standard user.
    """
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = first_name
    password = make_password('test')
	
	
	
		
