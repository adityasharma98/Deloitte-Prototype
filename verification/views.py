from rest_framework.views import APIView
from verification.models import User, Registration
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import serializers, status
from verification.utils import send_code
import requests

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    publicKey = serializers.CharField()
    privateKey = serializers.CharField()
        
    def create(self, validated_data):
        try:
            email = validated_data.get("email")
            publicKey = validated_data.get("publicKey")
            privateKey = validated_data.get("privateKey")
            user = User.objects.create_user(email, email=email)
            request = self.context.get('request')
            send_code(email, user.confirmation_key, request)
            key = Registration.objects.create(user=user, publicKey=publicKey, privateKey=privateKey)
            return key

        except IntegrityError:
            user = User.objects.get(username=email)
            if user.is_confirmed:
                raise serializers.ValidationError({"email":"User is already confirmed"})
            else:
                raise serializers.ValidationError({"email":"Verification email has already been sent"})

# Create your views here.
class SendEmailView(APIView):
    """
    POST: The email address to verify.
    """
    def post(self, request):
        s = RegistrationSerializer(data=request.data, context={"request":request})
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegistrationDetailView(APIView):
    """
    GET: The /email@example.com will retrive the public key and encrypted private key
    """
    def get(self, request, email):
        try:
            key = Registration.objects.get(user__username=email)
            return Response(RegistrationSerializer(key).data)
        except Registration.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
         
    
class VerifyEmailView(APIView):
    """
    GET: The code sent to the email
    """
    def get(self, request, code, email):
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            return Response({"error":"The email id does not exist in the database. Make a post request first."}, status=status.HTTP_400_BAD_REQUEST)
        if user.is_confirmed:
            return Response({"error":"User already confirmed","publicKey":user.registration.publicKey}, status=status.HTTP_200_OK)
        else:
            user.confirm_email(code)
            if user.is_confirmed:
                return Response({"success":"Email verification successful", "publicKey":user.registration.publicKey}, status=status.HTTP_202_ACCEPTED)
            