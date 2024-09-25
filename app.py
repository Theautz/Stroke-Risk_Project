from flask import Flask, render_template, request ,redirect,url_for,flash,session
import joblib
import os
import  numpy as np
import pickle
from flask_mysqldb import MySQL
import bcrypt , re


app= Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='stroke_db'
app.secret_key='your_secret_key_here'
mysql=MySQL(app)


@app.route("/")
def index():
    if 'user_id' in session:
         session.pop('user_id',None)
        # flash('Your have been logged out successfully')
    return render_template("index.html")

@app.route('/login',methods=['GET','POST'])
def login():
      if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
        
            cursor=mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email=%s ",(email,))
            user=cursor.fetchone()
            cursor.close()

            if user and bcrypt.checkpw(password.encode('utf-8'),user[3].encode('utf-8')):
                    session['user_id']=user[0]
                    return redirect(url_for('form'))
            else:
                return render_template('login.html', error='Invalid username or password')
        
      return render_template('login.html')



@app.route('/register',methods=['GET','POST'])
def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if len(password)<8:
                 flash("รหัสผ่านขั้นต่ำ 8 ตัวอักษร")
                 return redirect(url_for('register'))  
            
            elif not re.search(r'[A-Z]',password):
                 flash("รหัสผ่านต้องมีตัวพิมพ์ใหญ่(A-Z)อย่างน้อยหนึ่งตัวอักษร")
                 return redirect(url_for('register')) 
                 
            elif not re.search(r'[a-z]',password):
                 flash("รหัสผ่านต้องมีตัวพิมพ์เล็ก(a-z)อย่างน้อยหนึ่งตัวอักษร")
                 return redirect(url_for('register'))
            
            elif not re.search(r'[@$!%*?&]',password):
                 flash("รหัสผ่านต้องมีอักขระพิเศษ(@,$,!,%,*,?,&)อย่างน้อยหนึ่งตัวอักษร")
                 return redirect(url_for('register'))
            
            elif password!=confirm_password:
                 flash("รหัสผ่านไม่ตรงกัน")
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
            cursor=mysql.connection.cursor()
            cursor.execute("INSERT INTO users (username,email,password) VALUES(%s,%s,%s)",(username,email,hash_password,))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('login'))
        return render_template('register.html')


@app.route("/form",methods=['GET','POST'])
def form():
    if 'user_id' in session:
        #   user_id = session['user_id']
        
        #   cursor=mysql.connection.cursor()
        #   cursor.execute("SELECT * FROM users where id=%s",(user_id,))
        #   user=cursor.fetchone()
        #   cursor.close()

        #   if user:
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
    residence_type = int(request.form['Residence_type'])
    avg_glucose = float(request.form['avg_glucose_level'])
    bmi = float(request.form['bmi'])
    smoking_status = int(request.form['smoking_status'])

    x=np.array([gender,age,hypertension,heart_disease,ever_married,work_type,residence_type,
                    avg_glucose,bmi,smoking_status]).reshape(1,-1)
        
        
    model_path=os.path.join(r"C:\Users\Warit\OneDrive\Desktop\Stroke Risk_Project\model\model_stroke.pkl")
    dt=joblib.load(model_path)

    Y_pred=dt.predict(x)

    # cursor=mysql.connection.cursor()
    # cursor.execute("INSERT INTO prediction_results (gender,age,hypertension,heart_disease,ever_married,work_type,residence_type,avg_glucose,bmi,smoking_status,stroke) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #                ,(gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose, bmi, smoking_status, Y_pred[0]))
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

