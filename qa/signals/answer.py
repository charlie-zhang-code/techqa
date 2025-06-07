# qa/signals/answer.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from qa.models import Answer, Notification


@receiver(post_save, sender=Answer)
def notify_question_author(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            notification_type='question_answered',
            recipient=instance.question.author,
            actor=instance.author,
            question=instance.question,
            answer=instance
        )

    if instance.is_accepted:
        Notification.objects.create(
            notification_type='answer_accepted',
            recipient=instance.author,
            actor=instance.question.author,
            question=instance.question,
            answer=instance
        )