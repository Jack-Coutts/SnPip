import plotly.express as px
import pandas as pd
import math

pd.set_option("display.max_rows", None, "display.max_columns", None)

nan = ''

input = {
('bebG', 'cheG'): {34391: 0.004792769890834558, 34392: 0.008720055331335992, 34393: 0.08894859385461486, 34394: 0.006271770061016251, 34395: 0.00588603200502687, 34396: 0.1857435642095363, 34397: 0.1758335008015241, 34398: 0.1712545419428566, 34399: 0.015575137304248204, 34400: 0.0, 34401: nan},
('bebG', 'esnG'): {34391: 0.13735341931132794, 34392: 0.09760595356848271, 34393: 0.06040574492419674, 34394: 0.16131435247034537, 34395: 0.046720955059722166, 34396: 0.24656285748513682, 34397: 0.24189833808858197, 34398: 0.17271875312621543, 34399: 0.31839603457667726, 34400: 0.059563145880648705, 34401: 0.0},
('bebG', 'gbrG'): {34391: 0.0034215846272509912, 34392: 0.0097276126769356, 34393: 0.04083460141063343, 34394: 0.003978888183962327, 34395: 0.009569087897197948, 34396: 0.041621195871237394, 34397: 0.046953022507817736, 34398: 0.05086638371703101, 34399: 0.03234449432950526, 34400: 0.0, 34401: 0.02209944751381218},
('bebG', 'pelG'): {34391: 0.0458295996116751, 34392: 0.05922610751498519, 34393: 0.14691628602824522, 34394: 0.042617399144085515, 34395: 0.040238186273293064, 34396: 0.1463896635674748, 34397: 0.2113571176316211, 34398: 0.24972659880023207, 34399: 0.047487598831093686, 34400: 0.00198392101226109, 34401: nan},
('cheG', 'esnG'): {34391: 0.15665351335278288, 34392: 0.13931539676274687, 34393: 0.12207598059189505, 34394: 0.18605731943817558, 34395: 0.08528869593763302, 34396: 0.16804542165058764, 34397: 0.4130568998265453, 34398: 0.3647083325107957, 34399: 0.36578909818063526, 34400: 0.07166318303971346, 34401: 0.0},
('cheG', 'gbrG'): {34391: -0.002777776354533896, 34392: -0.004149663325658024, 34393: 0.03262814959518372, 34394: 0.005655894986418901, 34395: 0.001070498532718919, 34396: 0.057185779843027786, 34397: 0.04571878292360917, 34398: 0.10817516129032746, 34399: 0.10549737736853947, 34400: 0.0, 34401: 0.02209944751381218},
('cheG', 'pelG'): {34391: 0.08291824802143762, 34392: 0.09959815394847532, 34393: 0.37973450542493475, 34394: 0.0747915043629141, 34395: 0.07735160616341488, 34396: 0.48793384739612244, 34397: 0.5424401059577914, 34398: 0.5358304561652808, 34399: 0.06675909035190808, 34400: 0.0039447731755424, 34401: nan},
('esnG', 'gbrG'): {34391: 0.15589696720833252, 34392: 0.14103762889713062, 34393: 0.11765276421878212, 34394: 0.19498634749083052, 34395: 0.09655660736816672, 34396: 0.18003059831114374, 34397: 0.3229163584574005, 34398: 0.28671453518946993, 34399: 0.3761315754714064, 34400: 0.06735294299054478, 34401: 0.016158384814382615},
('esnG', 'pelG'): {34391: 0.08030734818983139, 34392: 0.03369344458901529, 34393: 0.1323555293365743, 34394: 0.07619435285642608, 34395: -0.0023537456739497124, 34396: 0.43475408969540413, 34397: 0.1926228954112988, 34398: 0.08911281297860016, 34399: 0.1902692115123271, 34400: 0.05140492301594556, 34401: 0.0},
('gbrG', 'pelG'): {34391: 0.08115603159743075, 34392: 0.1022885043014491, 34393: 0.29582981493571175, 34394: 0.08381926778527013, 34395: 0.08778332361227041, 34396: 0.3037846049143894, 34397: 0.3808037936276532, 34398: 0.4605344942598781, 34399: 0.1290420147420863, 34400: 0.0030081650193381987, 34401: 0.02209944751381218}
}

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


# NOTE: Generates a scatter graph if given a dictionary of values
def FSTscatter(input, start, stop):
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
             (strink(n)+'-'+strink(min(n+step, stop)))
             for n in range(start, stop, step)
             ]
    print(len(bounds))

    # NOTE: Maps each nested key from the input dict to a boundary
    first = ik[0:vlen[0]]
    keydict = dict(zip(first, bounds))

    # NOTE: Creates df for graph
    df = pd.DataFrame.from_dict(input, orient='index').stack().reset_index()
    df['Pop'] = df[['level_0', 'level_1']].agg('-'.join, axis=1)
    del df['level_0']
    del df['level_1']
    df = df.fillna('')
    df.columns = ['Range', 'FST', 'Pop']
    df['Range'].replace(keydict, inplace=True)

    # NOTE: Sorts the FST values in the df to auto set max axis values
    FST = list(df['FST'])
    FST = [i for i in FST if i != '']
    FST.sort(key=float)

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
                      yaxis_range=[FST[0] - 0.01, FST[-1] + 0.01])
    fig.add_hline(y=0.12, line_width=2, line_dash="dash", line_color="gray")

    fig.show()


FSTscatter(input, start, stop)


def optibin(num):
    bins = []
    n = num
    for i in range(1, 200):
        if n % i == 0:
            bins.append(i)
    divn = min(bins, key=lambda x: abs(x-15))
    if divn == 1:
        return bins[1]
    else:
        print(divn)
        return divn
