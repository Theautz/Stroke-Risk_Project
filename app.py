from flask import Flask, render_template, request ,redirect,url_for,flash,session
import joblib
import os
import  numpy as np
import pickle
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email
import bcrypt , re


app= Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='mydatabase'
app.secret_key='your_secret_key_here'


mysql=MySQL(app)

class RegisterForm(FlaskForm):
      name = StringField("Name:",validators=[DataRequired()])
      email = StringField("Email:",validators=[DataRequired(),Email()])
      password = PasswordField("Password:",validators=[DataRequired()])
      confirmpassword = PasswordField("Confirm Password:",validators=[DataRequired()])
      submit=SubmitField("Create Now")

class LoginForm(FlaskForm):
      email = StringField("Email:",validators=[DataRequired(),Email()])
      password = PasswordField("Password:",validators=[DataRequired()])
      submit=SubmitField("Sing in")


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login',methods=['GET','POST'])
def login():
      form = LoginForm()
      if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            cursor=mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email=%s ",(email,))
            user=cursor.fetchone()
            cursor.close()
            if user and bcrypt.checkpw(password.encode('utf-8'),user[3].encode('utf-8')):
                  session['user_id']=user[0]
                  return redirect(url_for('form'))
            else:
                  flash("Login failed. Please check your email and password")
                  return redirect(url_for('login'))
      
      return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
        form = RegisterForm()
        if form.validate_on_submit():
             name=form.name.data
             email=form.email.data
             password=form.password.data
             confirmpassword=form.confirmpassword.data
             

             if len(password)<8:
                 flash("The password must be least 8 characters")
                 return redirect(url_for('register'))  
                #  return render_template("register.html")

             elif password!=confirmpassword:
                 flash("Passwords don't match")
                 return redirect(url_for('register'))
            
             elif not re.search(r'[A-Z]',password):
                 flash("Password must contain at least one uppercase character")
                 return redirect(url_for('register')) 
             
             elif not re.search(r'[a-z]',password):
                 flash("Password must contain at least one lowercase character")
                 return redirect(url_for('register'))
             
             elif not re.search(r'[@$!%*?&]',password):
                 flash("Password must contain at least one special character")
                 return redirect(url_for('register'))
             

             cursor=mysql.connection.cursor()
             cursor.execute("SELECT * FROM users WHERE email=%s ",(email,))
             user=cursor.fetchone()
             cursor.close()
             if user:
                    if user[2] == email:
                     flash("Email Already Exists!")
                     return redirect(url_for('register'))
             
             hash_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
             # store data into database
            #  cursor=mysql.connection.cursor()
             cursor.execute("INSERT INTO users (name,email,password) VALUES(%s,%s,%s)",(name,email,hash_password))
             mysql.connection.commit()
             cursor.close()
                
             return redirect(url_for('login'))
        return render_template('register.html',form=form)





@app.route("/dashboard")
def dashboard():
     if 'user_id' in session:
          user_id = session['user_id']
          
          cursor=mysql.connection.cursor()
          cursor.execute("SELECT * FROM users where id=%s",(user_id,))
          user=cursor.fetchone()
          cursor.close()

          if user:
            return render_template('dashboard.html',user=user)
          
     return redirect('login')

@app.route("/logout")
def logout():
     session.pop('uer_id',None)
     flash('Your have been logged out successfully')
     return redirect(url_for('login'))

@app.route("/form",methods=['GET','POST'])
def form():
    if 'user_id' in session:
          user_id = session['user_id']

          cursor=mysql.connection.cursor()
          cursor.execute("SELECT * FROM users where id=%s",(user_id,))
          user=cursor.fetchone()
          cursor.close()

          if user:
            return render_template('form.html')
    return redirect('login')

@app.route("/result",methods=['POST','GET'])
def result():
    gender=int(request.form['gender'])
    age=int(request.form['age'])
    hypertension=int(request.form['hypertension'])
    heart_disease = int(request.form['heart_disease'])
    ever_married = int(request.form['ever_married'])
    work_type = int(request.form['work_type'])
    Residence_type = int(request.form['Residence_type'])
    avg_glucose_level = float(request.form['avg_glucose_level'])
    bmi = float(request.form['bmi'])
    smoking_status = int(request.form['smoking_status'])

    x=np.array([gender,age,hypertension,heart_disease,ever_married,work_type,Residence_type,
                    avg_glucose_level,bmi,smoking_status]).reshape(1,-1)
        

        #scaler_path=pickle.load(open('scaler.pkl','rb'))

        #scaler_path=os.path.join('D:/Python37/Projects/Stroke Prediction','models/scaler.pkl')
    scaler_path=os.path.join(r"C:\Users\Warit\OneDrive\Desktop\Stroke Risk_Project\model\scaler.pkl")
    scaler=None
        #scaler=pickle.load(open('scaler.pkl','rb'))
        #scaler=joblib.load('scaler.pkl')
    with open(scaler_path,'rb') as scaler_file:
        scaler=pickle.load(scaler_file)

    # x=scaler.transform(x)

        #model_path=os.path.join('D:/Python37/Projects/Stroke Prediction','models/dt.sav')
    model_path=os.path.join(r"C:\Users\Warit\OneDrive\Desktop\Stroke Risk_Project\model\model_stroke.pkl")
        #dt=pickle.load(open('trained_model_stroke.sav','rb'))
        #dt = joblib.load('dt.sav')
    dt=joblib.load(model_path)

    Y_pred=dt.predict(x)

    # cursor=mysql.connection.cursor()
    # cursor.execute("INSERT INTO data (gender,age,hypertension,heart_disease,ever_married,work_type,Residence_type,avg_glucose_level,bmi,smoking_status,result) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #                ,(gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status, Y_pred[0]))
    # mysql.connection.commit()
    # cursor.close()

        # for No Stroke Risk
    if Y_pred[0]==0:
        #return send_from_directory(os.getcwd(), 'nostroke.html')
        return render_template('result-good.html')
    else:
        #return send_from_directory(os.getcwd(), 'stroke.html')
        return render_template('result-bad.html')
    

@app.route("/contact",methods=['POST','GET'])
def contact():
     return render_template('contact.html')

if __name__=="__main__":
    app.run(debug=True)

