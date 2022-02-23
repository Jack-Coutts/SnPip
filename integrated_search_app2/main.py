# import the app factory (the app)
from os import sep
from Website import create_app
# Import flask and associated packages 
from flask import render_template, redirect, request, send_file, send_from_directory
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


### Pages/structure of app ###

# define a route or view
@app.route('/') # this is the home page
def home(): # this function will run whenever we go to this route
    return render_template('home.html') # Home page template

@app.route('/about') # this is the about page
def about(): # this function will run whenever we go to this route
    return render_template('about.html')

@app.route('/documentation') # this is the documentation page
def documentation(): # this function will run whenever we go to this route
    return render_template('documentation.html')



@app.route('/search', methods=['GET', 'POST']) # this is the search page
def search(): # this function will run whenever we go to this route

        if request.method == "POST": # Wehn form is filled out and search button pressed

            select=request.form['select'] # The option selected from dopdown bar

            #Time how long it takes to run
            start_time = time.time()

            BEB=''
            GBR=''
            CHB=''
            PEL=''
            ESN=''
            bhead=''
            ghead=''
            chead=''
            phead=''
            ehead=''
            btitle=''
            gtitle=''
            ctitle=''
            ptitle=''
            etitle=''

            try:
                # Create a list containing the population codes of selected populations
                subpop=request.form.getlist('subpop')

            except:

                # If no populations are selected
                return 'You must select at least one population'



            # If searching by snp name (from select menu)
            if select == 'SNP Name':

                # SNP Name refers to the text search bar - store that as a string
                snp = request.form['snp']

                # Search the database to select info from SNP table
                mycursor.execute("SELECT CHROM, POS, GENE, ID, REF, ALT FROM snp WHERE ID = %s ", [snp])
                data = mycursor.fetchall() # List containing extracted data
                data=pd.DataFrame(data).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                head=['CHROM', 'POS', 'GENE', 'ID', 'REF', 'ALT'] # Header of table displaying SNP info

                for item in subpop: # Iterate over list of selected populations

                    if item == 'BEB': # If this population selected 
                        # Search subpop table 
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'Bengali'", [snp])
                        BEB = mycursor.fetchall() # list containing extracted data
                        BEB=pd.DataFrame(BEB).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        bhead=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']# Header of table displaying subpop info


                    elif item == 'GBR': # If this population selected
                        # Search subpop table 
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'GBR'", [snp])
                        GBR = mycursor.fetchall() # list containing extracted data
                        GBR=pd.DataFrame(GBR).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        ghead=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']# Header of table displaying subpop info

                    elif item == 'CHB': # If this population selected
                        # Search subpop table
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'China'", [snp])
                        CHB = mycursor.fetchall() # list containing extracted data
                        CHB=pd.DataFrame(CHB).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        chead=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']# Header of table displaying subpop info

                    elif item == 'PEL': # If this population selected
                        # Search subpop table
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'Peru'", [snp])
                        PEL = mycursor.fetchall() # list containing extracted data
                        PEL=pd.DataFrame(PEL).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        phead=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF'] # Header of table displaying subpop info

                    elif item == 'ESN': # If this population selected
                        # Search subpop table
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'Nigeria'", [snp])
                        ESN = mycursor.fetchall() # list containing extracted data
                        ESN=pd.DataFrame(ESN).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        ehead=['ID', 'SUBPOP', 'AF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']# Header of table displaying subpop info

                    else: # If item not one of our subpop skip it
                        pass
                
                # Return runtime of search/data extraction
                runtime=('Search time: '+ str(time.time() - start_time)+ ' seconds.')  

                # Return the search template with these vairables newly defined 
                return render_template('search.html', 
                                        data=data, 
                                        BEB=BEB, 
                                        GBR=GBR, 
                                        CHB=CHB, 
                                        PEL=PEL, 
                                        ESN=ESN,
                                        head=head,
                                        bhead=bhead,
                                        ghead=ghead,
                                        chead=chead,
                                        phead=phead,
                                        ehead=ehead,
                                        runtime=runtime
                                        )
            
            # If searching by Gene name (from select menu)
            if select == 'Gene Name':
                # Store the gene name entered into the text search box as a string
                gene = request.form['snp'].upper()

                # Search the SNP table for all SNPs in that gene - for counting
                mycursor.execute("SELECT ID FROM snp WHERE GENE LIKE %s ", [gene])
                allsnps=mycursor.fetchall()
                snps = len(allsnps) # Store data in a list
                # String infomring the number of SNPs in the gene - counter
                num_snps = ('Number of SNPs found in ' + gene.upper() + ': ' + (str(snps) + '.')) 

                # SNP info table - search all infor for SNPs in gene
                mycursor.execute("SELECT CHROM, POS, GENE, ID, REF, ALT FROM snp WHERE GENE LIKE %s ", [gene])
                data = mycursor.fetchall() # Store data in a string
                data=pd.DataFrame(data).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)

                head=('Chromosome','Position', 'Gene','rsID','Reference','Alternate') # Table head - columns selected 
                SNPtitle='SNP Information' # Table title 

                

                for item in subpop: # iterate list of selected populations

                    if item == 'BEB': # If this population selected
                        # Select info from subpop where the ID is in a list of IDs that are found in the gene
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Bengali' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        BEB = mycursor.fetchall()  # list containing extracted data
                        BEB=pd.DataFrame(BEB).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        bhead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')# Header of table displaying subpop info
                        btitle='Bengali' # Table title 

                    elif item == 'GBR': # If this population selected
                        # Select info from subpop where the ID is in a list of IDs that are found in the gene
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'GBR' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        GBR = mycursor.fetchall() # list containing extracted data
                        GBR=pd.DataFrame(GBR).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        ghead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF') # Header of table displaying subpop info
                        gtitle='Great Britain' # Table title 

                    elif item == 'CHB': # If this population selected
                        # Select info from subpop where the ID is in a list of IDs that are found in the gene
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'China' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        CHB = mycursor.fetchall() # list containing extracted data
                        CHB=pd.DataFrame(CHB).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        chead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF') # Header of table displaying subpop info
                        ctitle='China' # Table title 

                    elif item == 'PEL': # If this population selected
                        # Select info from subpop where the ID is in a list of IDs that are found in the gene
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Peru' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        PEL = mycursor.fetchall() # list containing extracted data
                        PEL=pd.DataFrame(PEL).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        phead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF') # Header of table displaying subpop info
                        ptitle='Peru' # Table title 
                    
                    elif item == 'ESN': # If this population selected
                        # Select info from subpop where the ID is in a list of IDs that are found in the gene
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Nigeria' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        ESN = mycursor.fetchall()  # list containing extracted data
                        ESN=pd.DataFrame(ESN).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        ehead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF') # Header of table displaying subpop info
                        etitle='Nigeria'  # Table title 
                    
                    else:
                        pass
                
                ### FST ###

                # Select genotype string for SNPs in searched gene
                mycursor.execute("SELECT GT FROM snp WHERE GENE LIKE %s ", [gene])
                geno_list = mycursor.fetchall()

                # Run all fst comparisons
                fst = all_hudson_fsts(geno_list, subpop)
                
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
                
                
                # Calculate shannon diversity
                Shann=Shannon(allsnps, BAF, GAF, CAF, PAF, EAF, subpop)
                
                # Return runtime of search/data extraction
                runtime=('Search time: '+ str(time.time() - start_time)+ ' seconds.')

                # Return the search template with these vairables newly defined 
                return render_template('search.html',
                                        data=data, 
                                        SNPtitle=SNPtitle, 
                                        head=head,
                                        BEB=BEB, 
                                        GBR=GBR, 
                                        CHB=CHB, 
                                        PEL=PEL, 
                                        ESN=ESN, 
                                        bhead=bhead, 
                                        ghead=ghead, 
                                        chead=chead, 
                                        phead=phead,
                                        ehead=ehead,
                                        btitle=btitle,
                                        gtitle=gtitle,
                                        ctitle=ctitle,
                                        ptitle=ptitle,
                                        etitle=etitle,
                                        num_snps=num_snps,
                                        runtime=runtime,
                                        fst=fst,
                                        Shann=Shann)

                                       

            # If searching by location/position (from select menu)
            if select == 'Location':
                # Store the gene name entered into the text search box as a string
                location = request.form['snp']
                # Split the tring at the dash 
                location=location.split('-')
                # Turn the two numbers in the list in to inetgers and seperate them
                areastart=int(location[0])
                areaend=int(location[1])

                # Search the SNP table for all SNPs in that gene - for counting
                mycursor.execute("SELECT ID FROM snp WHERE %s <= POS AND POS <= %s ", (areastart, areaend ))
                allsnps=mycursor.fetchall()
                snps = len(allsnps) # Store data in a list
                # String infomring the number of SNPs in the gene - counter
                num_snps = ('Number of SNPs found in the range of ' + str(areastart) + ' - ' + str(areaend) + ': ' + (str(snps) + '.'))

                # SNP info table - search all infor for SNPs in position windown
                mycursor.execute("SELECT CHROM, POS, GENE, ID, REF, ALT FROM snp WHERE %s <= POS AND POS <= %s ", (areastart, areaend ))
                data = mycursor.fetchall() # Store data in a string
                data=pd.DataFrame(data).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                head=('Chromosome','Position', 'Gene','rsID','Reference','Alternate') # Table head - columns selected 
                SNPtitle='SNP Information'  # Table title 

                for item in subpop: # iterate list of selected populations

                    if item == 'BEB': # If this population selected
                        # Select info from subpop where the ID is in a list of IDs that are found in the position window
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Bengali' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                        BEB = mycursor.fetchall() # list containing extracted data
                        BEB=pd.DataFrame(BEB).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        bhead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF') # Header of table displaying subpop info
                        btitle='Bengali' # Table title 

                    elif item == 'GBR': # If this population selected
                        # Select info from subpop where the ID is in a list of IDs that are found in the position window
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'GBR' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                        GBR = mycursor.fetchall() # list containing extracted data
                        GBR=pd.DataFrame(GBR).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        ghead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF') # Header of table displaying subpop info
                        gtitle='Great Britain' # Table title

                    elif item == 'CHB': # If this population selected
                        # Select info from subpop where the ID is in a list of IDs that are found in the position window
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'China' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                        CHB = mycursor.fetchall() # list containing extracted data
                        CHB=pd.DataFrame(CHB).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        chead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF') # Header of table displaying subpop info
                        ctitle='China' # Table title

                    elif item == 'PEL': # If this population selected
                        # Select info from subpop where the ID is in a list of IDs that are found in the position window
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Peru' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                        PEL = mycursor.fetchall() # list containing extracted data
                        PEL=pd.DataFrame(PEL).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        phead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF') # Header of table displaying subpop info
                        ptitle='Peru' # Table title
      
                    elif item == 'ESN': # If this population selected
                        # Select info from subpop where the ID is in a list of IDs that are found in the position window
                        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Nigeria' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                        ESN = mycursor.fetchall() # list containing extracted data
                        ESN=pd.DataFrame(ESN).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
                        ehead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF') # Header of table displaying subpop info
                        etitle='Nigeria' # Table title

                    else:
                        pass
                
                ### FST ###

                # Select genotype string for SNPs in searched gene
                mycursor.execute("SELECT GT FROM snp WHERE ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                geno_list = mycursor.fetchall()

                # Run all fst comparisons
                fst = all_hudson_fsts(geno_list, subpop)

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

                
                # Return runtime of search/data extraction
                runtime=('Search time: '+ str(time.time() - start_time)+ ' seconds.')

                # Return the search template with these vairables newly defined
                return render_template('search.html',
                                        data=data, 
                                        SNPtitle=SNPtitle, 
                                        head=head,
                                        BEB=BEB, 
                                        GBR=GBR, 
                                        CHB=CHB, 
                                        PEL=PEL, 
                                        ESN=ESN, 
                                        bhead=bhead, 
                                        ghead=ghead, 
                                        chead=chead, 
                                        phead=phead,
                                        ehead=ehead,
                                        btitle=btitle,
                                        gtitle=gtitle,
                                        ctitle=ctitle,
                                        ptitle=ptitle,
                                        etitle=etitle,
                                        num_snps=num_snps,
                                        runtime=runtime,
                                        fst=fst,
                                        Shann=Shann)

                

            # If search by not specified
            else:
                pass

        # Return search template
        return render_template('search.html')



if __name__ == '__main__': # only if we run this file will we execute the line below
    # run the Flask app & start a web server
    app.run(debug=True) # debug means that if code changes server is auto re-run
