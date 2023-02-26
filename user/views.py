from .models import CCUser, CCUserManager, CCUserProfile
from .serializers import CCUserProfileSerializer
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.request import Request

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

    def get(self, request: Request, format=None):
        userId = request.query_params.get('user_id')
        user = CCUser.objects.get(pk=userId)
        if user == None:
            return Response(status=404)
        else:
            return Response(CCUserProfileSerializer(user.profile).data)
