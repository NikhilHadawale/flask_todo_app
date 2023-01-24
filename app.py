from flask import Flask,render_template,request,redirect,session,send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytube import YouTube
from io import BytesIO

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///project.db"
app.config['SECRET_KEY']="nikhil"
db = SQLAlchemy(app)


class ToDO(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    item = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(2000))
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.item}-{self.desc}"

@app.route("/",methods=['POST','GET'])
def main():
    if request.method=='POST':
        item=request.form['item'];
        desc=request.form['desc']
        todo=ToDO(item=item,desc=desc)
        db.session.add(todo)
        db.session.commit()

    alltodo=list(db.session.execute(db.select(ToDO)).scalars())
    return render_template('index.html',alltodo=alltodo)  

@app.route('/delete/<int:sno>')
def delete(sno):
    item=db.get_or_404(ToDO,sno)
    db.session.delete(item)
    db.session.commit()
    return redirect('/')

@app.route("/about")
def about():

    return render_template('about.html')

@app.route("/update/<int:sno>",methods=['POST','GET'])
def update(sno):
    if request.method=='POST':
         item=request.form['item']
         desc=request.form['desc']
         todo=db.get_or_404(ToDO,sno)
         todo.item=item
         todo.desc=desc
         db.session.add(todo)
         db.session.commit()
         return redirect('/')
    else:     
        todo_update=db.get_or_404(ToDO,sno)
        return render_template('update.html',todo=todo_update)

@app.route("/downloader/",methods=['GET','POST'])
def downloader():
    if request.method=='POST':
        session['link']=request.form['link']
        link=request.form['link']
        yt=YouTube(link)
        link=link.replace('/','+')
        session['title']=yt.title
        new_yt={'link':link,'name':yt.title,'thumbnail':yt.thumbnail_url,'author':yt.author,}
        return render_template('downloader.html',vdo=new_yt)
    else:
        return render_template('downloader.html')

@app.route("/downloader/<string:vdolink>",methods=['GET','POST'])
def start_download(vdolink):
    vdolink=vdolink.replace('+','/')
    yt=YouTube(vdolink)
    vdo=yt.streams.get_highest_resolution()
    try:
        buffer=BytesIO()
        vdo.stream_to_buffer(buffer)
        buffer.seek(0)
    except:
        return "An Error Occured"
    return send_file(buffer,as_attachment=True,download_name=session['title']+'.mp4',mimetype="video/mp4")

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=8000) 