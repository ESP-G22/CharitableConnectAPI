from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets
from rest_framework.status import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import django

class CCEventListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Gets a list of events", responses={200: openapi.Response("OK", CCEventSerializer(many=True))})
    def get(self, request, format=None):
        return Response([CCEventSerializer(event).data for event in Event.objects.all()])

class CCEventView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Gets the specified event", responses={200: openapi.Response("OK", CCEventSerializer()),404: openapi.Response("Event not found")})
    def get(self, request, pk):
        try:
            event = Event.objects.get(pk = pk)
        except Event.DoesNotExist:
            return Response({"ok": False, "error": "Event not found."},status=HTTP_404_NOT_FOUND)
        return Response(CCEventSerializer(event).data,status=HTTP_200_OK)
    
    @swagger_auto_schema(operation_description="Updates the specified event",query_serializer=CCEventSerializer() ,responses={200: openapi.Response("OK"),404: openapi.Response("Event Not Found"),401: openapi.Response("Unauthorized. This may occur if a non-staff user attempts to update an event for which they are not an organiser."),400: openapi.Response("Bad Request. The input data may be in the incorrect format. Refer to documentation.")})
    def put(self, request, pk):
        try:
            event = Event.objects.get(pk = pk)
        except Event.DoesNotExist:
            return Response({"ok": False, "error": "Event not found."},status=HTTP_404_NOT_FOUND)
        if not request.user.is_staff and event.organiser.pk != request.user.id:
            return Response({"ok": False, "error": "Unauthorized: You are not event organiser."}, status=HTTP_401_UNAUTHORIZED)
        serializer = CCEventSerializer(event,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"ok": True, "msg": "Event has been successfully updated."}, status=HTTP_200_OK)
        else:
            return Response({"ok": False, "error": serializer.errors}, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Deletes the specified event", responses={200: openapi.Response("OK"),404: openapi.Response("Event Not Found"),401: openapi.Response("Unauthorized. This may occur if a non-staff user attempts to delete an event for which they are not an organiser.")})
    def delete(self, request, pk):
        try:
            event = Event.objects.get(pk = pk)
        except Event.DoesNotExist:
            return Response({"ok": False, "error": "Event not found."},status=HTTP_404_NOT_FOUND)
        if not request.user.is_staff and event.organiser.pk != request.user.id:
            return Response({"ok": False, "error": "Unauthorized: You are not event organiser."}, status=HTTP_401_UNAUTHORIZED)
        event.delete()
        return Response({"ok": True, "msg": "Event has been successfully deleted."}, status=HTTP_200_OK)

class CCEventCreationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Creates a new event",query_serializer=CCNewEventSerializer(),responses={200: openapi.Response("OK", CCEventSerializer()),400: openapi.Response("Bad Request. The input data may be in the incorrect format. Refer to documentation.")})
    def post(self, request):
        serializers = CCNewEventSerializer(data = request.data)
        if serializers.is_valid():
            validated_data = serializers.validated_data
            validated_data['organiser'] = request.user
            serializers.save()
            return Response({"ok": True, "msg": "New Event has been created", "data": CCEventSerializer(serializers.validated_data).data}, status=HTTP_200_OK)
        else:
            return Response({"ok": False, "error": serializers.errors}, status=HTTP_400_BAD_REQUEST)