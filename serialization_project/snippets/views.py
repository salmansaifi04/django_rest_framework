from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetModelSerializer

# Create your views here.
@csrf_exempt
def snippet_list(request):
    """
        List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetModelSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        if request.content_type != 'application/json':
            return JsonResponse({'msg':'Unsupported Content-Type. Use application/json'}, status=415)
        if not request.body:
            return JsonResponse({'msg':'request body can\'t be blank'}, status=400)
        try:
            data = JSONParser().parse(request)
            print(data)
            serializer = SnippetModelSerializer(data=data)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'error':str(e)})
    

@csrf_exempt
def snippet_details(request, pk):
    """
        Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(id=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = SnippetModelSerializer(snippet)
        return JsonResponse(serializer.data, status=200)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetModelSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
    
    return JsonResponse({"msg":"Please select the valid request method"}, status=400)