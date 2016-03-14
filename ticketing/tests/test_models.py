from django.test import TestCase
from ticketing.factories import ClientFactory, ProductFactory, FeatureRequestFactory
from ticketing.models import Client, Product, FeatureRequest

class ClientTest(TestCase):
	def setUp(self):		
		self.client = Client(name="Client 1")
		self.client.save()
	
	def tearDown(self):
		self.client.delete()
	
	def test_string_method(self):
		self.assertEqual("Client 1", self.client.__str__())

class ProductTest(TestCase):
	def setUp(self):		
		self.product = Product(name="Product 1")
		self.product.save()
	
	def tearDown(self):
		self.product.delete()
	
	def test_string_method(self):
		self.assertEqual("Product 1", self.product.__str__())

class FeatureRequestTest(TestCase):
	def setUp(self):	
		self.client = Client(name="Client 1")
		self.client.save()	
		self.product = Product(name="Product 1")
		self.product.save()
		self.featurerequest = FeatureRequest(
									title='This is a title for Feature Request',
									desc='Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
									priority='1',
									targetdate='2016-03-24',
									url='http://www.example.com',
									client=self.client,
									productarea=self.product								
								)
		self.featurerequest.save()
	
	def tearDown(self):
		self.client.delete()
		self.product.delete()
		self.featurerequest.delete()
	
	def test_string_method(self):
		self.assertEqual("This is a title for Feature Request", self.featurerequest.__str__())
