# Generated by Django 4.2.7 on 2023-12-19 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreationСomponents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('componentsnumber', models.IntegerField(db_column='componentsnumber', default=0)),
            ],
            options={
                'db_table': 'creationcomponents',
                'managed': False,
            },
        ),
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
            name='DatacenterCreations',
            fields=[
                ('creationid', models.BigAutoField(primary_key=True, serialize=False)),
                ('creationdate', models.DateTimeField(auto_now_add=True)),
                ('creationformdate', models.DateTimeField(blank=True, null=True)),
                ('creationcompleteddate', models.DateTimeField(blank=True, null=True)),
                ('creationstatus', models.SmallIntegerField(default=0)),
                ('userid', models.ForeignKey(db_column='userid', default=2, on_delete=django.db.models.deletion.DO_NOTHING, to='dcapi.users')),
            ],
            options={
                'db_table': 'datacentercreations',
            },
        ),
    ]
