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

    Staff = StaffSerializer()
    class Meta:
        model = Returns
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        staff_data = validated_data.pop('Staff')
        staff, created = Staffs.objects.get_or_create(**staff_data)

        returns = Returns.objects.create(Staff=staff, **validated_data)
        return returns
    
    def update(self, instance, validated_data):
        staff_data = validated_data.pop('Staff')
        staff, created = Staffs.objects.get_or_create(**staff_data)

        instance.Staff = staff
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'