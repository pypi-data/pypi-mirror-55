from gxdltk.config import Config
import torch.nn as nn

class Trainer(object):
    def __init__(self, model:nn.Module):
        self.model = model
        self.config = None # your config

    def set_config(self, cfg:Config):
        """
        setup your model config
        Args:
            cfg:

        Returns:

        """
        self.config = cfg

    def eval(self):
        """
        eval method, you need your implement your eval method
        Returns:

        """
        raise NotImplementedError

    def saver(self):
        """
        model saver method, you need to implement yourself
        Returns:

        """
        raise NotImplementedError

    def logger(self):
        """
        Model logger
        Returns:

        """
        raise NotImplementedError
