from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

import json
from datetime import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView

from .models import *
from .serializers import *

# Create your views here.

class CategoryListView(ListAPIView):
    authentication_classes = []
    serializer_class = CategorySerializer
    model = Category
    queryset = Category.objects.all()

class LetteringItemCategoryListView(ListAPIView):
    authentication_classes = []
    serializer_class = LetteringItemCategorySerializer
    model = LetteringItemCategory
    queryset = LetteringItemCategory.objects.all()

class ProductListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    model = Product
    queryset = Product.objects.all()

class ProductFromCategoryListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    model = Product
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        category_id = self.kwargs.get(self.lookup_url_kwarg)
        return Product.objects.filter(category__id=category_id)

class ProductColorListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductColorSerializer
    model = ProductColor
    queryset = ProductColor.objects.all()

class LogoListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    model = Product
    queryset = Product.objects.filter(category__title='Truck Sign', is_uploaded=False)

class ProductDetail(RetrieveAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    model = Product
    lookup_field = 'id'
    queryset = Product.objects.all()

class ProductVariationRetrieveView(RetrieveAPIView):
    authentication_classes = []
    serializer_class = ProductVariationSerializer
    model = ProductVariation
    lookup_field = 'id'
    queryset = ProductVariation.objects.all()

class CreateOrder(GenericAPIView):
    authentication_classes = []
    serializer_class = OrderSerializer

    def post(self, request, id, format=None):
        data = request.data

        product = Product.objects.get(id=id)

        product_variation = ProductVariation(product=product)
        product_variation.save()

        lettering_items = data['lettering_items']
        for custom_lettering_item in lettering_items:
            if custom_lettering_item['text'] and custom_lettering_item['text'].strip():
                item_category = LetteringItemCategory.objects.get(title=custom_lettering_item['title'])
                item_category.save()
                lettering_item = LetteringItemVariation(lettering_item_category=item_category, lettering=custom_lettering_item['text'], product_variation=product_variation)
                lettering_item.save()

        try:
            product_color = ProductColor.objects.get(id=data['product_color_id'])
        except:
            product_color = None
        product_variation.product_color = product_color
        product_variation.amount = 1
        product_variation.save()

        order_serializer = OrderSerializer(data=data['order'])
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save(product=product_variation, payment=None)
        order_serializer = OrderSerializer(order)

        return Response({"Result": order_serializer.data}, status=status.HTTP_200_OK)

class RetrieveOrder(RetrieveAPIView):
    authentication_classes = []
    serializer_class = OrderSerializer
    model = Order
    lookup_field = 'id'
    queryset = Order.objects.all()

class CommentsView(ListAPIView):
    authentication_classes = []
    serializer_class = CommentSerializer
    model = Comment
    queryset = Comment.objects.all().filter(visible=True)

class CommentCreateView(CreateAPIView):
    authentication_classes = []
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class UploadCustomerImage(GenericAPIView):
    authentication_classes = []

    def post(self, request, form=None):
        data = request.data
        product_title = "Customer-Image-" + str(datetime.now())
        category = Category.objects.get(title="Truck Sign")
        product = Product(category=category, title=product_title, is_uploaded=True)
        product.save()

        product_serializer = ProductSerializer(product, data=data, partial=True)
        product_serializer.is_valid(raise_exception=True)
        product = product_serializer.save()
        product.detail_image = product.image
        product.save()
        product_serializer = ProductSerializer(product)
        return Response({"Result": product_serializer.data}, status=status.HTTP_200_OK)