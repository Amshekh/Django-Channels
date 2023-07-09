from django.urls import path
from .import views

urlpatterns = [
    path('<str:group_name>/', views.index),
    path('test/viewtocons/', views.msg_from_view), # i'm doing this for testing purpose i.e. sending message to group from view
]