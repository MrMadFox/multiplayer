from flask import Flask,request
import sqlite3
app=Flask("one")
@app.route("/post",methods=["POST","GET"])
def post():
    conn=sqlite3.connect("data")
    cursor=conn.cursor()
    if request.form["user.id"]=="1":
        cursor.execute("update fight set one='%s' where playingid='%s';"%(request.form["y"],request.form["playingid"]))
    if request.form["user.id"]=="2":
        cursor.execute("update fight set two='%s' where playingid='%s';"%(request.form["y"],request.form["playingid"]))
    cursor.fetchall()
    conn.commit()
    ############
    if request.form["user.id"]=="1":
        cursor.execute("select two from fight where playingid='%s';"%(request.form["playingid"]))
    if request.form["user.id"]=="2":
        cursor.execute("select one from fight where playingid='%s';" % (request.form["playingid"]))
    return(str(cursor.fetchall()[0][0]))

    ##################
    return("0")
# @app.route("/get",methods=["GET"])
# def getit():
#     conn=sqlite3.connect("data")
#     cursor=conn.cursor()
#     if request.form["user.id"]=="1":
#         cursor.execute("select two from fight where playingid='%s';"%(request.form["playingid"]))
#     if request.form["user.id"]=="2":
#         cursor.execute("select one from fight where playingid='%s';" % (request.form["playingid"]))
#     return(str(cursor.fetchall()[0][0]))
@app.route("/ready",methods=["POST"])
def ready1():
    conn=sqlite3.connect("data")
    cursor=conn.cursor()
    if request.form["user.id"]=="1":
        exe="update details set one='%s' where playingid='%s';"%(request.form["ready"],request.form["playingid"])
        cursor.execute(exe)
    if request.form["user.id"]=="2":
        exe="update details set two='%s' where playingid='%s';"%(request.form["ready"],request.form["playingid"])
        cursor.execute(exe)
    conn.commit()
    return("0")
@app.route("/ready",methods=["GET"])
def ready2():
    conn=sqlite3.connect("data")
    cursor=conn.cursor()
    exe="select one,two from details where playingid='%s'"%(request.form["playingid"])
    cursor.execute(exe)
    x,y=cursor.fetchall()[0]
    if x==1 and y==1:
        return("0")
        #shouldnotbe there
    return("1")#(1=not ready) (0=ready)
app.run(host="0.0.0.0")

# CREATE TABLE details ( `playingid` INT NOT NULL , `one` INT NOT NULL DEFAULT '0' , `two` INT NOT NULL DEFAULT '0' );
# CREATE TABLE fight ( `playingid` INT NOT NULL , `one` INT NOT NULL DEFAULT '50' , `two` INT NOT NULL DEFAULT '50' );
