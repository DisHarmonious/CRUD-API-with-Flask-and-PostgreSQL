from flask import Flask, Response, stream_with_context, render_template, url_for, redirect, request, jsonify
import logging, requests
import psycopg2, random, datetime, json

con = psycopg2.connect(dbname="panel", user="postgres", password="root")
cur = con.cursor()

app=Flask(__name__)

@app.route("/", methods=["GET"])
def main_landing_page():
    return ("welcome")



@app.route("/api/employee/list", methods=["GET"])
def get_list_of_employees():
    def f1():
        sql="select * from employees"
        cur.execute(sql)
        latest=cur.fetchall()
        data= []
        for i in range(len(latest)):
            a=dict(id=latest[i][0], fname=latest[i][1], lname=latest[i][2], phone=latest[i][3], email=latest[i][4])
            data.append(a)
        connectivity={}
        connectivity['message']=str('connection response:')
        connectivity['connection']=str(requests.get('http://127.0.0.1:5000'))
        return f'{data}', f'{connectivity}'
    return Response(stream_with_context(f1()))

@app.route("/api/employee/get/<int:id>", methods=["GET", "POST"])
def get_specific_employee(id):
    def f2():
        sql="select * from employees where id=%s"
        cur.execute(sql, [id,])
        latest=cur.fetchall()
        a=dict(id=latest[0][0], fname=latest[0][1], lname=latest[0][2], phone=latest[0][3], email=latest[0][4])
        connectivity={}
        connectivity['message']=str('connection response:')
        connectivity['connection']=str(requests.get('http://127.0.0.1:5000'))
        return f'{a}', f'{connectivity}'
    return Response(stream_with_context(f2()))

@app.route("/api/employee/create/<int:id>/<string:fname>/<string:lname>/<int:phone>/<string:email>", methods=["GET", "POST"])
def create_employee(id, fname, lname, phone, email):
    sql="insert into employees values (%s, %s, %s, %s, %s)"
    values=[id, fname, lname, phone, email]
    cur.execute(sql, values)
    con.commit()
    def f3():
        sql="select * from employees where id=%s"
        cur.execute(sql, [id,])
        latest=cur.fetchall()
        a=dict(id=latest[0][0], fname=latest[0][1], lname=latest[0][2], phone=latest[0][3], email=latest[0][4])
        connectivity={}
        connectivity['message']=str('connection response:')
        connectivity['connection']=str(requests.get('http://127.0.0.1:5000'))
        return f'{a}', f'{connectivity}'
    return Response(stream_with_context(f3()))

@app.route("/api/employee/update/<int:id>/<string:fname>/<string:lname>/<int:phone>/<string:email>", methods=["GET", "POST"])
def update_employee(id, fname, lname, phone, email):
    sql="delete from employees where id=%s"
    cur.execute(sql, [id,])
    con.commit()
    sql="insert into employees values (%s, %s, %s, %s, %s)"
    values=[id, fname, lname, phone, email]
    cur.execute(sql, values)
    con.commit()
    def f4():
        sql="select * from employees where id=%s"
        cur.execute(sql, [id,])
        latest=cur.fetchall()
        a=dict(id=latest[0][0], fname=latest[0][1], lname=latest[0][2], phone=latest[0][3], email=latest[0][4])
        connectivity={}
        connectivity['message']=str('connection response:')
        connectivity['connection']=str(requests.get('http://127.0.0.1:5000'))
        return f'{a}', f'{connectivity}'
    return Response(stream_with_context(f4()))

@app.route("/api/employee/delete/<int:id>", methods=["GET", "POST"])
def delete_employee(id):
    sql="delete from employees where id=%s"
    cur.execute(sql, [id,])
    con.commit()
    connectivity={}
    connectivity['message']=str('connection response:')
    connectivity['connection']=str(requests.get('http://127.0.0.1:5000'))
    return("employee deleted", f'{connectivity}')


if __name__=="__main__":
    app.run(debug=True)

