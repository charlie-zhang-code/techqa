# qa/signals/comment.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from qa.models import Comment, Notification


@receiver(post_save, sender=Comment)
def notify_comment_target(sender, instance, created, **kwargs):
    if not created:
        return

    recipient = None
    if instance.question:
        recipient = instance.question.author
    elif instance.answer:
        recipient = instance.answer.author

    if recipient and recipient != instance.author:
        Notification.objects.create(
            notification_type='answer_commented' if instance.answer else 'question_commented',
            recipient=recipient,
            actor=instance.author,
            question=instance.question,
            answer=instance.answer,
            comment=instance
        )

    if instance.reply_to and instance.reply_to.author != instance.author:
        Notification.objects.create(
            notification_type='comment_replied',
            recipient=instance.reply_to.author,
            actor=instance.author,
            question=instance.question,
            answer=instance.answer,
            comment=instance
        )