from .colors import *
import plotly.graph_objects as go
import plotly.io as pio

plotly_template = pio.templates["plotly_white"]

plotly_template.layout.colorscale = go.layout.Colorscale(
    diverging=diverging,
    sequential=sequential,
    sequentialminus=sequentialminus
)

plotly_template.layout.font = go.layout.Font(
    color = fontColor,
    family = "'Open Sans', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'"
)

plotly_template.layout.colorway = ("#C86151", "#FFA733", "#FFD81A", "#38A161", "#77A186", "#A3AA6F","#3385D1", "#337C9B", "#826BA1")




