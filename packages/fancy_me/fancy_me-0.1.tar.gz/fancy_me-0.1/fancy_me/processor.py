from functools import wraps
from typing import Any, Text, Dict


class Processor:
    process_map = dict()

    def register_event(self, event_type: Text, func) -> None:
        if event_type not in self.process_map.keys():
            self.process_map[event_type] = [func]
        if event_type in self.process_map.keys():
            if func not in self.process_map.get(event_type):
                self.process_map.get(event_type).append(func)

    def process_event(self, event_type: Text, **kwargs: Dict) -> None:
        """批量处理数据"""
        try:
            for func in self.process_map.get(event_type):
                func(**kwargs)
        except TypeError:
            pass

processor = Processor()


def ipo(type):
    def decorate(func):
        processor.register_event(type, func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            pass

        return wrapper

    return decorate
