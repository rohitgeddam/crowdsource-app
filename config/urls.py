"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views
from core.courier import views as courier_views
from core.customer import views as customer_views
from django.contrib.auth import views as auth_views
from django.conf import settings

courier_patterns = [

    path("", courier_views.home, name="home")
]

customer_patterns = [
    path("profile/", customer_views.profile, name="profile"),
    path("payment_method/", customer_views.payment_method, name="payment_method"),
    path("create_job/", customer_views.create_job, name="create_job"),
    path("", customer_views.home, name="home")
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign-in/', auth_views.LoginView.as_view(template_name="sign-in.html"), name="sign-in"),
    path('sign-out/', auth_views.LogoutView.as_view(next_page="/")),
    path('sign-up/', views.signUp, name="sign-up"),
    path("courier/", include((courier_patterns, 'courier'))),
    path("customer/", include((customer_patterns, 'customer'))),
    path("", views.home)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)