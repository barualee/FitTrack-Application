from django.shortcuts import render
from django.http import JsonResponse
def set_cors_headers(response):
  response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
  response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Add allowed methods
  response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'  # Add allowed headers
  return response
# Create your views here.
def prediction(request):
     response=JsonResponse({'predicted':'predicted'})
     return set_cors_headers(response)