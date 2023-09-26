from rest_framework import serializers
from .models import Staffs, Expences, Returns, Products


class StaffSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  Staffs
        fields = '__all__'


class ExpencesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expences
        fields = '__all__'


class ReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Returns
        fields = '__all__'
        depth = 2


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'