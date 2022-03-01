# import the app factory (the app)
from audioop import reverse
from operator import itemgetter
from os import sep

from Website import create_app
# Import flask and associated packages 
from flask import render_template, redirect, request, send_file, send_from_directory, url_for, session
# MySQL connector to connect to and search db
import mysql.connector 
from mysql.connector import connect, Error
# To time searches
import time
# import pandas 
import pandas as pd

#Import stat functions
from Website.stat_functions import *

# Start app
app = create_app()

# Set up a connection with the MySQL database
try:
    mydb = mysql.connector.connect(host="localhost",
                                    user="root",
                                    password="password",
                                    database="SnPip") # Database Name

    mycursor = mydb.cursor(buffered=True)
except Error as e:
    print(e)


@app.route('/') # this is the home page
def home(): # this function will run whenever we go to this route
    return render_template('home.html') # Home page template

@app.route('/about') # this is the about page
def about(): # this function will run whenever we go to this route
    return render_template('about.html')

@app.route('/documentation') # this is the documentation page
def documentation(): # this function will run whenever we go to this route
    return render_template('documentation.html')

@app.route('/doc_download')
def doc_download():
    return send_file('static/Documentation.pdf', as_attachment=True, cache_timeout=0)

@app.route('/No_Gene') # this is the documentation page
def No_Gene(): # this function will run whenever we go to this route
    return render_template('No_Gene.html')

@app.route('/No_Position') # this is the documentation page
def No_Position(): # this function will run whenever we go to this route
    return render_template('No_Position.html')

@app.route('/No_SNP') # this is the documentation page
def No_SNP(): # this function will run whenever we go to this route
    return render_template('No_SNP.html')

@app.route('/No_Subpop') # this is the documentation page
def No_Subpop(): # this function will run whenever we go to this route
    return render_template('No_Subpop.html')

@app.route('/snp_info') # this is the documentation page
def snp_info(): # this function will run whenever we go to this route

    # Need to handle it not being gene

    try:

        gene=session['gene']


        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT CHROM, POS, GENE, ID, REF, ALT, FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM snp WHERE GENE LIKE %s ", [gene])
        data = mycursor.fetchall() # Store data in a string
        data=pd.DataFrame(data, columns=['Chromosome','Position', 'Gene','rsID','Reference','Alternate','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)

        return render_template('snp_info.html', data=data)

    except:
        pass

    try:

        snp=session['snp']

        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT CHROM, POS, GENE, ID, REF, ALT, FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM snp WHERE ID LIKE %s ", [snp])
        data = mycursor.fetchall() # Store data in a string
        data=pd.DataFrame(data, columns=['Chromosome','Position', 'Gene','rsID','Reference','Alternate','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)

        return render_template('snp_info.html', data=data)

    except:
        pass

    try:

        areastart=session['areastart']
        areaend=session['areaend']

        mycursor.execute("SELECT CHROM, POS, GENE, ID, REF, ALT, FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM snp WHERE %s <= POS AND POS <= %s ", (areastart, areaend ))
        data = mycursor.fetchall() # Store data in a string
        data=pd.DataFrame(data, columns=['Chromosome','Position', 'Gene','rsID','Reference','Alternate','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
        return render_template('snp_info.html', data=data)

    except:
        pass


@app.route('/BEB_info') # this is the documentation page
def BEB_info(): # this function will run whenever we go to this route

    # Need to handle it not being gene

    try:

        gene=session['gene']


        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Bengali' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
        BEB = mycursor.fetchall() # list containing extracted data
        BEB=pd.DataFrame(BEB, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('BEB_info.html', BEB=BEB)

    except:
        pass

    try:

        snp=session['snp']

        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'Bengali'", [snp])
        BEB = mycursor.fetchall() # list containing extracted data
        BEB=pd.DataFrame(BEB, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('BEB_info.html', BEB=BEB)

    except:
        pass

    try:

        areastart=session['areastart']
        areaend=session['areaend']

        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Bengali' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s)", (areastart, areaend))
        BEB = mycursor.fetchall() # list containing extracted data
        BEB=pd.DataFrame(BEB, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('BEB_info.html', BEB=BEB)

    except:
        pass



@app.route('/GBR_info') # this is the documentation page
def GBR_info(): # this function will run whenever we go to this route

    # Need to handle it not being gene

    try:

        gene=session['gene']


        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'GBR' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
        GBR = mycursor.fetchall() # list containing extracted data
        GBR=pd.DataFrame(GBR, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('GBR_info.html', GBR=GBR)

    except:
        pass

    try:

        snp=session['snp']

        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'GBR'", [snp])
        GBR = mycursor.fetchall() # list containing extracted data
        GBR=pd.DataFrame(GBR, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('GBR_info.html', GBR=GBR)

    except:
        pass

    try:

        areastart=session['areastart']
        areaend=session['areaend']

        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'GBR' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s)", (areastart, areaend))
        GBR = mycursor.fetchall() # list containing extracted data
        GBR=pd.DataFrame(GBR, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('GBR_info.html', GBR=GBR)

    except:
        pass



@app.route('/CHB_info') # this is the documentation page
def CHB_info(): # this function will run whenever we go to this route

    # Need to handle it not being gene

    try:

        gene=session['gene']


        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'China' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
        CHB = mycursor.fetchall() # list containing extracted data
        CHB=pd.DataFrame(CHB, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('CHB_info.html', CHB=CHB)

    except:
        pass

    try:

        snp=session['snp']

        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'China'", [snp])
        CHB = mycursor.fetchall() # list containing extracted data
        CHB=pd.DataFrame(CHB, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('CHB_info.html', CHB=CHB)

    except:
        pass

    try:

        areastart=session['areastart']
        areaend=session['areaend']

        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'China' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s)", (areastart, areaend))
        CHB = mycursor.fetchall() # list containing extracted data
        CHB=pd.DataFrame(CHB, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('CHB_info.html', CHB=CHB)

    except:
        pass



@app.route('/PEL_info') # this is the documentation page
def PEL_info(): # this function will run whenever we go to this route

    # Need to handle it not being gene

    try:

        gene=session['gene']


        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Peru' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
        PEL = mycursor.fetchall() # list containing extracted data
        PEL=pd.DataFrame(PEL, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('PEL_info.html', PEL=PEL)

    except:
        pass

    try:

        snp=session['snp']

        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'Peru'", [snp])
        PEL = mycursor.fetchall() # list containing extracted data
        PEL=pd.DataFrame(PEL, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('PEL_info.html', PEL=PEL)

    except:
        pass

    try:

        areastart=session['areastart']
        areaend=session['areaend']

        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Peru' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s)", (areastart, areaend))
        PEL = mycursor.fetchall() # list containing extracted data
        PEL=pd.DataFrame(PEL, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('PEL_info.html', PEL=PEL)

    except:
        pass


@app.route('/ESN_info') # this is the documentation page
def ESN_info(): # this function will run whenever we go to this route

    # Need to handle it not being gene

    try:

        gene=session['gene']


        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Nigeria' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
        ESN = mycursor.fetchall() # list containing extracted data
        ESN=pd.DataFrame(ESN, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('ESN_info.html', ESN=ESN)

    except:
        pass

    try:

        snp=session['snp']

        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'Nigeria'", [snp])
        ESN = mycursor.fetchall() # list containing extracted data
        ESN=pd.DataFrame(ESN, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('ESN_info.html', ESN=ESN)

    except:
        pass

    try:

        areastart=session['areastart']
        areaend=session['areaend']

        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Nigeria' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s)", (areastart, areaend))
        ESN = mycursor.fetchall() # list containing extracted data
        ESN=pd.DataFrame(ESN, columns=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        
        return render_template('ESN_info.html', ESN=ESN)

    except:
        pass
    



@app.route('/search_one')
def search_one():
    
    # SNP distribution graph
    map_snp=snp_map(100000, mydb) # Only visible pre-search 

    return render_template('search_one.html', map_snp=map_snp)


@app.route('/search_out', methods=['GET', 'POST']) # this is the search page
def search_out(): # this function will run whenever we go to this route


    select=request.form['select'] # The option selected from dopdown bar

        #Time how long it takes to run
    start_time = time.time()

    BEB='Sub-Population not selected.'
    GBR='Sub-Population not selected.'
    CHB='Sub-Population not selected.'
    PEL='Sub-Population not selected.'
    ESN='Sub-Population not selected.'

    


    try:
        # Create a list containing the population codes of selected populations
        subpop=request.form.getlist('subpop')

    except:

        # If no populations are selected
        return 'You must select at least one population'

    
    if len(subpop) == 0:

        return render_template('No_Subpop.html')

    else:


        bclick=''
        gclick=''
        cclick=''
        pclick=''
        eclick=''
        
        for item in subpop:

            if item == 'BEB':
                bclick='Open BEB SNP Infomormation'

            elif item == 'GBR':
                gclick='Open GBR SNP Infomormation'

            elif item == 'CHB':
                cclick='Open CHB SNP Infomormation'
            
            elif item == 'PEL':
                pclick='Open PEL SNP Infomormation'
                
            elif item == 'ESN':
                eclick='Open ESN SNP Infomormation'
            
            else:
                pass

        # If searching by snp name (from select menu)
        if select == 'SNP Name':

            sp=str(subpop).strip("[]")
            sp=sp.replace("'","")
            Searched_pops='Sub-Populations searched: ' + sp + '.'

            # Check that search item is in the databse
            mycursor.execute("SELECT ID FROM snp") # Select all rsIDs from snp table
            snptbl_rsIDs=mycursor.fetchall() # list of tuples of strings of all rsIDs
            snptbl_rsIDs=[a for item in snptbl_rsIDs for a in item] # list of strings of all rsIDs

            snp = request.form['snp']

            if snp in snptbl_rsIDs:


                # SNP Name refers to the text search bar - store that as a string
                

                session['snp']=snp

                # Select position for gene distribution table
                mycursor.execute("SELECT POS FROM snp WHERE ID = %s ", [snp])
                pos = float(str(mycursor.fetchall()).strip("''[](),")) # Position number

                # Gene map graph relevant to the search
                gene_map=gene_list_graph(pos, mydb, 1000000)
                
                # Return runtime of search/data extraction
                runtime=('Search time: '+ str(time.time() - start_time)+ ' seconds.')  

                # Return the search template with these vairables newly defined 
                return render_template('search_out.html',
                                        runtime=runtime,
                                        gene_map=gene_map,
                                        Searched_pops=Searched_pops,
                                        bclick=bclick, 
                                        gclick=gclick,
                                        cclick=cclick,
                                        pclick=pclick,
                                        eclick=eclick
                                        )
            else:

                return render_template('No_SNP.html')
        
        # If searching by Gene name (from select menu)
        if select == 'Gene Name':
            # Store the gene name entered into the text search box as a string
            gene = request.form['snp'].upper()

            session['gene']=gene

            sp=str(subpop).strip("[]")
            sp=sp.replace("'","")
            Searched_pops='Sub-Populations searched: ' + sp + '.'


            # Check that search item is in the databse
            mycursor.execute("SELECT GENE FROM snp") # Select all genes from snp table
            snptbl_genes=mycursor.fetchall() # list of tuples of strings of all genes
            snptbl_genes=[a for item in snptbl_genes for a in item] # list of strings of all genes

            if gene in snptbl_genes: # Gene is in the databse 

                # Search the SNP table for all SNPs in that gene - for counting
                mycursor.execute("SELECT ID FROM snp WHERE GENE LIKE %s ", [gene])
                allsnps=mycursor.fetchall()
                snps = len(allsnps) # Store data in a list
                # String infomring the number of SNPs in the gene - counter
                num_snps = ('Number of SNPs found in ' + gene.upper() + ': ' + (str(snps) + '.')) 

                # Save the gene name for SNP search table page
                session['gene']= gene

                head=('Chromosome','Position', 'Gene','rsID','Reference','Alternate') # Table head - columns selected 
                SNPtitle='SNP Information' # Table title 

                # Select position for gene distribution table
                mycursor.execute("SELECT POS FROM snp WHERE GENE = %s ", [gene])
                pos = float(str(mycursor.fetchone()).strip("''[](),")) # Position number

                # Gene map graph relevant to the search
                gene_map=gene_list_graph(pos, mydb, 1000000)

                
                ### FST ###

                # Select genotype string for SNPs in searched gene
                mycursor.execute("SELECT GT FROM snp WHERE GENE LIKE %s ", [gene])
                geno_list = mycursor.fetchall()

                #Make genotype array
                array=makeArray(geno_list)

                # Run all fst comparisons
                fst = all_hudson_fsts(array, subpop)
                
                ### Shannon Diversity ###

                # Empty lists of tuples of strings if  population not selected
                BAF=[('1')]
                GAF=[('1')]
                CAF=[('1')]
                PAF=[('1')]
                EAF=[('1')]

                # Extract allele frequency data from databse 
                for item in subpop:

                    if item == 'BEB':
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'Bengali' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        BAF=mycursor.fetchall() #list of tuples

                    elif item == 'GBR':
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'GBR' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        GAF=mycursor.fetchall() #list of tuples
                    
                    elif item == 'CHB':
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'China' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        CAF=mycursor.fetchall() #list of tuples

                    elif item == 'PEL':
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'Peru' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        PAF=mycursor.fetchall() #list of tuples
                    
                    elif item == 'ESN':
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'Nigeria' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        EAF=mycursor.fetchall() #list of tuples
                    
                    else:
                        pass
                
                # Creating an FST graph
                mycursor.execute("SELECT POS FROM snp WHERE GENE = %s",[gene])
                positions=mycursor.fetchall()
                positions=[float(a) for item in positions for a in item]

                sorting=positions
                sorting.sort(reverse=False, key=float)

                dist=(sorting[-1]-sorting[0])
                dist=int(0.1*dist)
                
                # Create a dictionary that can be used as input for the graph function
                gd=fst_dict_calc(positions, array, dist )

                graph=FSTscatter(gd, int(positions[0]), int(positions[-1]), dist)

                

                # Calculate shannon diversity
                Shann=Shannon(allsnps, BAF, GAF, CAF, PAF, EAF, subpop)

                ShannG=ShannonG(allsnps, BAF, GAF, CAF, PAF, EAF, subpop, positions)

                ShannGG=ShannonGraph(ShannG)



                # Tajimas D

                Taj=Tajimas(array, subpop)

                td=moving_tajimas_d(array)

                #td=taj_dict_calc(positions, array, dist)

                tdg=TD_Bar(td)

                
                
                # Return runtime of search/data extraction
                runtime=('Search time: '+ str(time.time() - start_time)+ ' seconds.')

                # Return the search template with these vairables newly defined 
                return render_template('search_out.html',
                                        num_snps=num_snps,
                                        runtime=runtime,
                                        fst=fst,
                                        Shann=Shann,
                                        Taj=Taj,
                                        gene_map=gene_map,
                                        Searched_pops=Searched_pops,
                                        bclick=bclick, 
                                        gclick=gclick,
                                        cclick=cclick,
                                        pclick=pclick,
                                        eclick=eclick,
                                        graph=graph,
                                        dist=dist,
                                        gd=gd,
                                        tdg=tdg,
                                        ShannGG=ShannGG
                                        )


            else: # Gene not in database

                return render_template('No_Gene.html')


        # If searching by location/position (from select menu)
        if select == 'Location':
            # Store the gene name entered into the text search box as a string
            location = request.form['snp']

            try:
                # Split the tring at the dash 
                location=location.split('-')
                # Turn the two numbers in the list in to inetgers and seperate them
                areastart=int(location[0])
                areaend=int(location[1])
            except:
                return render_template('No_Position.html')

            # Saved for SNP table page 
            session['areastart']=areastart
            session['areaend']=areaend

            sp=str(subpop).strip("[]")
            sp=sp.replace("'","")
            Searched_pops='Sub-Populations searched: ' + sp + '.'

            # Check that search item is in the databse
            mycursor.execute("SELECT POS FROM snp") # Select all positions from snp table
            snptbl_position=mycursor.fetchall() # list of tuples of strings of all positions
            snptbl_position=[float(a) for item in snptbl_position for a in item] # list of strings of all positions

            not_out_of_bounds=0

            for item in snptbl_position:

                if item > areastart and item < areaend: # if position falls in given range
                    not_out_of_bounds+=1
                else:
                    pass
            
            if not_out_of_bounds > 0: # If positon range given conatins snps


                # Search the SNP table for all SNPs in that gene - for counting
                mycursor.execute("SELECT ID FROM snp WHERE %s <= POS AND POS <= %s ", (areastart, areaend ))
                allsnps=mycursor.fetchall()
                snps = len(allsnps) # Store data in a list
                # String infomring the number of SNPs in the gene - counter
                num_snps = ('Number of SNPs found in the range of ' + str(areastart) + ' - ' + str(areaend) + ': ' + (str(snps) + '.'))

                # Gene map graph relevant to the search
                gene_map=gene_list_graph(areastart, mydb, 1000000)
                
                ### FST ###

                # Select genotype string for SNPs in searched gene
                mycursor.execute("SELECT GT FROM snp WHERE ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                geno_list = mycursor.fetchall()

                # Creating an FST graph
                mycursor.execute("SELECT POS FROM snp WHERE ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                positions=mycursor.fetchall()
                positions=[float(a) for item in positions for a in item]

                sorted=positions.sort(reverse=True)
                dist=math.ceil((sorted[0]-sorted[-1])/15)

                # Make genotype array
                array=makeArray(geno_list)

                # Run all fst comparisons
                fst = all_hudson_fsts(array, subpop)

                # Create a dictionary that can be used as input for the graph function
                gd=fst_dict_calc(positions, array )

                #Plot the graph
                graph=FSTscatter(gd, int(positions[0]), int(positions[-1]), int(dist))

                ### Shannon Diversity ###

                # Empty lists of tuples of strings if  population not selected
                BAF=[('1')]
                GAF=[('1')]
                CAF=[('1')]
                PAF=[('1')]
                EAF=[('1')]

                # Extract allele frequency data from databse 
                for item in subpop:

                    if item == 'BEB':
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'Bengali' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                        BAF=mycursor.fetchall() #list of tuples

                    elif item == 'GBR':
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'GBR' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                        GAF=mycursor.fetchall() #list of tuples
                    
                    elif item == 'CHB':
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'China' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                        CAF=mycursor.fetchall() #list of tuples

                    elif item == 'PEL':
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'Peru' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                        PAF=mycursor.fetchall() #list of tuples
                    
                    elif item == 'ESN':
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'Nigeria' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                        EAF=mycursor.fetchall() #list of tuples
                    
                    else:
                        pass
                
                
                # Calculate shannon diversity
                Shann=Shannon(allsnps, BAF, GAF, CAF, PAF, EAF, subpop)

                # Tajimas D
                Taj=Tajimas(array, subpop)
                
                # Return runtime of search/data extraction
                runtime=('Search time: '+ str(time.time() - start_time)+ ' seconds.')

                # Return the search template with these vairables newly defined
                return render_template('search_out.html',
                                        num_snps=num_snps,
                                        runtime=runtime,
                                        fst=fst,
                                        Shann=Shann,
                                        Taj=Taj,
                                        gene_map=gene_map,
                                        Searched_pops=Searched_pops,
                                        bclick=bclick, 
                                        gclick=gclick,
                                        cclick=cclick,
                                        pclick=pclick,
                                        eclick=eclick,
                                        graph=graph)

            else:

                return render_template('No_Position.html')


        





if __name__ == '__main__': # only if we run this file will we execute the line below
    # run the Flask app & start a web server
    app.run(debug=True) # debug means that if code changes server is auto re-run
