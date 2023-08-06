from typing import List, Dict, Type, Callable, ClassVar, TypeVar
import random
import string
import logging
import logging.config
import asyncio

from macrobase.cli import Cli, ArgumentParsingException
from macrobase.pool import DriversPool
from macrobase.hook import HookNames
# from macrobase.context import context

# from macrobase.logging import get_logging_config
from macrobase_driver import MacrobaseDriver
from macrobase_driver.config import CommonConfig, AppConfig, DriverConfig

from structlog import get_logger

log = get_logger('macrobase')


class Application:

    def __init__(self, config: AppConfig, name: str = None):
        """Create Application object.

        :param loop: asyncio compatible event loop
        :param name: string for naming drivers
        :return: Nothing
        """
        self.name = name
        self._config = config
        self._pool = None
        self._hooks: Dict[HookNames, List[Callable]] = {}
        self._drivers: Dict[str, MacrobaseDriver] = {}

    @property
    def config(self) -> AppConfig:
        return self._config

    def get_driver(self, driver_cls: Type[MacrobaseDriver], driver_config: Type[DriverConfig], *args, **kwargs) -> MacrobaseDriver:
        # TODO: fix type hints
        common_config = CommonConfig(self.config, driver_config)
        driver = driver_cls(config=common_config, *args, **kwargs)

        return driver

    def add_driver(self, driver: MacrobaseDriver, alias: str = None):
        if alias is None:
            alias = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
        self._drivers[alias] = driver

    def add_drivers(self, drivers: List[MacrobaseDriver]):
        [self.add_driver(d) for d in drivers]

    def add_hook(self, name: HookNames, handler):
        if name not in self._hooks:
            self._hooks[name] = []

        self._hooks[name].append(handler)

    def _call_hooks(self, name: HookNames):
        if name not in self._hooks:
            return

        for handler in self._hooks[name]:
            handler(self)

    # TODO: fix logging
    # def _apply_logging(self):
    #     self._logging_config = get_logging_config(self.config.app)
    #     logging.config.dictConfig(self._logging_config)

    def _prepare(self):
        # self._apply_logging()
        pass

    def run(self, argv: List[str] = None):
        if argv is None:
            argv = ['start', 'all']

        self._prepare()

        self._call_hooks(HookNames.before_start)

        try:
            Cli(list(self._drivers.keys()), self._action_start, self._action_list).parse(argv)
        except ArgumentParsingException as e:
            print(e.message)

        self._call_hooks(HookNames.after_stop)

    def _action_start(self, aliases: List[str]):
        if len(aliases) == 1:
            try:
                self._drivers.get(aliases[0]).run()
            finally:
                asyncio.get_event_loop().close()
        else:
            self._pool = DriversPool()
            self._pool.start([d for a, d in self._drivers.items() if a in aliases])

    def _action_list(self, aliases: List[str]):
        print(f"Available drivers to start: \n{[n for n in aliases]}")
