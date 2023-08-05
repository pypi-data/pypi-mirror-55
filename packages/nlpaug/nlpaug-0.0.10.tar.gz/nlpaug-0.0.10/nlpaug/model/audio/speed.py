# Reference: https://www.kaggle.com/CVxTz/audio-data-augmentation

try:
    import librosa
except ImportError:
    # No installation required if not using this function
    pass
import numpy as np

from nlpaug.model.audio import Audio


class Speed(Audio):
    """
    Adjusting speed

    :param speed_range: Factor for time stretch. Audio will be slowing down if value is between 0 and 1.
        Audio will be speed up if value is larger than 1.
    """
    def __init__(self, speed_range):
        super(Speed, self).__init__()
        # TODO: Validation
        # if speed_factor < 0:
        #     raise ValueError(
        #         'speed_factor should be positive number while {} is passed.'.format(speed_factor))
        self.speed_range = speed_range

        try:
            librosa
        except NameError:
            raise ImportError('Missed librosa library. Install it via `pip install librosa`')

    def manipulate(self, data):
        speeds = [round(i, 1) for i in np.arange(self.speed_range[0], self.speed_range[1], 0.1)]
        speed = speeds[np.random.randint(len(speeds))]

        return librosa.effects.time_stretch(data, speed)
