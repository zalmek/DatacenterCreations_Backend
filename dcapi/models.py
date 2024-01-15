import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models
from django.db.models import AutoField, BigAutoField


# Create your models here.
class Components(models.Model):
    componentid = models.BigAutoField(primary_key=True)
    componentname = models.CharField(max_length=100)
    componentprice = models.IntegerField()
    componentimage = models.CharField(max_length=100000, null=True, blank=True)
    componentdescription = models.CharField(max_length=10000, blank=True, null=True)
    componentstatus = models.SmallIntegerField(blank=True, null=True, default=1)

    class Meta:
        db_table = 'components'


class CreationСomponents(models.Model):
    creation = models.ForeignKey('DatacenterCreations', models.DO_NOTHING, db_column='creationid')
    component = models.ForeignKey('Components', models.DO_NOTHING, db_column='componentid')
    componentsnumber = models.IntegerField(db_column="componentsnumber", default=0)

    class Meta:
        db_table = 'creationcomponents'
        unique_together = (("creation", "component"),)


class NewUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    objects = NewUserManager()

    email = models.EmailField(("email адрес"), unique=True)
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=255, verbose_name="Пароль")
    is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")

    USERNAME_FIELD = 'email'


class DatacenterCreations(models.Model):
    creationid = models.BigAutoField(primary_key=True)
    creationdate = models.DateTimeField(auto_now_add=True)
    creationformdate = models.DateTimeField(null=True)
    creationcompleteddate = models.DateTimeField(null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid', to_field='id',
                             related_name="user")
    moderator = models.ForeignKey('Users', models.DO_NOTHING, db_column='moderatorid', blank=True, to_field='id',
                                  related_name="moderator")

    def _set_user_email(self):
        return Users.objects.get(id=self.user.id).email

    def _set_moderator_email(self):
        return Users.objects.get(id=self.moderator.id).email

    def _set_full_name(self, combined_name):
        self.first_name, self.last_name = combined_name.split(' ', 1)

    useremail = property(_set_user_email)
    moderatoremail = property(_set_moderator_email)
    creationstatus = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'datacentercreations'
        managed = False


class CreationСomponents(models.Model):
    class Meta:
        db_table = 'creationcomponents'
        managed = False
        unique_together = (("creation", "component"),)

    creation = models.ForeignKey('DatacenterCreations', models.DO_NOTHING, db_column='creationid')
    component = models.ForeignKey('Components', models.DO_NOTHING, db_column='componentid')
    componentsnumber = models.IntegerField(db_column="componentsnumber", default=0)
