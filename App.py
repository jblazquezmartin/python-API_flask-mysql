from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)

#mysql connection
app.config['MYSQL_HOST'] = '192.168.1.x'   
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_BD'] = 'flaskcontacts'
mysql = MySQL(app)

# settings
app.secret_key='mysecretkey'

@app.route('/')
def Index():
    cur=mysql.connection.cursor()
    cur.execute("USE flaskcontacts")
    cur.execute('SELECT * FROM contacts')
    data=cur.fetchall()
    print(data)
    return render_template('index.html', contacts=data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("USE flaskcontacts")
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("USE flaskcontacts")
    cur.execute(f"SELECT * FROM contacts WHERE id={id}")
    data=cur.fetchall()
    return render_template('edit-contact.html', contact=data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method=='POST':
        fullname=request.form['fullname']
        phone=request.form['phone']
        email=request.form['email']
    cur=mysql.connection.cursor()
    cur.execute("USE flaskcontacts")
    cur.execute (f"UPDATE contacts SET fullname=%s,email=%s,phone=%s WHERE id=%s",
    (fullname, email, phone, id))
    mysql.connection.commit()
    flash('Contact Update Successfully')
    return redirect(url_for('Index'))


@app.route('/delete/<string:id>')
def delete_contact(id):
    cur=mysql.connection.cursor()
    cur.execute('USE flaskcontacts')
    cur.execute('DELETE FROM contacts WHERE ID = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Succesfull')
    return redirect (url_for('Index'))

if __name__== '__main__':
 app.run(port = 3000, debug = True)
