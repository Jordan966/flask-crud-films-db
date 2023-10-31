from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
app=Flask(__name__)
app.secret_key='123abc'

@app.route("/")
@app.route("/index")
def index():
    con=sql.connect("filmflix.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from tblFilms")
    records=cur.fetchall()
    return render_template("index.html",allRecords=records)

@app.route("/addFilm",methods=['POST','GET'])
def addFilm():
    if request.method=='POST':
        title=request.form['title']
        released=request.form['yearReleased']
        rating=request.form['rating']
        duration=request.form['duration']
        genre=request.form['genre']
        con=sql.connect("filmflix.db")
        cur=con.cursor()
        cur.execute("insert into tblFilms(title, yearReleased, rating, duration, genre) values (?,?,?,?,?)",(title,released,rating,duration,genre))
        con.commit()
        flash('Film Added','success')
        return redirect(url_for("index"))
    return render_template("addFilm.html")

@app.route("/editFilm/<string:filmID>",methods=['POST','GET'])
def editFilm(filmID):
    if request.method=='POST':
        title=request.form['title']
        released=request.form['yearReleased']
        rating=request.form['rating']
        duration=request.form['duration']
        genre=request.form['genre']
        con=sql.connect("filmflix.db")
        cur=con.cursor()
        cur.execute("update tblFilms set title=?, yearReleased=?, rating=?, duration=?, genre=? where filmID=?",(title, released, rating, duration, genre, filmID))
        con.commit()
        flash('User Updated','success')
        return redirect(url_for("index"))
    con=sql.connect("filmflix.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from tblFilms where filmID=?",(filmID,))
    data=cur.fetchone()
    return render_template("editFilm.html",datas=data)
    
@app.route("/delete_user/<string:filmID>",methods=['GET'])
def delete_user(filmID):
    con=sql.connect("filmflix.db")
    cur=con.cursor()
    cur.execute("delete from tblFilms where filmID=?",(filmID,))
    con.commit()
    flash('User Deleted','warning')
    return redirect(url_for("index"))
    
# if __name__=='__main__':
#     app.run(debug=False)