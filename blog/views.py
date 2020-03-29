from django.http import JsonResponse
from user.models import UserProfile


def test_api(request):
    # 加入分布式锁
    import redis

    r = redis.Redis(host="127.0.0.1",port=6379,db=0)

    while True:
        try:
            with r.lock('alicinya',blocking_timeout=3):
                # 对score字段进行+1操作
                u = UserProfile.objects.get(username="alicinya")
                u.score += 1
                u.save()
            break
        except Exception as e:
            print('Lock is Failed----')
    return JsonResponse({'code': 200})
