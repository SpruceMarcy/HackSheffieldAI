from flask import Flask, render_template, url_for, request, make_response
from cryptography.fernet import Fernet
import projectEmailGetter
import Python_Classifier as pyClass
app = Flask(__name__)
key = Fernet.generate_key()

def runFromEmail(email):
    with open("data.txt","w") as file:
        file.write(email)
    return pyClass.run("data.txt")
    

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
        start=0
        if 'start' in formdata:
            start=formdata['start']
        print(formdata['server'],formdata['username'],formdata['password'])
        emails=list(reversed(projectEmailGetter.getBriefFromEmails(projectEmailGetter.getEmailsIMAP(formdata['server'],
                                                                                      formdata['username'],
                                                                                      formdata['password'],
                                                                                      ssl=True,
                                                                                      start=start))))
        res=make_response(render_template("choose.html",emails=enumerate(emails),index=start))
        res.set_cookie("username",Fernet(key).encrypt(formdata['username'].encode()))
        res.set_cookie("password",Fernet(key).encrypt(formdata['password'].encode()))
        res.set_cookie("serverRL",Fernet(key).encrypt(formdata['server'].encode()))
        return res
    return render_template("submit.html")

@app.route('/check/<int:v>',methods=["GET","POST"])
def check(v):
    username=request.cookies.get('username')
    username=Fernet(key).decrypt(username.encode())
    password=request.cookies.get('password')
    password=Fernet(key).decrypt(password.encode())
    serverRL=request.cookies.get('serverRL')
    serverRL=Fernet(key).decrypt(serverRL.encode())
    rawemail=projectEmailGetter.getEmailsIMAP(serverRL.decode("utf-8"),
                                                                                      username.decode("utf-8"),
                                                                                      password.decode("utf-8"),
                                                                                      ssl=True,
                                                                                      start=v,
                                                                                      count=1)
    emails=projectEmailGetter.getPlainFromEmails(rawemail)
    emailbrief=list(reversed(projectEmailGetter.getBriefFromEmails(rawemail)))
    fraudulence=runFromEmail(projectEmailGetter.stripToText(projectEmailGetter.getPlainFromEmails(rawemail)[0]))[0]
    return render_template("show.html",content=emails[0],email=emailbrief[0],fraud=fraudulence)

@app.route('/upload',methods=["GET","POST"])
def upload():
    if request.method == "POST":
        #formdata=request.form
        #start=0
        #if 'start' in formdata:
        #    start=formdata['start']
        #print(formdata['server'],formdata['username'],formdata['password'])
        #emails=list(reversed(projectEmailGetter.getBriefFromEmails(projectEmailGetter.getEmailsIMAP(formdata['server'],
        #                                                                              formdata['username'],
        #                                                                              formdata['password'],
        #                                                                              ssl=True,
        #                                                                              start=start))))
        #res=make_response(render_template("choose.html",emails=enumerate(emails),index=start))
        #res.set_cookie("username",Fernet(key).encrypt(formdata['username'].encode()))
        #res.set_cookie("password",Fernet(key).encrypt(formdata['password'].encode()))
        #res.set_cookie("serverRL",Fernet(key).encrypt(formdata['server'].encode()))
        #return res
        f = request.files['file']
        readf=f.read()
        fraudulence=runFromEmail(projectEmailGetter.stripToText(projectEmailGetter.getPlainFromEmails([readf])[0]))[0]
        return render_template("show.html",content=projectEmailGetter.getPlainFromEmails([readf])[0],email=projectEmailGetter.getBriefFromEmails([readf])[0],fraud=fraudulence)
    return render_template("upload.html")

if __name__ == '__main__':
    app.run(debug=True)
