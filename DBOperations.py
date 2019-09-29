import sqlite3

class DBManager:

    def __init__(self):
        self.connection = sqlite3.connect("DataBase/PatientTracking.db")
        self.cursor = self.connection.cursor()

    #=============== INSERT ===============#
    def InsertHasta(self,HastaAdi,HastaSoyadi,TcKimlikNo,DogumTarihi,Adres,ID,SIFRE):
        values = HastaAdi,HastaSoyadi,TcKimlikNo,DogumTarihi,Adres,ID,SIFRE
        self.cursor.execute("INSERT INTO Hasta(HastaAdi,HastaSoyAdi,TcKimlikNo,DogumTarihi,Adres,ID,SIFRE) VALUES(?,?,?,?,?,?,?);",values)
        self.connection.commit()

    def InsertDoktor(self,DoktorAdi,DoktorSoyAdi,Unvan,ID,SIFRE):
        values = DoktorAdi,DoktorSoyAdi,Unvan,ID,SIFRE
        self.cursor.execute("INSERT INTO Doktor(DoktorAdi,DoktorSoyAdi,Unvan,ID,SIFRE) VALUES(?,?,?,?,?);",values)
        self.connection.commit()

    def InsertTeknisyen(self,teknisyenAdi,teknisyenSoyAdi,ID,SIFRE):
        values = teknisyenAdi,teknisyenSoyAdi,ID,SIFRE
        self.cursor.execute("INSERT INTO Teknisyen(TeknisyenAdi,TeknisyenSoyAdi,ID,SIFRE) VALUES(?,?,?,?);",values)
        self.connection.commit()

    def InsertRontgen(self,TahlilID,ImageLoc):
        values = ImageLoc,TahlilID
        self.cursor.execute("INSERT INTO RontgenFilmi(RontgenFilmi,TahlilID) VALUES(?,?);",values)
        self.connection.commit()

    def InsertTahlil(self,Sikayet,TahlilAdi,Tarih,HastaID):
        values = Sikayet,TahlilAdi,Tarih,HastaID
        self.cursor.execute("INSERT INTO TAHLIL(Sikayet,TahlilAdi,Tarih,HastaID) VALUES(?,?,?,?);", values) 
        self.connection.commit()

    def InsertTeshis(self,Teshis,Tarih,HastaID,DoktorID,TahlilID):
        values = Teshis,Tarih,HastaID,DoktorID,TahlilID
        self.cursor.execute("INSERT INTO Teshis(Teshis,Tarih,HastaID,DoktorID,TahlilID) VALUES(?,?,?,?,?);",values)
        self.connection.commit()
    #=============== INSERT ===============#

    #=============== SELECT ===============#
    def GetHasta(self,ID,SIFRE):
        self.cursor.execute("SELECT * FROM Hasta WHERE ID=? and SIFRE=?",(ID,SIFRE))
        listHasta = self.cursor.fetchall()
        return listHasta[0][0],listHasta[0][1],listHasta[0][2],listHasta[0][3],listHasta[0][4],listHasta[0][5],listHasta[0][6],listHasta[0][7],listHasta[0][8]
  
    def GetDoktor(self,ID,SIFRE):
        self.cursor.execute("SELECT * FROM Doktor WHERE ID=? and SIFRE=?",(ID,SIFRE))
        listDoktor = self.cursor.fetchall()
        return listDoktor[0][0],listDoktor[0][1],listDoktor[0][2],listDoktor[0][3],listDoktor[0][4],listDoktor[0][5],listDoktor[0][6]

    def GetTeknisyen(self,ID,SIFRE):
        self.cursor.execute("SELECT * FROM Teknisyen WHERE ID=? and SIFRE=?",(ID,SIFRE))
        listTeknisyen = self.cursor.fetchall()
        return listTeknisyen[0][0],listTeknisyen[0][1],listTeknisyen[0][2],listTeknisyen[0][3],listTeknisyen[0][4]

    def GetHastaID(self,Isim,Soyisim,TC):
        self.cursor.execute("SELECT HastaID FROM Hasta WHERE HastaAdi=? and HastaSoyAdi=? and TcKimlikNo=?",(Isim,Soyisim,TC))
        hastaID = self.cursor.fetchall()
        return hastaID

    def GetHastaIDWithoutTC(self,Isim,Soyisim):
        self.cursor.execute("SELECT HastaID FROM Hasta WHERE HastaAdi=? and HastaSoyAdi=?",(Isim,Soyisim))
        hastaID = self.cursor.fetchall()
        return hastaID

    def SearchTeshisForHasta(self,ID):
        self.cursor.execute("SELECT * FROM Teshis WHERE HastaID=?",ID)
        teshis = self.cursor.fetchall()
        return teshis

    def SearchTeshisForDoktor(self,ID):
        self.cursor.execute("SELECT * FROM Teshis WHERE DoktorID=?",ID)
        teshis = self.cursor.fetchall()
        return teshis

    def SearchTeshisForAll(self):
        self.cursor.execute("SELECT * FROM Teshis")
        teshis = self.cursor.fetchall()
        return teshis

    def SearchHasta(self,Isim,Soyisim,TC):
        if(Isim=="" and Soyisim=="" and TC==""):
            self.cursor.execute("SELECT HastaAdi,HastaSoyAdi,TcKimlikNo FROM Hasta")
            listhasta = self.cursor.fetchall()
        else:
            self.cursor.execute("SELECT HastaAdi,HastaSoyAdi,TcKimlikNo FROM Hasta WHERE HastaAdi like ? or HastaSoyAdi like ? or TcKimlikNo like ?",(Isim,Soyisim,TC))
            listhasta = self.cursor.fetchall()
        return listhasta

    def SearchTahlil(self,hastaADi,hastaSoyAdi,Tarih,TahlilTipi):
        if(hastaADi=="" and hastaSoyAdi==""):
            self.cursor.execute("SELECT TahlilID,HastaAdi,HastaSoyAdi,Tarih,TahlilAdi FROM Hasta INNER JOIN TAHLIL Where Hasta.HastaID = TAHLIL.HastaID and TahlilAdi=? ORDER BY TahlilID",(TahlilTipi,))
            result = self.cursor.fetchall()
        else:
            self.cursor.execute("SELECT TahlilID,HastaAdi,HastaSoyAdi,Tarih,TahlilAdi FROM Hasta INNER JOIN TAHLIL Where Hasta.HastaID = TAHLIL.HastaID and TahlilAdi=? and HastaAdi like ? or HastaSoyAdi like ? or Tarih=? ORDER BY TahlilID",(TahlilTipi,hastaADi,hastaSoyAdi,Tarih))
            result = self.cursor.fetchall()
        return result