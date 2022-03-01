from django.conf import settings
from django.db.models.signals import pre_save
from blogapp.models import Blogger
from django.dispatch import receiver

@receiver(pre_save,sender=settings.AUTH_USER_MODEL)
def name_to_lower(sender,**kwargs):
    kwargs['instance'].first_name=kwargs['instance'].first_name.title()
    kwargs['instance'].last_name=kwargs['instance'].last_name.title()
        