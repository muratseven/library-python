import psycopg2
from psycopg2 import pool
import sys
import PyQt5.QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtTest import *

try:
    postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
                                                         password="1234",
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

baslikfont = QFont("Century Gothic", 38)
versionfont = QFont("Century Gothic", 15)
butonFont = QFont("Century Gothic", 20)
yaziFont = QFont("Century Gothic", 18)


class intro(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        horizontal = PyQt5.QtWidgets.QHBoxLayout()

        self.yazi = PyQt5.QtWidgets.QLabel("Library Project ")
        self.yaziversion = PyQt5.QtWidgets.QLabel("V1.0")

        horizontal.addStretch()
        horizontal.addWidget(self.yazi)
        horizontal.addWidget(self.yaziversion)
        horizontal.addStretch()

        self.yazi.setFont(baslikfont)
        self.yaziversion.setFont(versionfont)
        self.setLayout(horizontal)


class kitapListesi(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        try:
            postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
                                                                 password="1234",
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

        horizontal = PyQt5.QtWidgets.QHBoxLayout()
        Vertical = PyQt5.QtWidgets.QVBoxLayout()
        ustBolum(self)

        baslik = PyQt5.QtWidgets.QLabel("BOOKS")
        aciklama = PyQt5.QtWidgets.QLabel("Book Name")
        aciklama.setFont(versionfont)
        aciklama.setStyleSheet("color: rgb(227,148,29)")
        baslik.setFont(baslikfont)
        liste = PyQt5.QtWidgets.QListWidget()
        yeniEkle = PyQt5.QtWidgets.QPushButton("New a Boook")
        yeniEkle.setFont(butonFont)
        yeniEkle.clicked.connect(self.yeniEkle)
        if (ps_connection):
            print("successfully received connection from connection pool ")
            ps_cursor = ps_connection.cursor()
            liste = PyQt5.QtWidgets.QListWidget()

            ps_cursor.execute("select * from books")
            mobile_records = ps_cursor.fetchall()
            print("Displaying rows from mobile table")
            for row in mobile_records:
                liste.addItem(row[6])
                liste.sortItems()

            ps_cursor.close()
            postgreSQL_pool.putconn(ps_connection)
            print("Put away a PostgreSQL connection")
        # liste.itemClicked.connect(self.kitapBilgi)

        Vertical.addWidget(baslik)
        Vertical.addWidget(aciklama)
        Vertical.addWidget(liste)
        Vertical.addWidget(yeniEkle)

        horizontal.addStretch()
        horizontal.addLayout(Vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

    def kitapBilgi(self, item):
        if (postgreSQL_pool):
            print("Connection pool created successfully")
        ps_connection = postgreSQL_pool.getconn()
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute("select * from kitap")
        ps_connection = postgreSQL_pool.getconn()
        if (ps_connection):
            print("successfully received connection from connection pool ")
            ps_cursor = ps_connection.cursor()
        kitapismi = item.text()
        kontrol = ps_cursor.execute("SELECT * FROM kitap WHERE kadi = ?", (kitapismi,))
        durum = kontrol.fetchall()[0][2]

        if (durum == 0):
            PyQt5.QtWidgets.QMessageBox.information(self, "Kitap Bilgisi", kitapismi + " isimli kitap şu anda boşta !")
        else:
            kimde = ps_cursor.execute("SELECT * FROM kitap WHERE kadi = ?", (kitapismi,))
            ogrenci = kimde.fetchall()[0][1]
            print("heree", ogrenci)
            PyQt5.QtWidgets.QMessageBox.information(self, "Kitap Bilgisi", kitapismi + " isimli kitap şu anda ")

    def yeniEkle(self):

        self.yeni = yeniKitap()
        self.yeni.showFullScreen()

    def geriDon(self):
        self.close()


class yeniKitap(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        ustBolum(self)
        horizontal = PyQt5.QtWidgets.QHBoxLayout()
        Vertical = PyQt5.QtWidgets.QVBoxLayout()

        self.setWindowTitle("Yeni Öğrenci Ekle")
        baslik = PyQt5.QtWidgets.QLabel("Kitap Ekle")
        baslik.setFont(baslikfont)

        self.Vertical = PyQt5.QtWidgets.QVBoxLayout()

        baslik = PyQt5.QtWidgets.QLabel("New a Book")
        aciklama = PyQt5.QtWidgets.QLabel("Fill in The Information Below to Add a New Book.")
        baslik.setFont(baslikfont)
        aciklama.setFont(yaziFont)

        bookid = PyQt5.QtWidgets.QLineEdit()
        bookid.setPlaceholderText("Enter a Book ID")
        editionNumber = PyQt5.QtWidgets.QLineEdit()
        editionNumber.setPlaceholderText("Enter Edition Number ")
        pageNumber = PyQt5.QtWidgets.QLineEdit()
        pageNumber.setPlaceholderText("Enter Page Number")
        ISBN = PyQt5.QtWidgets.QLineEdit()
        ISBN.setPlaceholderText("Enter ISBN")
        editionYear = PyQt5.QtWidgets.QLineEdit()
        editionYear.setPlaceholderText("Enter Edition Year")
        ArrivalDate = PyQt5.QtWidgets.QLineEdit()
        ArrivalDate.setPlaceholderText("Enter Arrival Date")
        bookName = PyQt5.QtWidgets.QLineEdit()
        bookName.setPlaceholderText("Enter a Book Name")
        languageNo = PyQt5.QtWidgets.QLineEdit()
        languageNo.setPlaceholderText("Enter a Language Number")
        companyNo = PyQt5.QtWidgets.QLineEdit()
        companyNo.setPlaceholderText("Enter Company No")
        category = PyQt5.QtWidgets.QLineEdit()
        category.setPlaceholderText("Enter Category No")
        authorNo = PyQt5.QtWidgets.QLineEdit()
        authorNo.setPlaceholderText("Enter Author No")
        memberNo = PyQt5.QtWidgets.QLineEdit()
        memberNo.setPlaceholderText("Enter Member No")

        save = PyQt5.QtWidgets.QPushButton("Save")
        save.clicked.connect(self.save)
        Vertical.addWidget(baslik)
        Vertical.addWidget(aciklama)

        Vertical.addStretch()

        Vertical.addWidget(bookid)
        Vertical.addWidget(editionNumber)
        Vertical.addWidget(pageNumber)
        Vertical.addWidget(ISBN)
        Vertical.addWidget(editionYear)
        Vertical.addWidget(ArrivalDate)
        Vertical.addWidget(bookName)
        Vertical.addWidget(languageNo)
        Vertical.addWidget(companyNo)
        Vertical.addWidget(category)
        Vertical.addWidget(authorNo)
        Vertical.addWidget(memberNo)

        Vertical.addStretch()
        Vertical.addWidget(save)
        Vertical.addStretch()

        horizontal.addStretch()
        horizontal.addLayout(Vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

    def geriDon(self):
        self.close()

    def save(self):
        kaydediliyor = PyQt5.QtWidgets.QLabel("Kaydediliyor. Lütfen bekleyin...")
        self.Vertical.addWidget(kaydediliyor)
        QTest.qWait(750)
        BOOKID = self.kitapismi.text()
        editionNumber = self.editionNumber.text()
        pageNumber = self.pageNumber.text()
        ISBN = self.ISBN.text()
        editionYear = self.editionYear.text()
        ArrivalDate = self.ArrivalDate.text()
        bookName = self.bookName.text()
        languageNo = self.languageNo.text()
        companyNo = self.companyNo.text()
        category = self.category.text()
        authorNo = self.authorNo.text()
        memberNo = self.memberNo.text()
        ps_connection = postgreSQL_pool.getconn()
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute(
            "INSERT INTO BOOKS (book_id,editionNumber,pageNumber,ISBN,editionYear,ArrivalDate,bookName,languageNo,companyNo,category,authorNo,memberNo) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (BOOKID, editionNumber, pageNumber, ISBN, editionYear, ArrivalDate, bookName, languageNo, companyNo,
             category, authorNo, memberNo))
        kaydediliyor.setText("Registration Successful !")
        QTest.qWait(500)
        self.close()


def ustBolum(mevcutPencere):
    geriButon = PyQt5.QtWidgets.QPushButton("<", mevcutPencere)
    geriButon.setFont(baslikfont)
    geriButon.setGeometry(20, 20, 50, 50)
    geriButon.clicked.connect(mevcutPencere.geriDon)

    kapatButon = PyQt5.QtWidgets.QPushButton("X", mevcutPencere)
    kapatButon.setFont(baslikfont)
    kapatButon.setGeometry(1300, 20, 50, 50)
    kapatButon.clicked.connect(Pencere.kapat)


try:
    postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
                                                         password="1234",
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


class yardimHakkimizda(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        ustBolum(self)

        horizontal = PyQt5.QtWidgets.QHBoxLayout()
        Vertical = PyQt5.QtWidgets.QVBoxLayout()

        baslik = PyQt5.QtWidgets.QLabel("  About")
        baslik.setFont(baslikfont)
        yazi = PyQt5.QtWidgets.QLabel(
            "Welcome to the Library Project.\n\nMURAT SEVEN 201618957\nIŞILAY ŞEKEROĞLU 201619198 \nGÜLCAN BAĞCI 201614742 \nGAMZE NUR UZUN 201619726 \nHATİCE İLAYDA YILMAZLAR 201620210")
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


class yeniOgrenci(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        def __init__(self):
            super().__init__()
            ustBolum(self)
            horizontal = PyQt5.QtWidgets.QHBoxLayout()
            Vertical = PyQt5.QtWidgets.QVBoxLayout()

            self.setWindowTitle("New a Student")
            baslik = PyQt5.QtWidgets.QLabel("New a Book")
            baslik.setFont(baslikfont)

            self.Vertical = PyQt5.QtWidgets.QVBoxLayout()

            baslik = PyQt5.QtWidgets.QLabel("New a Student")
            baslik.setFont(baslikfont)

            ogrenciismi = PyQt5.QtWidgets.QLineEdit()
            ogrenciismi.setPlaceholderText("Kitap numarasını Giriniz")
            ogrenciismi = PyQt5.QtWidgets.QLineEdit()
            ogrenciismi.setPlaceholderText("Kitap İsmini Giriniz")
            ogrenciismi = PyQt5.QtWidgets.QLineEdit()
            ogrenciismi.setPlaceholderText("Öğrenci İsmini Giriniz")
            ogrenciismi = PyQt5.QtWidgets.QLineEdit()
            ogrenciismi.setPlaceholderText("Öğrenci İsmini Giriniz")

            save = PyQt5.QtWidgets.QPushButton("Save")
            save.clicked.connect(self.save)
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

    def save(self):
        kaydediliyor = PyQt5.QtWidgets.QLabel("Kaydediliyor. Lütfen bekleyin...")
        self.Vertical.addWidget(kaydediliyor)
        QTest.qWait(750)
        if (postgreSQL_pool):
            print("Connection pool created successfully")
        ps_connection = postgreSQL_pool.getconn()
        isim = self.ogrenciismi.text()
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute("INSERT INTO ogrenciler (ogrenci_ad) VALUES (?)", (isim,))
        ps_connection = postgreSQL_pool.getconn()
        if (ps_connection):
            print("successfully received connection from connection pool ")
            ps_cursor = ps_connection.cursor()
            ps_cursor.execute("select * from kitap")
            mobile_records = ps_cursor.fetchall()
        ps_cursor = ps_connection.cursor()
        isim = self.ogrenciismi.text()
        ps_cursor.execute("INSERT INTO ogrenciler (ogrenci_ad) VALUES (?)", (isim,))

        kaydediliyor.setText("Kayıt Başarılı !")
        QTest.qWait(500)
        self.close()


class ogrenciListesi(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        try:
            postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
                                                                 password="1234",
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

        horizontal = PyQt5.QtWidgets.QHBoxLayout()
        Vertical = PyQt5.QtWidgets.QVBoxLayout()
        ustBolum(self)

        baslik = PyQt5.QtWidgets.QLabel("STUDENTS")
        aciklama = PyQt5.QtWidgets.QLabel("Name    -      Surname")
        aciklama.setFont(versionfont)
        aciklama.setStyleSheet("color: rgb(227,148,29)")
        baslik.setFont(baslikfont)
        liste = PyQt5.QtWidgets.QListWidget()
        yeniEkle = PyQt5.QtWidgets.QPushButton("New a Student")
        yeniEkle.setFont(butonFont)
        yeniEkle.clicked.connect(self.yeniEkle)
        if (ps_connection):
            print("successfully received connection from connection pool ")
            ps_cursor = ps_connection.cursor()
            liste = PyQt5.QtWidgets.QListWidget()

            ps_cursor.execute("select * from member")
            mobile_records = ps_cursor.fetchall()
            print("Displaying rows from mobile table")
            for row in mobile_records:
                liste.addItem(row[2] + row[1])
                liste.sortItems()
            ps_cursor.close()
            postgreSQL_pool.putconn(ps_connection)
            print("Put away a PostgreSQL connection")

        # liste.itemClicked.connect(self.kitapBilgi)

        Vertical.addWidget(baslik)
        Vertical.addWidget(aciklama)
        Vertical.addWidget(liste)
        Vertical.addWidget(yeniEkle)

        horizontal.addStretch()
        horizontal.addLayout(Vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

    def kitapBilgi(self, item):
        if (postgreSQL_pool):
            print("Connection pool created successfully")
        ps_connection = postgreSQL_pool.getconn()
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute("select * from books")
        ps_connection = postgreSQL_pool.getconn()
        if (ps_connection):
            print("successfully received connection from connection pool ")
            ps_cursor = ps_connection.cursor()
        kitapismi = item.text()
        kontrol = ps_cursor.execute("SELECT * FROM books WHERE book_name = ?", (kitapismi,))
        durum = kontrol.fetchall()[0][2]

        if (durum == 0):
            PyQt5.QtWidgets.QMessageBox.information(self, "Kitap Bilgisi", kitapismi + " isimli kitap şu anda boşta !")
        else:
            kimde = ps_cursor.execute("SELECT * FROM books WHERE book_name = ?", (kitapismi,))
            ogrenci = kimde.fetchall()[0][1]
            PyQt5.QtWidgets.QMessageBox.information(self, "Kitap Bilgisi", kitapismi + " isimli kitap şu anda ")

    def yeniEkle(self):

        self.yeni = yeniKitap()
        self.yeni.showFullScreen()

    def geriDon(self):
        self.close()


class oduncListesi(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        try:
            postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
                                                                 password="1234",
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

        horizontal = PyQt5.QtWidgets.QHBoxLayout()
        Vertical = PyQt5.QtWidgets.QVBoxLayout()
        ustBolum(self)

        baslik = PyQt5.QtWidgets.QLabel("LOAN")
        baslik.setFont(baslikfont)
        liste = PyQt5.QtWidgets.QListWidget()
        yeniEkle = PyQt5.QtWidgets.QPushButton("Add a New Loan")
        iadeEkle = PyQt5.QtWidgets.QPushButton("Add a New Return")
        yeniEkle.setFont(butonFont)
        iadeEkle.setFont(butonFont)
        yeniEkle.clicked.connect(self.yeniEkle)
        if (ps_connection):
            print("successfully received connection from connection pool ")
            ps_cursor = ps_connection.cursor()
            liste = PyQt5.QtWidgets.QListWidget()
            ps_cursor.execute("select * from borrow")
            mobile_records = ps_cursor.fetchall()
            print("Displaying rows from mobile table")
            for row in mobile_records:
                liste.addItem("NAME:    " + row[6] + " " + " BOOK NAME:     " + row[5])
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
            print("successfully received connection from connection pool ")
            ps_cursor = ps_connection.cursor()
        kitapismi = item.text()
        kontrol = ps_cursor.execute("SELECT * FROM BORROW WHERE BOOK_NAME = ?", (kitapismi,))
        durum = kontrol.fetchall()[0][2]

        if (durum == 0):
            PyQt5.QtWidgets.QMessageBox.information(self, "Information", kitapismi + " is not in one.!")
        else:
            kimde = ps_cursor.execute("SELECT * FROM BORROW WHERE BOOK_NAME = ?", (kitapismi,))
            ogrenci = kimde.fetchall()[0][1]
            PyQt5.QtWidgets.QMessageBox.information(self, "Information", kitapismi + " isimli kitap şu anda ")

    def yeniEkle(self):

        self.yeni = yeniKitap()
        self.yeni.showFullScreen()

    def geriDon(self):
        self.close()


class Pencere(PyQt5.QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.giris = intro()
        self.giris.showFullScreen()

        QTest.qWait(1000)

        kapatButon = PyQt5.QtWidgets.QPushButton("X", self)
        kapatButon.setFont(baslikfont)
        kapatButon.setGeometry(1300, 20, 50, 50)
        kapatButon.clicked.connect(self.kapat)

        horizontal = PyQt5.QtWidgets.QHBoxLayout()
        Vertical = PyQt5.QtWidgets.QVBoxLayout()

        baslik = PyQt5.QtWidgets.QLabel("The Library Center")
        baslik.setFont(baslikfont)
        baslik.setStyleSheet("color: rgb(227,148,29)")

        kitapButon = PyQt5.QtWidgets.QPushButton("BOOKS")
        ogrenciButon = PyQt5.QtWidgets.QPushButton("STUDENTS")
        islemlerButon = PyQt5.QtWidgets.QPushButton("LOAN")
        yardimButon = PyQt5.QtWidgets.QPushButton("ABOUT")

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
        PyQt5.QtWidgets.qApp.quit()


uygulama = PyQt5.QtWidgets.QApplication(sys.argv)
pencere = Pencere()
sys.exit(uygulama.exec_())
