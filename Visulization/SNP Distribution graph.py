import mysql.connector
import pandas as pd
import plotly.graph_objects as go
import numpy as np

mydb = mysql.connector.connect(host="localhost",
                               port="3366",
                               user="root",
                               password="my-secret-pw",
                               database="SnPip")

mycursor = mydb.cursor()

df = pd.read_sql(('SELECT POS, GENE, ID FROM snp'), mydb)

pos = df['POS'][:]


def variant_density(pos, windowsize):
    # NOTE: Creates the windowsize
    bin = np.arange(0, pos.max(), windowsize)

    # NOTE: Uses the window midpoints as x coordinate
    x = (bin[1:] + bin[:-1])/2

    # NOTE: Compute variant density in each window
    h, _ = np.histogram(pos, bins=bin)
    y = h / windowsize

    # NOTE: plots & configures the graph
    fig = go.Figure(go.Line(x=x, y=y,
                            hovertemplate=
                            'Variant density (bp<sup>-1</sup>): %{y}' +
                            '<br>Chromosome position (bp)<extra></extra>: %{x}'))
    fig.update_traces(line_color='goldenrod')

    # NOTE: Centers the title and fonts
    fig.update_layout(title={'text': "Raw Varient Density",
                             'x':0.5,
                             'xanchor': 'center',
                             'yanchor': 'top'},
                      xaxis_title="Chromosome position (bp)",
                      yaxis_title="Variant density (bp<sup>-1</sup>)",
                      font_family="Times New Roman",
                      font_color="Black",
                      title_font_family="Times New Roman",
                      title_font_color="Black")

    # NOTE: Adds cross section cursor
    fig.update_xaxes(showspikes=True, spikecolor="Grey", spikesnap="cursor",
                     spikemode="across")
    fig.update_yaxes(showspikes=True, spikecolor="Black", spikethickness=2)
    fig.update_layout(spikedistance=1000, hoverdistance=100)

    fig.show()


variant_density(pos, 100000)
