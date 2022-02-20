from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Blogger(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    # follows = models.ManyToManyField('self',blank=True,symmetrical=False)
    # followed_by = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='followers')

    class Meta:
        verbose_name = _('blogger')
        verbose_name_plural = _('bloggers')


class Blog(models.Model):
    title = models.CharField(_("Blog Title"), max_length=300)
    description = models.TextField(_("Details : "), null=True, blank=True)
    created_at = models.DateTimeField(
        _("Creation Date & Time"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(
        _("Last Updated: "), auto_now=True, db_index=True)
    creator = models.ForeignKey(
        Blogger, on_delete=models.CASCADE, related_name='blogs')

    class Meta:
        ordering = ["-created_at", "title"]

    def __str__(self) -> str:
        return f"{self.id} [ {self.title} ]"

    def get_short_description(self) -> str:
        return self.description[:30]+"..."


class Comment(models.Model):
    boktobyo = models.TextField()
    created_at = models.DateTimeField(
        _("Creation Date & Time"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(
        _("Last Updated: "), auto_now=True, db_index=True)
    commentor = models.ForeignKey(
        Blogger, on_delete=models.CASCADE, related_name='comments')
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        ordering = ["-created_at", "updated_at"]

    def __str__(self) -> str:
        return f"ID: {self.id}"

    def get_short_boktobyo(self) -> str:
        return f"{self.boktobyo[:15]}..."
