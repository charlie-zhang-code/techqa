# qa/signals/question.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from qa.models import Question, Notification, Vote, Answer


@receiver(post_save, sender=Question)
def update_tag_usage(sender, instance, created, **kwargs):
    if created:
        for tag in instance.tags.all():
            tag.usage_count += 1
            tag.save()


@receiver(post_delete, sender=Question)
def decrease_tag_usage(sender, instance, **kwargs):
    for tag in instance.tags.all():
        tag.usage_count -= 1
        tag.save()


@receiver(post_save, sender=Answer)
def update_hot_score_on_answer(sender, instance, created, **kwargs):
    if created:
        instance.question.update_hot_score()


@receiver(post_save, sender=Vote)
@receiver(post_delete, sender=Vote)
def update_hot_score_on_vote(sender, instance, **kwargs):
    if instance.question:
        instance.question.update_hot_score()
