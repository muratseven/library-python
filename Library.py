import psycopg2
from psycopg2 import pool
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtTest import *

try:
    postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
                          password="123",
                          host="localhost",
                          port="5432",
                          database="postgres")
    if (postgreSQL_pool):
        print("Connection pool created successfully")
        print("Put away a PostgreSQL connection")
except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (postgreSQL_pool):
        postgreSQL_pool.closeall
    print("PostgreSQL connection pool is closed")

baslikfont = QFont("Century Gothic",38)
versionfont = QFont("Century Gothic",15)
butonFont = QFont("Century Gothic",20)
yaziFont = QFont("Century Gothic",18)

class intro(QWidget):
    def __init__(self):
        super().__init__()

        horizontal = QHBoxLayout()

        self.yazi = QLabel("Library Project ")
        self.yaziversion = QLabel("V1.0")

        horizontal.addStretch()
        horizontal.addWidget(self.yazi)
        horizontal.addWidget(self.yaziversion)
        horizontal.addStretch()

        self.yazi.setFont(baslikfont)
        self.yaziversion.setFont(versionfont)
        self.setLayout(horizontal)

class kitapListesi(QWidget):
    def __init__(self):
        super().__init__()

        try:
            postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
                                                                 password="123",
                                                                 host="localhost",
                                                                 port="5432",
                                                                 database="postgres")

            if (postgreSQL_pool):
                print("Connection pool created successfully")
            ps_connection = postgreSQL_pool.getconn()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if (postgreSQL_pool):
                postgreSQL_pool.closeall
            print("PostgreSQL connection pool is closed")

        horizontal = QHBoxLayout()
        Vertical = QVBoxLayout()
        ustBolum(self)

        baslik = QLabel("BOOKS")
        aciklama = QLabel("Book Name")
        aciklama.setFont(versionfont)
        aciklama.setStyleSheet("color: rgb(227,148,29)")
        baslik.setFont(baslikfont)
        liste = QListWidget()
        yeniEkle = QPushButton("New a Boook")
        yeniEkle.setFont(butonFont)
        yeniEkle.clicked.connect(self.yeniEkle)
        if (ps_connection):
            print("successfully recived connection from connection pool ")
            ps_cursor = ps_connection.cursor()
            liste = QListWidget()

            ps_cursor.execute("select * from books")
            mobile_records = ps_cursor.fetchall()
            print("Displaying rows from mobile table")
            for row in mobile_records:
                liste.addItem(row[6])
                liste.sortItems()

            ps_cursor.close()
            postgreSQL_pool.putconn(ps_connection)
            print("Put away a PostgreSQL connection")
        #liste.itemClicked.connect(self.kitapBilgi)

        Vertical.addWidget(baslik)
        Vertical.addWidget(aciklama)
        Vertical.addWidget(liste)
        Vertical.addWidget(yeniEkle)

        horizontal.addStretch()
        horizontal.addLayout(Vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

    def kitapBilgi(self,item):
        if (postgreSQL_pool):
            print("Connection pool created successfully")
        ps_connection = postgreSQL_pool.getconn()
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute("select * from kitap")
        ps_connection = postgreSQL_pool.getconn()
        if (ps_connection):
            print("successfully recived connection from connection pool ")
            ps_cursor = ps_connection.cursor()
        kitapismi = item.text()
        kontrol = ps_cursor.execute("SELECT * FROM kitap WHERE kadi = ?",(kitapismi,))
        durum = kontrol.fetchall()[0][2]

        if(durum==0):
            QMessageBox.information(self,"Kitap Bilgisi",kitapismi + " isimli kitap şu anda boşta !")
        else:
            kimde = ps_cursor.execute("SELECT * FROM kitap WHERE kadi = ?",(kitapismi,))
            ogrenci = kimde.fetchall()[0][1]
            print("heree",ogrenci)
            QMessageBox.information(self,"Kitap Bilgisi",kitapismi + " isimli kitap şu anda ")

    def yeniEkle(self):

        self.yeni = yeniKitap()
        self.yeni.showFullScreen()

    def geriDon(self):
        self.close()

class yeniKitap(QWidget):
    def __init__(self):
        super().__init__()
        ustBolum(self)
        horizontal = QHBoxLayout()
        Vertical = QVBoxLayout()

        self.setWindowTitle("Yeni Öğrenci Ekle")
        baslik = QLabel("Kitap Ekle")
        baslik.setFont(baslikfont)

        self.Vertical = QVBoxLayout()

        baslik = QLabel("New a Book")
        acıklama = QLabel("Fill in The Information Below to Add a New Book.")
        baslik.setFont(baslikfont)
        acıklama.setFont(yaziFont)

        bookid = QLineEdit()
        bookid.setPlaceholderText("Enter a Book ID")
        editionnumber = QLineEdit()
        editionnumber.setPlaceholderText("Enter Edition Number ")
        pagenumber = QLineEdit()
        pagenumber.setPlaceholderText("Enter Page Number")
        ISBN = QLineEdit()
        ISBN.setPlaceholderText("Enter ISBN")
        editionyear = QLineEdit()
        editionyear.setPlaceholderText("Enter Edition Year")
        ArrivalDate = QLineEdit()
        ArrivalDate.setPlaceholderText("Enter Arrival Date")
        Bookname = QLineEdit()
        Bookname.setPlaceholderText("Enter a Book Name")
        languageno = QLineEdit()
        languageno.setPlaceholderText("Enter a Language Number")
        companyno = QLineEdit()
        companyno.setPlaceholderText("Enter Company No")
        catogary = QLineEdit()
        catogary.setPlaceholderText("Enter Category No")
        authorno = QLineEdit()
        authorno.setPlaceholderText("Enter Author No")
        memberno = QLineEdit()
        memberno.setPlaceholderText("Enter Member No")

        kaydet = QPushButton("Save")
        kaydet.clicked.connect(self.kaydet)
        Vertical.addWidget(baslik)
        Vertical.addWidget(acıklama)

        Vertical.addStretch()

        Vertical.addWidget(bookid)
        Vertical.addWidget(editionnumber)
        Vertical.addWidget(pagenumber)
        Vertical.addWidget(ISBN)
        Vertical.addWidget(editionyear)
        Vertical.addWidget(ArrivalDate)
        Vertical.addWidget(Bookname)
        Vertical.addWidget(languageno)
        Vertical.addWidget(companyno)
        Vertical.addWidget(catogary)
        Vertical.addWidget(authorno)
        Vertical.addWidget(memberno)

        Vertical.addStretch()
        Vertical.addWidget(kaydet)
        Vertical.addStretch()

        horizontal.addStretch()
        horizontal.addLayout(Vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

    def geriDon(self):
        self.close()

    def kaydet(self):
        kaydediliyor = QLabel("Kaydediliyor. Lütfen bekleyin...")
        self.Vertical.addWidget(kaydediliyor)
        QTest.qWait(750)
        BOOKID = self.kitapismi.text()
        editionnumber = self.editionnumber.text()
        pagenumber = self.pagenumber.text()
        ISBN= self.ISBN.text()
        editionyear = self.editionyear.text()
        ArrivalDate = self.ArrivalDate.text()
        Bookname = self.Bookname.text()
        languageno = self.languageno.text()
        companyno = self.companyno.text()
        catogary = self.catogary.text()
        authorno = self.authorno.text()
        memberno = self.memberno.text()
        ps_connection = postgreSQL_pool.getconn()
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute("INSERT INTO BOOKS (book_id,editionnumber,pagenumber,ISBN,editionyear,ArrivalDate,Bookname,languageno,companyno,catogary,authorno,memberno) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (BOOKID,editionnumber,pagenumber,ISBN,editionyear,ArrivalDate,Bookname,languageno,companyno,catogary,authorno,memberno))
        kaydediliyor.setText("Registration Successful !")
        QTest.qWait(500)
        self.close()
def ustBolum(mevcutPencere):
    geriButon = QPushButton("<",mevcutPencere)
    geriButon.setFont(baslikfont)
    geriButon.setGeometry(20,20,50,50)
    geriButon.clicked.connect(mevcutPencere.geriDon)

    kapatButon = QPushButton("X",mevcutPencere)
    kapatButon.setFont(baslikfont)
    kapatButon.setGeometry(1300,20,50,50)
    kapatButon.clicked.connect(Pencere.kapat)

try:
    postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
                          password="123",
                          host="localhost",
                          port="5432",
                          database="postgres")
    if (postgreSQL_pool):
        print("Connection pool created successfully")
        print("Put away a PostgreSQL connection")
except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (postgreSQL_pool):
        postgreSQL_pool.closeall
    print("PostgreSQL connection pool is closed")
class yardimHakkimizda(QWidget):
    def __init__(self):
        super().__init__()
        ustBolum(self)

        horizontal = QHBoxLayout()
        Vertical = QVBoxLayout()

        baslik = QLabel("  About")
        baslik.setFont(baslikfont)
        yazi = QLabel("Welcome to the Library Project.\n\nMURAT SEVEN 201618957\nIŞILAY ŞEKEROĞLU 201619198 \nGÜLCAN BAĞCI 201614742 \nGAMZE NUR UZUN 201619726 \nHATİCE İLAYDA YILMAZLAR 201620210")
        yazi.setFont(yaziFont)
        Vertical.addWidget(baslik)
        Vertical.addStretch()
        Vertical.addWidget(yazi)
        Vertical.addStretch()

        horizontal.addStretch()
        horizontal.addLayout(Vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

    def geriDon(self):
        self.close()

class yeniOgrenci(QWidget):
    def __init__(self):
        super().__init__()

        def __init__(self):
            super().__init__()
            ustBolum(self)
            horizontal = QHBoxLayout()
            Vertical = QVBoxLayout()

            self.setWindowTitle("New a Student")
            baslik = QLabel("New a Book")
            baslik.setFont(baslikfont)

            self.Vertical = QVBoxLayout()

            baslik = QLabel("New a Student")
            baslik.setFont(baslikfont)

            ogrenciismi = QLineEdit()
            ogrenciismi.setPlaceholderText("Kitap numarasını Giriniz")
            ogrenciismi = QLineEdit()
            ogrenciismi.setPlaceholderText("Kitap İsmini Giriniz")
            ogrenciismi = QLineEdit()
            ogrenciismi.setPlaceholderText("Öğrenci İsmini Giriniz")
            ogrenciismi = QLineEdit()
            ogrenciismi.setPlaceholderText("Öğrenci İsmini Giriniz")

            kaydet = QPushButton("Save")
            kaydet.clicked.connect(self.kaydet)
            Vertical.addWidget(baslik)
            Vertical.addStretch()
            Vertical.addWidget(ogrenciismi)
            Vertical.addWidget(ogrenciismi)
            Vertical.addWidget(ogrenciismi)
            Vertical.addWidget(ogrenciismi)
            Vertical.addWidget(ogrenciismi)

            Vertical.addStretch()

            horizontal.addStretch()
            horizontal.addLayout(Vertical)
            horizontal.addStretch()

            self.setLayout(horizontal)

        def geriDon(self):
            self.close()

    def kaydet(self):
        kaydediliyor = QLabel("Kaydediliyor. Lütfen bekleyin...")
        self.Vertical.addWidget(kaydediliyor)
        QTest.qWait(750)
        if (postgreSQL_pool):
            print("Connection pool created successfully")
        ps_connection = postgreSQL_pool.getconn()
        isim = self.ogrenciismi.text()
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute("INSERT INTO ogrenciler (ogrenci_ad) VALUES (?)",(isim,))
        ps_connection = postgreSQL_pool.getconn()
        if (ps_connection):
            print("successfully recived connection from connection pool ")
            ps_cursor = ps_connection.cursor()
            ps_cursor.execute("select * from kitap")
            mobile_records = ps_cursor.fetchall()
        ps_cursor = ps_connection.cursor()
        isim = self.ogrenciismi.text()
        ps_cursor.execute("INSERT INTO ogrenciler (ogrenci_ad) VALUES (?)",(isim,))

        kaydediliyor.setText("Kayıt Başarılı !")
        QTest.qWait(500)
        self.close()

class ogrenciListesi(QWidget):
    def __init__(self):
        super().__init__()
        try:
            postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
                                                                 password="123",
                                                                 host="localhost",
                                                                 port="5432",
                                                                 database="postgres")

            if (postgreSQL_pool):
                print("Connection pool created successfully")
            ps_connection = postgreSQL_pool.getconn()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if (postgreSQL_pool):
                postgreSQL_pool.closeall
            print("PostgreSQL connection pool is closed")

        horizontal = QHBoxLayout()
        Vertical = QVBoxLayout()
        ustBolum(self)

        baslik = QLabel("STUDENTS")
        aciklama = QLabel("Name    -      Surname")
        aciklama.setFont(versionfont)
        aciklama.setStyleSheet("color: rgb(227,148,29)")
        baslik.setFont(baslikfont)
        liste = QListWidget()
        yeniEkle = QPushButton("New a Student")
        yeniEkle.setFont(butonFont)
        yeniEkle.clicked.connect(self.yeniEkle)
        if (ps_connection):
            print("successfully recived connection from connection pool ")
            ps_cursor = ps_connection.cursor()
            liste = QListWidget()

            ps_cursor.execute("select * from member")
            mobile_records = ps_cursor.fetchall()
            print("Displaying rows from mobile table")
            for row in mobile_records:
                liste.addItem(row[2]+row[1])
                liste.sortItems()
            ps_cursor.close()
            postgreSQL_pool.putconn(ps_connection)
            print("Put away a PostgreSQL connection")

        #liste.itemClicked.connect(self.kitapBilgi)

        Vertical.addWidget(baslik)
        Vertical.addWidget(aciklama)
        Vertical.addWidget(liste)
        Vertical.addWidget(yeniEkle)

        horizontal.addStretch()
        horizontal.addLayout(Vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

    def kitapBilgi(self,item):
        if (postgreSQL_pool):
            print("Connection pool created successfully")
        ps_connection = postgreSQL_pool.getconn()
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute("select * from books")
        ps_connection = postgreSQL_pool.getconn()
        if (ps_connection):
            print("successfully recived connection from connection pool ")
            ps_cursor = ps_connection.cursor()
        kitapismi = item.text()
        kontrol = ps_cursor.execute("SELECT * FROM books WHERE book_name = ?",(kitapismi,))
        durum = kontrol.fetchall()[0][2]

        if(durum==0):
            QMessageBox.information(self,"Kitap Bilgisi",kitapismi + " isimli kitap şu anda boşta !")
        else:
            kimde = ps_cursor.execute("SELECT * FROM books WHERE book_name = ?",(kitapismi,))
            ogrenci = kimde.fetchall()[0][1]
            QMessageBox.information(self,"Kitap Bilgisi",kitapismi + " isimli kitap şu anda ")

    def yeniEkle(self):

        self.yeni = yeniKitap()
        self.yeni.showFullScreen()


    def geriDon(self):
        self.close()

class oduncListesi(QWidget):
    def __init__(self):
        super().__init__()

        try:
            postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
                                                                 password="123",
                                                                 host="localhost",
                                                                 port="5432",
                                                                 database="postgres")

            if (postgreSQL_pool):
                print("Connection pool created successfully")
            ps_connection = postgreSQL_pool.getconn()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if (postgreSQL_pool):
                postgreSQL_pool.closeall
            print("PostgreSQL connection pool is closed")

        horizontal = QHBoxLayout()
        Vertical = QVBoxLayout()
        ustBolum(self)

        baslik = QLabel("LOAN")
        baslik.setFont(baslikfont)
        liste = QListWidget()
        yeniEkle = QPushButton("Add a New Loan")
        iadeEkle = QPushButton("Add a New Return")
        yeniEkle.setFont(butonFont)
        iadeEkle.setFont(butonFont)
        yeniEkle.clicked.connect(self.yeniEkle)
        if (ps_connection):
            print("successfully recived connection from connection pool ")
            ps_cursor = ps_connection.cursor()
            liste = QListWidget()
            ps_cursor.execute("select * from borrow")
            mobile_records = ps_cursor.fetchall()
            print("Displaying rows from mobile table")
            for row in mobile_records:
                liste.addItem("NAME:    "+row[6]+" "+" BOOK NAME:     " +row[5])
            ps_cursor.close()
            postgreSQL_pool.putconn(ps_connection)
            print("Put away a PostgreSQL connection")

        Vertical.addWidget(baslik)
        Vertical.addWidget(liste)
        Vertical.addWidget(yeniEkle)
        Vertical.addWidget(iadeEkle)

        horizontal.addStretch()
        horizontal.addLayout(Vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

    def kitapBilgi(self, item):
        if (postgreSQL_pool):
            print("Connection pool created successfully")
        ps_connection = postgreSQL_pool.getconn()
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute("select * from BORROW")
        ps_connection = postgreSQL_pool.getconn()
        if (ps_connection):
            print("successfully recived connection from connection pool ")
            ps_cursor = ps_connection.cursor()
        kitapismi = item.text()
        kontrol = ps_cursor.execute("SELECT * FROM BORROW WHERE BOOK_NAME = ?", (kitapismi,))
        durum = kontrol.fetchall()[0][2]

        if (durum == 0):
            QMessageBox.information(self, "Information", kitapismi + " is not in one.!")
        else:
            kimde = ps_cursor.execute("SELECT * FROM BORROW WHERE BOOK_NAME = ?", (kitapismi,))
            ogrenci = kimde.fetchall()[0][1]
            QMessageBox.information(self, "Information", kitapismi + " isimli kitap şu anda ")

    def yeniEkle(self):

        self.yeni = yeniKitap()
        self.yeni.showFullScreen()

    def geriDon(self):
        self.close()

class Pencere(QWidget):

    def __init__(self):
        super().__init__()

        self.giris = intro()
        self.giris.showFullScreen()

        QTest.qWait(1000)

        kapatButon = QPushButton("X", self)
        kapatButon.setFont(baslikfont)
        kapatButon.setGeometry(1300, 20, 50, 50)
        kapatButon.clicked.connect(self.kapat)

        horizontal = QHBoxLayout()
        Vertical = QVBoxLayout()

        baslik = QLabel("The Library Center")
        baslik.setFont(baslikfont)
        baslik.setStyleSheet("color: rgb(227,148,29)")

        kitapButon = QPushButton("BOOKS")
        ogrenciButon = QPushButton("STUDENTS")
        islemlerButon = QPushButton("LOAN")
        yardimButon = QPushButton("ABOUT")

        kitapButon.setFont(butonFont)
        ogrenciButon.setFont(butonFont)
        islemlerButon.setFont(butonFont)
        yardimButon.setFont(butonFont)
        kitapButon.setStyleSheet("background-color: #474787;color:rgb(255,255,255)")
        ogrenciButon.setStyleSheet("background-color: #474787;color:rgb(255,255,255)")
        islemlerButon.setStyleSheet("background-color: #474787;color:rgb(255,255,255)")
        yardimButon.setStyleSheet("background-color: rgb(221,148,29);color:rgb(255,255,255)")

        kitapButon.clicked.connect(self.kitapAc)
        ogrenciButon.clicked.connect(self.ogrenciAc)
        islemlerButon.clicked.connect(self.islemAc)
        yardimButon.clicked.connect(self.yardimAc)

        Vertical.addWidget(baslik)
        Vertical.addStretch()
        Vertical.addWidget(kitapButon)
        Vertical.addStretch()
        Vertical.addWidget(ogrenciButon)
        Vertical.addStretch()
        Vertical.addWidget(islemlerButon)
        Vertical.addStretch()
        Vertical.addWidget(yardimButon)

        horizontal.addStretch()
        horizontal.addLayout(Vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

        self.showFullScreen()

    def kitapAc(self):
        self.kitap = kitapListesi()
        self.kitap.showFullScreen()

    def kitapAc(self):
        self.kitap = kitapListesi()
        self.kitap.showFullScreen()
    def ogrenciAc(self):
        self.ogrenci = ogrenciListesi()
        self.ogrenci.showFullScreen()
    def islemAc(self):
        self.islem = oduncListesi()
        self.islem.showFullScreen()
    def yardimAc(self):
        self.yardim = yardimHakkimizda()
        self.yardim.showFullScreen()
    def kapat(self):
        qApp.quit()


uygulama = QApplication(sys.argv)
pencere = Pencere()
sys.exit(uygulama.exec_())