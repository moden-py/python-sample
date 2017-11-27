"""Utils for simple scrappers."""

import json


class Singleton(type):
    """Singleton."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Overwrite call method."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Storage(dict, metaclass=Singleton):
    """Storage."""

    def dump(self):
        """Dump dict to local file in json format."""
        for task_name, data in self.items():
            with open('{}.json'.format(task_name), 'w') as f:
                json.dump(self[task_name], f)
