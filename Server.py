from flask import Flask,render_template,request,url_for,jsonify
from imageai.Prediction.Custom import CustomImagePrediction
import tensorflow as tf
import os
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping
from tensorflow.python.keras.backend import set_session
from DBOperations import DBManager
import json
from datetime import date
from PIL import Image
import numpy as np
import cv2

def init():
	#Prepare and load model
	global execution_path,prediction,graph,session
	execution_path = os.getcwd()
	session = tf.Session()
	graph = tf.get_default_graph()
	tf.keras.backend.set_session(session)
	prediction = CustomImagePrediction()
	prediction.setModelTypeAsResNet()
	prediction.setModelPath(execution_path + "/Train&Test/chest_xray/models/model_ex-003_acc-0.773026.h5")
	prediction.setJsonPath(execution_path + "/Train&Test/chest_xray/json/model_class.json")
	prediction.loadModel(num_objects=2)
	
app = Flask(__name__)
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/delete/<string:id>")
def deleteId(id):
	return "Id " + id

@app.route("/Login",methods = ["GET","POST"])#Hasta
def Login():
	if request.method == "POST":
		try:
			ID = request.form['txtID']
			SIFRE = request.form['txtSifre']
			dbman = DBManager()
			HastaID,HastaAdi,HastaSoyadi,TcKimlikNo,DogumTarihi,Adres,ID,SIFRE,PP = dbman.GetHasta(ID,SIFRE)
			return render_template('hastaMain.html',message = [HastaID,HastaAdi,HastaSoyadi,TcKimlikNo,DogumTarihi,Adres,ID,SIFRE,PP])
		except:
			return render_template('hastaLoginError.html')
	else:
		pass

@app.route("/KayitOl",methods = ["GET","POST"])
def KayitOl():
	if request.method == "POST":
		try:
			AD = request.form['isim']
			Soyad = request.form['Soyisim']
			TC = request.form['TC']
			dt = request.form['dogumT']
			adres = request.form['Adres']
			ID = request.form['txtID']
			SIFRE = request.form['txtSifre']
			dbman = DBManager()
			if (AD!="" and Soyad!="" and TC!="" and dt!="" and adres!="" and  ID!="" and  SIFRE!="" ):
				dbman.InsertHasta(AD,Soyad,TC,dt,adres,ID,SIFRE)
				return render_template('kayit.html',message = "İşlem Başarısız")
			else:
				return render_template('kayit.html' , message = "İşlem Başarısız Lütfen Tekrar Deneyin")
		except:
			return render_template('kayit.html' , message = "İşlem Başarısız Lütfen Tekrar Deneyin")
	else:
		return render_template('kayit.html')

@app.route("/doktorLogin",methods = ["GET","POST"])
def doktorLogin():
	if request.method == "POST":
		try:
			ID = request.form['txtID']
			SIFRE = request.form['txtSifre']
			dbman = DBManager()
			DoktorID,DoktorAdi,DoktorSoyAdi,Unvan,ID,SIFRE,DoktorPP = dbman.GetDoktor(ID,SIFRE)
			return render_template('doktor.html',message = [DoktorID,DoktorAdi,DoktorSoyAdi,Unvan,ID,SIFRE,DoktorPP])
		except:
			return render_template('doktorLoginError.html')
	else:
		return render_template('doktorLogin.html')

@app.route("/teknisyenLogin",methods = ["GET","POST"])
def teknisyenLogin():
	if request.method == "POST":
		try:
			ID = request.form['txtID']
			SIFRE = request.form['txtSifre']
			dbman = DBManager()
			tekID,tekAd,tekSoyad,ID,SIFRE = dbman.GetTeknisyen(ID,SIFRE)
			return render_template('teknisyen.html')
		except:
			return render_template('teknisyenLogin.html',message = "Giriş İşlem Başarısız Lütfen Tekrar Deneyin")
	else:
		return render_template('teknisyenLogin.html')


@app.route("/tumTeshilerisAra/",methods = ["POST"])
def tumTeshilerisAra():
	if request.method == "POST":
		response = request.get_json()
		val = json.loads(json.dumps(response))
		dbman = DBManager()
		result = dbman.SearchTeshisForAll()
		return jsonify({'response':result})


@app.route("/hastaTeshisAra/",methods = ["POST"])
def hastaTeshisAra():
	if request.method == "POST":
		response = request.get_json()
		val = json.loads(json.dumps(response))
		ID = str(val['message'])
		dbman = DBManager()
		result = dbman.SearchTeshisForHasta(ID)
		return jsonify({'response':result})

@app.route("/doktorTeshisAra/",methods = ["POST"])
def doktorTeshisAra():
	if request.method == "POST":
		response = request.get_json()
		val = json.loads(json.dumps(response))
		ID = str(val['message'])
		dbman = DBManager()
		result = dbman.SearchTeshisForDoktor(ID)
		return jsonify({'response':result})

img = []
illness = ""
@app.route("/predict/",methods = ["GET","POST"])
def predict():
	if request.method == "POST":
		rontgen_img = request.files.get('send')
		npimg = np.fromfile(rontgen_img, np.uint8)
		global img
		img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
		with session.as_default():
			set_session(session)
			predictions, probabilities = prediction.predictImage(rontgen_img, result_count=2)
			global illness
			illness = predictions[0]
			return jsonify({'response':(predictions[0],probabilities[0])})

resim_img = []
@app.route("/resimYukle/",methods = ["GET","POST"])
def resimYukle():
	if request.method == "POST":
		resim = request.files.get('resim')

		npimg = np.fromfile(resim, np.uint8)
		resim_img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
		response = request.get_json()
		values = json.loads(json.dumps(response))
		print(values)
		return jsonify({'response':'success'})

@app.route("/rontgenGir/",methods = ["GET","POST"])
def rontgenGir():
	if request.method == "POST":
		response = request.get_json()
		values = json.loads(json.dumps(response))
		ad = str(values['message'][1])
		soyad = str(values['message'][2])
		tarih = str(values['message'][3])
		cv2.imwrite(str(os.getcwd())+"/DataBase/hastaRontgen/"+ad+soyad+tarih+".jpg",img)
		dbman = DBManager()
		dbman.InsertRontgen(str(values['message'][0]),str(os.getcwd())+"/DataBase/hastaRontgen/"+ad+soyad+tarih+".jpg")
		hastaID = dbman.GetHastaIDWithoutTC(ad,soyad)
		today = date.today()
		dbman.InsertTeshis(str(illness),today,hastaID[0][0],None,str(values['message'][0]))
		return jsonify({'response':'success'})
		

@app.route("/hastaAra/",methods = ["POST"])
def hastaAra():
	if request.method == "POST":
		response = request.get_json()
		values = json.loads(json.dumps(response))
		dbman = DBManager()
		result = dbman.SearchHasta(values['message'][0],values['message'][1],values['message'][2])
		return jsonify({'response':result})

@app.route("/tahlilAra/",methods = ["POST"])
def tahlilAra():
	if request.method == "POST":
		response = request.get_json()
		values = json.loads(json.dumps(response))
		dbman = DBManager()
		result = dbman.SearchTahlil(values['message'][0],values['message'][1],values['message'][2],values['message'][3])
		return jsonify({'response':result})

@app.route("/tahlilGir/",methods = ["POST"])
def tahlilGir():
	if request.method == "POST":
		response = request.get_json()
		values = json.loads(json.dumps(response))
		dbman = DBManager()
		hastaID = dbman.GetHastaID(values['message'][0],values['message'][1],values['message'][2])[0][0]
		today = date.today()

		if(values['message'][3] == True and values['message'][4] == True ):
			dbman.InsertTahlil(values['message'][5],"Rontgen",today,hastaID)
			dbman.InsertTahlil(values['message'][5],"Ekg",today,hastaID)

		elif(values['message'][3] == True and values['message'][4] == False ):
			dbman.InsertTahlil(values['message'][5],"Rontgen",today,hastaID)

		else:
			dbman.InsertTahlil(values['message'][5],"Ekg",today,hastaID)

		return jsonify({'response':'success'})

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

if __name__ == "__main__":
	init()
	app.run(debug = True)