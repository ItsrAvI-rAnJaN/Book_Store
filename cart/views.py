from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.models import Cart
from cart.serializers import CartSerializer
import logging
from drf_yasg.utils import swagger_auto_schema

from user.utils import verify_token

logging.basicConfig(filename="cart.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class CartAPI(APIView):
    @swagger_auto_schema(request_body=CartSerializer, responses={201: 'Created', 400: 'BAD REQUEST'})
    @verify_token
    def post(self, request):
        """
        Function for adding books to the cart
        """
        try:
            serializer = CartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Cart Created Successfully', 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response({'message': str(e), 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema()
    @verify_token
    def get(self, request):
        """
        Function for get carts
        """
        try:
            item_list = Cart.objects.filter(user=request.data.get('user'))
            serializer = CartSerializer(item_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=CartSerializer, responses={204: 'Deleted', 400: 'BAD REQUEST'})
    @verify_token
    def delete(self, request, id):
        """
        Function for delete cart
        """
        try:
            cart = Cart.objects.get(id=id)
            cart.delete()
            return Response({"Message": "Cart Deleted Successfully", "status": 204})
        except Exception as err:
            logging.error(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)
