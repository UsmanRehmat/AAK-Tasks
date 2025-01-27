from rest_framework import serializers
from .models import Task, Label, User

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'owner']
        read_only_fields = ['owner']
    def validate_name(self, value):
        if Label.objects.filter(name=value, owner=self.context['request'].user).exists():
            raise serializers.ValidationError("Label with this name already exists for this user.")
        return value

class TaskSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'owner', 'labels']
        read_only_fields = ['owner']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user