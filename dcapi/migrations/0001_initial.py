# Generated by Django 4.2.6 on 2023-10-08 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Components',
            fields=[
                ('componentid', models.BigAutoField(primary_key=True, serialize=False)),
                ('componentname', models.CharField(max_length=100)),
                ('componentprice', models.IntegerField()),
                ('componentimage', models.CharField(max_length=256)),
                ('componentdescription', models.CharField(blank=True, max_length=10000, null=True)),
                ('componentstatus', models.SmallIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'components',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('userid', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('userrole', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Datacentercreations',
            fields=[
                ('creationid', models.BigAutoField(primary_key=True, serialize=False)),
                ('creationdate', models.DateField()),
                ('creationapproveddate', models.DateField(blank=True, null=True)),
                ('creationrejectiondate', models.DateField(blank=True, null=True)),
                ('creationcompleteddate', models.DateField(blank=True, null=True)),
                ('creationdeletiondate', models.DateField(blank=True, null=True)),
                ('creationstatus', models.SmallIntegerField()),
                ('userid', models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.DO_NOTHING, to='dcapi.users')),
            ],
            options={
                'db_table': 'datacentercreations',
            },
        ),
        migrations.CreateModel(
            name='Creationcomponents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('componentsnumber', models.IntegerField()),
                ('status', models.SmallIntegerField()),
                ('componentid', models.ForeignKey(db_column='componentid', on_delete=django.db.models.deletion.DO_NOTHING, to='dcapi.components')),
                ('creationid', models.ForeignKey(db_column='creationid', on_delete=django.db.models.deletion.DO_NOTHING, to='dcapi.datacentercreations')),
            ],
            options={
                'db_table': 'creationcomponents',
            },
        ),
    ]
