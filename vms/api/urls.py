from django.urls import path
from . import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

# Url patterns for application api
urlpatterns = [
    
    # Endpoint for obtaining JWT TOken ( access and refresh token ) for authentication provided by simple jwt
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Endpoint for refreshing JWT TOken ( refresh token ) provided by simple jwt
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Endpoint for listing all vendors and creating a new vendor. Accepts Get and Post requests
    path('vendors/', views.ListAllVendors.as_view(), name="all vendors"),

    # Endpoint for listing, updating and deleting of specific vendor by vendor_id. Accepts Get, Put and Delete requests
    path('vendors/<int:vendor_id>', views.ListVendorDetails.as_view(), name="vendor"),

    # Endpoint for listing performance info of specific vendor by vendor_id
    path('vendors/<int:vendor_id>/performance', views.ListVendorPerformance.as_view(), name="vendor performance"),

    # Endpoint for listing all purchase orders and creating a new purchase order. Accepts Get and Post requests
    path('purchase_orders/', views.ListAllPuchaseOrders.as_view(), name="all orders"),

    # Endpoint for listing, updating and deleting of specific purchase order by po_id. Accepts Get, Put and Delete requests
    path('purchase_orders/<int:po_id>', views.ListPurchaseOrder.as_view(), name="purchase order"),

    # Endpoint for vendors to acknowledge a purchase order through po_id, initiates re-calculation of average response time of the vendor
    path('purchase_orders/<int:po_id>/acknowledge', views.AcknowledgePurchaseOrder.as_view(), name="order acknowledge"),
    
]