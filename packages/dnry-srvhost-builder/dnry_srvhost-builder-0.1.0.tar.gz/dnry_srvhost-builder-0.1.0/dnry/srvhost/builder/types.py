from abc import ABC, abstractmethod
from typing import Callable, NewType
from pyioc3 import StaticContainerBuilder, StaticContainer

from dnry.config import IConfigFactory, IConfigSection


class IHostingEnvironment(ABC):
    @property
    @abstractmethod
    def application_name(self) -> str:
        raise NotImplemented()

    @application_name.setter
    @abstractmethod
    def application_name(self, val: str):
        raise NotImplemented()

    @property
    @abstractmethod
    def environment_name(self) -> str:
        raise NotImplemented()

    @environment_name.setter
    @abstractmethod
    def environment_name(self, val: str):
        raise NotImplemented()


class ISrvHostContext(ABC):
    @property
    @abstractmethod
    def configuration(self) -> IConfigSection:
        raise NotImplemented()

    @configuration.setter
    @abstractmethod
    def configuration(self, val: IConfigSection) -> IConfigSection:
        raise NotImplemented()

    @property
    @abstractmethod
    def environment(self) -> IHostingEnvironment:
        raise NotImplemented()

    @environment.setter
    @abstractmethod
    def environment(self, val: IHostingEnvironment):
        raise NotImplemented()


class ISrvHost(ABC):
    @property
    @abstractmethod
    def service_provider(self) -> StaticContainer:
        raise NotImplemented()

    @service_provider.setter
    @abstractmethod
    def service_provider(self, val: StaticContainer):
        raise NotImplemented()

    @property
    @abstractmethod
    def configuration(self) -> IConfigSection:
        raise NotImplemented()

    @configuration.setter
    @abstractmethod
    def configuration(self, val: IConfigSection):
        raise NotImplemented()

    @property
    @abstractmethod
    def environment(self) -> IHostingEnvironment:
        raise NotImplemented()

    @environment.setter
    @abstractmethod
    def environment(self, val: IHostingEnvironment):
        raise NotImplemented()

    @abstractmethod
    def run(self):
        raise NotImplemented()


class ISrvHostBuilder(ABC):
    @abstractmethod
    def build(self) -> ISrvHost:
        raise NotImplemented()

    @abstractmethod
    def config_configuration(self, config: "ConfigConfigurationDelegate") -> "ISrvHostBuilder":
        raise NotImplemented()

    @abstractmethod
    def config_services(self, config: "ConfigServicesDelegate") -> "ISrvHostBuilder":
        raise NotImplemented()

    @abstractmethod
    def add_setting(self, key: str, value: str) -> "ISrvHostBuilder":
        raise NotImplemented()

    @abstractmethod
    def get_setting(self, key: str) -> str:
        raise NotImplemented()


ConfigServicesDelegate = NewType("ConfigServicesDelegate", Callable[[ISrvHostContext], StaticContainerBuilder])
ConfigConfigurationDelegate = NewType("ConfigConfigurationDelegate", Callable[[ISrvHostContext], IConfigFactory])
