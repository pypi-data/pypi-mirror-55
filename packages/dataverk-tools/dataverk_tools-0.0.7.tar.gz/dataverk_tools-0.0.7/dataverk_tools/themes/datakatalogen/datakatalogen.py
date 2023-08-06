from .._colormaps import _linear3color
from .colors import *
import plotly.graph_objects as go
import plotly.io as pio

import plotly.graph_objects as go


sequential = _linear3color("#3385D1", "#66A4Dc", "#CCE1F3")
diverging = _linear3color("#C86151", "#FFA733", "#FFD81A")

sequentialminus = _linear3color("#C86151", "#FFA733", "#FFD81A")

colorscale = [[i/10,color] for i, color in enumerate(sequential)]
colorscale_diverging = [[i/10,color] for i, color in enumerate(sequential)]
colorscale_sequential = [[i/10,color] for i, color in enumerate(sequential)]
colorscale_sequentialminus = [[i/10,color] for i, color in enumerate(sequential)]


discrete = ["#C86151", "#FFA733", "#FFD81A", "#38A161", "#77A186", "#A3AA6F","#3385D1", "#337C9B", "#826BA1"]


plotly_template = pio.templates["plotly_white"]


plotly_template.layout.colorscale = go.layout.Colorscale(
    diverging=diverging,
    sequential=sequential,
    sequentialminus=sequentialminus
)

plotly_template.layout.font = go.layout.Font(
    color = 'black',
    family = "'Open Sans', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'"
)

plotly_template.layout.colorway = ("#C86151", "#FFA733", "#FFD81A", "#38A161", "#77A186", "#A3AA6F","#3385D1", "#337C9B", "#826BA1")




