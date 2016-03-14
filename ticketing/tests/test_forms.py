from django.test import TestCase
from django.core.exceptions import NON_FIELD_ERRORS
from ticketing.factories import ClientFactory, ProductFactory, FeatureRequestFactory
from ticketing.forms import FeatureRequestForm

# Create your tests here.

class FeatureRequestTest(TestCase):
	
	def setUp(self):
		self.client = ClientFactory()
		self.product = ProductFactory()
		self.new_feature_request = FeatureRequestFactory()
	
	def test_valid_form(self):			
		form = FeatureRequestForm(data={
			'title': "This is a test title",
			'desc': self.new_feature_request.desc,
			'targetdate': '03/24/2016',
			'url': 'http://www.example.com',	
			'client': self.client.pk,
			'productarea': self.product.pk,
		})
		
		self.assertTrue(form.is_valid())
	
	def test_no_title(self):
		form = FeatureRequestForm(data={
			'title': '',
			'desc': self.new_feature_request.desc,
			'targetdate': '03/24/2016',
			'url': 'http://www.example.com',	
			'client': self.client.pk,
			'productarea': self.product.pk,
		})
		
		self.assertFalse(form.is_valid())
		self.assertTrue(form.has_error('title', code='required'))	
		
	def test_no_desc(self):
		form = FeatureRequestForm(data={
			'title': 'This is a test title',
			'desc': '',
			'targetdate': '03/24/2016',
			'url': 'http://www.example.com',	
			'client': self.client.pk,
			'productarea': self.product.pk,
		})
		
		self.assertFalse(form.is_valid())
		self.assertTrue(form.has_error('desc', code='required'))
	
	def test_no_targetdate(self):
		form = FeatureRequestForm(data={
			'title': 'This is a test title',
			'desc': self.new_feature_request.desc,
			'targetdate': '',
			'url': 'http://www.example.com',	
			'client': self.client.pk,
			'productarea': self.product.pk,
		})
		
		self.assertFalse(form.is_valid())
		self.assertTrue(form.has_error('targetdate', code='required'))	
	
	def test_no_client(self):
		form = FeatureRequestForm(data={
			'title': 'This is a test title',
			'desc': self.new_feature_request.desc,
			'targetdate': '03/24/2016',
			'url': 'http://www.example.com',	
			'client': '',
			'productarea': self.product.pk,
		})
		
		self.assertFalse(form.is_valid())
		self.assertTrue(form.has_error('client', code='required'))	
	
	def test_rejects_feature_name_that_already_exists(self):
		form = FeatureRequestForm(data={
			'title': self.new_feature_request.title,
			'desc': self.new_feature_request.desc,
			'targetdate': '03/24/2016',
			'url': 'http://www.example.com',	
			'client': self.new_feature_request.client.pk,
			'productarea': self.new_feature_request.productarea.pk,
		})
		
		self.assertFalse(form.is_valid())
		self.assertTrue(form.has_error(NON_FIELD_ERRORS))	
	
