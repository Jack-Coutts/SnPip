import plotly.express as px
import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)

input = {('bebG-cheG'): [0.03543337, 0.0315438, 0.00944336, 0.04456595,
                         0.02946088, 0.02491669],
         ('bebG-esnG'): [0.02142849, 0.05582269, 0.11426458, 0.32566496,
                         0.13148831, 0.15959616],
         ('bebG-gbrG'): [0.06790303, 0.00856417, 0.02699473, 0.00512476,
                         0.00028977, 0.16291702],
         ('bebG-pelG'): [0.01733013, 0.03025453, 0.02291235, 0.10282672,
                         0.12648646, 0.07740511],
         ('cheG-esnG'): [0.05810838, 0.06303388, 0.19060241, 0.29045066,
                         0.15537565, 0.07898431],
         ('cheG-gbrG'): [0.19165262, 0.07118688, 0.07546849, 0.06820209,
                         0.04661426, 0.07510459],
         ('cheG-pelG'): [0.00366681, 0.01947445, 0.07142241, 0.11278983,
                         0.15059607, 0.01258583],
         ('esnG-gbrG'): [0.09610099, 0.0440949, 0.03436135, 0.28341565,
                         0.09397178, 0.01500246],
         ('esnG-pelG'): [0.02068164, 0.04520733, 0.04398022, 0.25958801,
                         0.24068202, 0.0321381],
         ('gbrG-pelG'): [0.14944938, 0.04998906, 0.0107279, 0.07794422,
                         0.13721246, 0.02307796]}

start = 200000
stop = 200600
step = 100


# NOTE: Converts 200000 to 2M for better legend formating
def strink(num):
    if len(str(num)) <= 5:
        snum = str(num/1000)+'k'
        return snum
    elif len(str(num)) >= 6:
        snum = str(num/1000000)+'M'
        return snum
    else:
        pass


# NOTE: Generates a scatter graph if given a dictionary of values
def FSTscatter(input, start, stop, step):
    # NOTE: Creates the range caterogies
    bounds = [
             (strink(n)+'-'+strink(min(n+step, stop)))
             for n in range(start, stop, step)
             ]
    # NOTE: Makes a nested dictionary
    nest = {}
    for k, v in input.items():
        # NOTE: Assigns the bounds to each value in the input dictionary
        nest[k] = dict(zip(bounds, v))

    # NOTE: Creates df for graph
    df = pd.DataFrame.from_dict(nest, orient='index').stack().reset_index()
    df.columns = ['Pop', 'Range', 'FST']

    # NOTE: plots the scatter graph
    fig = px.scatter(df, x="Pop", y="FST", color="Range",
                     color_discrete_sequence=px.colors.qualitative.Antique_r,
                     labels={"Range": "FST Region on Chromosome (bp)",
                             "Pop": "Population Group",
                             "FST": "FST Value"},
                     title="Hudson FST")
    fig.update_traces(marker=dict(size=12))

    # NOTE: Sets the fonts
    fig.update_layout(font_family="Times New Roman",
                      font_color="Black",
                      title_font_family="Times New Roman",
                      title_font_color="Black",
                      legend={'traceorder': 'reversed'})

    fig.add_hline(y=0.12, line_width=3, line_dash="dash", line_color="gray")

    fig.show()


FSTscatter(input, start, stop, step)
