from rest_framework import serializers

from . import models


class ViewListSerializer(serializers.Serializer):
    enabled = serializers.BooleanField()

    def create(self, validated_data):
        return models.View.objects.create(**validated_data)


class ViewDetailSerializer(serializers.Serializer):
    enabled = serializers.BooleanField()
