from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from authentication.models import CustomUser
from authentication.serializers import RegistrationSerializer


class CustomUserViewSet(viewsets.ViewSet):
    """
    A viewset to handle user creation and authentication.
    """
    queryset = CustomUser.objects.all()
    
    def list(self, request):
        serializer = RegistrationSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    
    def create(self, request):
        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    
