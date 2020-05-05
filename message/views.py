import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from message.models import Message
from tools.login_check import login_check
from topic.models import Topic
from user.models import UserProfile


@login_check("POST")
def messages(request):
    topic_id = request.path.split('/')[-1]
    if request.method != "POST":
        result = {'code': 401, 'error': 'please use POST'}
        return JsonResponse(result)

    user = request.user
    """
    print(user.__dict__)
    {'_state': <django.db.models.base.ModelState object at 0x7fc96ff9bb38>, 
    'username': 'alicinya', 
    'nickname': 'alicinya', 
    'email': 'no@no.no', 
    'password': 'e10adc3949ba59abbe56e057f20f883e', 
    'sign': '', 'info': '', 'avatar': ''}
    """
    json_str = request.body

    json_obj = json.loads(json_str.decode())
    # print(json_obj)
    # {'content': '<p>test<br></p>'}

    content = json_obj.get('content')

    if not content:
        result = {'code': 401, 'error': 'no content'}
        return JsonResponse(result)
    parent_id = json_obj.get('parent_id', 0)
    try:
        topic = Topic.objects.get(id=topic_id)
    except:
        # topic被删除 or 当前topic_id不真实
        result = {'code': 403, 'error': 'no topic!'}
        return JsonResponse(result)

    # 私有博客只能博主留言
    if topic.limit == 'private':
        # 检查身份
        if user.username != topic.author.username:
            result = {'code': 404, 'error': 'no want see my east west'}
            return JsonResponse(result)
    Message.objects.create(content=content, publisher=user, topic=topic, parent_message=parent_id)

    result = get_data(user)



    result = {'code': 200, 'data': {}}

    return JsonResponse(result)


def get_data(user):
    """

    """
    # print(user.__dict__)
    ...


if __name__ == "__main__":
    ...
