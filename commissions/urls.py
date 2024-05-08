from django.urls import path
from .views import comms_list, comm_detail

urlpatterns = [
    path('list', comms_list, name="comms_list"),
    path('detail/<int:id>', comm_detail, name="comm_detail"),
]

app_name = 'commissions'