from django.db import models

# Create your models here.
from topic.models import Topic
from user.models import UserProfile


class Message(models.Model):
    content = models.CharField(max_length=50, verbose_name='留言内容')
    created_time = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    publisher = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    parent_message = models.IntegerField(verbose_name='父留言ID', null=True)

    class Meta:
        db_table = 'message'
