from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Hive, HiveUpdate
from .serializers import HiveSerializer, HiveUpdateSerializer

# === Investor Views ===
class AvailableHivesView(generics.ListAPIView):
    queryset = Hive.objects.filter(status='available')
    serializer_class = HiveSerializer
    permission_classes = [IsAuthenticated]

class InvestInHiveView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        hive = get_object_or_404(Hive, pk=pk, status='available')
        amount = request.data.get('amount_hbar')
        if not amount or float(amount) != float(hive.price_hbar):
            return Response({'error': 'Invalid amount'}, status=400)
        
        hive.status = 'sold'
        hive.investor = request.user
        hive.save()
        return Response({'message': 'Investment recorded. NFT will be minted.'})

class MyPortfolioView(generics.ListAPIView):
    serializer_class = HiveSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Hive.objects.filter(investor=self.request.user)

# === Farmer Views ===
class FarmerHivesView(generics.ListAPIView):
    serializer_class = HiveSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Hive.objects.filter(farmer=self.request.user.farmer_profile)

class SubmitUpdateView(generics.CreateAPIView):
    serializer_class = HiveUpdateSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        hive = get_object_or_404(Hive, pk=self.kwargs['hive_pk'], farmer=self.request.user.farmer_profile)
        serializer.save(hive=hive)