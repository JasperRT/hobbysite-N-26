from django.urls import path
from .views import comms_list, comm_detail, comm_create, comm_update

urlpatterns = [
    path('list', comms_list, name="comms_list"),
    path('detail/<int:id>', comm_detail, name="comm_detail"),
    path('add/', comm_create, name='comm_create'),
    path('<int:id>/edit/', comm_update, name='comm_update'),
]

app_name = 'commissions'
