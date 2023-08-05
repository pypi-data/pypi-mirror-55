from gxdltk.header import *

__all__ = ["acc", "arr_sum"]

def acc(pred: list, label: list) -> float:
    """
    calc accuracy
    :param pred:
    :param label:
    :return:
    """
    assert len(pred) == len(label), "length of arg#1 must be equal to arg#2, " \
                                    f"length of pred is {len(pred)}, length " \
                                    f"of label is {len(label)}"
    p = np.array(pred)
    l = np.array(label)
    return np.sum(p == l) / len(label)


def arr_sum(arr: list) -> float:
    _arr = np.array(arr, dtype=np.float)
    return _arr.sum()
