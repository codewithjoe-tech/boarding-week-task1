from . models import Task
from rest_framework import serializers




class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id','created_at' , 'updated_at' , 'user' , 'is_deleted')