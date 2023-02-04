# importing Flask and other modules
from flask import Flask, request, render_template

app = Flask(__name__)  #flask constructor

# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])

def Run_Simulation():  # process functions
    
    return render_template("index1.html")

if __name__=='__main__':
    app.run()