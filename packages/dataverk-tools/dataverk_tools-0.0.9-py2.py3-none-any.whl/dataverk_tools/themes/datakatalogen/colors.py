from .._colormaps import _linear3color

fontColor = "#000000"
axisColor = '#EBF0F8'
gridColor = '#DFE8F3'
background = "#FFFFFF"


discrete = ["#3385D1", "#FFA733", "#C86151", "#337C9B", "#FFD81A", "#38A161", "#77A186", "#A3AA6F", "#826BA1"]

markColor = discrete[0]

sequential = _linear3color("#3385D1", "#66A4Dc", "#CCE1F3")
diverging = _linear3color("#C86151", "#FFA733", "#FFD81A")

sequentialminus = _linear3color("#C86151", "#FFA733", "#FFD81A")

colorscale = [[i/10,color] for i, color in enumerate(sequential)]
colorscale_diverging = [[i/10,color] for i, color in enumerate(sequential)]
colorscale_sequential = [[i/10,color] for i, color in enumerate(sequential)]
colorscale_sequentialminus = [[i/10,color] for i, color in enumerate(sequential)]