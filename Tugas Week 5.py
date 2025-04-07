import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QHBoxLayout, QLineEdit,
    QTextEdit, QComboBox, QPushButton, QMessageBox, QDateEdit
)
from PyQt5.QtCore import QDate, Qt

class FormValidation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Form Validation : F1D022145 - Muhammad Fiqri Jordy Ardianto")
        self.setGeometry(100, 100, 631, 600)
        self.setupUI()

    def setupUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.setSpacing(10)

        self.nama = QLineEdit()
        self.nim = QLineEdit()
        self.kelas = QLineEdit()
        self.email = QLineEdit()
        self.tempat_lahir = QLineEdit()
        self.tanggal_lahir = QDateEdit()
        self.usia = QLineEdit()
        self.nomor_hp = QLineEdit()
        self.alamat = QTextEdit()
        self.jenis_kelamin = QComboBox()
        self.pendidikan = QComboBox()

        self.tanggal_lahir.setCalendarPopup(True)
        self.tanggal_lahir.setDisplayFormat("dd-MM-yyyy")
        self.tanggal_lahir.setSpecialValueText("Pilih tanggal")
        self.tanggal_lahir.setDateRange(QDate(1998, 1, 1), QDate.currentDate())
        self.tanggal_lahir.setDate(self.tanggal_lahir.minimumDate())

        self.nomor_hp.setInputMask("+62 000 0000 0000;_")
        self.nomor_hp.setPlaceholderText("+62 999 9999 9999")

        self.jenis_kelamin.addItems(["Laki-Laki", "Perempuan"])
        self.jenis_kelamin.setCurrentIndex(-1)
        self.pendidikan.addItems(["SMA/SMK Sederajat", "Diploma (D2/D3)", "Sarjana (S1/D4)", "Magister (S2)", "Doktor(S3)"])
        self.pendidikan.setCurrentIndex(-1)

        for widget in [
            self.nama, self.nim, self.kelas, self.email, self.tempat_lahir,
            self.tanggal_lahir, self.usia, self.nomor_hp, self.jenis_kelamin, self.pendidikan
        ]:
            widget.setFixedWidth(280)
        self.alamat.setFixedWidth(280)

        layout.addRow("Nama :", self.nama)
        layout.addRow("NIM :", self.nim)
        layout.addRow("Kelas :", self.kelas)
        layout.addRow("Email :", self.email)
        layout.addRow("Tempat Lahir :", self.tempat_lahir)
        layout.addRow("Tanggal Lahir :", self.tanggal_lahir)
        layout.addRow("Usia :", self.usia)
        layout.addRow("Nomor Telepon :", self.nomor_hp)
        layout.addRow("Alamat :", self.alamat)
        layout.addRow("Jenis Kelamin :", self.jenis_kelamin)
        layout.addRow("Pendidikan :", self.pendidikan)

        self.btn_simpan = QPushButton("Simpan")
        self.btn_bersihkan = QPushButton("Bersihkan")
        self.btn_simpan.setFixedSize(100, 30)
        self.btn_bersihkan.setFixedSize(100, 30)

        self.btn_simpan.clicked.connect(self.validasi)
        self.btn_bersihkan.clicked.connect(self.bersihkan)

        tombol_layout = QHBoxLayout()
        tombol_layout.setAlignment(Qt.AlignCenter)
        tombol_layout.setSpacing(30)
        tombol_layout.addWidget(self.btn_simpan)
        tombol_layout.addWidget(self.btn_bersihkan)
        layout.addRow(tombol_layout)

        self.setLayout(layout)

    def validasi(self):
        nama = self.nama.text().strip()
        nim = self.nim.text().strip()
        kelas = self.kelas.text().strip()
        email = self.email.text().strip()
        tempat = self.tempat_lahir.text().strip()
        tanggal = self.tanggal_lahir.date()
        usia = self.usia.text().strip()
        hp = self.nomor_hp.text()
        alamat = self.alamat.toPlainText().strip()
        gender = self.jenis_kelamin.currentText()
        pendidikan = self.pendidikan.currentText()

        if not nama:
            return self.pesan("Nama harus diisi.")
        if not nama.replace(" ", "").isalpha():
            return self.pesan("Nama hanya boleh diisi huruf.")

        if not nim:
            return self.pesan("NIM harus diisi.")
        ada_angka = any(c.isdigit() for c in nim)
        ada_huruf = any(c.isalpha() for c in nim)
        if not (ada_angka and ada_huruf):
            return self.pesan("NIM harus mengandung huruf dan angka.")

        if not kelas:
            return self.pesan("Kelas harus diisi.")
        if len(kelas) != 1 or not kelas.isalpha() or not kelas.isupper():
            return self.pesan("Kelas hanya boleh 1 huruf kapital, tidak boleh angka dan huruf kecil.")

        if not email:
            return self.pesan("Email harus diisi.")
        pola_email = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(pola_email, email):
            return self.pesan("Format email tidak valid.")

        if not tempat:
            return self.pesan("Tempat lahir harus diisi.")
        if not tempat.replace(" ", "").isalpha():
            return self.pesan("Tempat lahir hanya boleh diisi huruf.")

        if tanggal == self.tanggal_lahir.minimumDate():
            return self.pesan("Tanggal lahir harus diisi.")

        if not usia:
            return self.pesan("Usia harus diisi.")
        if not usia.isdigit():
            return self.pesan("Usia hanya boleh diisi angka.")

        if not hp or "_" in hp or hp.replace(" ", "") == "+62":
            return self.pesan("Nomor HP harus diisi lengkap.")

        digit_hp = hp.replace("+62", "").replace(" ", "")
        if len(digit_hp) != 11:
            return self.pesan("Harus 11 digit angka setelah +62")
        if not digit_hp.isdigit():
            return self.pesan("Nomor HP hanya boleh berisi angka")

        if not alamat:
            return self.pesan("Alamat harus diisi.")
        if not alamat.replace(" ", "").isalpha():
            return self.pesan("Alamat hanya boleh diisi huruf.")

        if not gender:
            return self.pesan("Jenis kelamin harus dipilih.")
        if not pendidikan:
            return self.pesan("Pendidikan harus dipilih.")

        self.pesan("Data diri berhasil disimpan!", success=True)

    def bersihkan(self):
        self.nama.clear()
        self.nim.clear()
        self.kelas.clear()
        self.email.clear()
        self.tempat_lahir.clear()
        self.tanggal_lahir.setDate(self.tanggal_lahir.minimumDate())
        self.usia.clear()
        self.nomor_hp.clear()
        self.alamat.clear()
        self.jenis_kelamin.setCurrentIndex(-1)
        self.pendidikan.setCurrentIndex(-1)

    def pesan(self, isi, success=False):
        msg = QMessageBox()
        msg.setText(isi)
        msg.setIcon(QMessageBox.Information if success else QMessageBox.Warning)
        msg.setWindowTitle("Info" if success else "Peringatan")
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormValidation()
    window.show()
    sys.exit(app.exec_())
