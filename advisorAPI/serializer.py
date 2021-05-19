from django.contrib.auth import models
from django.db.models import fields
from django.http import request
from .models import Advisor, Booking, User, auth
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from django.contrib.auth import authenticate, login
import datetime
from django.contrib.auth.models import update_last_login
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
#from rest_framework_jwt.settings import api_settings

class AddAdvisorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Advisor
        fields = ('name','photo_url')
    
    def addAdvisor(self):
        name= self.validated_data['name']
        photo_url = self.validated_data['photo_url']
        newadvisor = Advisor(name = name , photo_url=photo_url)
        newadvisor.save()
        return newadvisor

class registerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','email','password')
    
    def registerUser(self):
        name = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        newuser = User.objects.create_user(username=name,email=email)
        newuser.set_password(password)
        newuser.save()
        payload = JWT_PAYLOAD_HANDLER(newuser)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        update_last_login(None, newuser)
        return newuser, jwt_token

class loginUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email','password')
    
    def loginUser(self):
        #name = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        #user = authenticate(email=email,password=password)
        
        try:
            user = User.objects.get(email=email)
            
            if check_password(password,user.password):
                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_token = JWT_ENCODE_HANDLER(payload)
                update_last_login(None, user)
                return user, jwt_token
            else:
                raise serializers.ValidationError("Password incorrect")
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exists")

class getAdvisorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advisor
        fields = ('__all__')

class bookAdvisorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ('booking_time',)
    # def bookAdvisor():
    #     pass

class getBookedCallsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ('__all__')


