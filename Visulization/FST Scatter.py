import plotly.express as px
import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)

input = {
         ('bebG', 'cheG'): {1: 0.033965142017862875, 2: 0.020338952458864853, 3: 0.02829640374557564, 5: 0.011969472066051177},
         ('bebG', 'esnG'): {1: 0.033950165902009506, 2: 0.22964449202370138, 3: 0.1439432092931027, 5: 0.104780270647522},
         ('bebG', 'gbrG'): {1: 0.04513583112102886, 2: 0.019293514982147947, 3: 0.043925149596432, 5: 0.06649401774038718},
         ('bebG', 'pelG'): {1: 0.022848016101287363, 2: 0.05748160747314586, 3: 0.1200093297802129, 5: 0.1675742115967348},
         ('cheG', 'esnG'): {1: 0.06016570098124014, 2: 0.2416076185889834, 3: 0.14795362128785383, 5: 0.0929974027699578},
         ('cheG', 'gbrG'): {1: 0.14513217793633923, 2: 0.07257541173870458, 3: 0.052244525622411726, 5: 0.029221633500032658},
         ('cheG', 'pelG'): {1: 0.010662917429055646, 2: 0.08879712970015427, 3: 0.13107618191745593, 5: 0.12901670484988106},
         ('esnG', 'gbrG'): {1: 0.0773255971059701, 2: 0.1920806796852942, 3: 0.09010871811293061, 5: 0.050164036520277365},
         ('esnG', 'pelG'): {1: 0.030874994446445793, 2: 0.18016576094794665, 3: 0.22694910747247382, 5: 0.31932352488357674},
         ('gbrG', 'pelG'): {1: 0.10799152555853336, 2: 0.04385200742540727, 3: 0.12841662227928322, 5: 0.2364799447642988}
         }

start = 1000
stop = 2000
step = 250
nstep = int((stop - start)/step)


# NOTE: Converts 200000 to 2M for better legend formating
def strink(num):
    if len(str(num)) <= 5:
        snum = str("{:.2f}".format(num/1000)+'k')
        return snum
    elif len(str(num)) >= 6:
        snum = str("{:.2f}".format(num/1000000)+'M')
        return snum
    else:
        pass


# NOTE: Replaces the step keys in the input dict with their boundaries
def replace_keys(old_dict, key_dict):
    new_dict = {}
    for key in old_dict.keys():
        new_key = key_dict.get(key, key)
        if isinstance(old_dict[key], dict):
            new_dict[new_key] = replace_keys(old_dict[key], key_dict)
        else:
            new_dict[new_key] = old_dict[key]
    return new_dict


# NOTE: Generates a scatter graph if given a dictionary of values
def FSTscatter(input, start, stop, step):
    # NOTE: Creates the range caterogies
    bounds = [
             (strink(n)+'-'+strink(min(n+step, stop)))
             for n in range(start, stop, step)
             ]
    # NOTE: Creates a list of nested keys from input dict
    ik = []
    for v in input.values():
        for key in v.keys():
            ik.append(key)

    # NOTE: Maps each nested key from the input dict to a boundary
    first = ik[0:nstep]
    keydict = dict(zip(first, bounds))

    # NOTE: Makes a nested dictionary
    nest = replace_keys(input, keydict)

    # NOTE: Creates df for graph
    df = pd.DataFrame.from_dict(nest, orient='index').stack().reset_index()
    df['Pop'] = df[['level_0', 'level_1']].agg('-'.join, axis=1)
    del df['level_0']
    del df['level_1']
    df.columns = ['Range', 'FST', 'Pop']

    # NOTE: plots the scatter graph
    fig = px.scatter(df, x="Pop", y="FST", color="Range",
                     color_discrete_sequence=px.colors.qualitative.Dark24,
                     labels={"Range": "FST Region on Chromosome (bp) ",
                             "Pop": "Population Group",
                             "FST": "FST Value"},
                     title="Hudson FST",
                     animation_frame="Range",
                     animation_group="Pop")
    fig.update_traces(marker=dict(size=12))

    # NOTE: Sets the fonts and layout
    fig.update_layout(font_family="Times New Roman",
                      font_color="Black",
                      title_font_family="Times New Roman",
                      title_font_color="Black",
                      legend={'traceorder': 'reversed'},
                      showlegend=False,
                      yaxis_range=[-0.1, 0.5])
    fig.add_hline(y=0.12, line_width=2, line_dash="dash", line_color="gray")

    fig.show()


FSTscatter(input, start, stop, step)
