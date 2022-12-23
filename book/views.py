import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from book.models import Book
from book.serialization import AllBookSerializer
from user.utils import verify_superuser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from book.redis_book import RedisBook


class BookAPI(APIView):
    @swagger_auto_schema(request_body=AllBookSerializer,
                         responses={201: 'CREATED', 400: 'BAD REQUEST'})
    @verify_superuser
    def post(self, request):
        try:
            serializer = AllBookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisBook().add_book(request.data.get("user"), serializer.data)
            return Response({"message": "Book added", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema()
    def get(self, request):
        try:
            # book_list = Book.objects.all()
            # serializer = AllBookSerializer(book_list, many=True)
            get_data = RedisBook().get_book(user=request.data.get("user"))
            return Response({"message": "Data retrieved","redis_data": get_data}, status=status.HTTP_200_OK)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'author': openapi.Schema(type=openapi.TYPE_STRING),
            'price': openapi.Schema(type=openapi.TYPE_INTEGER),
            "quantity": openapi.Schema(type=openapi.TYPE_INTEGER),
        }),
        responses={201: "ok", 400: "BAD REQUEST"})
    @verify_superuser
    def put(self, request):
        try:
            book_object = Book.objects.get(id=request.data.get("id"))
            serializer = AllBookSerializer(book_object, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisBook().update_book(request.data.get("user"), serializer.data)
            return Response({"message": "Update successful", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER)
        }),
        responses={200: 'OK', 400: 'BAD REQUEST'})
    @verify_superuser
    def delete(self, request):
        try:
            book_object = Book.objects.get(id=request.data.get("id"))
            book_object.delete()
            RedisBook().delete_note(request.data.get("id"))
            return Response({"message": "Book deleted"}, status=status.HTTP_200_OK)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)
