#app.py my edit
import os
from flask import Flask,render_template,request,redirect,url_for
import sqlite3
import pandas as pd
from werkzeug.utils import secure_filename



app = Flask(__name__)
UPLOAD_FOLDER = '\\uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def viewupdate(r):
	conn=sqlite3.connect('view.db')
	c=conn.cursor()
	st='SELECT "reg","view" FROM view WHERE "reg"='+r+' LIMIT 1;'
	c.execute(st)
	r=convert(c.fetchall())
	print("---------------------------------------------------")
	print("---------------------------------------------------")
	print("---------------------------------------------------")
	print(r)


def userinfo(a):
	k=[]
	#cur=mysql.connection.cursor()
	conn=sqlite3.connect('a.db')
	c=conn.cursor()
	statement='SELECT "REGD.NO","NAMEOFTHESTUDENT","Sem" FROM "sheet1" WHERE "REGD.NO" ='+a+' LIMIT 1'
	#print(statement)
	c.execute(statement)
	result=c.fetchone()
	#print(result)
	if result==None:
		return 1
	if len(result) > 0:
		c.close()
		k=list(result)
		k[0]=" Registration no : "+str(k[0])
		k[1]=" Name : "+k[1]
		k[2]=" Semester : "+k[2]
		info = k
		return info



def convert(a):
	lis=[]
	for l in a:
		k=[]
		for l1 in l:
			k.append(l1)
		lis.append(k)
	return lis

def gpa(a):
	lis=[]
	credit=[]
	for l in a:
		if(l[2]=="O" or l[2]=="10"):
			l[2]=10
			lis.append(l[2])
		elif(l[2]=="E" or l[2]=="9"):
			l[2]=9
			lis.append(l[2])
		elif(l[2]=="A" or l[2]=="8"):
			l[2]=8
			lis.append(l[2])
		elif(l[2]=="B" or l[2]=="7"):
			l[2]=7
			lis.append(l[2])
		elif(l[2]=="C" or l[2]=="6"):
			l[2]=6
			lis.append(l[2])
		elif(l[2]=="D" or l[2]=="5"):
			l[2]=5
			lis.append(l[2])
		elif(l[2]=="S" or l[2]=="0"):
			l[2]=0
			lis.append(l[2])
		elif(l[2]=="M" or l[2]=="0"):
			l[2]=0
			lis.append(l[2])
		elif(l[2]=="F" or l[2]=="0"):
			l[2]=0
			lis.append(l[2])
		else:
			lis.append(float(l[2]))
	
	for cr in a:
		
		creditrow=cr[3].split("+")
		
		for i in range(0, len(creditrow)):
			creditrow[i] = int(creditrow[i])
		print(sum(creditrow))
		credit.append(sum(creditrow))
	
	print(credit)
	print(lis)
	summ=0
	for i in range(0,len(credit)):
		summ=summ+(credit[i]*lis[i])
	print(summ)
	cgpa=summ/sum(credit)

	# summ=0
	# for i in lis:
	# 	summ=summ+i
	# cgpa=summ/len(lis)
	return cgpa
		
		

@app.route('/')
def index():
	return render_template("index.html")

@app.route("/result",methods=['GET','POST'])
def result():
	if request.method == "POST":
		rno=request.form['regno']
		regno=str(rno)
		inf=userinfo(rno)
		if(inf==1):
			redirect(url_for('index'))
		#print(regno)
		#cur=mysql.connection.cursor()
		conn=sqlite3.connect('a.db')
		c=conn.cursor()
		statement='SELECT "SUB.CODE","SUBJECTNAME","Grade","Credit" FROM "sheet1" WHERE "REGD.NO"='+regno
		print(statement)
		c.execute(statement)
		result=c.fetchall()
		print("##############################################################")
		print(result)
		if len(result) > 0:
			# res=c.fetchall()
			# print("##############################################################")
			# print(res)
			res2=convert(result)
			print(res2)
			cgpa=gpa(res2)
			#print(type(res))
			c.close()
			#viewupdate(rno)
			return render_template('result.html',res=res2,cgpa=cgpa,inf=inf)
		else:
			redirect(url_for('index'))

	return redirect('/')	

@app.route("/admin")
def adminpage():
	return render_template("admin.html")


@app.route('/uploadadmin', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			file.save(filename)
			conn = sqlite3.connect('a.db')
			c = conn.cursor()
			c.execute(''' DELETE FROM sheet1 WHERE 1 ''')
			csvfile=pd.read_csv(filename)
			csvfile.to_sql("sheet1", conn, if_exists='append', index = False)
			return redirect("/admin?code=Uploaded Successfully")
	return "Fail"


if __name__ == '__main__':
   app.run(debug=True,host="0.0.0.0",port='5000')
