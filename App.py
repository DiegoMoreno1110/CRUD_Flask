from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MYSQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'M0reno#11'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_DB'] = 'flask_contacts'
mysql = MySQL(app)

# Session settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def addContact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        print(fullname, phone)

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone) VALUES(%s, %s)', (fullname, phone))

        mysql.connection.commit()

        flash('Contact added succesfully')

        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def getContact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('editContact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def updateContact(id):

    if request.method == 'POST':

        fullname = request.form['fullname']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute('UPDATE contacts SET fullname = %s, phone = %s WHERE id = %s', (fullname, phone ,id))
        data = mysql.connection.commit()

        flash('Contact updated succesfully')

        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def deleteContact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = %s', (id))
    mysql.connection.commit()

    flash('Contact Removed Succesfully')

    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 8000, debug = True)