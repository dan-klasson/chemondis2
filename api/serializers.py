from rest_framework import serializers
from .models import Interview
from .validators import IsOnTheHourValidator


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = '__all__'


class SlotSerializer(serializers.Serializer):
    class Meta:
        validators = [
            IsOnTheHourValidator(fields=['date'])
        ]

    date = serializers.DateTimeField()


class SlotSerializer(serializers.Serializer):
    slots = SlotSerializer(many=True)
