"""Notification model."""

from django.db import models
from django.contrib.auth import get_user_model

from .fields import JSONField


class NotificationQuerySet(models.QuerySet):
    """Notifications QuerySet."""

    def all_unread(self):
        """Return all unread notifications."""

        return self.filter(is_read=False)

    def all_read(self):
        """Return all read notifications."""

        return self.filter(is_read=True)


class Notification(models.Model):
    """
    Model for notifications.

    Parameters:
    ----------
    source: A ForeignKey to Django's User model
        (Can be null if it's not a User to User Notification)

    source_display_name: A User Friendly name
        for the source of the notification.

    recipient: The Recipient of the notification.
        It's a ForeignKey to Django's User model.

    action: Verbal action for the notification
        E.g Sent, Cancelled, Bought e.t.c

    obj: The id of the object associated with the notification
        (Can be null)

    short_description: The body of the notification.

    url: The url of the object associated with the notification
        (Can be null)
    """

    User = get_user_model()

    class Meta:
        """Specify ordering for notifications."""
        ordering = ('-id',)

    source = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    source_display_name = models.CharField(max_length=150, null=True)
    recipient = models.ForeignKey(
        User, related_name='notifications', on_delete=models.CASCADE
    )
    action = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    obj = models.IntegerField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    short_description = models.CharField(max_length=100)
    extra_data = JSONField(default='')
    is_read = models.BooleanField(default=False)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    # register queryset
    objects = NotificationQuerySet.as_manager()

    def __str__(self):
        if self.source:
            res = '{}: {} {} {} => {}'.format(
                self.category, self.source, self.action,
                self.short_description, self.recipient
            )
        else:
            res = self.short_description

        return res

    def read(self):
        """Mark notification as read."""
        self.is_read = True
        self.save()

    def to_json(self):
        """Return JSON representation that can easily be serialized."""
        return {
            'source': self.source.username,
            'source_display_name': self.source_display_name,
            'recipient': self.recipient.username, 'category': self.category,
            'action': self.action, 'obj': self.obj,
            'short_description': self.short_description, 'url': self.url,
            'is_read': self.is_read
        }
