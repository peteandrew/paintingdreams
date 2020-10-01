from django.db import models


class HolidayMessage(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    website_message = models.TextField(blank=True)
    email_message = models.TextField(blank=True)
    wholesale_message = models.TextField(blank=True)

    class Meta:
        index_together = [
            ['start', 'end'],
        ]

        ordering = ['-start', '-end']