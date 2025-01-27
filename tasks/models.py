from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Label(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='labels')
    class Meta:
        unique_together = ['name', 'owner']

    def __str__(self):
        return self.name
    
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    labels = models.ManyToManyField(Label)

    def mark_completed(self):
        self.completed = True
        self.save()
    def mark_incomplete(self):
        self.completed = False
        self.save()
    def __str__(self):
        return self.title

