"""verify mint URL Configuration

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
from django.urls import path
from . import views

urlpatterns = [
    path('verify_mint/', views.verify_mint, name='verify_mint'),
    path('additive-card/', views.create_additive_card, name='create_additive_card'),
    path('multiplicative-card/', views.create_multiplicative_card, name='create_multiplicative_card')
]
