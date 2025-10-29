from django.db import models
from django.utils import timezone

class Block(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('bike', 'Bike'),
        ('car', 'Car'),
        ('truck_bus', 'Truck/Bus'),
    ]

    id = models.AutoField(primary_key=True)
    block_name = models.CharField(max_length=100, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    no_blocked = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.block_name} ({self.get_vehicle_type_display()})"




class ParkingSlot(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('bike', 'Bike'),
        ('car', 'Car'),
        ('truck_bus', 'Truck/Bus'),
    ]

    id = models.AutoField(primary_key=True)
    block = models.ForeignKey(
        'Block',                     
        on_delete=models.CASCADE,    
        related_name='slots'
    )
    type_of_vehicle = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPE_CHOICES
    )
    available = models.BooleanField(default=True)
    not_blocked = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Slot {self.id} - {self.block.block_name} ({self.type_of_vehicle})"