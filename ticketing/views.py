from django.shortcuts import render 
from django.views.generic import View,DetailView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json

# Custom
from .models import Client, Product, FeatureRequest
from .forms import FeatureRequestForm, SortRequestForm

# Create your views here.
class HomePage(View):	
	
	def get(self, request):
		
		clients 	= Client.objects.all()
		#products	= Product.objects.all()	
		count		= FeatureRequest.objects.all().count()	
		
		context = {
			'clients': clients,
			#'products': products,
			'form': FeatureRequestForm(),
			'menu': 'home-createfeature',
			'count': count,
		}
		
		return render(request, "index.html", context)
	
	def post(self, request):	
		
		if(request.method == 'POST'):
			form = FeatureRequestForm(request.POST)
			if(form and form.is_valid()):						
				tmpform = form.save(commit=False)
				
				tempClient = Client.objects.get(id=request.POST.get('client'))
				#temppriority = int(request.POST.get('priority'))
				
				#if temppriority == 0 or temppriority is None:
				if (tempClient.tickets.count() != 0):
					tempTicket = tempClient.tickets.latest('priority')
					tempTicket = tempTicket.priority							
				else:
					tempTicket = 0
					
				tmpform.priority = tempTicket + 1		
				
				try:
					tmpform.save()
					messages.success(request, 'Your Data Has Been Saved. Thank You.')
					return redirect('index')
				except:
					messages.error(request, 'Sorry! Cannot Save Your Data.')
					return redirect('index')
				
		clients 	= Client.objects.all()
		products	= Product.objects.all()
		
		context = {
			'clients': clients,
			#'products': products,
			'form': form,
			'menu': 'home-createfeature',
		}	
		
		return render(request, "index.html", context)

class FeaturePage(View):	
	
	def get(self, request):
		
		#clients 	= Client.objects.all()
		#products	= Product.objects.all()		
		
		context = {
			#'clients': clients,
			#'products': products,
			'form': SortRequestForm(),
			'menu': 'home-featurelist',
		}
		
		return render(request, "feature.html", context)
	
	def post(self, request):
		if(request.method == 'POST'):
			form = SortRequestForm(request.POST)
			if(form and form.is_valid()):
				client = Client.objects.get(id=request.POST.get('client'))
			else:
				client = ''  	
		else:
			return redirect('feature-list')
				
		if client:
			context = {
				'client': client,
				'form': SortRequestForm(),
				'menu': 'home-featurelist',
			}       
		else:
			context = {
				'form': SortRequestForm(),
				'menu': 'home-featurelist',
			}      
		
		return render(request, "feature.html", context)

class FeatureDetails(DetailView):
	model = FeatureRequest
	template_name = "feature-details.html"	

def update_priority(request):
	
	if (request.method == 'POST'):
		
		if request.is_ajax():
			
			objs = json.loads(request.body.decode())
			
			print(objs);
			
			if objs:
				
				length = len(objs) - 1
				
				#print(length)
				
				i = 0 
				pk = 0 
				priority = 0
				tempdict = {}
				
				while i < length:
					for key,value in objs[i].items():
						
						#print("{} - {}".format(key,value))
						
						if key == 'pk':
							pk = int(value)							
						if key == 'priority':
							priority = int(value)
						if (pk !=0 and priority !=0):
							
							#print("{} - {}".format(pk,priority))
							
							record = FeatureRequest.objects.get(pk = pk)
							record.priority = priority
							record.save(update_fields=["priority"])
					i += 1
				response_data = {}
				response_data['msg'] = 'Priority update successfully!'
			else:
				response_data = {}
				response_data['msg'] = 'Priority cannot be update successfully!'
							
			return JsonResponse(response_data)
			
	else:
		return JsonResponse({'msg':'Sorry! Data cannot be update.'})
	
	return redirect('feature-list')


def data_presentation(request):
	
	if (request.method == 'GET'):
		
		count		= FeatureRequest.objects.count()
		clients 	= Client.objects.all()
		products 	= Product.objects.all()
		features 	= FeatureRequest.objects.all()
		
		total_features = int(FeatureRequest.objects.count())
		
		client_feature_percent = {}
		for client in clients:
			client_feature_percent.update({client.name: int((client.tickets.count()/total_features)*100)})
		
		product_feature_total = {}
		for product in products:
			product_feature_total.update({product.name: product.tickets.count()})
		
		target_date_total = {}
		for feature in features:
			s = "-"
			tempDate = (str(feature.targetdate.year), str(feature.targetdate.month), str(feature.targetdate.day))
			target_date_total.update({s.join(tempDate): FeatureRequest.objects.filter(targetdate = feature.targetdate).count()})
				
				
		context = {
			'count': count,
			'clients': clients,
			'total_features': total_features,
			'client_feature_percent': client_feature_percent,
			'product_feature_total': product_feature_total,
			'target_date_total': target_date_total,
		}
		
		return render(request, 'data-presentation.html', context)
	else:
		return redirect('index')
	

def custom_login(request): 
	if (request.user.is_authenticated()):
		#return redirect('index')
		return redirect(request.GET.get('next', '/')) 
	else:
		return auth_views.login(request, template_name='login.html')
