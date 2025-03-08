from snippets.models import Snippet
from snippets.serializers import SnippetModelSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SnippetList(APIView):
    def get(self, request, format=None):
        snippet = Snippet.objects.all()
        serializer = SnippetModelSerializer(snippet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = SnippetModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetails(APIView):
    def get_object(self, pk):
        try:
            snippet = Snippet.objects.get(id=pk)
            return snippet
        except Snippet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        try:
            serializer = SnippetModelSerializer(snippet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            if snippet.status_code == 404:
                return Response({'msg':'data not found'}, status=status.HTTP_404_NOT_FOUND)
        
    
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        try:
            serializer = SnippetModelSerializer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            if snippet.status_code == 404:
                return Response({'msg':'data not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        try:
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            if snippet.status_code == 404:
                return Response({'msg':'data not found'}, status=status.HTTP_404_NOT_FOUND)