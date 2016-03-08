"""feature_request URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from ticketing.views import HomePage, FeaturePage, FeatureDetails, update_priority, data_presentation, custom_login

urlpatterns = [
	
	#Authorization
	url(r'^login/$', custom_login, name='login'),
	url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),

    url(r'^admin/', admin.site.urls),
    url(r'^$', login_required(HomePage.as_view()), name='index'),
    url(r'^features/$', login_required(FeaturePage.as_view()), name='feature-list'),
    url(r'^features/(?P<pk>[-\w]+)/$',login_required(FeatureDetails.as_view()), name='feature-details'),
    url(r'^priorityupdate/$', login_required(update_priority), name='feature-priority-update'),
    url(r'^datapresentation/$', login_required(data_presentation), name='data-presentation'),
]
