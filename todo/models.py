import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def current_date_time_validator(value):
    if value and value < timezone.now():
        raise ValidationError(
            _('%(value)s is in the past'),
            params={'value': value},
        )


def current_date_validator(value: datetime.date):
    if value and value < timezone.now().date():
        raise ValidationError(
            _('%(value)s is in the past'),
            params={'value': value},
        )


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    deadline_date = models.DateField(blank=True, null=True, validators=[current_date_validator])
    deadline_time = models.TimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    deadline_date = models.DateField(blank=True, null=True, validators=[current_date_validator])
    deadline_time = models.TimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    occurrence_minutes = models.IntegerField(blank=True, null=True)
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


class ChangeManager(models.Manager):
    def get_last_id(self, user):
        if not self.filter(owner=user).exists():
            return 0
        return self.filter(owner=user).last().change_id


class Change(models.Model):
    CREATED = 'C'
    UPDATED = 'U'
    DELETED = 'D'
    CHANGE_CHOICES = (
        (CREATED, 'Created'),
        (UPDATED, 'Updated'),
        (DELETED, 'Deleted'),
    )
    PROJECT = 'P'
    TASK = 'T'
    TAG = 'G'
    SHARED = 'S'
    MODEL_CHOICES = (
        (PROJECT, 'Project'),
        (TASK, 'Task'),
        (TAG, 'Tag'),
        (SHARED, 'Shared'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=1, choices=CHANGE_CHOICES)
    change_id = models.IntegerField()
    content_type = models.CharField(max_length=1, choices=MODEL_CHOICES)
    object_id = models.CharField(max_length=100)

    objects = ChangeManager()

    class Meta:
        unique_together = ('owner', 'change_id')


class Shared(models.Model):
    PROJECT = 'P'
    TASK = 'T'
    TAG = 'G'

    SHARED_CHOICES = (
        (PROJECT, 'Project'),
        (TAG, 'Tag'),
        (TASK, 'Task'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='share_owner')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='share_with')
    content_type = models.CharField(max_length=1, choices=SHARED_CHOICES)
    object_id = models.CharField(max_length=100)

