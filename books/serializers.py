from rest_framework import serializers

class TicketSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    priority = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
