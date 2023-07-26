from django.db.models.signals import post_save
from django.dispatch import receiver
from recharge.models import Transaction


@receiver(post_save, sender=Transaction)
def update_transaction_signal(sender, instance, created, **kwargs):
    print("sender ==> ", sender)
    print("instance ==> ", instance)
    print("created ==> ", created)
    if created:
        print("saved create model triggered")
    else:
        print("update model triggered")
