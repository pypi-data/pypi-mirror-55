from .._swatches import _swatches
from .._colormaps import _linear3color
from . import datakatalogen as _datakatalogen

def swatches():
    return _swatches(__name__, globals())

swatches.__doc__ = _swatches.__doc__

dcatRodGul = _linear3color("#C86151", "#FFA733", "#FFD81A")
dcacGrønn = _linear3color("#38A161", "#77A186", "#A3AA6F")
dcatBlåFiolet = _linear3color("#3385D1", "#337C9B", "#826BA1")
dcatRodGronn = _linear3color("#C86151", "#38A161", "#A3AA6F")
dcatysBlaMorkBla = _linear3color("#3385D1", "#66A4DC", "#CCE1F3")






   
