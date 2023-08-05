from rest_framework import serializers


class load_dsd_backend_products__serializer(serializers.Serializer):
    limit = serializers.IntegerField(required=False)
    publish = serializers.BooleanField(required=False)
