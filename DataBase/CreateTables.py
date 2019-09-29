import sqlite3

connection = sqlite3.connect("PatientTracking.db")

cursor = connection.cursor()

create_Hasta_Table       = """CREATE TABLE IF NOT EXISTS Hasta(
                                HastaID INTEGER PRIMARY KEY,
                                HastaAdi VARCHAR(25) NOT NULL,
                                HastaSoyAdi VARCHAR(25) NOT NULL,
                                TcKimlikNo VARCHAR(11) NOT NULL,
                                DogumTarihi DATE NOT NULL,
                                ADRES VARCHAR(50) NOT NULL,
				ID TEXT NOT NULL,
				SIFRE TEXT NOT NULL,
				HastaProfilResmi TEXT
                                );"""
cursor.execute(create_Hasta_Table)


create_Doktor_Table      = """CREATE TABLE IF NOT EXISTS Doktor(
                                DoktorID INTEGER PRIMARY KEY,
                                DoktorAdi VARCHAR(25)NOT NULL,
                                DoktorSoyAdi VARCHAR(25) NOT NULL,
                                Unvan VARCHAR(25) NOT NULL,
				ID TEXT NOT NULL,
				SIFRE TEXT NOT NULL,
				DoktorProfilResmi TEXT
                                );"""
cursor.execute(create_Doktor_Table)


create_Tahlil_Table      = """CREATE TABLE IF NOT EXISTS TAHLIL(
                                TahlilID INTEGER PRIMARY KEY,
                                Sikayet TEXT NOT NULL,
                                TahlilAdi TEXT NOT NULL,
                                Tarih DATE NOT NULL,
                                HastaID INTEGER NOT NULL,
                                FOREIGN KEY(HastaID) REFERENCES Hasta(HastaID)
                                );"""
cursor.execute(create_Tahlil_Table)


Create_Teshis_Table      = """CREATE TABLE IF NOT EXISTS Teshis(
                                TeshisID INTEGER PRIMARY KEY,
				TahlilID INTEGER NOT NULL,
                                Teshis TEXT NOT NULL,
                                Tarih DATE NOT NULL,
                                HastaID INTEGER NOT NULL,
                                DoktorID INTEGER,
                                FOREIGN KEY(HastaID) REFERENCES Hasta(HastaID),
                                FOREIGN KEY(DoktorID) REFERENCES Doktor(DoktorID),
				FOREIGN KEY(TahlilID) REFERENCES TAHLIL(TahlilID)
                                );"""
cursor.execute(Create_Teshis_Table)


create_RontgenFilmi_Table = """CREATE TABLE IF NOT EXISTS RontgenFilmi (
                                RontgenID INTEGER PRIMARY KEY,
                                RontgenFilmi Text,
                                TahlilID INTEGER NOT NULL,
                                FOREIGN KEY(TahlilID) REFERENCES TAHLIL(TahlilID)
                                );"""
cursor.execute(create_RontgenFilmi_Table)

create_teknisyenTable = """CREATE TABLE IF NOT EXISTS Teknisyen(
				TeknisyenID INTEGER PRIMARY KEY,
				TeknisyenAdi VARCHAR(25) NOT NULL,
				TeknisyenSoyAdi VARCHAR(25) NOT NULL,
				ID TEXT NOT NULL,
				SIFRE TEXT NOT NULL
				);"""
cursor.execute(create_teknisyenTable)