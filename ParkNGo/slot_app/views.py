# views.py
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Block, ParkingSlot
from .serilizer import BlockSerializer, ParkingSlotSerializer   

# Create a new Block
class BlockCreateAPIView(generics.CreateAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # add custom message but keep serializer data intact
        response.data = {
            "message": "Block created successfully!",
            "data": response.data
        }
        return response


class BlockRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        # call parent update (handles PUT and PATCH)
        response = super().update(request, *args, **kwargs)
        response.data = {
            "message": "Block updated successfully!",
            "data": response.data
        }
        return response


# Parking slot create (APIView)
class ParkingSlotCreateAPIView(APIView):
    """
    POST /api/slots/  -> create a parking slot
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = ParkingSlotSerializer(data=request.data)
        if serializer.is_valid():
            slot = serializer.save()
            return Response(
                {"message": "Slot created successfully", "data": ParkingSlotSerializer(slot).data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParkingSlotUpdateAPIView(APIView):
    """
    PUT /api/slots/<int:pk>/   -> full update
    PATCH /api/slots/<int:pk>/ -> partial update
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        return get_object_or_404(ParkingSlot, pk=pk)

    @transaction.atomic
    def put(self, request, pk, *args, **kwargs):
        slot = self.get_object(pk)
        serializer = ParkingSlotSerializer(slot, data=request.data)
        if serializer.is_valid():
            slot = serializer.save()
            return Response({"message": "Slot updated", "data": ParkingSlotSerializer(slot).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def patch(self, request, pk, *args, **kwargs):
        slot = self.get_object(pk)
        serializer = ParkingSlotSerializer(slot, data=request.data, partial=True)
        if serializer.is_valid():
            slot = serializer.save()
            return Response({"message": "Slot partially updated", "data": ParkingSlotSerializer(slot).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
