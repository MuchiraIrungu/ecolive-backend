# hives/serializers.py
from rest_framework import serializers
from .models import Hive, HiveUpdate

class HiveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiveUpdate
        fields = ['honey_kg', 'health', 'photo']

class HiveSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.full_name', read_only=True)
    updates = HiveUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = Hive
        fields = [
            'id', 'hive_id', 'location', 'price_hbar', 'status',
            'token_id', 'nft_serial', 'farmer_name', 'updates'
        ]