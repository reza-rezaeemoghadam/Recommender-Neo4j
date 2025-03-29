from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from recommender.models import User, Product
from recommender.api.v1.serializers import UserSerializer, ProductSerializer, RatingSerializer


@extend_schema(
    responses={200: UserSerializer(many=True)},  # The response schema is automatically inferred
    request=UserSerializer,  # Request body schema for POST requests
)
class UserAPIView(APIView):
    def get(self, request, format=None):
        # You can replace this with dynamic user input from request
        users = User.nodes.all()
        user_data = UserSerializer(users, many=True).data
        return Response(user_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # Create a new user
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Save user data in the database (Neo4j)
            user = User(username=serializer.validated_data['username'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    responses={200: ProductSerializer(many=True)},
    request=ProductSerializer,
)
class ProductAPIView(APIView):
    def get(self, request, format=None):
        products = Product.nodes.all()
        product_data = ProductSerializer(products, many=True).data
        return Response(product_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # Create a new product
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            # Save product data in the database (Neo4j)
            product = Product(name=serializer.validated_data['name'], category=serializer.validated_data['category'])
            product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    responses={200: RatingSerializer(many=True)},
    request=RatingSerializer,
)
class RatingAPIView(APIView):
    def get(self, request, format=None):
        # Get a user (replace with dynamic user input from request)
        user = User.nodes.get(username="Alice")  # You can replace this with dynamic input
        ratings = user.rated.all()  # Get all ratings related to this user

        # Prepare the data to be serialized
        data = []
        for rating in ratings:
            data.append({
                'product_name': rating.name,
                'score': rating.score,
            })

        # Return the serialized data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # Add a rating for a product by a user
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            # Get the user and product
            user = User.nodes.get(username=request.data['username'])  # Replace with dynamic username
            product = Product.nodes.get(name=request.data['product_name'])

            # Create a Rating relationship
            rating = user.rated.connect(product, {"score": serializer.validated_data['score']})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)