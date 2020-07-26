from flask import Flask,render_template,request,redirect,session
import json

app = Flask(__name__)
app.secret_key = 'itsASecret'
logstat = False
stat = 0
output = {}

def outp(usr,pwd):
    status = 0
    msg = '' 
    if usr.isalpha(): 
        if len(pwd)<6:
            status=201
            msg = 'Faliure:Password should be of length 6'
        elif pwd.isalpha():
            status=202
            msg = 'Faliure:Password to have 1 Character and 1 number' 
        else:
            status=200
            msg = 'Success'
    else: 
        status = 203
        msg = 'Faliure:Only Character allowed in Username'
    global stat
    global output
    stat = status
    output = {'Status':status,'msg':msg}
    jsonOut = json.dumps(output,indent=2)
    with open('data.json','w') as out:
        out.write(jsonOut)
    print(jsonOut)
    return status,msg
     

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')  
        status,_ = outp(username,password)
        if status==200:
            global logstat
            logstat = True
            return redirect('/')
        else:
            out = output['msg']
            return render_template("login.html",out =out,status=False)
    return render_template("login.html")

@app.route('/')
def dashboard():
    status = logstat
    if status == True or status == False:
        return render_template("index.html",status=status,stat=stat)
    return render_template("index.html")

@app.route('/logout')
def logout():
    global logstat
    logstat = False
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)