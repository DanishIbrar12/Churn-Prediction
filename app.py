import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_mail import Mail, Message
from random import randint
import re
import smtplib

app = Flask(__name__)
mail = Mail(app)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'fypproject292@gmail.com'
app.config['MAIL_PASSWORD'] = 'odohnefuoczrcbzx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
otp = randint(000000, 999999)

app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'database'

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = % s AND password = % s And status = %s', (username, password, 1))
        account = cursor.fetchone()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT status FROM admin WHERE username = % s', (username,))
        stat = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('main.html', msg=msg)

        elif stat == 0:
            msg = 'Account is not active yet!'
            return render_template('login.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/recover', methods=['GET', 'POST'])
def recover():
    msg = ''
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE email = % s ', (email,))
        account = cursor.fetchone()
        if account:
            msg = Message(subject='OTP', sender='fypproject292@gmail.com', recipients=[email])
            msg.body = str(otp)
            mail.send(msg)
            mesg = 'Enter the Recovery OTP'
            return render_template('recovery.html', msg=mesg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not email:
            msg = 'Please fill out the form !'
        else:
            msg = 'Account does not exists !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('recover.html', msg=msg)


@app.route('/OtpVerify', methods=['GET', 'POST'])
def OtpVerify():
    if request.method == 'POST' and 'OTP' in request.form and 'NewPassword' in request.form and 'NewPassword1' in request.form and 'username' in request.form:
        user_otp = request.form['OTP']
        user = request.form['username']
        pswd = request.form['NewPassword']
        conpass = request.form['NewPassword1']
        if otp == int(user_otp):
            if pswd == conpass:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM admin WHERE username = % s ', (user,))
                account = cursor.fetchone()
                if account:
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    sql = "UPDATE admin SET password = %s WHERE username = %s"
                    data = (pswd, user)
                    cursor.execute(sql, data)
                    mysql.connection.commit()
                    mesg = 'Password Updated Successfully'
                    return render_template('login.html', msg=mesg)
                else:
                    mesg = 'Incorrect username '
                    return render_template('recovery.html', msg=mesg)
            else:
                mesg1 = 'Password Does not Match'
                return render_template('recovery.html', msg=mesg1)
        else:
            msg = 'OTP not Correct 2'
            return render_template('recovery.html', msg=msg)
    elif request.method == 'POST':
        mesg2 = 'Please fill out the form'
        return render_template('recovery.html', msg=mesg2)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        stat = 1
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = % s AND status = % s', (username, stat))
        account = cursor.fetchone()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT status FROM admin WHERE username = % s', (username,))
        stat = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
            return render_template('register.html', msg=msg)
        elif stat == 0:
            status = 0
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('DELETE  admin WHERE username = % s', (username,))
            mysql.connection.commit()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO admin VALUES (% s, % s, % s, % s, % s)', ('', username, email, password, status))
            mysql.connection.commit()
            msg = Message(subject='OTP', sender='fypproject292@gmail.com', recipients=[email])
            msg.body = str(otp)
            mail.send(msg)
            mesg = 'Enter the verification Code'
            return render_template('verify.html', msg=mesg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            status = 0
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO admin VALUES (% s, % s, % s, % s, % s)', ('', username, email, password, status))
            mysql.connection.commit()
            msgg = Message(subject='OTP', sender='fypproject292@gmail.com', recipients=[email])
            msgg.body = str(otp)
            mail.send(msgg)
            mesg ='_Enter the verification Code'
            return render_template('verify.html', msg=mesg)

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route('/validate', methods=['GET', 'POST'])
def validate():
    user_otp = request.form['OTP']
    if otp == int(user_otp):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "SELECT * FROM admin ORDER BY id DESC LIMIT 1"
        cursor.execute(sql)
        account = cursor.fetchone()
        stat = 1
        uname = account['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "UPDATE admin SET status = %s WHERE username = %s"
        data = (stat, uname)
        cursor.execute(sql, data)
        mysql.connection.commit()
        msg = 'You have successfully registered'
        return render_template('login.html', msg=msg)
    else:
        msg = 'Please Try Again'
        return render_template('verify.html', msg=msg)


@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    return render_template("main.html")


@app.route('/main_handler', methods=['GET', 'POST'])
def main_handler():
    if request.method == 'POST':
        if request.form.get("analysis_btn"):
            return render_template("analysis.html")
        elif request.form.get("prediction_btn"):
            return render_template("prediction.html")
        elif request.form.get("dataset_btn"):
            import pandas as pd

            # to read csv file named "samplee"
            a = pd.read_csv("Telco-Customer-Churn.csv")

            # to save as html file
            # named as "Table"
            a.to_html("dataset.html")

            # assign it to a
            # variable (string)
            html_file = a.to_html()
            return html_file
    elif request.method == 'GET':
        return render_template('main.html')


@app.route('/prediction', methods=['GET', 'POST'])
def prediction_handler():
    # ls = [1, 1, 1, 1, 20, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 103, 1]
    list1 = []
    a = request.form['num1']
    list1.append(int(a))
    b = request.form['num2']
    list1.append(int(b))
    c = request.form['num3']
    list1.append(int(c))
    d = request.form['num4']
    list1.append(int(d))
    e = request.form['num5']
    list1.append(int(e))
    f = request.form['num6']
    list1.append(int(f))
    g = request.form['num7']
    list1.append(int(g))
    h = request.form['num8']
    list1.append(int(h))
    i = request.form['num9']
    list1.append(int(i))
    j = request.form['num10']
    list1.append(int(j))
    k = request.form['num11']
    list1.append(int(k))
    l = request.form['num12']
    list1.append(int(l))
    m = request.form['num13']
    list1.append(int(m))
    n = request.form['num14']
    list1.append(int(n))

    o = request.form['num15']
    list1.append(int(o))
    p = request.form['num16']
    list1.append(int(p))
    q = request.form['num17']
    list1.append(int(q))
    r = request.form['num18']
    list1.append(int(r))

    s = request.form['num19']
    list1.append(int(s))

    # print(list1)

    # print(type(list1))
    import model_with_total_charges as md
    res = md.pred(list1)
    print(res)
    user_pred = None
    if res != 0:
        user_pred = "User May Leave"
    else:
        user_pred = "User May Not Leave"
    # processed_text = text
    # print(processed_text)
    return render_template("prediction.html", user_pred=user_pred)


@app.route('/demographic_feats', methods=['GET'])
def demographic_feature_graph():
    plot = 'static/demographic_feats.png'
    # return send_file(file,attachment_filename='accnt_categ_feats_churn.png',
    #                  mimetype='image/png')
    return render_template("analysis.html", plot=plot)


@app.route('/demographic_feats_churn', methods=['GET'])
def demographic_feature_churn():
    plot = 'static/demographic_feats_churn.png'
    # return send_file(file,attachment_filename='accnt_categ_feats_churn.png',
    #                  mimetype='image/png')
    return render_template("analysis.html", plot=plot)


@app.route('/service_feats', methods=['GET'])
def service_feature_graph():
    plot = 'static/service_feats_distro.png'
    # return send_file(file,attachment_filename='accnt_categ_feats_churn.png',
    #                  mimetype='image/png')
    return render_template("analysis.html", plot=plot)


@app.route('/service_feats_churn', methods=['GET'])
def service_feature_churn():
    plot = 'static/sevice_feats_churn.png'
    # return send_file(file,attachment_filename='accnt_categ_feats_churn.png',
    #                  mimetype='image/png')
    return render_template("analysis.html", plot=plot)


@app.route('/account_categ_feats', methods=['GET'])
def account_categ_feats():
    plot = 'static/accnt_categ_feats_distro.png'
    # return send_file(file,attachment_filename='accnt_categ_feats_churn.png',
    #                  mimetype='image/png')
    return render_template("analysis.html", plot=plot)


@app.route('/account_feats_churn', methods=['GET'])
def account_feature_churn():
    plot = 'static/accnt_categ_feats_churn.png'
    # return send_file(file,attachment_filename='accnt_categ_feats_churn.png',
    #                  mimetype='image/png')
    return render_template("analysis.html", plot=plot)


@app.route('/num_feats', methods=['GET'])
def num_feature_churn():
    plot = 'static/num_accnt_churn.png'
    # return send_file(file,attachment_filename='accnt_categ_feats_churn.png',
    #                  mimetype='image/png')
    return render_template("analysis.html", plot=plot)


# demographic_feats()
# demographic_feats_churn()
# service_feats()
# service_feats_churn()
# accnt_categ_feats()
# accnt_categ_feats_churn()
# num_accnt_churn()

if __name__ == '__main__':
    app.run(debug=True)
