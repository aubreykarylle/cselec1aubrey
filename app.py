from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'  # Change to your password
app.config['MYSQL_DB'] = 'bookingdb'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bookings")
    bookings = cur.fetchall()
    cur.close()
    return render_template('index.html', bookings=bookings)

@app.route('/add_form')
def add_form():
    return render_template('add.html')

@app.route('/add', methods=['POST'])
def add():
    customer_name = request.form['customer_name']
    room_type = request.form['room_type']
    check_in_date = request.form['check_in_date']
    check_out_date = request.form['check_out_date']
    phone_number = request.form['phone_number']
    email = request.form['email']  # Capture email from the form

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO bookings (customer_name, room_type, check_in_date, check_out_date, phone_number, email) VALUES (%s, %s, %s, %s, %s, %s)", 
                (customer_name, room_type, check_in_date, check_out_date, phone_number, email))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        room_type = request.form['room_type']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        phone_number = request.form['phone_number']
        cur.execute("UPDATE bookings SET customer_name=%s, room_type=%s, check_in_date=%s, check_out_date=%s, phone_number=%s WHERE id=%s", 
                    (customer_name, room_type, check_in_date, check_out_date, phone_number, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    else:
        cur.execute("SELECT * FROM bookings WHERE id = %s", (id,))
        booking = cur.fetchone()
        cur.close()
        return render_template('edit.html', booking=booking)

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM bookings WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
