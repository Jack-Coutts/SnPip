# import the app factory (the app)
from Website import create_app

app = create_app()

if __name__ == '__main__': # only if we run this file will we execute the line below
    # run the Flask app & start a web server
    app.run(debug=True) # debug means that if code changes server is auto re-run
