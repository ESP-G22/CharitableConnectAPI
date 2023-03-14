from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser
from django.http.response import HttpResponse
from CharitableConnectAPI.authentication import BearerAuthentication
from .serializer import ImageSerializer, ImageUploadResponseSerializer
from .models import Image
import mimetypes
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ImageUploadView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Upload an image, return an uuid as the unique identifier of the image",
        responses={
            200: openapi.Response("Success", ImageUploadResponseSerializer()),
            400: openapi.Response("Incorrect format")
        },
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Image to be uploaded'),
        ],
    )
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(ImageUploadResponseSerializer(obj).data)
        return Response(serializer.errors, 400)


class ImageRetrieveView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Download an image using id",
        responses={
            200: ImageUploadResponseSerializer(),
            404: openapi.Response({"ok": False, "error": "Image not found"})
        }
    )
    def get(self, request, id):
        try:
            image = Image.objects.get(id=id)
            print(mimetypes.guess_type(image.file.path))
            print(image.file.path)
            resp = HttpResponse(open(image.file.path,'rb').read(),
                            content_type=mimetypes.guess_type(image.file.path)[0])
            return resp
        except Image.DoesNotExist:
            return Response({"ok": False, "error": "Image not found"}, status=404)