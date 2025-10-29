from rest_framework import serializers
from .models import Block,ParkingSlot

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        # include all fields (id, block_name, vehicle_type, created_at, updated_at)
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_block_name(self, value):
        # optional extra validation example: ensure non-empty / strip
        value = value.strip()
        if not value:
            raise serializers.ValidationError("block_name cannot be empty.")
        return value
    
class ParkingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, attrs):
        # when creating via serializer, block may be in attrs or available on instance during update
        block = attrs.get('block') or getattr(self.instance, 'block', None)
        type_of_vehicle = attrs.get('type_of_vehicle') or getattr(self.instance, 'type_of_vehicle', None)

        if block and type_of_vehicle:
            # enforce that slot vehicle type matches block vehicle type (optional rule)
            if block.vehicle_type != type_of_vehicle:
                raise serializers.ValidationError({
                    'type_of_vehicle': (
                        f"Slot vehicle type '{type_of_vehicle}' does not match block "
                        f"vehicle_type '{block.vehicle_type}'."
                    )
                })
        return attrs