from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    else:
        instance.auth_token.save()


class Group(models.Model):
    class meta:
        db_table  = 'groups'
        
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    members = ArrayField(models.IntegerField())


class Message(models.Model):
    class meta:
        db_table  = "message_table"
        
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=500)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE)
    likes = models.IntegerField(default = 0)
    


