from flask import Flask, render_template, json, request, redirect, session
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from pymysql.cursors import DictCursor

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'samsung234'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('showSignUp.html')


@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('signin.html')


@app.route('/userHome')
def userHome():
    conn = mysql.connect()
    if session.get('user'):
        cursor = conn.cursor(cursor=DictCursor)
        cursor.execute("select "
                       "pown.owner_name, pown.owner_surname, p.property_city, p.property_street, p.property_status "
                       "from tbl_property p join tbl_property_owner pown on p.property_owner_id = pown.owner_id")
        baselist = cursor.fetchall()
        return render_template('userHome.html', baselist=baselist)
    else:
        return render_template('error.html', error='Musisz sie zalogować')

@app.route('/adminHome')
def adminHome():
    conn = mysql.connect()
    cursor = conn.cursor(cursor=DictCursor)
    cursor.execute("select "
                   "user_id, user_name, user_username "
                   "from tbl_user")
    baselist = cursor.fetchall()
    return render_template('adminHome.html', baselist=baselist)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _username = request.form['inputUser']
        _password = request.form['inputPassword']

        if _username == 'admin':
            return redirect('/adminHome')
        else:
            cursor.callproc('sp_validateLogin', (_username,))
            data = cursor.fetchall()

            if len(data) > 0:
                if check_password_hash(str(data[0][3]), _password):
                    session['user'] = data[0][0]
                    return redirect('/userHome')
                else:
                    return render_template('error.html', error='Zły adres email lub hasło')
            else:
                return render_template('error.html', error='Zły adres email lub hasło')


    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    conn = mysql.connect()
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(port=5002)
