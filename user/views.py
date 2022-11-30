import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import LoginSerializer, RegisterSerializer
from .utils import JWT
from user.task import send_user_email_task


class Register(APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = JWT().encode(
                data={"username": serializer.data.get("username"), "user_id": serializer.data.get("id")})
            send_user_email_task.delay(token, serializer.data.get("email"))
            return Response({"message": "User registered successfully", 'status': 201, 'data': serializer.data},
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
            token = JWT().encode(data={"user_id": serializer.data.get("id")})
            return Response({"message": "Login Successfully", "status": 202, "data": token},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyToken(APIView):
    def get(self, request, token=None):
        try:
            decoded = JWT().decode(token)
            user = User.objects.get(username=decoded.get("username"))
            if not user:
                raise Exception("Invalid user")
            user.save()
            return Response("Token verified")
        except Exception as e:
            logging.exception(e)
            return Response(str(e), status=400)
