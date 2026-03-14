from django.db.models import QuerySet

from ..models import Room, RoomMember


def get_active_members_queryset(room: Room) -> QuerySet[RoomMember]:
    """
    Returns a queryset of participants
    considered "real."
    """
    return RoomMember.objects.filter(
        room=room,
        invitation_accepted=True,
        is_banned=False,
    )


def recount_room_participants(room: Room) -> int:
    """
    Recalculates participants_count for a room.
    Returns the new value.
    """
    real_count = get_active_members_queryset(room).count()

    Room.objects.filter(pk=room.pk).update(participants_count=real_count)

    return real_count
