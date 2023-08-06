from fancy_me.processor import processor

class MiddleWare(object):
    """消息处理中间件"""

    async def __call__(self, *args, **kwargs):
        """此处函数作为被调用----> 触发处理方法"""
        d = kwargs.get('data')
        t = kwargs.get('event_type')
        await processor.process_event(event_type=t, data=d)


middle_ware = MiddleWare()