import configparser
import os
import re
from typing import Type


class ConfigManager:
    __slots__ = '_name', '_config', '_path', 'settings'

    def __init__(self, name: str, config_file: str = None, **kwargs):
        self.settings = ('config', 'crypto', 'crypto_currency', 'crypto_compare', 'fiat')

        if name not in self.settings:
            raise RuntimeError('Named configuration not in registry')

        self._name = name
        self._path = None
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

        if config_file is not None and isinstance(config_file, str):
            try:
                if os.path.isfile(config_file):
                    self._path = config_file
                    config.read(config_file)
            except IOError:
                raise
            except Exception:
                raise
        else:
            config_name = name.lower()
            path = os.path.join(os.path.dirname(__file__), config_name)
            path += '.ini'
            if os.path.isfile(path):
                self._path = path
                config.read(path)

        if kwargs:
            # update the configuration with dynamic settings
            # existing section will be overridden but defaults remains
            # restrict dynamic entries to only alphanumeric characters
            config.update({k: v for k, v in kwargs.items() if isinstance(k, str)
                           and isinstance(v, str)})
        self._config = config

    def option(self, section: str, option: str = None):
        if self._config.has_option(section, option):
            return self._config.get(section, option)
        elif section in self._config:
            return self._config[section]

    def configurations(self):
        return self._config.sections()

    def get_by_value(self, section: str, option: str, as_type: Type = None, split: str = ','):
        out = self.option(section, option)
        if not out:
            raise ValueError('Specified entry not in configuration. Got: %s' % out)

        int_pattern = re.compile(r'(\d+)')
        float_pattern = re.compile(r'(\d+)\.(\d+)')
        false_pattern = ('false', 'False', 'no', 'No', 'null', 'none', 'None')
        truth_pattern = ('true', 'Truth', 1)
        try:
            if as_type:
                if issubclass(as_type, int):
                    return int(out) if int_pattern.match(out) else NotImplemented
                elif issubclass(as_type, float):
                    return float(out) if float_pattern.match(out) else NotImplemented
                elif issubclass(as_type, bool):
                    if out in false_pattern:
                        return False
                    elif out in truth_pattern:
                        return True
                    bool(out)
            if split and split in out:
                return out.split(split)
            if out == 'none' or out == 'None' or out == 'NONE':
                return None
            else:
                return out
        except Exception:
            raise

    @property
    def sections(self):
        return self._config.sections()

    @property
    def configuration(self):
        return self._name

    @property
    def path(self):
        return self._path


crypto_compare_config = ConfigManager(name='crypto_compare')
crypto_config = ConfigManager(name='crypto')
fiat_config = ConfigManager(name='fiat')
default_config = ConfigManager(name='config')
