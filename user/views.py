from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from CharitableConnectAPI.authentication import BearerAuthentication
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import django

class CCUserListView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Gets a list of users", responses={200: openapi.Response("OK", CCUserGetSerializer(many=True))})
    def get(self, request, format=None):
        if request.user.is_staff:
            usernames = [{'pk': user.pk, 'username': user.username} for user in CCUser.objects.all()]
        else:
            usernames = [{'pk': user.pk, 'username': user.username} for user in CCUser.objects.filter(is_staff=False)]
        return Response(usernames)

class CCUserProfileView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return CCUser.objects.get(pk=pk)
    
    @swagger_auto_schema(operation_description="Gets the specified user's profile information", responses={200: openapi.Response("OK", CCUserProfileSerializer()),404: openapi.Response("User not found")})
    def get(self, request: Request, pk, format=None):
        userId = request.query_params.get('user_id')
        try:
            user = CCUser.objects.get(pk=pk)
        except CCUser.DoesNotExist:
            return Response({},status=404)
        return Response(CCUserProfileSerializer(user.profile).data)
    
    @swagger_auto_schema(operation_description="Updates the specified user", responses={200: openapi.Response("OK", CCUserProfileSerializer()),404: openapi.Response("User not found"),400: openapi.Response("Bad request. The input data may be in the incorrect format. Refer to documentation."),403: openapi.Response("Forbidden. This may occur if a non-staff user attempts to update the profile of a user that isn't themselves.")})
    def put(self, request: Request, pk, format=None):
        try:
            user = self.get_object(pk)
        except CCUser.DoesNotExist:
            return Response({},status=404)
        if not request.user.is_staff and request.user.pk != user.pk:
            return Response({}, status=403)
        serializer = CCUserProfileSerializer(user.profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=400)


class CCUserRegisterView(APIView):
    authentication_classes = [BearerAuthentication]

    @swagger_auto_schema(operation_description="Registers a new user", responses={200: openapi.Response("OK", CCUserGetSerializer()),400: openapi.Response("Bad request. The input data may be in the incorrect format. Refer to documentation.")},query_serializer=CCUserRegisterSerializer())
    def post(self, request, format=None):
        serializer = CCUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            newCCUser = CCUser.objects.create(
                email = serializer.validated_data['email'],
                password = django.contrib.auth.hashers.make_password(serializer.validated_data['password']),
                username = serializer.validated_data['username']
            )
            newCCUser.save()
            responseData = CCUserGetSerializer(newCCUser)
            return Response(responseData.data)
        else:
            return Response(serializer.errors,status=400)

class CCUserPasswordChangeView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]
    model = CCUser

    @swagger_auto_schema(operation_description="Changes the password of a user", responses={200: openapi.Response("OK"),400: openapi.Response("Bad request. The old password might be incorrect, or the input data may be in the incorrect format. Refer to documentation.")},query_serializer=CCUserPasswordChangeSerializer())
    def put(self, request, format=None):
        user = self.request.user
        serializer = CCUserPasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('oldPassword')):
                return Response({'error':'Incorrect old password'}, status=400)
            user.set_password(serializer.data.get("newPassword"))
            user.save()
            return Response(status=200)
        return Response(serializer.errors, status=400)