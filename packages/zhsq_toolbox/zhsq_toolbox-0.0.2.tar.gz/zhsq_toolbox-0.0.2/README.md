# Toolbox (backend project)
  def and class for multiply projects

## Install

```bash
pipenv install -e git+https://git.dev.tencent.com/zhengwenjie/toolbox.git#egg=toolbox
```
## Features

- EncryptMixin
- TimeMixin
- timeout
- response_error
- get_client_ip,
- is_wechat
- is_qq
- is_alipay,
- AttrDict

## Usage

~ goto pay

```py
from toolbox import timeout, TimeMixin, is_wechat 

class Klass(TimeMixin):
  @timeout
  def get(self, request):
      if is_wechat(request):
          return HttpResponse('view by wechat')
```

- pretty AttrDict

```
>>> from toolbox import AttrDict
>>> d = {'a': 1, 'b': 'xx'}
>>> d = AttrDict(d)
>>> d.a == d['a'] and d.b == d['b']
True
```
