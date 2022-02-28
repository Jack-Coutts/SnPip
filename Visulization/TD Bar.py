import plotly.express as px
import pandas as pd
from input import input


# NOTE: Plots a Barchart for Tajima's D
def TD_Bar(input):
    for v in input.values():
        nstep = len(v)

    steplabels = list(range(1, nstep + 1, 1))

    # NOTE: Creates a nested dictionary for the input
    nest = {}
    for k, v in input.items():
        nest[k] = dict(zip(steplabels, v))

    # NOTE: Creates a df for the graph
    df = pd.DataFrame.from_dict(nest, orient='index').stack().reset_index()
    df.columns = ['Pop', 'Step', 'TD']

    # NOTE: Plots the graph
    fig = px.bar(df, x='Step', y='TD', color='Pop', barmode='overlay',
                 color_discrete_sequence=px.colors.qualitative.G10)

    # NOTE: Sets the fonts and layout
    fig.update_layout(font_family="Times New Roman",
                      font_color="Black",
                      title_font_family="Times New Roman",
                      title_font_color="Black")

    # NOTE: Creates a range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=200000,
                         label="200000bp",
                         step="all",
                         stepmode="backward"),
                    dict(count=400000,
                         label="400000bp",
                         step="all",
                         stepmode="backward"),
                    dict(count=600000,
                         label="600000bp",
                         step="all",
                         stepmode="backward"),
                    dict(count=800000,
                         label="800000bp",
                         step="all",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="linear"
        )
    )

    fig.show()


TD_Bar(input)
