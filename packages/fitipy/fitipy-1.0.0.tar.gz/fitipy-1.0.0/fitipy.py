import sys
from itertools import count
from os import makedirs

import pickle
from os.path import isfile, join, dirname
from typing import MutableSet, MutableMapping, MutableSequence


class Fiti:
    def __init__(self, default_data, *path):
        self.data = default_data
        self.filename = join(*path)
        self.reload()

    @staticmethod
    def _load(filename):
        with open(filename, 'rb') as handle:
            return pickle.load(handle)

    @staticmethod
    def _save(data, filename):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(data, f, protocol=-1)
        except FileNotFoundError:
            makedirs(dirname(filename), exist_ok=True)
            with open(filename, 'wb') as f:
                pickle.dump(data, f, protocol=-1)

    def backup(self):
        """Creates a copy of the file in a new file named {filename}.bak.n"""
        filename = ''
        for i in count():
            filename = self.filename + '.bak' + ('.' + str(i)) * bool(i)
            if not isfile(filename):
                break
        self._save(self.data, filename)
        return filename

    def reload(self):
        """Reloads the data from disk"""
        if isfile(self.filename):
            try:
                self.data = self._load(self.filename)
            except ValueError as e:
                backup_name = self.backup()
                print('Warning: Failed to parse file ({}). Moved to {}.'.format(e, backup_name), file=sys.stderr)

    def save(self, data=None):
        """Only necessary to call if you manually change object references inside the data structure"""
        self._save(self.data if data is None else data, self.filename)

    def __str__(self):
        return 'Fiti({})'.format(self.data)

    def __repr__(self):
        return 'Fiti({!r}, {!r})'.format(self.data, self.filename)

    def __eq__(self, other):
        if isinstance(other, Fiti):
            return self.data == other.data
        return self.data == other


class FSet(Fiti, MutableSet):
    def __init__(self, *path):
        super().__init__(set(), *path)

    def __contains__(self, item):
        return item in self.data

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def add(self, x):
        self.data.add(x)
        self.save()

    def discard(self, x):
        self.data.discard(x)
        self.save()


class FList(Fiti, MutableSequence):
    def __init__(self, *path):
        super().__init__(list(), *path)

    def insert(self, index: int, obj):
        self.data.insert(index, obj)
        self.save()

    def __setitem__(self, i: int, o):
        self.data[i] = o
        self.save()

    def __delitem__(self, i: int) -> None:
        del self.data[i]
        self.save()

    def __getitem__(self, i: int):
        return self.data[i]

    def __len__(self) -> int:
        return len(self.data)


class FDict(Fiti, MutableMapping):
    def __init__(self, *path):
        super().__init__(dict(), *path)

    def __getitem__(self, k):
        return self.data[k]

    def __delitem__(self, key):
        del self.data[key]
        self.save()

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save()
