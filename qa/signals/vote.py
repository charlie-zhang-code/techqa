# qa/signals/vote.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from qa.models import Vote


@receiver(post_save, sender=Vote)
def update_reputation_on_vote(sender, instance, created, **kwargs):
    if created:
        target_user = None
        points = 0

        if instance.question:
            target_user = instance.question.author
            points = 5 if instance.vote_type == 'up' else -2
        elif instance.answer:
            target_user = instance.answer.author
            points = 10 if instance.vote_type == 'up' else -2

        if target_user and target_user != instance.user:
            target_user.reputation += points
            target_user.save()


@receiver(post_delete, sender=Vote)
def revert_reputation_on_vote_delete(sender, instance, **kwargs):
    target_user = None
    points = 0

    if instance.question:
        target_user = instance.question.author
        points = -5 if instance.vote_type == 'up' else 2
    elif instance.answer:
        target_user = instance.answer.author
        points = -10 if instance.vote_type == 'up' else 2

    if target_user and target_user != instance.user:
        target_user.reputation += points
        target_user.save()