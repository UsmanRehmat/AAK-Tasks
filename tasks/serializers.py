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
    labels = serializers.PrimaryKeyRelatedField(many=True, queryset=Label.objects.all())
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'owner', 'labels']
        read_only_fields = ['owner']
    def update(self, instance, validated_data):
        labels = validated_data.pop('labels')
        if labels is not None:
            instance.labels.set(labels)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user