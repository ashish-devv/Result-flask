#app.py
from flask import Flask,render_template,request,redirect
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "result"

mysql=MySQL(app)

def userinfo(a):
	k=[]
	cur=mysql.connection.cursor()
	statement="SELECT `REGD. NO`,`NAME OF THE STUDENT`,`Sem` FROM `sheet1` WHERE `REGD. NO`= "+a
	result=cur.execute(statement)
	if result > 0:
		info=cur.fetchone()
		k=list(info)
		k[0]=" Registration no : "+str(k[0])
		k[1]=" Name : "+k[1]
		k[2]=" Semester : "+k[2]
		info = k
		print
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
		elif(l[2]=="F" or l[2]=="0"):
			l[2]=0
			lis.append(l[2])
		else:
			lis.append(float(l[2]))

	sum=0
	for i in lis:
		sum=sum+i
	cgpa=sum/len(lis)
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
		#print(regno)
		cur=mysql.connection.cursor()
		statement="SELECT `SUB.CODE`,`SUBJECT NAME`,`Grade` FROM `sheet1` WHERE `REGD. NO`= "+regno
		result=cur.execute(statement)
		if result > 0:
			res=cur.fetchall()
			res2=convert(res)
			cgpa=gpa(res2)
			#print(type(res))
			return render_template('result.html',res=res,cgpa=cgpa,inf=inf)

	return redirect('/')	
   

if __name__ == '__main__':
   app.run(debug=True,host="0.0.0.0",port='5000')