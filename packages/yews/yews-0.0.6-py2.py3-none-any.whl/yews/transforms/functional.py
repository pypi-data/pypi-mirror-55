import numpy as np
import torch

def _is_numpy_waveform(wav):
    return isinstance(wav, np.ndarray)

def _to_tensor(wav):
    """Convert a ``numpy.ndarray`` to tensor.
    See ``ToTensor`` for more details.
    Args:
        wav (numpy.ndarray): Waveform to be converted to tensor.
    Returns:
        Tensor: Converted array.
    """

    if not(_is_numpy_waveform(wav)):
        raise TypeError(f"wav should be ndarray. Got {type(wav)}")

    if wav.ndim == 1:
        wav = wav[None, :]

    return torch.from_numpy(wav).float()
