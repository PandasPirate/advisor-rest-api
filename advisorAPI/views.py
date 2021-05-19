from django.shortcuts import render
from rest_framework import response
from .models import Advisor
from rest_framework import serializers
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view , permission_classes 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def addAdvisor(request):
    serializers = AddAdvisorSerializer(data=request.data,many=False)
    # HttpResponse(request.data)
    if serializers.is_valid():
        serializers.addAdvisor()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def registerUser(request):
    serializers = registerUserSerializer(data=request.data,many=False)
    if serializers.is_valid():
        user,token = serializers.registerUser()
        return Response(data={"user_id":user.id,'Token':token},status=status.HTTP_200_OK)
    else:
        return Response(data=serializers.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def loginUser(request):
    serializers = loginUserSerializer(data=request.data,many=False)
    if serializers.is_valid():
        user,token = serializers.loginUser()
        return Response(data={'user_id':user.id,'username':user.username,'token':token},status=status.HTTP_200_OK)
    else:
        return Response(data=serializers.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAdvisorList(request, **kwargs):
    get = Advisor.objects.all()
    serializers = getAdvisorListSerializer(get, many=True) 
    return Response(data=serializers.data,status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookAdvisor(request,user_id,advisor_id):
    serializers = bookAdvisorSerializer(data=request.data,many=False)
    if serializers.is_valid():
        book = Booking.objects.create(userid=User.objects.get(id=user_id),advisorid=Advisor.objects.get(id=advisor_id),booking_time=dict(request.data)['booking_time'])
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(data=serializers.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBookedCalls(request,user_id):
    bookings = Booking.objects.all()
    resp = []
    for get in bookings:
        serializers = getBookedCallsSerializer(get,many=False)
        # print("this")
        # print(serializers.data['advisorid'])
        advisor = Advisor.objects.get(id=serializers.data['advisorid'])
        data = {
            'Advisor Name':advisor.name,
            'Advisor Profile_pic' : advisor.photo_url,
            'Advisor ID' : advisor.id,
            'Booking time' : serializers.data['booking_time'],
            'Booking ID' : serializers.data['id']
        }
        resp.append(data)
    return Response(data=resp,status=status.HTTP_200_OK)

