from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from base.models import PurchaseOrder, Vendor, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils import timezone
# Create your views here.


@api_view(['GET'])
def index(request):
    print(request.user)
    return Response("api")

@permission_classes([IsAuthenticated])
class ListAllVendors(APIView):
    def get(self, request):
        all_vendors = Vendor.objects.all()
        serializer = VendorSerializer(all_vendors, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"message" : "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    

@permission_classes([IsAuthenticated])
class ListVendorDetails(APIView):
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)
                
    def put(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors)
    
    def delete(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        serializer = VendorSerializer(vendor)
        vendor.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
class ListAllPuchaseOrders(APIView):
    def get(self, request):
        all_po = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(all_po, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        print(request.data)
        vendor_id : int = request.data.pop('vendor')
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        try:
            new_po = PurchaseOrder.objects.create(vendor=vendor, **request.data)
            new_po.save()
            serializer = PurchaseOrderSerializer(new_po)
            return Response(serializer.data)
        except:
            return Response({"message":"invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    

@permission_classes([IsAuthenticated])
class ListPurchaseOrder(APIView):
    def get(self, request, po_id):
        po = get_object_or_404(PurchaseOrder, pk=po_id)
        serializer = PurchaseOrderSerializer(po)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self, request, po_id):
        po = get_object_or_404(PurchaseOrder, pk=po_id)
        serializer = PurchaseOrderSerializer(po)
        po.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, po_id):
        po = get_object_or_404(PurchaseOrder, pk=po_id)
        serializer = PurchaseOrderSerializer(po, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors)
    
@permission_classes([IsAuthenticated])
class ListVendorPerformance(APIView):
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        vhp = HistoricalPerformance.objects.filter(vendor=vendor).all()
        serializer = HistoricalPerformanceSerializer(vhp, many=True)
        return Response(serializer.data)
    
# @permission_classes([IsAuthenticated])
class AcknowledgePurchaseOrder(APIView):
    def post(self, request, po_id):
        po = get_object_or_404(PurchaseOrder, pk=po_id)
        po.acknowledgement_date = timezone.now()
        po.save()

        return Response({"message":"Acknowledge Success"}, status=status.HTTP_200_OK)
    


