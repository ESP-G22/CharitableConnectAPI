from .models import CCUser, CCUserManager, CCUserProfile
from .serializers import CCUserProfileSerializer
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets
import django
class ListUsersView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if request.user.is_staff:
            usernames = [user.username for user in CCUser.objects.all()]
        else:
            usernames = [user.username for user in CCUser.objects.filter(is_staff=False)]
        return Response(usernames)

class CCUserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return CCUser.objects.get(pk=pk)
    
    def get(self, request: Request, pk, format=None):
        userId = request.query_params.get('user_id')
        try:
            user = CCUser.objects.get(pk=pk)
        except CCUser.DoesNotExist:
            return Response({},status=404)
        return Response(CCUserProfileSerializer(user.profile).data)

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

    # TODO: POST
    # TODO: Password Change