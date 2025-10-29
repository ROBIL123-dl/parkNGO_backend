
from django.urls import path,include
from . import views

   
urlpatterns = [
    path('v1/blocks/',views.BlockCreateAPIView.as_view(), name='block-create'),
    path('v1/blocks/<int:id>/', views.BlockRetrieveUpdateAPIView.as_view(), name='block-detail-update'),
    path('v1/slots/', views.ParkingSlotCreateAPIView.as_view(), name='slot-create'),
    path('v1/slots/<int:pk>/',views.ParkingSlotUpdateAPIView.as_view(), name='slot-update'),
]

 