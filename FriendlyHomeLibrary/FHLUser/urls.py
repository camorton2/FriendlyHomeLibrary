from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
   url(r'^login/$', auth_views.LoginView.as_view(), {'template_name':'FHLUser/login.html'},name='FHLUser_Login'),
   url(r'^logout/$', auth_views.LogoutView.as_view(), 
     {
     'template_name':'FHLUser/logged_out.html', 
     'extra_context': {'form':AuthenticationForm}
     },
     name='FHLUser_Logout'
   ),
]
