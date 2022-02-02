
# library.py
from ftplib import error_proto
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
from pymysql import NULL


app = Flask(__name__)

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

#endpoint for search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        select=request.form['select']

        # If searching by snp name
        if select == 'SNP Name':

            snp = request.form['snp']
            # search by author or book
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



if __name__ == '__main__':
    app.debug = True
    app.run()