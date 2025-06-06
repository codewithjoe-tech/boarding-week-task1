from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.core.signing import BadSignature, SignatureExpired
from django.core import signing
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .tasks import send_verification_mail,send_otp
import random

User  = get_user_model()




class RegisterUser(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self ,request):
        data= request.data
        serializer=UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data ,status=200)
        return Response(serializer.errors , status=400)
    


class VerifyEmail(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self,request, id):
        try:
            email = signing.loads(id ,salt="email-verification", max_age=1500)
            user = User.objects.get(email = email)
            user.is_verified=True
            user.save()
            return Response({'message' : 'Verification successfull'} , status=200 )
        except (BadSignature , SignatureExpired) as e:
            print(e)
            return Response({'message' : "Link expired."} , status=400)
        except Exception as e:
            return Response({'message' : str(e)} , status=500)
        
    # def post(self ,request):
    #     data= request.data
    #     email = data.get('email')




class Login(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self ,request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({'message' : "User does not exist."} , status=400)
        if not user.check_password(password):
            return Response({'message' : "Incorrect password."} , status=400)
        if not user.is_verified:
            key = f"{email}_verification"
            cach = cache.get(key)
            if cach:
                return Response({'message' : "Email is not verified. Old email is still valid for verification please use it and verify"} , status=400)
            send_verification_mail.delay(email , user.full_name)

            return Response({'message' : "Email is not verified. New email has been sent"} , status=400)
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)

        response = Response(serializer.data , status=200)

        response.set_cookie(key='refresh_token' , value=str(refresh) , httponly=True)
        response.set_cookie(key='access_token' , value=str(refresh.access_token) , httponly=True)

        return response
    


class RefreshView(APIView):
    def post(self ,request):
        
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'message' : "Refresh token not found."} , status=400)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = Response({'access_token' : access_token} , status=200)
            response.set_cookie(key='access_token' , value=access_token , httponly=True)
            return response
        except Exception as e:

            response =  Response({'message' : str(e)} , status=500)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response


class LoginOtp(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self ,request):
        
        
        """
        Handle POST request to send OTP to user's email.

        This method retrieves the email from the request data and checks if the user exists.
        It tracks the number of OTP resend attempts using cache and limits the number of
        attempts to prevent abuse. If the number of attempts is exceeded, it returns an 
        appropriate error message. Otherwise, it generates a new OTP, caches it with a 
        time-to-live based on the attempt count, and sends it to the user's email.

        Args:
            request: The HTTP request object containing user data.

        Returns:
            Response: A DRF Response object with status 200 on success, or 400 with an 
            error message if user doesn't exist or attempt limit is exceeded.
        """
        data = request.data
        email = data.get('email')
        user = User.objects.filter(email=email).first()
        email_attempt = f"{email}_attempt"
        attempt = cache.get(email_attempt)
        if not attempt:
            attempt  =1
            cache.set(email_attempt , 1 , 2*60*60)
        else:
            attempt += 1
            cache.set(email_attempt , attempt , 2*60*60)

        if attempt > 4:
            return Response({'message' : "Too many attempts. Please try again later."} , status=400)
        if user is None:
            return Response({'message' : "User does not exist."} , status=400)
        otp = random.randint(100000 , 999999)
        cache.set(email , otp , 60*attempt+6)
        send_otp.delay(email , otp)
        return Response(status=200)
    

class ResentOTP(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self ,request):
        """
        Handle POST request to resend OTP to user's email.

        This method retrieves the email from the request data and checks if the user exists.
        It tracks the number of OTP resend attempts using cache and limits the number of
        attempts to prevent abuse. If the number of attempts is exceeded, it returns an 
        appropriate error message. Otherwise, it generates a new OTP, caches it with a 
        time-to-live based on the attempt count, and sends it to the user's email.

        Args:
            request: The HTTP request object containing user data.

        Returns:
            Response: A DRF Response object with status 200 on success, or 400 with an 
            error message if user doesn't exist or attempt limit is exceeded.
        """
        
        data = request.data
        email = data.get('email')
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({'message' : "User does not exist."} , status=400)
        email_attempt = f"{email}_attempt"
        attempt = cache.get(email_attempt)
        if not attempt:
            attempt  =1
            cache.set(email_attempt , 1 , 2*60*60)
        else:
            attempt += 1
            cache.set(email_attempt , attempt , 2*60*60)

        if attempt > 4:
            return Response({'message' : "Too many attempts. Please try again later."} , status=400)
        otp = random.randint(100000 , 999999)
        cache.set(email , otp , 60*attempt+6)
        send_otp.delay(email , otp)

        return Response(status=200)
    

class VerifyOTP(APIView):
    permission_classes = []
    authentication_classes  = []

    def post(self , request):

        """
        Verify the OTP sent to user's email.
        
        Args:
            email (str): The email of the user.
            otp (str): The OTP sent to the user.
        
        Returns:
            Response: A response containing a refresh token and an access token if the OTP is valid.
        """

        data = request.data
        email = data.get('email')
        otp = data.get('otp')
        otp_from_cache = cache.get(email)
        if otp_from_cache != int(otp):
          
            return Response({'message' : "Invalid OTP"} , status=400)
        user = User.objects.filter(email=email).first()
        user.is_verified = True
        user.save()
        refresh  = RefreshToken.for_user(user)
        email_attempt = f"{email}_attempt"
        cache.delete(email_attempt)
        
        response =  Response({'message' : "Login successful"} , status=200)
        response.set_cookie(key='refresh_token' , value=str(refresh) , httponly=True)
        response.set_cookie(key='access_token' , value=str(refresh.access_token) , httponly=True)
        return response



class Logout(APIView):
    def post(self , request):
        response =  Response({'message' : "Logout successful"} , status=200)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response