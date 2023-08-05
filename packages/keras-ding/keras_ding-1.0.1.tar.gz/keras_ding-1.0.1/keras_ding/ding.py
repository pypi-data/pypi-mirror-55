from tensorflow import keras
import os
from typing import List
from environments_utils import is_notebook
from .utils import InvisibleAudio
import simpleaudio

__all__ = ["Ding"]


class Ding(keras.callbacks.Callback):
    def __init__(self, path: str = None):
        r"""Create a new Ding callback.

        Ding simply plays the sound at given path when the training is complete.

        Parameters
        ------------------------------------------
        path:str, the path to the file to play. If None, as by default, a simple *ding* sound will be played.

        Raises
        ----------------------
        ValueError
            If the given path does not correspond to a playable object.

        Returns
        ----------------------
        Return a new Ding object.
        """
        super(Ding, self).__init__()
        if path is None:
            path = "{cwd}/ding.wav".format(
                cwd=os.path.dirname(os.path.realpath(__file__))
            )
        if not os.path.exists(path):
            raise ValueError("Given path does not exists.")

        if not any([path.endswith(ext) for ext in ["mp3", "wav"]]):
            raise ValueError("Given path is not an mp3 or wav file.")

        self._path = path

    def on_train_end(self, *args: List):
        if is_notebook():
            InvisibleAudio(path=self._path).play()
        else:
            simpleaudio.WaveObject.from_wave_file(self._path).play()
