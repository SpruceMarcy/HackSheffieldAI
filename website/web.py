from flask import Flask, render_template, url_for
import projectEmailGetter
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")
   

@app.route('/about')
def about():
   return render_template("about.html", title = "about")


@app.route('/submit')
def submit():
    if request.method == "POST":
        return "HEllo PWORWFL"
    return render_template("submit.html")



if __name__ == '__main__':
    app.run(debug=True)
