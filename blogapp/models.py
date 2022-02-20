from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Blogger(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    # follows = models.ManyToManyField('self',blank=True,symmetrical=False)
    # followed_by = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='followers')

    class Meta:
        verbose_name = _('blogger')
        verbose_name_plural = _('bloggers')

class Blog(models.Model):
    title = models.CharField(_("Blog Title"),max_length=300)
    description = models.TextField(_("Details : "),null=True,blank=True)
    created_at = models.DateTimeField(_("Creation Date & Time"),auto_now_add=True)
    updated_at = models.DateTimeField(_("Last Updated: "),auto_now=True)
    creator = models.ForeignKey(Blogger,on_delete=models.CASCADE,related_name='blogs')