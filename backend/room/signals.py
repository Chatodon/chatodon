from django.db.models import F
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import RoomMember


@receiver(post_save, sender=RoomMember)
def increment_participants_count(sender, instance, created, **kwargs):
    if created:
        instance.room.__class__.objects.filter(pk=instance.room.pk).update(
            participants_count=F("participants_count") + 1
        )


@receiver(post_delete, sender=RoomMember)
def decrement_participants_count(sender, instance, **kwargs):
    instance.room.__class__.objects.filter(pk=instance.room.pk).update(
        participants_count=F("participants_count") - 1
    )
