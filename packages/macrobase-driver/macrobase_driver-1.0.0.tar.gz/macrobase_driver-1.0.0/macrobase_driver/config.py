import os
from typing import get_type_hints, Type, List, Dict, Callable, Any, Generic, TypeVar

from enum import Enum

from .exceptions import ConfigFileNotFoundException, ConfigFileNotSupportFormatException, ConfigFileParseException


class LogFormat(Enum):
    json = 'json'
    plain = 'plain'

    @property
    def raw(self) -> str:
        return str(self.value).lower()


class LogLevel(Enum):
    critical = 'CRITICAL'
    error = 'ERROR'
    warning = 'WARNING'
    info = 'INFO'
    debug = 'DEBUG'
    notset = 'NOTSET'

    @property
    def raw(self) -> str:
        return str(self.value).lower()


class BaseConfig(object):

    _file_parsers: Dict[str, Callable[[str], dict]] = {}
    _type_parsers: Dict[Type, Callable[[str], Any]] = {}

    def __init__(self, file: str = None, *arg, **kwargs):
        if file is not None:
            if not os.path.isfile(file):
                raise ConfigFileNotFoundException

            self._import_file(file)

    def _import_file(self, path: str):
        ext = path.split('.')[-1].lower()

        if ext not in self._file_parsers:
            raise ConfigFileNotSupportFormatException

        with open(path, 'rb') as file:
            values = self._file_parsers[ext](file)

        self._import_dict(values)

    def _import_dict(self, values: dict):
        type_hints = get_type_hints(type(self))

        for p in dir(self):
            if p not in values or not self._should_wrap(p):
                continue

            attr = getattr(self, p)

            if issubclass(attr.__class__, BaseConfig):
                attr._import_dict(values.get(p))
            else:
                if isinstance(attr, list):
                    if not isinstance(values.get(p), list):
                        raise ConfigFileParseException(f'Key `{p}` have not match type `list`')

                    child_types = type_hints.get(p)

                    if not hasattr(child_types, '__args__') or child_types.__args__ is None or len(child_types.__args__) == 0:
                        setattr(self, p, values.get(p))
                        continue

                    value_type = child_types.__args__[0]
                    ls = []

                    for el in values.get(p):
                        ls.append(self._parse_value(value_type, el))

                    setattr(self, p, ls)
                elif isinstance(attr, dict):
                    if not isinstance(values.get(p), dict):
                        raise ConfigFileParseException(f'Key `{p}` have not match type `dict`')

                    child_types = type_hints.get(p)

                    if not hasattr(child_types, '__args__') or child_types.__args__ is None or len(child_types.__args__) == 0:
                        setattr(self, p, values.get(p))
                        continue

                    key_type = child_types.__args__[0]
                    value_type = child_types.__args__[0]
                    ls = {}

                    for k, v in values.get(p).items():
                        key = self._parse_value(key_type, k)
                        value = self._parse_value(value_type, v)
                        ls[key] = value

                    setattr(self, p, ls)
                else:
                    setattr(
                        self,
                        p,
                        self._parse_value(type_hints.get(p), values.get(p))
                    )

    def _should_wrap(self, name: str) -> bool:
        return not name.startswith('_') and not callable(getattr(self, name))

    def _parse_value(self, tp: Type, value: str) -> Any:
        if type(value) == tp or tp not in self._type_parsers:
            return value

        return self._type_parsers.get(tp)(value)

    def set(self, key: str, value: Any):
        setattr(self, key, value)

    @staticmethod
    def file_parser(extensions: List[str]):
        def decorator(parser):
            for ext in extensions:
                BaseConfig._file_parsers[ext] = parser

            return parser

        return decorator

    @staticmethod
    def type_parser(tp: Type):
        def decorator(parser):
            BaseConfig._type_parsers[tp] = parser
            return parser

        return decorator


class AppConfig(BaseConfig):

    logo: str = """
                                    _                    
                                   | |                   
     _ __ ___   __ _  ___ _ __ ___ | |__   __ _ ___  ___ 
    | '_ ` _ \ / _` |/ __| '__/ _ \| '_ \ / _` / __|/ _ \\
    | | | | | | (_| | (__| | | (_) | |_) | (_| \__ \  __/
    |_| |_| |_|\__,_|\___|_|  \___/|_.__/ \__,_|___/\___|
"""

    version: str = '0.0'
    name: str = 'macrobase'
    # TODO: fix it
    workers: int = 1

    debug: bool = False
    log_format: LogFormat = LogFormat.json
    log_level: LogLevel = LogLevel.info


class DriverConfig(BaseConfig):

    logo: str = """
 _____       _
|  __ \     (_)               
| |  | |_ __ ___   _____ _ __ 
| |  | | '__| \ \ / / _ \ '__|
| |__| | |  | |\ V /  __/ |   
|_____/|_|  |_| \_/ \___|_|
"""


AT = TypeVar('AT')
DT = TypeVar('DT')


class CommonConfig(Generic[AT, DT]):

    def __init__(self, app_config: AT, driver_config: DT):
        self._app = app_config
        self._driver = driver_config

    @property
    def app(self) -> AT:
        return self._app

    @property
    def driver(self) -> DT:
        return self._driver


@BaseConfig.file_parser(['yaml', 'yml'])
def yaml_parser(content: str) -> dict:
    from yaml import load, YAMLError
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader

    try:
        return load(content, Loader=Loader)
    except YAMLError as e:
        raise ConfigFileParseException


@BaseConfig.file_parser(['json'])
def json_parser(content: str) -> dict:
    from rapidjson import loads

    try:
        return loads(content)
    except Exception as e:
        raise ConfigFileParseException


@BaseConfig.type_parser(str)
def parse_str(value) -> str:
    return str(value)


@BaseConfig.type_parser(bool)
def parse_bool(value) -> bool:
    return str(value).lower() in ('true', 'y', 'yes', '1', 'on')


@BaseConfig.type_parser(int)
def parse_int(value) -> int:
    return int(value)


@BaseConfig.type_parser(float)
def parse_float(value) -> float:
    return float(str(value))


@BaseConfig.type_parser(LogLevel)
def parse_log_level(value: str) -> LogLevel:
    return LogLevel(value.upper())


@BaseConfig.type_parser(LogFormat)
def parse_log_format(value: str) -> LogFormat:
    return LogFormat(value.lower())
