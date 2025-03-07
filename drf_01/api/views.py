from django.shortcuts import render
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse

STATIC_TOKEN = "your_static_token_here"

# Create your views here.
def Student_info(request, pk):
    token = request.headers.get("Authorization")
    if token!=STATIC_TOKEN:
        return JsonResponse({
            "data": {},
            "status_code": 401,
            "msg": "Unauthorized: Invalid or missing token"
        }, status=401)
    try:
        stu = Student.objects.get(id=pk)
        serializer = StudentSerializer(stu)
        # json_data = JSONRenderer().render(serializer.data)
        data_dict = {
            "data":serializer.data,
            "status_code":200,
            "msg":"success",
            "error":""
        }
        return JsonResponse(data_dict, status=200)
        # return HttpResponse(data_dict)
    except Student.DoesNotExist:
        data_dict = {
            "data":{},
            "status_code":404,
            "msg":"Student not found",
            "error":""
        }
        return JsonResponse(data_dict, status=404)
    except Exception as e:
        data_dict = {
            "data":{},
            "status_code":404,
            "msg":"error",
            "error":str(e)
        }
        return JsonResponse(data_dict, status=404)
    
def Student_list(request):
    token = request.headers.get("Authorization")
    if token!=STATIC_TOKEN:
        return JsonResponse({
            "data": {},
            "status_code": 401,
            "msg": "Unauthorized: Invalid or missing token"
        }, status=401)
    try:
        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        # json_data = JSONRenderer().render(serializer.data)
        data_dict = {
            "data":serializer.data,
            "status_code":200,
            "msg":"success",
            "error":""
        }
        return JsonResponse(data_dict, status=200)
        # return HttpResponse(data_dict)
    except Student.DoesNotExist:
        data_dict = {
            "data":{},
            "status_code":404,
            "msg":"Student not found",
            "error":""
        }
        return JsonResponse(data_dict, status=404)
    except Exception as e:
        data_dict = {
            "data":{},
            "status_code":404,
            "msg":"error",
            "error":str(e)
        }
        return JsonResponse(data_dict, status=404)