import sqlite3


def get_details(email):
    sql1 = """
    SELECT gender FROM User WHERE email='%s'""" %email
    sql2 = """
        SELECT dob FROM User WHERE email='%s'""" % email
    sql3 = """
        SELECT college FROM User WHERE email='%s'""" % email
    gender = execute_query(sql1).fetchall()
    dob = execute_query(sql2).fetchall()
    col = execute_query(sql3).fetchall()
    return gender[0][0], dob[0][0], col[0][0]


def insert_user(email, name, password, gen, dob, col):
    sql = """
    INSERT INTO User(email, name,password, gender, dob, college) VALUES('%s', '%s', '%s', '%s', '%s', '%s')""" % (email, name, password, gen, dob, col)
    execute_query(sql)


def get_password(email):
    sql_query = """
    SELECT password FROM User WHERE email='%s'""" % email
    password = execute_query(sql_query).fetchall()
    return password


def get_name(email):
    sql_query = """
        SELECT name FROM User WHERE email='%s'""" % email
    name = execute_query(sql_query).fetchall()
    return name


def get_inbox(email):
    sql1 = """
    SELECT sender FROM Mail WHERE receiver ='%s' AND del_r = %s """ % (email, 1)
    sql2 = """
    SELECT subject FROM Mail WHERE receiver ='%s' AND del_r = %s """ % (email, 1)
    sql3 = """
    SELECT time FROM Mail WHERE receiver ='%s' AND del_r = %s """ % (email, 1)
    sql4 = """
    SELECT no FROM Mail WHERE receiver ='%s' AND del_r = %s """ % (email, 1)
    rev = execute_query1(sql1)
    sub = execute_query1(sql2)
    time = execute_query1(sql3)
    no = execute_query1(sql4)
    return rev.fetchall(), sub.fetchall(), time.fetchall(), no.fetchall()


def get_sent(email):
    sql1 = """
        SELECT receiver FROM Mail WHERE sender ='%s' AND del_s = %s """ % (email, 1)
    sql2 = """
        SELECT subject FROM Mail WHERE sender ='%s' AND del_s = %s """ % (email, 1)
    sql3 = """
        SELECT time FROM Mail WHERE sender ='%s' AND del_s = %s """ % (email, 1)
    sql4 = """
        SELECT no FROM Mail WHERE sender ='%s' AND del_s = %s """ % (email, 1)
    rev = execute_query1(sql1)
    sub = execute_query1(sql2)
    time = execute_query1(sql3)
    no = execute_query1(sql4)
    return rev.fetchall(), sub.fetchall(), time.fetchall(), no.fetchall()


def check_email(email):
    sql = """
    SELECT email FROM User WHERE email = '%s'""" % email
    return execute_query(sql).fetchall()


def send_mail(send, receiver, subject, content, time, org, alias):
    sql = """INSERT INTO Mail(sender, receiver, subject, content, time, att, att_als, del_s, del_R) VALUES('%s', 
    '%s', '%s', '%s', '%s', '%s', '%s', %s, %s)""" % (
        send, receiver, subject,
        content, time, org, alias, 1, 1)
    execute_query1(sql)


def view_mail(no):
    sql1 = """
    SELECT content FROM Mail WHERE no = %s """ % no
    sql2 = """
        SELECT att FROM Mail WHERE no = %s """ % no
    sql3 = """
        SELECT att_als FROM Mail WHERE no = %s """ % no
    sql4 = """
        SELECT subject FROM Mail WHERE no = %s """ % no
    sql5 = """
        SELECT sender FROM Mail WHERE no = %s """ % no
    sql6 = """
        SELECT receiver FROM Mail WHERE no = %s """ % no
    return execute_query1(sql1).fetchall(), execute_query1(sql2).fetchall(), execute_query1(sql3).fetchall(), \
           execute_query1(sql4).fetchall(), execute_query1(sql5).fetchall(), execute_query1(sql6).fetchall()


def delete_mail_i(no):
    sql = """
    UPDATE Mail
    SET del_r = 0
    WHERE no = %s""" % no
    permanent_del()
    execute_query1(sql).fetchall()


def delete_mail_s(no):
    sql = """
    UPDATE Mail
    SET del_s = 0
    WHERE no = %s""" % no
    permanent_del()
    execute_query1(sql).fetchall()


def permanent_del():
    sql = """
    DELETE FROM Mail WHERE del_s = %s AND del_r = %s""" % (0, 0)
    execute_query1(sql).fetchall()


def del_acc(email):
    sql = """
    DELETE FROM User WHERE email = '%s'""" % email
    sql1 = """
        UPDATE Mail
        SET del_s = 0
        WHERE sender = '%s'""" % email
    sql2 = """
            UPDATE Mail
            SET del_r = 0
            WHERE receiver = '%s'""" % email
    execute_query(sql).fetchall()
    execute_query1(sql1).fetchall()
    execute_query1(sql2).fetchall()
    permanent_del()


def s_con_i(key, email):
    s_key = "%" + key + "%"
    sql1 = """
    SELECT time FROM Mail WHERE content LIKE '%s' AND receiver = '%s'""" % (s_key, email)
    sql2 = """
    SELECT sender FROM Mail WHERE content LIKE '%s' AND receiver = '%s'""" % (s_key, email)
    sql3 = """
    SELECT subject FROM Mail WHERE content LIKE '%s' AND receiver = '%s'""" % (s_key, email)
    sql4 = """
    SELECT no FROM Mail WHERE content LIKE '%s' AND receiver = '%s'""" % (s_key, email)
    return execute_query1(sql1).fetchall(), execute_query1(sql2).fetchall(), execute_query1(sql3).fetchall(), execute_query1(sql4).fetchall()


def s_con_s(key, email):
    s_key = "%" + key + "%"
    sql1 = """
    SELECT time FROM Mail WHERE content LIKE '%s' AND sender = '%s'""" % (s_key, email)
    sql2 = """
    SELECT subject FROM Mail WHERE content LIKE '%s' AND sender = '%s'""" % (s_key, email)
    sql3 = """
    SELECT receiver FROM Mail WHERE content LIKE '%s' AND sender = '%s'""" % (s_key, email)
    sql4 = """
    SELECT no FROM Mail WHERE content LIKE '%s' AND sender = '%s'""" % (s_key, email)
    return execute_query1(sql1).fetchall(), execute_query1(sql2).fetchall(), execute_query1(sql3).fetchall(), execute_query1(sql4).fetchall()


def s_id(key):
    key = "%" + key + "%"
    sql1 = """
        SELECT time FROM Mail WHERE sender LIKE '%s' """ % key
    sql2 = """
        SELECT sender FROM Mail WHERE sender LIKE '%s' """ % key
    sql3 = """
        SELECT subject FROM Mail WHERE sender LIKE '%s' """ % key
    sql4 = """
        SELECT receiver FROM Mail WHERE sender LIKE '%s' """ % key
    sql5 = """
        SELECT no FROM Mail WHERE sender LIKE '%s' """ % key
    return execute_query1(sql1).fetchall(), execute_query1(sql2).fetchall(), execute_query1(sql3).fetchall(), \
           execute_query1(sql4).fetchall(), execute_query1(sql5).fetchall()


def execute_query(sql_query):
    with sqlite3.connect("user.db") as conn:
        cur = conn.cursor()
        result = cur.execute(sql_query)
        conn.commit()
    return result


def execute_query1(sql_query):
    with sqlite3.connect("mail.db") as conn:
        cur = conn.cursor()
        result = cur.execute(sql_query)
        conn.commit()
    return result
