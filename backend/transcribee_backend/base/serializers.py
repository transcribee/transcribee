from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Document, Task, User, Worker


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("id", "name", "audio_file", "created_at", "changed_at")
        ordering = ["-created_at", "id"]


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ("id", "name")


class TaskSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        document_queryset = kwargs["context"].pop("document_queryset")
        super().__init__(*args, **kwargs)
        self.fields["document"].queryset = document_queryset

    class Meta:
        model = Task
        fields = (
            "id",
            "document",
            "task_type",
            "progress",
            "task_parameters",
            "assigned_worker",
            "last_keepalive",
        )
        read_only_fields = ("assigned_worker", "last_keepalive", "progress")

    def validate_task_parameters(self, value):
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValidationError("Must be a dict")
        return value
