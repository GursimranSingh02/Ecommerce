from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import serializers, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product


class ProductCreateInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    inStock = serializers.BooleanField()
    image = serializers.FileField()


class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = ProductCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        values = serializer.validated_data

        image_storage = FileSystemStorage(location=Path(settings.BASE_DIR) / "Images")
        saved_image_name = image_storage.save(values["image"].name, values["image"])
        image_path = f"Images/{saved_image_name}"

        product = Product.objects.create(
            name=values["name"],
            description=values["description"],
            price=values["price"],
            inStock=values["inStock"],
            imagePath=image_path,
        )

        return Response(
            {
                "status": status.HTTP_201_CREATED,
                "message": "Product created successfully.",
                "data": {
                    "id": product.pk,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "inStock": product.inStock,
                    "imagePath": product.imagePath,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class ProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            page = int(request.query_params.get("page", 1))
            page_size = int(request.query_params.get("pageSize", 10))
        except (TypeError, ValueError):
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "page and pageSize must be positive integers.",
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if page < 1 or page_size < 1:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "page and pageSize must be positive integers.",
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        products = Product.objects.order_by("pk")
        start = (page - 1) * page_size
        end = start + page_size
        page_products = products[start:end]

        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": "Products retrieved successfully.",
                "data": {
                    "products": [
                        {
                            "id": product.pk,
                            "name": product.name,
                            "description": product.description,
                            "price": product.price,
                            "inStock": product.inStock,
                            "imagePath": product.imagePath,
                        }
                        for product in page_products
                    ],
                    "nextPage": products.count() > end,
                },
            },
            status=status.HTTP_200_OK,
        )
