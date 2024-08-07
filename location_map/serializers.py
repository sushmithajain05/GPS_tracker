from rest_framework import serializers
from .models import Location,TrainStation
#for location model
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'latitude', 'longitude','created_at']

#for trainstation model
class TrainStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainStation
        fields = '__all__'