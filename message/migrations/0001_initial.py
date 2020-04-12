# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-09-02 14:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('topic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=50, verbose_name='留言内容')),
                ('created_time', models.DateField(auto_now_add=True)),
                ('parent_message', models.IntegerField(null=True, verbose_name='父留言ID')),
                ('pulisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserProfile')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topic.Topic')),
            ],
        ),
    ]