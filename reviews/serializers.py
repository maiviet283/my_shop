from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user_full_name', 'product_name', 'comment', 'rating']

    def get_user_full_name(self, obj):
        return obj.user.full_name if obj.user else None

    def get_product_name(self, obj):
        return obj.product.name if obj.product else None
