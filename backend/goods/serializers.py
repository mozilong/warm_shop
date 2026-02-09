from rest_framework import serializers
from .models import Category, Tag, Goods

class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'is_active']

class TagSerializer(serializers.ModelSerializer):
    """标签序列化器"""
    class Meta:
        model = Tag
        fields = ['id', 'name']

class GoodsListSerializer(serializers.ModelSerializer):
    """商品列表序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Goods
        fields = ['id', 'name', 'price', 'stock', 'image', 'sales', 'category_name', 'tags']

class GoodsDetailSerializer(serializers.ModelSerializer):
    """商品详情序列化器"""
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    tag_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Goods
        fields = ['id', 'name', 'category', 'category_id', 'tags', 'tag_ids', 
                  'price', 'stock', 'image', 'description', 'sales', 'is_active', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'sales', 'created_at', 'updated_at']

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        goods = Goods.objects.create(**validated_data)
        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            goods.tags.set(tags)
        return goods

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)
        # 更新商品基本信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # 更新标签
        if tag_ids is not None:
            tags = Tag.objects.filter(id__in=tag_ids)
            instance.tags.set(tags)
        return instance