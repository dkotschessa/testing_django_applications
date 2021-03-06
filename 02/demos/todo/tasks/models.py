from __future__ import unicode_literals

from django.utils import timezone

from django.db import models
from django.conf import settings


class Task(models.Model):
    """
    Task

    The most important object for this application.
    Allows users to create and edit tasks that they
    need to complete. They can set names, descriptions,
    and due dates.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)

    title = models.CharField(max_length = 100, null = False)
    description = models.TextField(blank = True)
    due_date = models.DateField(blank = True, null = True)
    complete_time = models.DateTimeField(blank = True, null = True)

    @property
    def is_complete(self):
        """
        Checks if a task is complete.
        :return: True if task has been completed as indicated by a truthy
        value for complete_time. Otherwise, False.
        """
        return bool(
            self.complete_time and self.complete_time < timezone.now())

    @property
    def due_soon(self):
        """
        Checks if a task is due soon.
        :return: True if task is due within two days. Otherwise, False.
        """
        if self.complete_time is None:
            due_soon = False
        else:
            due_soon = self.complete_time < (timezone.now() - timezone.timedelta(days = 2))
        return bool(due_soon)
            

    def mark_complete(self):
        """
        Marks a task as complete by storing the current UTC time in complete_time
        """
        self.complete_time = timezone.now()
        self.save()

    def mark_incomplete(self):
        """
        Marks a task as incomplete by storing None in complete_time
        """
        self.complete_time = None
        self.save()
