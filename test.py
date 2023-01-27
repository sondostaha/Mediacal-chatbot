1-
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'GET' and 'email' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        session.pop('visitor', None)
        if form.validate_on_submit():
            con = sqlite3.connect("mydatabase.db")
            cur = con.cursor()
            query_string = """SELECT * FROM user WHERE email=? AND password=?"""
            cur.execute(query_string, (form.email.data,form.password.data,))
            users = cur.fetchall()
            con.close()
            if len(users) > 0:
                session['email'] = form.email.data
                session['firstname'] = users[0][1]
                session['lastname'] = users[0][2]
                session['sex'] = users[0][5]
                session['age'] = users[0][6]
                session['accType'] = users[0][7]
                flash(f'Welcome back {users[0][1]}!','success')
                return redirect(url_for('home'))
            else :
                flash(f'Login Faild!','danger')
    return render_template('login.html', form=form)


@app.route('/edit-profile', methods=['POST', 'GET'])
def edit_profile():
    form = RegistrationForm()
    if request.method == 'GET' and 'email' in session:
        con = sqlite3.connect("mydatabase.db")
        cur = con.cursor()
        query_string = """SELECT * FROM user WHERE email =?"""
        cur.execute(query_string, (session['email'],))
        user = cur.fetchall()
        con.close()
        return render_template('edit-profile.html', form=form, uFirstname=user[0][1], uLastname=user[0][2],
                               uEmail=user[0][3], uSex=user[0][5], uAge=user[0][6], uAccType=user[0][7])
    if request.method == 'POST':
        con = sqlite3.connect("mydatabase.db")
        cur = con.cursor()
        query_string = """UPDATE user SET firstName=?,lastName=?,age=?,password=? WHERE email=?"""
        cur.execute(query_string, (
        request.form['firstName'], request.form['lastName'], request.form['age'], request.form['password'],
        session['email']))
        con.commit()
        flash(f'Account updated!', 'success')
        return redirect(url_for('home'))

    return redirect(url_for('home'))

def getAllSyms(disease):
    con = sqlite3.connect("mydatabase.db")
    cur = con.cursor()
    query_string = """SELECT symptom FROM symptoms WHERE disease=?"""
    cur.execute(query_string, (disease,))
    symptoms = cur.fetchall()
    cur.close()
    result = []
    if len(symptoms) > 0:
        for s in symptoms:
            result.append(s[0])
        return result
    return []