import plotly.express as px
import pandas as pd
from input import input

pd.set_option("display.max_rows", None, "display.max_columns", None)

start = 41577800
stop = 41589900


# NOTE: Converts 200000 to 2M for better legend formating
def strink(num):
    if len(str(num)) <= 5:
        snum = str("{:.6f}".format(num/1000)+'k')
        return snum
    elif len(str(num)) >= 6:
        snum = str("{:.6f}".format(num/1000000)+'M')
        return snum
    else:
        pass


# NOTE: Plots a Barchart for Tajima's D
def TD_Bar(input, start, stop):
    # NOTE: Creates a list of nested keys from input dict
    ik = []
    for v in input.values():
        for key in v.keys():
            ik.append(key)

    # NOTE: records the number of steps in the input data
    vlen = []
    for v in input.values():
        vlen.append(len(v.values()))
    print(vlen)

    # NOTE: Calculates the step size of the input data
    step = int((stop - start)/vlen[0])
    print(step)

    # NOTE: Creates the range caterogies
    bounds = [
             (strink(n+1)+''+'-'+''+strink(min(n+step, stop)))
             for n in range(start, stop, step)
             ]
    print(bounds)

    # NOTE: Maps each nested key from the input dict to a boundary
    first = ik[0:vlen[0]]
    keydict = dict(zip(first, bounds))
    print(len(keydict))

    # NOTE: Creates df for graph
    df = pd.DataFrame.from_dict(input, orient='index').stack().reset_index()
    df = df.fillna('')
    df.columns = ['Pop', 'Step', 'TD']
    df['Step'].replace(keydict, inplace=True)
    print(df)

    # NOTE: Plots the graph
    fig = px.bar(df, y='TD', x='Step', color='Pop', barmode='overlay',
                 labels={"Step": "Region on Chromosome (bp) ",
                         "Pop": "Population Group",
                         "TD": "Tajima's D"},
                 title="Tajima's Diversity",
                 color_discrete_sequence=px.colors.qualitative.G10)

    # NOTE: Sets the fonts and layout
    fig.update_layout(font_family="Times New Roman",
                      font_color="Black",
                      title_font_family="Times New Roman",
                      title_font_color="Black")



    fig.show()


TD_Bar(input, 41577800, 41589900)
