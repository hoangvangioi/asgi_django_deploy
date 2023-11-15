from django.shortcuts import render
from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer

# Create your views here.


class MessageListView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save()
