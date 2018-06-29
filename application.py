from flask import Flask, render_template, json, request, redirect, session, flash
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from pymysql.cursors import DictCursor

mysql = MySQL()
application = Flask(__name__)
application.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
application.config['MYSQL_DATABASE_USER'] = 'student'
application.config['MYSQL_DATABASE_PASSWORD'] = 'student'
application.config['MYSQL_DATABASE_DB'] = 'BucketList'
application.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(application)


@application.route('/')
def main():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('index.html')


@application.route('/showSignUp')
def showSignUp():
    return render_template('showSignUp.html')


@application.route('/showSignin')
def showSignin():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('signin.html')


@application.route('/userHome')
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


@application.route('/userHomeProperties')
def userHomeProperties():
    conn = mysql.connect()
    if session.get('user'):
        cursor = conn.cursor(cursor=DictCursor)
        cursor.execute("select p.property_id, "
                       "p.property_city, p.property_street, p.property_status "
                       "from tbl_property p")
        baselist = cursor.fetchall()
        return render_template('userHomeProperties.html', baselist=baselist)
    else:
        return render_template('error.html', error='Musisz sie zalogować')


@application.route('/userHomePropertyDetail', methods=['GET'])
def userHomePropertyDetail():
    prop_id = request.args['prop_id']
    return render_template('userHomePropertyDetail.html', prop_id=prop_id)


@application.route('/userHomeTenants')
def userHomeTenants():
    conn = mysql.connect()
    if session.get('user'):
        cursor = conn.cursor(cursor=DictCursor)
        cursor.execute("select l.locator_name, "
                       "l.locator_surname, l.locator_gender, p.property_street, p.property_id "
                       "from tbl_property p, tbl_property_locator l where l.property_id = p.property_id")
        baselist = cursor.fetchall()
        return render_template('userHomeTenents.html', baselist=baselist)
    else:
        return render_template('error.html', error='Musisz sie zalogować')


@application.route('/userHomeOwners')
def userHomeOwners():
    conn = mysql.connect()
    if session.get('user'):
        cursor = conn.cursor(cursor=DictCursor)
        cursor.execute("select o.owner_name, "
                       "o.owner_surname, o.owner_gender, p.property_street, p.property_id "
                       "from tbl_property p, tbl_property_owner o where o.owner_id = p.property_owner_id")
        baselist = cursor.fetchall()
        return render_template('userHomeOwners.html', baselist=baselist)
    else:
        return render_template('error.html', error='Musisz sie zalogować')


@application.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@application.route('/validateLogin', methods=['POST'])
def validateLogin():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _username = request.form['inputUser']
        _password = request.form['inputPassword']

        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                flash("Zły login lub hasło")
                return redirect('/')
        else:
            flash("Zły login lub hasło")
            return redirect('/')

    except Exception as e:
        flash(str(e))
        return redirect('/')
    finally:
        cursor.close()
        conn.close()


@application.route('/signUp', methods=['POST'])
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
    application.debug = True
    application.run(port=5000)
