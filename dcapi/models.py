import datetime

from django.db import models
from django.db.models import AutoField, BigAutoField


# Create your models here.
class Components(models.Model):
    componentid = models.BigAutoField(primary_key=True)
    componentname = models.CharField(max_length=100)
    componentprice = models.IntegerField()
    componentimage = models.CharField(max_length=100000)
    componentdescription = models.CharField(max_length=10000, blank=True, null=True)
    componentstatus = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'components'


class DatacenterCreations(models.Model):
    creationid = models.BigAutoField(primary_key=True)
    creationdate = models.DateTimeField(auto_now_add=True)
    creationformdate = models.DateTimeField(blank=True, null=True)
    creationcompleteddate = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='useremail', default="null")
    creationstatus = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'datacentercreations'


class CreationСomponents(models.Model):
    class Meta:
        db_table = 'creationcomponents'
        managed = False
        unique_together = (("creation", "component"),)

    creation = models.ForeignKey('DatacenterCreations', models.DO_NOTHING, db_column='creationid')
    component = models.ForeignKey('Components', models.DO_NOTHING, db_column='componentid')
    componentsnumber = models.IntegerField(db_column="componentsnumber", default=0)


class Users(models.Model):
    email = models.CharField(db_column="email")
    userid = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100)
    userrole = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'
