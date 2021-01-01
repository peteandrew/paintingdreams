from django.db import models
from django.utils import timezone


class Feedback(models.Model):
    feedback = models.TextField()
    author_name = models.CharField(max_length=100, blank=True)
    author_email = models.EmailField(blank=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created',]
        verbose_name_plural = 'Feedback items'

    def __str__(self):
        return str(self.created)


class FeedbackProduct(models.Model):
    feedback = models.ForeignKey('Feedback', related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', related_name='feedback_items', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('feedback', 'product')