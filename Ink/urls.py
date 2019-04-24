from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.conf.urls.static import static


urlpatterns = [
	
    # Main Urls
    path('', LoginView.as_view(template_name='Ink/login.html'), name="login"),
    path('register', views.register, name='register'),
    path('home', views.home, name='home'),
    path('company', views.company, name='company'),
    path('profile', views.profile, name='profile'),
    path('createComp', views.createComp, name='createComp'),
    path('compHome/<cmp_id>', views.compHome, name='compHome'),
    path('ownComp', views.ownComp, name='ownComp'),
    path('join/<companyName>', views.join, name='join'), 
    path('leave/<companyName>', views.leave, name='leave'), 
    path('employee', views.employee, name='employee'),
    path('type/<username>', views.type, name='type'),
    path('logout', LogoutView.as_view(template_name='Ink/logout.html'), name="logout"),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)