from flask import Flask, render_template, json, request, redirect, session, flash
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from pymysql.cursors import DictCursor
import os

mysql = MySQL()
application = Flask(__name__)
application.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
application.config['MYSQL_DATABASE_USER'] = os.environ['RDS_USERNAME']
application.config['MYSQL_DATABASE_PASSWORD'] = os.environ['RDS_PASSWORD']
application.config['MYSQL_DATABASE_DB'] = os.environ['RDS_DB_NAME']
application.config['MYSQL_DATABASE_HOST'] = os.environ['RDS_HOSTNAME']
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
    conn = mysql.connect()
    cursor = conn.cursor(cursor=DictCursor)
    cursor.execute("select p.property_id, p.property_city, p.property_street, p.property_status, p.property_owner_id "
                   "from tbl_property p where p.property_id = {0}".format(prop_id))
    prop_details = cursor.fetchall()
    cursor.execute("select o.owner_name, o.owner_surname from tbl_property_owner o "
                   "where o.owner_id = {0}".format(prop_details[0]['property_owner_id']))
    prop_owner = cursor.fetchall()
    cursor.execute("select l.locator_name, l.locator_surname from tbl_property_locator l "
                   "where property_id = {0}".format(prop_details[0]['property_id']))
    prop_locators = cursor.fetchall()
    print(prop_locators)
    return render_template('userHomePropertyDetail.html', prop_details=prop_details[0], prop_owner=prop_owner[0],
                           prop_locators=prop_locators)


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


@application.route('/propertyAction', methods=['POST'])
def propertyAction():
    conn = mysql.connect()
    try:
        checkbox_list = request.form.getlist('proplist')
        operation = request.form.getlist('operation')[0]

        if operation == 'delete':
            cursor = conn.cursor()
            for prop in checkbox_list:
                cursor.callproc('sp_deleteProperty', prop)

            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return redirect('/userHomeProperties')
            else:
                return json.dumps({'proc_error': str(data[0])})
        else:
            return json.dumps({"message": "operation \'{0}\' not supported!".format(operation)})
    except Exception as e:
        return json.dumps({'general_error': str(e)})


@application.context_processor
def utility_processor():
    def prepareStatusBody(status):
        if status == 0:
            return 'OK <span class="fa fa-check-circle" style="color:green"></span>'
        if status == 1:
            return 'ERR <span class="fa fa-exclamation-circle" style="color:red"></span>'
    return dict(prepareStatusBody=prepareStatusBody)

if __name__ == "__main__":
    application.debug = True
    application.run(port=5000)
