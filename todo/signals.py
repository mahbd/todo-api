from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Change, Project, Tag, Task, Shared


@receiver(post_save)
def project_post_save(sender, instance, created, **kwargs):
    if sender == Project:
        content_type = Change.PROJECT
    elif sender == Tag:
        content_type = Change.TAG
    elif sender == Task:
        content_type = Change.TASK
    elif sender == Shared:
        content_type = Change.SHARED
    else:
        return
    if created:
        Change.objects.create(
            owner=instance.owner,
            action=Change.CREATED,
            content_type=content_type,
            object_id=str(instance.pk),
            change_id=Change.objects.get_last_id(instance.owner) + 1
        )
    else:
        Change.objects.create(
            owner=instance.owner,
            action=Change.UPDATED,
            content_type=content_type,
            object_id=str(instance.pk),
            change_id=Change.objects.get_last_id(instance.owner) + 1
        )


@receiver(post_delete)
def project_post_delete(sender, instance, **kwargs):
    if sender == Project:
        content_type = Change.PROJECT
    elif sender == Tag:
        content_type = Change.TAG
    elif sender == Task:
        content_type = Change.TASK
    elif sender == Shared:
        content_type = Change.SHARED
    else:
        return
    Change.objects.create(
        owner=instance.owner,
        action=Change.DELETED,
        content_type=content_type,
        object_id=str(instance.pk),
        change_id=Change.objects.get_last_id(instance.owner) + 1
    )
