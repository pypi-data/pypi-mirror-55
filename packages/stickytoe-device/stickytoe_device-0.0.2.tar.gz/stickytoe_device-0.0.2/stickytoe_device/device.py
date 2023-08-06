from abc import ABCMeta, abstractmethod
import pathlib
import subprocess
import importlib

# local imports
from . import constants


def get_device(pip: pathlib.Path, config: dict):
    try:
        mod = importlib.import_module(config["package"])
    except ModuleNotFoundError:
        subprocess.run(["bash", constants.BINPATH.joinpath(
            "pip"), str(pip), config["package"], config["version"]], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        
        try:
            mod = importlib.import_module(config["package"])
        except ModuleNotFoundError:
            raise ValueError("cannot import {}=={}".format(config["package"], config["version"]))

    return mod.get_device(config["config"])

class _Device(metaclass=ABCMeta):
    """the private base class that requires certain function signatures for general usage.

        DO NOT INHERIT DIRECTLY FROM _DEVICE.
    """
    @abstractmethod
    def __init__(self, config: dict):
        pass

    @abstractmethod
    def execute(self, payload: str):
        pass


class I2C(_Device):
    """an abstract class that extends the functionality of the private, skeleton class Device.

        raises a ValueError if two or more devices allocate the same address.

        Implement an execute(self, payload:str) function to finish this abstract class.
    """

    I2C_REGISTER = []

    def __init__(self, config: dict):
        if all(k in config for k in constants.I2C_KEYS):
            addr = config[constants.ADDRESS_KEY]

            if addr in I2C.I2C_REGISTER:
                raise ValueError(
                    "Addr: {} already has been allocated".format(addr))

            I2C.I2C_REGISTER.append(addr)
            self.bus = config[constants.BUS_KEY]
            self.addr = addr
        else:
            raise ValueError("Missing key in {}".format(config))
