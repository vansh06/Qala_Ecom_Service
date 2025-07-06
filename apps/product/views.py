from django.shortcuts import render,get_object_or_404
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Product,Review
from django.db.models import Q
from qalankarwaan.utils.pagination import CustomProductPagination
from .serializers import ProductSerializer,ReviewSerializer

# Create your views here.
class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    # return Response({'data':serializer_class.data},status=status.HTTP_200_OK)


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomProductPagination


    def get_queryset(self):
        queryset = Product.objects.all()
        params = self.request.GET

        category = params.get('category')       # category ID
        brand = params.get('brand')
        price_min = params.get('price_min')
        price_max = params.get('price_max')
        stock_status = params.get('stock_status')
        search = params.get('search')

        if category:
            queryset = queryset.filter(category_id=category)
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if stock_status:
            queryset = queryset.filter(stock_status__iexact=stock_status)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        return queryset 
    
class ProductReviewAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, product_id):
        """
        List all reviews for a product
        """
        product = get_object_or_404(Product, id=product_id)
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        """
        Add a new review for a product
        """
        print("product_id--->",product_id)
        print("data--->",request.data)
        print("User instance:", request.user, "Type:", type(request.user))

        product = get_object_or_404(Product, id=product_id)

        # Check if the user already reviewed this product
        if Review.objects.filter(product=product, user_id=(request.user.id)).exists():
            return Response({'detail': 'You have already reviewed this product.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)