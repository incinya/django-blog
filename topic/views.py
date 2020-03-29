import json

from django.http import JsonResponse
from django.shortcuts import render

from message.models import Message
from tools.login_check import login_check, get_user_by_request
from .models import Topic
from user.models import UserProfile


# Create your views here.
@login_check('POST', 'DELETE')
def topics(request, author_id):
    if request.method == 'GET':
        # 获取用户博客数据
        # 前端地址 -> http://127.0.0.1:5000/<username>/topics
        # author_id 被访问的博客的博主用户名

        # visitor 访客 【1，登陆了 2，游客（未登录）】
        # author  博主  当前被访问博客的博主
        authors = UserProfile.objects.filter(username=author_id)
        if not authors:
            result = {'code': 308, 'error': 'no author'}
            return JsonResponse(result)
        # 取出结果中的博主
        author = authors[0]

        # visitor ?
        visitor = get_user_by_request(request)
        visitor_name = None
        if visitor:
            visitor_name = visitor.username

        # 获取 t_id
        t_id = request.GET.get('t_id')
        # 若有t_id存在,执行tid查询语句
        if t_id:
            # 此变量代表是否是自己访问自己(给默认值的时候给Flase,否则如果后面逻辑问题.会直接显示隐私)
            is_self = False

            t_id = int(t_id)
            # 根据t_id进行查询
            if author_id == visitor_name:
                # 此情况表示博主访问自己的博客
                try:
                    author_topic = Topic.objects.get(id=t_id)
                    # 测试 #
                    """
                    {'_state': <django.db.models.base.ModelState object at 0x7f7ed6a82048>, 
                    'id': 2, 'title': 'the first', 
                    'category': 'tec', 
                    'limit': 'public', 
                    'introduce': 'this is the first blog', 
                    'content': '<p>this is the first blog</p>', 
                    'created_time': datetime.datetime(2019, 9, 2, 9, 35, 12, 646314), 
                    'modified_time': datetime.datetime(2019, 9, 2, 9, 35, 12, 646345), 
                    'author_id': 'alicinya'}
                    """



                except Exception:
                    result = {'code': 312, 'error': 'no topic'}
                    return JsonResponse(result)
            else:
                # 此情况表示访客访问博主的博客
                try:
                    author_topic = Topic.objects.get(id=t_id, limit='public')


                except Exception as e:
                    result = {'code': 313, 'error': 'no topic!'}
                    return JsonResponse(result)

            # author_topic文章搜寻对象的主体
            result = make_topic_res(author, author_topic, is_self)
            aa = 1
            return JsonResponse(result)

        category = request.GET.get('category')
        if category:
            topics = Topic.objects.filter(category=category)
        else:
            topics = Topic.objects.all()
        # 返回
        res = make_topics_res(author, topics)
        return JsonResponse(res)


    elif request.method == 'POST':
        # 创建用户博客数据
        json_str = request.body
        if not json_str:
            result = {'code': 301, 'error': 'Please give me json'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        title = json_obj.get('title')

        # xss注入
        import html
        # 进行转义
        title = html.escape(title)

        if not title:
            result = {'code': 302, 'error': 'Please give me title'}
            return JsonResponse(result)
        content = json_obj.get('content')
        if not content:
            result = {'code': 303, 'error': 'Please give me content'}
            return JsonResponse(result)
        # 获取纯文本内容 - 用于切割文章简介
        content_text = json_obj.get('content_text')
        if not content_text:
            result = {'code': 304, 'error': 'Please give me content_text'}
            return JsonResponse(result)
        # 切割简介
        introduce = content_text[:30]
        limit = json_obj.get('limit')
        if limit not in ['public', 'private']:
            result = {'code': 305, 'error': 'Your limit is wrong'}
            return JsonResponse(result)
        category = json_obj.get('category')

        # 创建数据
        Topic.objects.create(title=title, category=category, limit=limit, content=content, introduce=introduce,
                             author=request.user)
        result = {'code': 200, 'username': request.user.username}
        return JsonResponse(result)

    elif request.method == 'DELETE':
        # 博主删除自己的文章
        # /v1/topics/<author_id>
        # token存储的用户
        author = request.user
        token_author_id = author.username
        # url中传过来的author_id 必须与token中的用户名相等
        if author_id != token_author_id:
            result = {'code': 309, 'error': 'You can not do it '}
            return JsonResponse(result)

        topic_id = request.GET.get('topic_id')

        try:
            topic = Topic.objects.get(id=topic_id)
        except:
            result = {'code': 310, 'error': 'You can not do it !'}
            return JsonResponse(result)

        # 删除
        if topic.author.username != author_id:
            result = {'code': 311, 'error': 'You can not do it !! '}
            return JsonResponse(result)

        topic.delete()
        res = {'code': 200}
        return JsonResponse(res)

    return JsonResponse({'code': 200, 'error': 'this is test'})


def make_topics_res(author, topics):
    res = {'code': 200, 'data': {}}
    data = {}
    data['nickname'] = author.nickname
    topics_list = []
    for topic in topics:
        d = {}
        d['id'] = topic.id
        d['title'] = topic.title
        d['category'] = topic.category
        d['introduce'] = topic.introduce
        d['author'] = topic.author_id
        d['created_time'] = topic.created_time.strftime('%Y-%m-%d %H:%M:%S')
        # 测试 #
        # print(topic.__dict__)
        """
        {'_state': <django.db.models.base.ModelState object at 0x7fba73c2f0f0>,
         'id': 4, 
         'title': 'alice first',
         'category': 'tec', 
         'limit': 'public', 
         'introduce': "this is the alice's first blog", 
         'content': "<p>this is the alice's first blog<br></p>",
         'created_time': datetime.datetime(2019, 9, 2, 9, 52, 17, 905548),
         'modified_time': datetime.datetime(2019, 9, 2, 9, 52, 17, 905576), 
         'author_id': 'alice'}
        
        """
        # print(author.__dict__)
        """
        {'_state': <django.db.models.base.ModelState object at 0x7ff901892588>, 
        'username': 'alice', 
        'nickname': 'alice', 
        'email': 'no@no.no', 
        'password': 'e10adc3949ba59abbe56e057f20f883e', 
        'sign': '', 'info': '', 'avatar': ''}
        
        """

        topics_list.append(d)

    data['topics'] = topics_list
    res['data'] = data
    return res


def make_topic_res(author, author_topic, is_self):
    """
    拼接详情页 返回的数据

    """
    if is_self:
        # 博主访问自己的博客
        # 下一个文章: 取出ID大于当前博客ID的第一个且author为当前作者的
        # 例如 (1,4,6,8)当前是1--->下一个是4
        next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author).first()
        # 上一篇文章: 取出ID小于当前博客ID的最后一个且author为当前作者的
        last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author).last()

    else:
        # 访客访问博主的,区别就是访客只能看到limit='public'属性的文章
        # 下一篇
        next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author, limit='public').first()
        last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author, limit='public').last()

    if next_topic:
        next_id = next_topic.id
        next_title = next_topic.title
    else:
        next_id = None
        next_title = None

    if last_topic:
        last_id = last_topic.id
        last_title = last_topic.title
    else:
        last_id = None
        last_title = None

    """
    "messages": [
            {"id": 1,
            "content": "<p>写得不错啊,大哥<br></p>",
            "publisher": "guoxiaonao",
            "publisher_avatar": "avatar/头像 2.png",
            "reply": [
                {"publisher": "guoxiaonao",
                "publisher_avatar": "avatar/头像 2.png",
                "created_time": "2019-06-03 07:52:16",
                "content": "谢谢您的赏识",
                "msg_id": 2}
            ],
            "created_time": "2019-06-03 07:52:02"}],
            "messages_count": 2}}
    """

    all_messages = Message.objects.filter(topic=author_topic).order_by('-created_time')
    msg_list = []
    reply_dict = {}
    msg_count = 0
    for msg in all_messages:
        msg_count += 1
        if msg.parent_message == 0:
            # 当前是留言
            msg_list.append({'id': msg.id, 'content': msg.content, 'publisher': msg.publisher.nickname,
                             'publisher_avatar': str(msg.publisher.avatar),
                             'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S'), 'reply': []})
        else:
            reply_dict.setdefault(msg.parent_message, [])
            reply_dict[msg.parent_message].append({})
            reply_dict[msg.parent_message].append({'msg.id': msg.id, 'content': msg.content,
                                                   'publisher': msg.publisher.nickname,
                                                   'publisher_avatar': str(msg.publisher.avatar),
                                                   'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S')
                                                   })
    for each_comment in reply_dict.values():
        for comment_dict in each_comment:
            if not comment_dict:
                each_comment.remove(comment_dict)

    # 合并 msg_list 和 reply_dict
    for _msg in msg_list:
        if _msg['id'] in reply_dict:
            _msg['reply'] = reply_dict[_msg['id']]

    res = {'code': 200, 'data': {}}
    res['data']['nickname'] = author.nickname
    res['data']['title'] = author_topic.title
    res['data']['category'] = author_topic.category
    res['data']['created_time'] = author_topic.created_time.strftime('%Y-%m-%d %H:%M:%S')
    res['data']['content'] = author_topic.content
    res['data']['introduce'] = author_topic.introduce
    res['data']['author'] = author.nickname

    res['data']['next_id'] = next_id
    res['data']['next_title'] = next_title
    res['data']['last_id'] = last_id
    res['data']['last_title'] = last_title
    # message 评论信息 暂时为假数据
    res['data']['messages'] = msg_list
    res['data']['message_count'] = len(msg_list)
    return res
