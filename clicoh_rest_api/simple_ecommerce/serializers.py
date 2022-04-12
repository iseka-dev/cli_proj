from rest_framework import serializers
from .models import Product, Order, OrderDetail
from drf_writable_nested.serializers import WritableNestedModelSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"

class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model=OrderDetail
        fields=["id","quantity","product"]
        extra_kwargs = {'id': {'read_only': False, 'required': True}}


class OrderSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(source='details',many=True)
    total = serializers.SerializerMethodField()
    total_en_usd = serializers.SerializerMethodField()

    class Meta:
        model=Order
        fields=["id","date_time","order_detail","total","total_en_usd"]

    def get_total(self, obj):
        return obj.get_total()

    def get_total_en_usd(self,obj):
        return obj.get_total_usd()

    def create(self, validated_data):
        detail = validated_data.pop('details')
        order = Order.objects.create(**validated_data)
        order_detail = OrderDetail.objects.create(
            order=order,
            quantity=detail['quantity'],
            product=detail['product']
        )
        return order

    def update(self, instance, validated_data):
        date_time=validated_data['date_time']
        if instance.date_time != date_time:
            instance.date_time=date_time
            instance.save()
        for det in validated_data['details']:
            detail = OrderDetail.objects.get(id=det['id'])
            changed_quantity = detail.quantity != det['quantity']
            changed_product = detail.product != det['product']
            if changed_quantity | changed_product:
                q_dif = detail.quantity - det['quantity']
                detail.quantity=det['quantity']
                detail.product=det['product']
                detail.save()
                prod = Product.objects.get(id=det['product'].id)
                if q_dif != 0:
                    prod.stock = prod.stock + q_dif
                    prod.save()
        return instance
