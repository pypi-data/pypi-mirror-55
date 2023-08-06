from django.urls import path
from .views import *

urlpatterns = [
    path('', InitiatePaymentView.as_view(), name='index'),
    path('initiate/', InitiatePaymentView.as_view(), name='initiate'),

]

app_name = 'paytm:checkout'
