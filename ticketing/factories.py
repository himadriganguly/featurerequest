import factory
from django.utils.timezone import now
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
	
	
	
		
