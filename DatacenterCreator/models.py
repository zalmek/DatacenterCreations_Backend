from django.db import models


class Components(models.Model):
    componentid = models.BigAutoField(primary_key=True)
    componentname = models.CharField(max_length=100)
    componentprice = models.IntegerField()
    componentimage = models.BinaryField()
    componentdescription = models.CharField(max_length=1000, blank=True, null=True)
    componentstatus = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'components'


class Creationcomponents(models.Model):
    creationid = models.ForeignKey('Datacentercreations', models.DO_NOTHING, db_column='creationid')
    componentid = models.ForeignKey(Components, models.DO_NOTHING, db_column='componentid')
    componentsnumber = models.IntegerField()
    status = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'creationcomponents'


class Datacentercreations(models.Model):
    creationid = models.BigAutoField(primary_key=True)
    creationdate = models.DateField()
    creationapproveddate = models.DateField(blank=True, null=True)
    creationrejectiondate = models.DateField(blank=True, null=True)
    creationcompleteddate = models.DateField(blank=True, null=True)
    creationdeletiondate = models.DateField(blank=True, null=True)
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    creationstatus = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'datacentercreations'


class Users(models.Model):
    userid = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100)
    userrole = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'users'
