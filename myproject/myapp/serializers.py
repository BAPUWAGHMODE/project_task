from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']

class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    client_name = serializers.CharField(source='client.client_name', read_only=True)
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'client_name', 'users', 'created_at', 'created_by']

    def create(self, validated_data):
        users = validated_data.pop('users', [])
        project = Project.objects.create(**validated_data)
        project.users.set(users)
        return project
