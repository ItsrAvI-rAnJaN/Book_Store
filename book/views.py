import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from book.models import Book
from book.serialization import AllBookSerializer
from user.utils import verify_superuser


class BookAPI(APIView):
    @verify_superuser
    def post(self, request):
        try:
            serializer = AllBookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Book added", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            book_list = Book.objects.all()
            serializer = AllBookSerializer(book_list, many=True)
            return Response({"message": "Data retrieved", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_superuser
    def put(self, request):
        try:
            book_object = Book.objects.get(id=request.data.get("id"))
            serializer = AllBookSerializer(book_object, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Update successful", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_superuser
    def delete(self, request):
        try:
            book_object = Book.objects.get(id=request.data.get("id"))
            book_object.delete()
            return Response({"message": "Book deleted"}, status=status.HTTP_200_OK)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)
