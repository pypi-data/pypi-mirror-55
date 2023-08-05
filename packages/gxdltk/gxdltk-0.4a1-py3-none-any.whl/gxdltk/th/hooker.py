"""
General Hooker for forward and backward
"""
from gxdltk.th.header import *
import torch.nn as nn
__all__ = ["observer", "Hooker"]


def observer(module:nn.Module, it, output):
    """
    Forward hook for watch all var size
    using Name tensor in torch1.3
    :param module: torch.nn.Module
    :param it: any type
    :param output: any type, model output
    """
    print(f"---Module {type(module)}--- \n {module}")
    if isinstance(it, th.Tensor):
        print(f"Input shape {it.shape}")
    elif isinstance(it, tuple):
        for i in range(len(it)):
            print(f"Input Tensor {i} shape {it[i].shape}")

    if isinstance(output, th.Tensor):
        print(f"Output shape {output.shape}")
    elif isinstance(output, tuple):
        for i in range(len(output)):
            print(f"Output Tensor {i} shape {output[i].shape}")

class Hooker(object):
    """
    Hooker class
    """
    def __init__(self, model:nn.Module):
        self.model = model
        self.handler = list()

    def register(self, full:bool=True):
        """

        Args:
            full: register to all sub_module if true(default)

        Returns:

        """
        modules = self.model.named_children()
        for name, module in modules:
            h = module.register_forward_hook(observer)
            self.handler.append(h)

    def remove(self):
        """
        Remove hooker
        """
        for h in self.handler:
            h.remove()
