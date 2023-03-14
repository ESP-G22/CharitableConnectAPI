from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from .serializer import *
from events.models import Event
from .models import RSVP
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from CharitableConnectAPI.authentication import BearerAuthentication

class CCRSVPCreationView(APIView):
    """
    This view creates a new RSVP request on an event.
    POST Parameter:
        event: int
    """
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="This view creates a new RSVP request on an event.",
        responses={
            201: openapi.Response("Event Created.", CCRSVPSerializer()),
            400: openapi.Response("Event does not exist."),
            409: openapi.Response("User has already RSVPed.")
        },
        query_serializer=CCRSVPCreationSerializer()
    )
    def post(self, request):
        serializer = CCRSVPCreationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                event = Event.objects.get(pk=serializer.validated_data['event'])
            except Event.DoesNotExist: # If event is not found return error
                return Response({
                    'ok': False,
                    'error': "Event does not exist."
                }, status=HTTP_400_BAD_REQUEST)

            if any([r.user.pk == request.user.pk for r in event.rsvp_set.all()]):
                return Response({
                    'ok': False,
                    'error': "RSVP has already been created."
                }, status=HTTP_409_CONFLICT)

            # Create new RSVP
            newRSVP = RSVP(
                event=event,
                user=request.user
            )
            newRSVP.save()

            # Return new RSVP object
            return Response({
                'ok': True,
                'data': CCRSVPSerializer(newRSVP).data
            }, status=HTTP_201_CREATED)

        else: # POST body validation failed
            return Response({
                'ok': False,
                'errors': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)

class CCRSVPView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="This view gets the detail of a RSVP using ID",
        responses={
            200: openapi.Response("OK", CCRSVPSerializer()),
            400: openapi.Response("RSVP does not exist."),
            401: openapi.Response("Unauthorized. This RSVP does not belong to current user.")
        }
    )
    def get(self, request, pk):
        try:
            rsvp = RSVP.objects.get(pk=pk)
        except RSVP.DoesNotExist:  # If event is not found return error
            return Response({
                'ok': False,
                'error': "Event does not exist."
            }, status=HTTP_400_BAD_REQUEST)
        if not (rsvp.user.pk == request.user.pk or rsvp.event.organiser.pk == request.user.pk):
            return Response({
                'ok': False,
                'error': "Unauthorized. This rsvp does not belong to current user."
            }, status=HTTP_401_UNAUTHORIZED)
        return Response({
                'ok': True,
                'data': CCRSVPSerializer(rsvp).data
            }, status=HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="This view deletes an RSVP.",
        responses={
            200: openapi.Response("OK"),
            400: openapi.Response("RSVP does not exist."),
            401: openapi.Response("Unauthorized. This RSVP does not belong to current user.")
        }
    )
    def delete(self, request, pk):
        try:
            rsvp = RSVP.objects.get(pk=pk)
        except RSVP.DoesNotExist:  # If event is not found return error
            return Response({
                'ok': False,
                'error': "RSVP does not exist."
            }, status=HTTP_400_BAD_REQUEST)
        if rsvp.user.pk != request.user.pk:
            return Response({
                'ok': False,
                'error': "Unauthorized. This RSVP does not belong to current user."
            }, status=HTTP_401_UNAUTHORIZED)
        rsvp.delete()
        return Response({
                'ok': True,
                'msg': "RSVP has been deleted."
            }, status=HTTP_200_OK)
