# Shannon Diveristy
import math
from math import log as ln
# FST
import numpy as np
import pandas as pd
import allel



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
def all_hudson_fsts(genotype_list, subpop):

    # create gt arrays from the gt strings
    g=makeArray(genotype_list)

    # extract genotype array into samples
    bebG, chbG, esnG, gbrG, pelG = g

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

    FSTs = pd.DataFrame(list(fsts.items()),columns = ['Populations','Hudson FST']).to_html(classes=' content-area clusterize-content table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=False, header=True) #table-responsive makes the table as small as possible

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
            poplst.append(GAF)
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

    Shannon = pd.DataFrame(list(dictionary.items()),columns = ['SNP name','Shannon Diversity for selected populations']).to_html(classes='content-area clusterize-content table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=False, header=True) #table-responsive makes the table as small as possible

    return Shannon


    

        


