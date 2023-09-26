from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import Staffs, Expences, Returns, Sales, Products
from .serializers import StaffSerializer, ExpencesSerializer, ReturnSerializer, ProductSerializer
from .utils import get_filtered_sales, get_current_month_full, filterSales, getSummary

# Create your views here.


class CustomAuthToken(ObtainAuthToken):
   def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if(user.username == 'admin'):
            print(user.username, '-----')
            role = 'admin'
            profile = ''

            return Response({
                'token': token.key,
                'role': role,
            }, status=status.HTTP_200_OK)
        else:
            role = 'staff'
            profile = Staffs.objects.get(email = user.username)
            staff_serializer = StaffSerializer(profile)

            return Response({
                'token': token.key,
                'role': role,
                'profile': staff_serializer.data
            }, status=status.HTTP_200_OK)


class StaffListCreateView(ListCreateAPIView):

    serializer_class = StaffSerializer
    
    def get_queryset(self):
        queryset = Staffs.objects.all()
        return queryset
    

    def post(self, request):
        data = request.data
        staff = StaffSerializer(data=data)
        staff.is_valid()
        staff.save()

        email = data.get('email')
        phone_number = data.get('phoneNumber')

        user = User.objects.create_user(username=email, password=phone_number)

        return Response('profile created successfully.', status=status.HTTP_201_CREATED)


class StaffDetailUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Staffs.objects.all()
    lookup_field = 'id'
    serializer_class = StaffSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StaffSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        if not isinstance(data["profile_picture"],str):
            data['profile_picture'] = data["profile_picture"]
        else:
            data['profile_picture'] = None

        if not isinstance(data["attachment"],str):
            data['attachment'] = data["attachment"]
        else:
            data['attachment'] = None    


        staff = StaffSerializer(instance, data=data)
        staff.is_valid()
        staff.save()

        if instance:
            return Response("Profile updated successfully", status=status.HTTP_200_OK)
        return Response("Error with request data", status=status.HTTP_400_BAD_REQUEST)
        

class ExpenceListView(ListCreateAPIView):

    serializer_class = ExpencesSerializer
    
    def get_queryset(self):
        queryset = Expences.objects.all()
        return queryset
    

    def post(self, request):
        data = request.data
        expence = ExpencesSerializer(data=data)
        expence.is_valid()
        expence.save()
        return Response('Expence added successfully.', status=status.HTTP_201_CREATED)
    

class ExpenceDetailUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Expences.objects.all()
    lookup_field = 'id'
    serializer_class = ExpencesSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ExpencesSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        ecpence = ExpencesSerializer(instance, data=data)
        ecpence.is_valid()
        ecpence.save()

        if instance:
            return Response("Expence updated successfully", status=status.HTTP_200_OK)
        return Response("Error with request data", status=status.HTTP_400_BAD_REQUEST)
    
    
class ReturnListView(ListCreateAPIView):

    serializer_class = ReturnSerializer
    
    def get_queryset(self):
        queryset = Returns.objects.all()
        return queryset
    

    def post(self, request):
        data = request.data
        returns = ReturnSerializer(data=data)
        returns.is_valid()
        returns.save()
        return Response('Return added successfully.', status=status.HTTP_201_CREATED)
    

class ReturnDetailUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Returns.objects.all()
    lookup_field = 'id'
    serializer_class = ReturnSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ReturnSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        returns = ReturnSerializer(instance, data=data)
        returns.is_valid()
        returns.save()

        if instance:
            return Response("Return updated successfully", status=status.HTTP_200_OK)
        return Response("Error with request data", status=status.HTTP_400_BAD_REQUEST)
    

class ProductListView(ListCreateAPIView):

    serializer_class = ProductSerializer
    
    def get_queryset(self):
        queryset = Products.objects.all()
        return queryset
    

    def post(self, request):
        data = request.data
        product = ProductSerializer(data=data)
        product.is_valid()
        product.save()
        return Response('Product added successfully.', status=status.HTTP_201_CREATED)
    

class ProductDetailUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    lookup_field = 'id'
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        product = ProductSerializer(instance, data=data)
        product.is_valid()
        product.save()

        if instance:
            return Response("Product updated successfully", status=status.HTTP_200_OK)
        return Response("Error with request data", status=status.HTTP_400_BAD_REQUEST)
    

class SalesView(APIView):

    def get(self, request):
        current_month = request.GET.get('month', datetime.now().month)
        filtered_sales = get_filtered_sales(request, current_month)
        card_info = getSummary(filtered_sales, current_month)

        data = {
            'sales': filtered_sales,
            'card_data': card_info
        }
        return Response(data, status = status.HTTP_200_OK)
    
    def post(self, request):
        values = dict(request.POST.items())
        products = Products.objects.all()

        for product in products:
            db = Sales()
            db.Date = values['date']
            db.Product = product
            db.NumberOfSales = values.get(product.name, 0)
            db.Discount = int(request.POST.get('discount'))
            db.Staff = Staffs.objects.get(id=values['staff'])
            db.save()
            
        return Response({'message': 'Sale Created successfully.'}, status=status.HTTP_200_OK)
        

    def put(self, request):
        # Retrieve data from the request
        sale_id = request.data.get('id')
        new_quantity_sold = int(request.data.get('quantity_sold'))
        new_discount = int(request.data.get('discount'))

        try:
            sale = Sales.objects.get(id=sale_id)
            sale.NumberOfSales = new_quantity_sold
            sale.Discount = new_discount
            sale.save()
        
            return Response({'message': 'Sale updated successfully.'}, status=status.HTTP_200_OK)
        
        except Sales.DoesNotExist:
            return Response({'message': 'Sale not found.'}, status=status.HTTP_404_NOT_FOUND)