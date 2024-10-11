from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer


class ClientViewSet(viewsets.ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        instance=serializer.save(updated_at=self.request.user)
        return Response({'updated_at': instance.updated_at}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_project(self, request, pk=None):
        client = self.get_object()
        project_name = request.data.get('project_name')
        users = request.data.get('users')

        project = Project.objects.create(
            project_name=project_name,
            client=client,
            created_by=request.user
        )
        for user in users:
            user_obj = User.objects.get(id=user['id'])
            project.users.add(user_obj)

        project.save()
        return Response(ProjectSerializer(project).data)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        instance=serializer.save(updated_by=self.request.user)
        return Response({'updated_at': instance.updated_at}, status=status.HTTP_200_OK)


        
