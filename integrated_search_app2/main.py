# import the app factory (the app)
from Website import create_app
from flask import render_template, redirect, request, send_file, send_from_directory
from flaskext.mysql import MySQL

import mysql.connector 
from mysql.connector import connect, Error


from IPython.display import HTML

import datetime
import io
from io import BytesIO 
from io import StringIO

import pandas as pd

#from Website.functions import *


app = create_app()


try:
    mydb = mysql.connector.connect(host="localhost",
                                    user="root",
                                    password="password",
                                    database="SnPip")

    mycursor = mydb.cursor()
except Error as e:
    print(e)



'''
# Database connection info. Note that this is not a secure connection.
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'snpip'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Initialises MySQL
mysql = MySQL()
mysql.init_app(app)

# Create a cursor to manipulate data in database
conn = mysql.connect()
cursor = conn.cursor()

'''

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

        if request.method == "POST":
            select=request.form['select']

            try:

                subpop=request.form.getlist('subpop')

            except:

                return 'You must select at least one population'



            # If searching by snp name
            if select == 'SNP Name':

                snp = request.form['snp']

                # search by SNP
                mycursor.execute("SELECT CHROM, POS, GENE, ID, REF, ALT FROM snp WHERE ID = %s ", [snp])
                data = mycursor.fetchall()

                if len(data) > 0:
                    headings=['Chromosome','Position', 'Gene','rsID','Reference','Alternate']
                    SNPtitle='SNP Information'

                if len(data) <= 0:
                    headings=''
                    SNPtitle=''
                
                if 'BEB' in subpop:

                    mycursor.execute("SELECT ID, SUBPOP, AF, ('ALT|REF'), ('REF|ALT'), ('ALT|ALT'), ('REF|REF') FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'Bengali'", [snp])
                    BEB = mycursor.fetchall()

                    if len(BEB) == 0:

                        BEB = 'Bengali not found.'
                        bhead=''
                        btitle=''
                    else:
                        bhead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        btitle='Bengali'

                if 'BEB' not in subpop:
                    BEB=''
                    bhead=''
                    btitle=''

                if 'GBR' in subpop:

                    mycursor.execute("SELECT ID, SUBPOP, AF, ('ALT|REF'), ('REF|ALT'), ('ALT|ALT'), ('REF|REF') FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'GBR'", [snp])
                    GBR = mycursor.fetchall()

                    if len(GBR) == 0:
                        GBR = 'GBR not found.'
                        gtitle=''
                        ghead=''
                    else:
                        ghead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        gtitle='Great Britain'

                if 'GBR' not in subpop:
                    GBR=''
                    ghead=''
                    gtitle=''
                
                if 'CHB' in subpop:

                    mycursor.execute("SELECT ID, SUBPOP, AF, ('ALT|REF'), ('REF|ALT'), ('ALT|ALT'), ('REF|REF') FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'China'", [snp])
                    CHB = mycursor.fetchall()

                    if len(CHB) == 0:

                        CHB = 'China not found.'
                        ctitle=''
                        chead=''

                    else:
                        chead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        ctitle='China'

                if 'CHB' not in subpop:
                    CHB=''
                    chead=''
                    ctitle=''

                if 'PEL' in subpop:

                    mycursor.execute("SELECT ID, SUBPOP, AF, ('ALT|REF'), ('REF|ALT'), ('ALT|ALT'), ('REF|REF') FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'Peru'", [snp])
                    PEL = mycursor.fetchall()

                    if len(PEL) == 0:

                        PEL = 'Peru not found.'
                        ptitle=''
                        phead=''

                    else:
                        phead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        ptitle='Peru'
                
                if 'PEL' not in subpop:
                    PEL=''
                    phead=''
                    ptitle=''

                if 'ESN' in subpop:

                    mycursor.execute("SELECT ID, SUBPOP, AF, ('ALT|REF'), ('REF|ALT'), ('ALT|ALT'), ('REF|REF') FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'Nigeria'", [snp])
                    ESN = mycursor.fetchall()

                    if len(ESN) == 0:

                        ESN = 'Nigeria not found.'
                        etitle=''
                        ehead=''

                    else:
                        ehead=('rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        etitle='Nigeria'

                if 'ESN' not in subpop:
                    ESN=''
                    ehead=''
                    etitle=''

                else:
                    pass

                


                return render_template('search.html', 
                                        data=data, 
                                        headings=headings, 
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
                                        SNPtitle=SNPtitle,
                                        btitle=btitle,
                                        gtitle=gtitle,
                                        ctitle=ctitle,
                                        ptitle=ptitle,
                                        etitle=etitle,
                                        df=df )
            
            # If searching by Gene name
            if select == 'Gene Name':

                gene = request.form['snp'].upper()

                mycursor.execute("SELECT ID FROM snp WHERE GENE LIKE %s ", [gene])
                snps = len(mycursor.fetchall())
                num_snps = ('Number of SNPs found in ' + gene.upper() + ': ' + (str(snps) + '.'))


                # SNP info table

                mycursor.execute("SELECT CHROM, POS, GENE, ID, REF, ALT FROM snp WHERE GENE LIKE %s ", [gene])
                data = mycursor.fetchall()

                if len(data) > 0:
                    headings=('Chromosome','Position', 'Gene','rsID','Reference','Alternate')
                    SNPtitle='SNP Information'

                if len(data) <= 0:
                    headings=''
                    SNPtitle=''
                    data=''


                if 'BEB' in subpop:

                    mycursor.execute("SELECT * FROM subpop WHERE SUBPOP LIKE 'Bengali' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                    BEB = mycursor.fetchall()

                    

                    if len(BEB) == 0:

                        BEB = 'Bengali not found.'
                        bhead=''
                        btitle=''
                    else:
                        bhead=('PK','rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        btitle='Bengali'

                if 'BEB' not in subpop:
                    BEB=''
                    bhead=''
                    btitle=''

                if 'GBR' in subpop:

                    mycursor.execute("SELECT * FROM subpop WHERE SUBPOP LIKE 'GBR' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                    GBR = mycursor.fetchall()

                    if len(GBR) == 0:
                        GBR = 'GBR not found.'
                        gtitle=''
                        ghead=''
                    else:
                        ghead=('PK','rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        gtitle='Great Britain'

                if 'GBR' not in subpop:
                    GBR=''
                    ghead=''
                    gtitle=''
                
                if 'CHB' in subpop:

                    mycursor.execute("SELECT * FROM subpop WHERE SUBPOP LIKE 'China' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                    CHB = mycursor.fetchall()


                    if len(CHB) == 0:

                        CHB = 'GBR not found.'
                        ctitle=''
                        chead=''

                    else:
                        chead=('PK','rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        ctitle='China'

                if 'CHB' not in subpop:
                    CHB=''
                    chead=''
                    ctitle=''

                if 'PEL' in subpop:

                    mycursor.execute("SELECT * FROM subpop WHERE SUBPOP LIKE 'Peru' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                    PEL = mycursor.fetchall()


                    if len(PEL) == 0:

                        PEL = 'GBR not found.'
                        ptitle=''
                        phead=''

                    else:
                        phead=('PK','rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        ptitle='Peru'
                
                if 'PEL' not in subpop:
                    PEL=''
                    phead=''
                    ptitle=''

                if 'ESN' in subpop:

                    mycursor.execute("SELECT * FROM subpop WHERE SUBPOP LIKE 'Nigeria' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                    ESN = mycursor.fetchall()

                    if len(ESN) == 0:

                        ESN = 'GBR not found.'
                        etitle=''
                        ehead=''

                    else:
                        ehead=('PK','rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        etitle='Nigeria'

                if 'ESN' not in subpop:
                    ESN=''
                    ehead=''
                    etitle=''

                else:
                    pass

                return render_template('search.html',
                                        data=data, 
                                        SNPtitle=SNPtitle, 
                                        headings=headings,
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
                                        df=df)

            # If searching by Location
            if select == 'Location':

                location = request.form['snp']
                location=location.split('-')
                areastart=int(location[0])
                areaend=int(location[1])

                mycursor.execute("SELECT ID FROM snp WHERE %s <= POS AND POS <= %s ", ([areastart], [areaend] ))
                snps = len(mycursor.fetchall())
                num_snps = ('Number of SNPs found in the range of ' + str(areastart) + ' - ' + str(areaend) + ': ' + (str(snps) + '.'))

                mycursor.execute("SELECT CHROM, POS, GENE, ID, REF, ALT FROM snp WHERE %s <= POS AND POS <= %s ", ([areastart], [areaend] ))
                data = mycursor.fetchall()

                if len(data) > 0:
                    headings=('Chromosome','Position', 'Gene','rsID','Reference','Alternate')
                    SNPtitle='SNP Information'

                if len(data) <= 0:
                    headings=''
                    SNPtitle=''
                    data=''



                if 'BEB' in subpop:

                    mycursor.execute("SELECT * FROM subpop WHERE SUBPOP LIKE 'Bengali' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", ([areastart], [areaend] ))
                    BEB = mycursor.fetchall()

                    if len(BEB) == 0:

                        BEB = 'Bengali not found.'
                        bhead=''
                        btitle=''
                    else:
                        bhead=('PK','rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        btitle='Bengali'

                if 'BEB' not in subpop:
                    BEB=''
                    bhead=''
                    btitle=''

                if 'GBR' in subpop:

                    mycursor.execute("SELECT * FROM subpop WHERE SUBPOP LIKE 'GBR' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", ([areastart], [areaend] ))
                    GBR = mycursor.fetchall()

                    if len(GBR) == 0:
                        GBR = 'GBR not found.'
                        gtitle=''
                        ghead=''
                    else:
                        ghead=('PK','rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        gtitle='Great Britain'

                if 'GBR' not in subpop:
                    GBR=''
                    ghead=''
                    gtitle=''
                
                if 'CHB' in subpop:

                    mycursor.execute("SELECT * FROM subpop WHERE SUBPOP LIKE 'China' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", ([areastart], [areaend] ))
                    CHB = mycursor.fetchall()

                    if len(CHB) == 0:

                        CHB = 'GBR not found.'
                        ctitle=''
                        chead=''

                    else:
                        chead=('PK','rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        ctitle='China'

                if 'CHB' not in subpop:
                    CHB=''
                    chead=''
                    ctitle=''

                if 'PEL' in subpop:

                    mycursor.execute("SELECT * FROM subpop WHERE SUBPOP LIKE 'Peru' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", ([areastart], [areaend] ))
                    PEL = mycursor.fetchall()


                    if len(PEL) == 0:

                        PEL = 'GBR not found.'
                        ptitle=''
                        phead=''

                    else:
                        phead=('PK','rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        ptitle='Peru'
                
                if 'PEL' not in subpop:
                    PEL=''
                    phead=''
                    ptitle=''

                if 'ESN' in subpop:

                    mycursor.execute("SELECT * FROM subpop WHERE SUBPOP LIKE 'Nigeria' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", ([areastart], [areaend] ))
                    ESN = mycursor.fetchall()

                    if len(ESN) == 0:

                        ESN = 'GBR not found.'
                        etitle=''
                        ehead=''

                    else:
                        ehead=('PK','rsID','Subpopulation','Allele Frequency','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF')
                        etitle='Nigeria'

                if 'ESN' not in subpop:
                    ESN=''
                    ehead=''
                    etitle=''

                else:
                    pass

                return render_template('search.html',
                                        data=data, 
                                        SNPtitle=SNPtitle, 
                                        headings=headings,
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
                                        num_snps=num_snps)

                





                




            # If search by not specified
            else:
                pass


        return render_template('search.html')






if __name__ == '__main__': # only if we run this file will we execute the line below
    # run the Flask app & start a web server
    app.run(debug=True) # debug means that if code changes server is auto re-run
