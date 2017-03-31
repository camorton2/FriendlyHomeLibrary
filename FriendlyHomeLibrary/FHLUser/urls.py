from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import RedirectView

urlpatterns = [
   url(r'^login/$', auth_views.login, {'template_name':'FHLUser/login.html'},name='FHLUser_Login'),
   url(r'^logout/$', auth_views.logout, 
     {
     'template_name':'FHLUser/logged_out.html', 
     'extra_context': {'form':AuthenticationForm}
     },
     name='FHLUser_Logout'
   ),
]
