# import the app factory (the app)
from Website import create_app
from flask import render_template, redirect, request, send_file, send_from_directory
from flaskext.mysql import MySQL
import datetime
import io
from io import BytesIO 
from io import StringIO


app = create_app()


# Database connection info. Note that this is not a secure connection.
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'chr22'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Initialises MySQL
mysql = MySQL()
mysql.init_app(app)

# Create a cursor to manipulate data in database
conn = mysql.connect()
cursor = conn.cursor()


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

            # If searching by snp name
            if select == 'SNP Name':

                snp = request.form['snp']
                # search by SNP
                cursor.execute("SELECT * from pop WHERE ID LIKE %s ", (snp))
                conn.commit()
                data = cursor.fetchall()
                if len(data) > 0:
                    headings=('SNP Name','Allele Frequency','EAF','AMR','AFR','AUR','SAS')
                else:
                    headings=''
                return render_template('search.html', data=data, headings=headings)
            
            # If searching by Gene name
            if select == 'Gene Name':
                pass


            # If searching by Location
            if select == 'Location':
                pass

            # If search by not specified
            else:
                pass


        return render_template('search.html')


#Still working on it 
@app.route('/download')
def download():


    basename = "SNP"
    suffix = datetime.datetime.now().strftime("%H%M%S")
    filename = "".join([basename, suffix]) 
    summaryFile = f'{filename}.txt'



    output = io.StringIO()
    writer = csv.writer(output)


    headings=('SNP Name','Allele Frequency','EAF','AMR','AFR','AUR','SAS')
    writer.writerow(headings)

    #for row in result:
        #writer.writerow(row)

    
    output.seek(0)


    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=new.txt"})
    cursor.close() 
    conn.close()





if __name__ == '__main__': # only if we run this file will we execute the line below
    # run the Flask app & start a web server
    app.run(debug=True) # debug means that if code changes server is auto re-run
