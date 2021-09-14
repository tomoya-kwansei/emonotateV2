from __future__ import unicode_literals

from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

import random
import string


def randomname(n=6):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)


class EmailUserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser,
                     **extra_fields):
        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        is_active = extra_fields.pop("is_active", True)

        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        is_staff = extra_fields.pop("is_staff", False)

        return self._create_user(
            username,
            email,
            password,
            is_staff,
            False,
            **extra_fields
        )

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(
            username,
            email, password,
            True,
            True,
            **extra_fields
        )


class EmailUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32, default=randomname(8))

    email = models.EmailField(
        max_length=256,
        unique=True,
        error_messages={
            'unique': 'That email address is already taken.'
        }
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    objects = EmailUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.email

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return '%s(%s)' % (self.username, self.email)


class ValueType(models.Model):
    user = models.ForeignKey(EmailUser, default=1, on_delete=models.CASCADE)
    title = models.CharField(default='', max_length=256)
    axis_type = models.IntegerField(choices=(
        (1, '平常状態を含んで上と下がある値'),
        (2, '平常状態から上にしか上がらない値')), default=1)

    def __str__(self):
        return self.title


class Content(models.Model):
    user = models.ForeignKey(EmailUser, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    url = models.URLField(default='', max_length=1024)
    data_type = models.CharField(default='video/mp4', max_length=32)

    def __str__(self):
        return self.title


class Curve(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(EmailUser,
                             default=1,
                             on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.PROTECT)
    value_type = models.ForeignKey(ValueType, default=1, on_delete=models.CASCADE)
    values = JSONField()
    version = models.CharField(max_length=16)

    def __str__(self):
        return '{} {}'.format(self.content.title, self.id)


class Request(models.Model):
    room_name = models.CharField(max_length=6, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128, default="")
    description = models.TextField(blank=False, default="")
    owner = models.ForeignKey(EmailUser, 
                              default=1,
                              on_delete=models.CASCADE, 
                              related_name='owner')
    participants = models.ManyToManyField(EmailUser)
    content = models.ForeignKey(
        Content, 
        default=1,
        on_delete=models.CASCADE)
    value_type = models.ForeignKey(
        ValueType,
        default=1,
        on_delete=models.CASCADE
    )

    def save(self, **kwargs):
        if not self.room_name:
            self.room_name = randomname()
            while Request.objects.filter(room_name=self.room_name).exists():
                self.room_name = randomname()
        super(Request, self).save(**kwargs)
    
    def __str__(self):
        return f'{self.title}({self.room_name})'


class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(EmailUser, default=1, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, default=1, null=True, on_delete=models.SET_NULL)
    value_type = models.ForeignKey(ValueType, default=1, null=True, on_delete=models.SET_NULL)
    room = models.CharField(max_length=128, default="")
    description = models.TextField(blank=False, default="")
    state = models.CharField(max_length=128, default="")
