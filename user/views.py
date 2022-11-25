import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer
from django.contrib.auth import authenticate


class Register(APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "User registered sucessfully", 'status': 201, 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        """
         for logging of the user
        """
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Login successfully!', 'status': 202},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)
