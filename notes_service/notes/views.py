from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NoteSerializer, UserSerializer
from .models import Note
from functools import wraps


def validate_id(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        pk = kwargs.get('pk')
        # Validate the ID parameter
        try:
            Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return Response({"error": f'Note with id {pk} not found'}, status=status.HTTP_404_NOT_FOUND)
        return view_func(request, *args, **kwargs)

    return wrapper


@permission_classes([IsAuthenticated])
class NotesList(APIView):

    def get(self, request):
        note = Note.objects.all()
        return Response(NoteSerializer(note, many=True).data)

    @swagger_auto_schema(request_body=NoteSerializer)
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class NotesView(APIView):

    def get(self, request, pk):
        note = Note.objects.get(pk=pk)
        return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=NoteSerializer)
    def put(self, request, pk):
        note = Note.objects.get(pk=pk)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @validate_id
    def delete(self, request, pk):
        note = Note.objects.get(pk=pk)
        note.delete()
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
