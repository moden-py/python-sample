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

    def __init__(self, name, *args, **kwargs):
        """Init storage."""
        self.name = name
        super().__init__(*args, **kwargs)

    def dump(self):
        """Dump dict to local file in json format."""
        with open('{}.json'.format(self.name), 'w') as f:
            json.dump(self, f)
