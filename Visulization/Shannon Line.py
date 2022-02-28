import pandas as pd
import os
import plotly.express as px

os.chdir(r"C:\Users\yido6\Documents\Uni\Level 7\SnPip\Visulization")

# NOTE: The shannon line graph function takes a df as the input
# NOTE: the DF need the position of the snp as the first col
df = pd.read_csv('Shannon.tsv', sep='\t')


def ShannonGraph(df):

    df.columns = ['POS', 'SNP', 'Shannon']

    # NOTE: Plots the graph
    fig = px.line(df, y='Shannon', x='POS',
                  hover_data=["POS", "Shannon", "SNP"],
                  labels={"POS": "Chromosome Position (bp)",
                          "Shannon": "Shannon Diversity",
                          "SNP": "SNP"})
    fig.update_traces(line_color='goldenrod')

    # NOTE: Centers the title and fonts
    fig.update_layout(title={'text': "Shannon Diversity",
                             'x':0.5,
                             'xanchor': 'center',
                             'yanchor': 'top'},
                      xaxis_title="Chromosome position (bp)",
                      yaxis_title="Shannon Diversity",
                      font_family="Times New Roman",
                      font_color="Black",
                      title_font_family="Times New Roman",
                      title_font_color="Black")

    # NOTE: Adds cross section cursor
    fig.update_xaxes(showspikes=True, spikecolor="Grey", spikesnap="cursor",
                     spikemode="across")
    fig.update_yaxes(showspikes=True, spikecolor="Black", spikethickness=2)
    fig.update_layout(spikedistance=1000, hoverdistance=100)

    # NOTE: Adds sliding window
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


ShannonGraph(df)
