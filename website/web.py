from flask import Flask, render_template, url_for, request
import projectEmailGetter
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")
   

@app.route('/about')
def about():
   return render_template("about.html", title = "about")


@app.route('/submit',methods=["GET","POST"])
def submit():
    if request.method == "POST":
        formdata=request.form
        print(formdata['server'],formdata['password'],formdata['password'])
        emails=list(reversed(projectEmailGetter.getBriefFromEmails(projectEmailGetter.getEmailsIMAP(formdata['server'],
                                                                                      formdata['username'],
                                                                                      formdata['password'],
                                                                                      ssl=True))))
        return render_template("choose.html",emails=emails)
    return render_template("submit.html")


if __name__ == '__main__':
    app.run(debug=True)
