from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    next_occurrence = models.DateTimeField(blank=True, null=True)
    last_occurrence = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(default=1,
                                   validators=[MinValueValidator(1), MaxValueValidator(5)])
    tags = models.ManyToManyField(Tag, blank=True)
    reminder_minutes = models.IntegerField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
