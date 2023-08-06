from base64 import urlsafe_b64decode, urlsafe_b64encode
from binascii import a2b_hex, b2a_hex
from pathlib import Path

import maya

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self



def debug_log(base, fname, *args, **kwargs):
    """log data to file, used when debugging at server"""
    ss = list(args)
    ss.extend([f"{k}: {v}" for k, v in kwargs.items()])
    ss.extend([f"{maya.now().datetime('Asia/Shanghai')}", "-" * 20, ""])
    with Path(base).with_name(fname).open("a") as fp:
        fp.write("\n".join(map(str, ss)))


def get_client_ip(request):
    """get the ip of the visitor"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def resolve_url(request, pk_xx, url_name="notify", app_name=None):
    """get absolute url as: https://www.host.com/wechats/notify/{pk_xx}/"""
    from django.urls import reverse

    app_name = app_name or request.resolver_match.app_name
    url_name = f"{app_name}:{url_name}"
    return request.build_absolute_uri(reverse(url_name, args=(pk_xx,)))


def be_star(s):
    if not s:
        return s
    if len(s) > 200:
        head, tail = 50, -45
        length = 6
    else:
        head, tail = 3, -4
        length = len(s) - head + tail
    return f'{s[:head]}{"*"*length}{s[tail:]}'


def star_attr(obj, *args):
    for attr in args:
        setattr(obj, attr, be_star(getattr(obj, attr)))
    return obj


def is_alipay(request):
    """check whether the browser if alipay"""
    return "AlipayClient/" in request.META.get("HTTP_USER_AGENT", "")


def is_wechat(request):
    """check whether the browser is wechat"""
    return "MicroMessenger/" in request.META.get("HTTP_USER_AGENT", "")


def is_qq(request):
    """check whether the browser is qq"""
    return " QQ/" in request.META.get("HTTP_USER_AGENT", "")


def get_scan_type(request):
    """tell the scan tool"""
    if is_wechat(request) or is_qq(request):
        return "wechat"
    if is_alipay(request):
        return "alipay"
    return "unknown"


def pk_encrypted(pk):
    """19 -> 4d546b3d"""
    return b2a_hex(urlsafe_b64encode(str(pk).encode())).decode()


def decrypt_pk(s):
    """4d546b3d -> 19"""
    return urlsafe_b64decode(a2b_hex(s)).decode()


# -- Deprecated --
# from django.conf import settings
# from django.http import Http404
# class RobotFilter:
#     """对于请求过于频繁的ip，直接返回404"""
#
#     cishu = 1000
#     expire = 40 * 60
#
#     @classmethod
#     def check(cls, ip):
#         red = redis.StrictRedis(settings.REDIS_SERVER)
#         if red.get(ip) and int(red.get(ip)) >= cls.cishu:
#             # raise Http404(_("非法请求次数过多，页面让外星人劫持了"))
#             raise Http404
#
#     @classmethod
#     def incr(cls, ip):
#         red = redis.StrictRedis(settings.REDIS_SERVER)
#         if red.get(ip):
#             red.incr(ip)
#         else:
#             red.set(ip, 1, cls.expire)
