from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, Label
from .serializers import TaskSerializer, LabelSerializer
from .permissions import IsOwner

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.request.user.tasks.all()
    def perform_create(self, serializer):
        owner=self.request.user
        serializer.save(owner=owner)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['POST'])
    def mark_completed(self, request, pk=None):
        task = self.get_object()
        task.mark_completed()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['POST'])
    def mark_incomplete(self, request, pk=None):
        task = self.get_object()
        task.mark_incomplete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return self.request.user.labels.all()
    
    def perform_create(self, serializer):
        owner= self.request.user
        serializer.save(owner=owner)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)