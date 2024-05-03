from django.urls import path
from . import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('', views.index, name="index"),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('vendors/', views.ListAllVendors.as_view(), name="all vendors"),
    path('vendors/<int:vendor_id>', views.ListVendorDetails.as_view(), name="vendor"),
    path('vendors/<int:vendor_id>/performance', views.ListVendorPerformance.as_view(), name="vendor performance"),

    path('purchase_orders/', views.ListAllPuchaseOrders.as_view(), name="all orders"),
    path('purchase_orders/<int:po_id>', views.ListPurchaseOrder.as_view(), name="purchase order"),
    path('purchase_orders/<int:po_id>/acknowledge', views.AcknowledgePurchaseOrder.as_view(), name="order acknowledge"),
    

]