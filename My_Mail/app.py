from flask import Flask, request, render_template, redirect, url_for, session, flash, send_file
from db_opr import insert_user, get_password, check_email, send_mail, get_inbox, get_sent, view_mail, \
    get_name, delete_mail_i, delete_mail_s, s_con_i, s_con_s, s_id, get_details, del_acc
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import random
import pytz

app = Flask(__name__)
app.secret_key = "123@abc"
change = False
upload_folder = "uploads"
app.config['UPLOAD_FOLDER'] = upload_folder


def set_session(email, name):
    session["logged_in"] = True
    session["email"] = email
    session["name"] = name


def reset_session():
    if "logged_in" in session:
        del session["logged_in"]
        del session["email"]
        del session["name"]


def verify_login(email, password):
    stored_password = get_password(email)
    name = get_name(email)
    if len(stored_password):
        if password == stored_password[0][0]:
            set_session(email, name[0][0])
            return redirect("/")
        else:
            flash("Wrong Password")
            return redirect("/login")
    else:
        flash("No Email Found")
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["pwd"]
        verify_login(email, password)
        return redirect(url_for("index"))


@app.route('/register', methods=["GET", "POST"])
def register():
    global change
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["pwd"]
        gender = request.form["Gender"]
        dob = request.form["DOB"]
        col = request.form["college"]
        validate = check_email(email)
        if not len(validate):
            insert_user(email, name, password, gender, dob, col)
            return redirect("/")
        else:
            flash("Email Already Exists")
            return render_template('reg.html')

    elif request.method == "GET":
        if not change:
            change = True
            return render_template('reg.html')
        else:
            change = False
            return redirect(url_for('login'))


@app.route("/compose", methods=["POST", "GET"])
def compose():
    if request.method == "POST":
        rec = request.form["recv"]
        sub = request.form["subj"]
        con = request.form["cont"]
        validate = check_email(rec)
        if len(validate):
            if rec != session["email"]:
                try:
                    f = request.files['file']
                    org = f.filename
                    name = f.filename
                    val = name.split(".")
                    a = str(random.randrange(1000, 5000))
                    name = a + "_" + val[0] + "." + val[1]
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(name)))
                except IndexError:
                    org = "None"
                    name = "None"
                IST = pytz.timezone('Asia/Kolkata')
                now = datetime.now(IST)
                time = now.strftime("%H:%M")

                send_mail(session["email"], rec, sub, con, time, org, name)
                return redirect("/")
            else:
                return redirect("/")
        else:
            return redirect("/")
    else:
        return render_template("compose.html", email=session["email"], name=session["name"], con="", sub="")


@app.route("/inbox", methods=["GET", "POST"])
def inbox():
    if request.method == "GET":
        sen, sub, time, no = get_inbox(session["email"])
        length = len(sen)
        return render_template("inbox.html", email=session["email"], sen=sen, sub=sub, time=time, length=length, name=session["name"], no=no)
    else:
        if request.form['btn'] == 'View':
            text = request.form["text"]
            con, org, als, sub, sen, _ = view_mail(int(text))
            if org[0][0] == "None":
                return render_template('view.html', rev=session["email"], sen=sen[0][0], sub=sub[0][0], con=con[0],
                                       name=session["name"], inbox=True, att=False)
            else:
                return render_template('view.html', rev=session["email"], sen=sen[0][0], sub=sub[0][0], con=con[0],
                                       name=session["name"], inbox=True, att=True, org=org[0][0], als=als[0][0])
        elif request.form['btn'] == 'Delete':
            text = request.form["text"]
            delete_mail_i(int(text))
            sen, sub, time, no = get_inbox(session["email"])
            length = len(sen)
            return render_template("inbox.html", email=session["email"], sen=sen, sub=sub, time=time, length=length,
                                   name=session["name"], no=no)

        else:
            key = request.form["key"]
            if key != "":
                if request.form['opt'] == "1":
                    time, sen, sub, no = s_con_i(key, session["email"])
                elif request.form['opt'] == "2":
                    time, sen, sub, _, no = s_id(key)
                else:
                    sen, sub, time, no = get_inbox(session["email"])
                length = len(sen)
                return render_template("inbox.html", email=session["email"], sen=sen, sub=sub, time=time, length=length,
                                   name=session["name"], no=no)
            else:
                return redirect("/inbox")


@app.route("/sent", methods=["GET", "POST"])
def sent():
    if request.method == "GET":
        rev, sub, time, no = get_sent(session["email"])
        length = len(rev)
        return render_template("sent.html", email=session["email"], rev=rev, sub=sub, time=time, length=length, name=session["name"], no=no)
    else:
        if request.form['btn'] == 'View':
            text = request.form["text"]
            con, org, als, sub, _, rev = view_mail(int(text))
            if org[0][0] == "None":
                return render_template('view.html', sen=session["email"], rev=rev[0][0], sub=sub[0][0], con=con[0], name=session["name"], inbox=False, att=False)
            else:
                return render_template('view.html', sen=session["email"], rev=rev[0][0], sub=sub[0][0], con=con[0], name=session["name"], inbox=False, att=True, org=org[0][0], als=als[0][0])

        elif request.form['btn'] == 'Delete':
            text = request.form["text"]
            delete_mail_s(int(text))
            rev, sub, time, no = get_sent(session["email"])
            length = len(rev)
            return render_template("sent.html", email=session["email"], rev=rev, sub=sub, time=time, length=length, name=session["name"], no=no)

        else:
            key = request.form["key"]
            if key != "":
                if request.form['opt'] == "1":
                    time, sub, rev, no = s_con_s(key, session["email"])
                elif request.form['opt'] == "2":
                    time, _, sub, rev, no = s_id(key)
                else:
                    rev, sub, time, no = get_sent(session["email"])
                length = len(rev)
                return render_template("sent.html", email=session["email"], rev=rev, sub=sub, time=time, length=length,
                                   name=session["name"], no=no)
            else:
                return redirect("/sent")


@app.route("/view", methods=["GET", "POST"])
def view():
    if request.form['btn'] == 'Forward':
        text = request.form["text"]
        text = text.split("/")
        forward = " ---Forwarded Message---\n From: " + text[2] + "\n Sub: " + text[0] + "\n To: " + text[3] + "\n ----\n\n"

        return render_template("compose.html", email=session["email"], name=session["name"], con=text[1], sub=text[0],
                               val=forward)
    else:
        text = request.form["text"]
        text = text.split("/")
        reply = " " + text[2] + " wrote: \n"
        cls = "\n ----\n\n"
        return render_template("compose.html", email=session["email"], name=session["name"], con=text[1], sub=text[0],
                               val=reply, rev=text[3], cls=cls)


@app.route("/download", methods=["POST"])
def download():
    text = request.form["att_val"]
    return send_file("uploads/" + text, as_attachment=True)


@app.route("/logout")
def logout():
    reset_session()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    print("aaaaa")
    del_acc(session["email"])
    reset_session()
    return redirect(url_for('login'))


@app.route("/")
def index():
    if "logged_in" in session:
        gen, dob, col = get_details(session["email"])
        return render_template('email.html', email=session["email"], name=session["name"], Gender=gen, DOB=dob, college=col)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
