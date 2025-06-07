from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .models import Task
from . serializers import TaskSerializer
User  = get_user_model()






class TaskView(APIView):
    def get(self, request):
        date = request.query_params.get('date')
        tasks = Task.objects.filter(user=request.user , date=date).order_by('-created_at','-completed')
        serializer = TaskSerializer(tasks, many=True)
        cache.set(f'tasks_{request.user.id}_{date}', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)