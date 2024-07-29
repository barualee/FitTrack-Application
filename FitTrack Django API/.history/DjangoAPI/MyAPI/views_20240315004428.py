from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def prediction(request):
     response=JsonResponse({'predicted':'predicted'})
     return set_cors_headers(response)