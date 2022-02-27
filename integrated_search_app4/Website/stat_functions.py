# Shannon Diveristy
import math
from math import log as ln
# FST
import numpy as np
import pandas as pd
import allel
import plotly

#Tajimas D
from itertools import combinations

# Initial graphs
import plotly.express as px
import json
from json import JSONEncoder
import plotly.io as pio
import plotly.graph_objects as go



# Initial Graphs 
# Gene Map
def gene_list_graph(position, database, increment_size):

    # note: Numbers for data to be selected based on position
    start = (position - increment_size)
    finish = (position + increment_size)

    df = pd.read_sql(('SELECT POS, GENE, ID FROM snp WHERE POS BETWEEN %(dstart)s AND %(dfinish)s'), database,
                 params={"dstart": start, "dfinish": finish})

    # note: Gets the first and last positions of each gene in the imported df
    first = dict(df.groupby('GENE')['POS'].first())
    last = dict(df.groupby('GENE')['POS'].last())
    num = df.value_counts('GENE').reset_index(name='NUM')  # note: counts snp num


    # note: Creates a new df of each gene and their start and end positions
    df2 = pd.DataFrame({'first': pd.Series(first), 'last': pd.Series(last)})
    df2.reset_index(level=0, inplace=True)
    df2.columns = ['GENE', 'START', 'END']
    df2['length'] = df2['END'] - df2['START']

    # note: Creates a new df with the SNP numbers in it
    df3 = pd.merge(df2, num, how='inner', on='GENE')
    df3.columns = ['GENE', 'START', 'END', 'Length', 'SNP NUM']

    # note: Sorts the df by Start position
    df4 = df3.sort_values(by=['START'])
    print(df4)

    # note: Plots the graph
    fig = px.bar(df4,
                x='Length',
                y='GENE',
                base='START',
                orientation='h',
                color='SNP NUM',
                custom_data=['START', 'END', 'Length', 'SNP NUM'],
                labels={'GENE': 'Genes',
                        'START': 'Start position',
                        'END': 'End position',
                        'SNP NUM': 'Number of SNPs'})

    # note: Configures the floating label
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{y}</b><br>",
            "First SNP Position: %{customdata[0]:s}",
            "Last SNP Position: %{customdata[1]:s}",
            "Length between SNPs (bp): %{customdata[2]:s}",
            "Number of SNPs: %{customdata[3]:s}"
        ])
    )


    # note: Sets the title & fonts of the graph
    fig.update_layout(title={'text': "Gene Map",
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                    xaxis_title="Chromosome position (bp)",
                    yaxis_title="Genes",
                    font_family="Times New Roman",
                    font_color="Black",
                    title_font_family="Times New Roman",
                    title_font_color="Black")

    # note: Creates a range slider
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

    # note: Adds a line at the input
    fig.add_vline(x=position, line_width=2, line_dash="dash", line_color="gray")
    
    a=pio.to_html(fig)



    #fig.update_layout(width=1500, height=500)
    #plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  
    return a


def snp_map(windowsize, database):

    df = pd.read_sql(('SELECT POS, GENE, ID FROM snp'), database)

    pos = df['POS'][:]

    # note: Creates the windowsize
    bin = np.arange(0, pos.max(), windowsize)

    # note: Uses the window midpoints as x coordinate
    x = (bin[1:] + bin[:-1])/2

    # note: Compute variant density in each window
    h, _ = np.histogram(pos, bins=bin)
    y = h / windowsize

    # note: plots & configures the graph
    fig = go.Figure(go.Line(x=x, y=y,
                            hovertemplate=
                            'Variant density (bp<sup>-1</sup>): %{y}' +
                            '<br>Chromosome position (bp)<extra></extra>: %{x}'))
    fig.update_traces(line_color='goldenrod')

    # note: Centers the title and fonts
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

    # note: Adds cross section cursor
    fig.update_xaxes(showspikes=True, spikecolor="Grey", spikesnap="cursor",
                     spikemode="across")
    fig.update_yaxes(showspikes=True, spikecolor="Black", spikethickness=2)
    fig.update_layout(spikedistance=1000, hoverdistance=100)

    # note: Adds sliding window to the graph
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

    graph=pio.to_html(fig)

    return graph








def makeArray(strings):
    
    # initialize sample array with empty list
    bebG, cheG, esnG, gbrG, pelG = [], [], [], [], []
    
    # swap the keys and values in the dictionary below
    nested_dictionary = {'GBR':{'e':'a', 'f':'b', 'g':'c', 'h': 'd'},
                         'PEL':{'i':'a', 'j':'b', 'k':'c', 'l': 'd'},
                         'ESN':{'m':'a', 'n':'b', 'o':'c', 'p': 'd'},
                         'BEB':{'q':'a', 'r':'b', 's':'c', 't': 'd'},
                         'CHE':{'u':'a', 'v':'b', 'w':'c', 'x': 'd'}}

    ginfo = {'a':'1|0', 'b':'1|1', 'c':'0|1', 'd':'0|0'}

    dic = {'e':'GBR', 'f':'GBR', 'g':'GBR', 'h':'GBR',
           'i':'PEL', 'j':'PEL', 'k':'PEL', 'l':'PEL',
           'm':'ESN', 'n':'ESN', 'o':'ESN', 'p':'ESN',
           'q':'BEB', 'r':'BEB', 's':'BEB', 't':'BEB',
           'u':'CHE', 'v':'CHE', 'w':'CHE', 'x':'CHE'}
    
    lst=[]
    for item in strings:

        for p in item:

            lst.append(p)

    for string in lst:
        string = string.strip()
        genotypes = {}
        N = len(string)

        for i, c in enumerate(string):
            # take sample as key and 0|1 etc as value
            genotypes.setdefault(dic[c], []).append(ginfo[nested_dictionary[dic[c]][c]])

        # sort dictionary alphabetically
        genotypes = dict(sorted(genotypes.items(), key = lambda x:x[0].lower()))
        # split each 0|1 etc by | and make a list,,,thus apply on each sample
        genotype_array = [[list(map(int, v.split('|'))) for v in val] for val in genotypes.values()]

        # extracting genotype array samples
        bebG.append(genotype_array[0])
        cheG.append(genotype_array[1])
        esnG.append(genotype_array[2])
        gbrG.append(genotype_array[3])
        pelG.append(genotype_array[4])
        
    return (bebG, cheG, esnG, gbrG, pelG)


# Gives you sinnge value fst for population comparison
def calc_hudson_fst_1v1(pop_array1, pop_array2):
    genotype_array1 = allel.GenotypeArray(pop_array1)
    genotype_array2 = allel.GenotypeArray(pop_array2)
    ac1 = genotype_array1.count_alleles()
    ac2 = genotype_array2.count_alleles()
    num, den = allel.hudson_fst(ac1, ac2)
    fst = np.sum(num) / np.sum(den)
    return fst 

# Moving window definded so that the number of fsts is always the same - as long as number of snps is not too small
def moving_hudson(pop_array1, pop_array2, moving_window):
    
    genotype_array1 = allel.GenotypeArray(pop_array1)
    genotype_array2 = allel.GenotypeArray(pop_array2)
    ac1 = genotype_array1.count_alleles()
    ac2 = genotype_array2.count_alleles()
    mfst=allel.moving_hudson_fst(ac1, ac2, moving_window)
    
    return mfst

# Get the FST for all comparisons of the populations selected
def all_hudson_fsts(array, subpop):

    # extract genotype array into samples
    bebG, chbG, esnG, gbrG, pelG = array

    fsts={}

    # Run FST comparisons
    if 'BEB' in subpop and 'GBR' in subpop:

        BvG = calc_hudson_fst_1v1(bebG, gbrG)
        fsts['Bengali vs Great Britain']=BvG

    if 'BEB' in subpop and 'CHB' in subpop:

        BvC = calc_hudson_fst_1v1(bebG, chbG)
        fsts['Bengali vs China']=BvC

    if 'BEB' in subpop and 'PEL' in subpop:

        BvP = calc_hudson_fst_1v1(bebG, pelG)
        fsts['Bengali vs Peru']=BvP

    if 'BEB' in subpop and 'ESN' in subpop:

        BvE = calc_hudson_fst_1v1(bebG, esnG)
        fsts['Bengali vs Nigeria']=BvE

    if 'GBR' in subpop and 'CHB' in subpop:

        GvC = calc_hudson_fst_1v1(gbrG, chbG)
        fsts['Great Britain vs China']=GvC

    if 'GBR' in subpop and 'PEL' in subpop:

        GvP = calc_hudson_fst_1v1(gbrG, pelG)
        fsts['Great Britain vs Peru']=GvP

    if 'GBR' in subpop and 'ESN' in subpop:

        GvE = calc_hudson_fst_1v1(gbrG, esnG)
        fsts['Great Britain vs Nigeria']=GvE

    if 'CHB' in subpop and 'PEL' in subpop:

        CvP = calc_hudson_fst_1v1(chbG, pelG)
        fsts['China vs Peru']=CvP

    if 'CHB' in subpop and 'ESN' in subpop:

        CvE = calc_hudson_fst_1v1(chbG, esnG)
        fsts['China vs Nigeria']=CvE

    if 'PEL' in subpop and 'ESN' in subpop:

        PvE = calc_hudson_fst_1v1(pelG, esnG)
        fsts['Peru vs Nigeria ']=PvE

    else:
        pass

    FSTs = pd.DataFrame(list(fsts.items()),columns = ['Populations','Hudson FST']).to_html(classes=' content-area clusterize-content table table-stripped table-striped table-bordered table-sm" id = "my_id', justify='left', index=False, show_dimensions=False, header=True) #table-responsive makes the table as small as possible

    return FSTs

# Shannon Diveristy 
def sdi(af): #A list of allele frequencies per snp 
    index = []
  
    for x in af:
        if x > 0:
            Pi = (x) * ln(x)
            index.append(Pi)
        else:
            pass
    H = -sum(index)
    return H

def Shannon(allsnps, BAF, GAF, CAF, PAF, EAF, subpop):

    # Turn extracted list of tuples of strings into a list of floats
    BAF=[float(a) for item in BAF for a in item]
    GAF=[float(a) for item in GAF for a in item]
    CAF=[float(a) for item in CAF for a in item]
    PAF=[float(a) for item in PAF for a in item]
    EAF=[float(a) for item in EAF for a in item]


    #list to be zipped together
    poplst=[]
    for item in subpop:
        if item == 'BEB':
            poplst.append(BAF)

        elif item == 'GBR':
            poplst.append(GAF)
        
        elif item == 'CHB':
            poplst.append(CAF)

        elif item == 'PEL':
            poplst.append(PAF)
        
        elif item == 'ESN':
            poplst.append(EAF)
        else:
            pass

    # Combine lists together into a nested list so that each sublist contains the AF for each subpop
    afs=[list(l) for l in zip(*poplst)]

    allsnp=allsnps # List of tuples the SNPs
    # Convert list of tuples of strings to list of strings
    allsnps=[a for item in allsnp for a in item]

    snlst=[]
    for item in allsnps:

        snlst.append(item)

    shnnlst=[]

    for item in afs:

        shnn=sdi(item)
        shnnlst.append(shnn)

    
    zip_iterator = zip(snlst, shnnlst)
    dictionary=dict(zip_iterator)

    Shannon = pd.DataFrame(list(dictionary.items()),columns = ['SNP name','Shannon Diversity for Selected Populations']).to_html(classes='content-area clusterize-content table table-stripped table-striped table-bordered table-sm" id = "my_id1', justify='left', index=False, show_dimensions=False, header=True) #table-responsive makes the table as small as possible

    return Shannon

# Tajimas D

def Tajimas(genotype_array, subpop):

    # extract genotype array into samples
    bebG, cheG, esnG, gbrG, pelG = genotype_array

    # ONly retain selected populations
    poplst=[]
    poplst2=[]
    for item in subpop:
        if item == 'BEB':
            poplst.append('Bengali')
            poplst2.append(bebG)

        elif item == 'GBR':
            poplst.append('Great Britain')
            poplst2.append(gbrG)
        
        elif item == 'CHB':
            poplst.append('China')
            poplst2.append(cheG)

        elif item == 'PEL':
            poplst.append('Peru')
            poplst2.append(pelG)
        
        elif item == 'ESN':
            poplst.append('Nigeria')
            poplst2.append(esnG)
        else:
            pass



    Tajima_D = {}
    
    for pair,val in zip( combinations([*poplst],1), combinations([*poplst2],1)):
        
        ac = allel.GenotypeArray(val[0]).count_alleles()
       
        fst = allel.tajima_d(ac)
    
        Tajima_D.update({str(pair).strip("(''),") : fst})

    Tajima = pd.DataFrame(list(Tajima_D.items()),columns = ['Subpopulation',"Tajima's D for Selected Population"]).to_html(classes='content-area clusterize-content table table-stripped table-striped table-bordered table-sm" id = "my_id2', justify='left', index=False, show_dimensions=False, header=True) #table-responsive makes the table as small as possible
    
    return Tajima

    

def hudson_sliding(areastart, areaend, database, pre_array):

    windowsize=(areaend-areastart)/15

    df = pd.read_sql(('SELECT POS, GENE, ID FROM snp WHERE %s <= POS AND POS <= %s', (areastart, areaend )), database)

    pos = df['POS'][:]

    # note: Creates the windowsize
    bin = np.arange(0, pos.max(), windowsize)

    # note: Uses the window midpoints as x coordinate
    x = (bin[1:] + bin[:-1])/2

    # extract genotype array into samples
    bebG, cheG, esnG, gbrG, pelG = pre_array

    # Create a dictionary of 10 arrays - one for each population comparison
    FSTs = {}
    
    for pair,val in zip( combinations(['bebG','cheG','esnG','gbrG','pelG'],2), combinations([bebG,cheG,esnG,gbrG,pelG],2)):
        ac1 = allel.GenotypeArray(val[0]).count_alleles()
        ac2 = allel.GenotypeArray(val[1]).count_alleles()
        fst = allel.moving_hudson_fst(ac1, ac2, 10)
    
        FSTs.update({str(pair).strip("(''),") : fst})







    # note: Compute variant density in each window
    h, _ = np.histogram(pos, bins=bin)
    y = h / windowsize

    # note: plots & configures the graph
    fig = go.Figure(go.Line(x=x, y=y,
                            hovertemplate=
                            'Variant density (bp<sup>-1</sup>): %{y}' +
                            '<br>Chromosome position (bp)<extra></extra>: %{x}'))
    fig.update_traces(line_color='goldenrod')

    # note: Centers the title and fonts
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

    # note: Adds cross section cursor
    fig.update_xaxes(showspikes=True, spikecolor="Grey", spikesnap="cursor",
                     spikemode="across")
    fig.update_yaxes(showspikes=True, spikecolor="Black", spikethickness=2)
    fig.update_layout(spikedistance=1000, hoverdistance=100)

    # note: Adds sliding window to the graph
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

    graph=pio.to_html(fig)

    return graph


