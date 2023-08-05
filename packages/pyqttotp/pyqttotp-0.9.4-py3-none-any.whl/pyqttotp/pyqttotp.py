import pyqttotp
import sys
from io import BytesIO

from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtGui import QPixmap

import pyotp
import qrcode
from PIL import Image


class QrCodeForm(QDialog):

    def __init__(self, parent=None):
        super(QrCodeForm, self).__init__(parent)
        self.setWindowTitle("PyQtTOTP Generator")
        self.edit_token = QLineEdit("")
        self.edit_name = QLineEdit("")
        self.edit_issuer_name = QLineEdit("")
        self.button = QPushButton("Generate QrCode")
        self.label = QLabel()
        self.label_token = QLabel()
        self.label_token.setText("Token")
        self.label_name = QLabel()
        self.label_name.setText("Name")
        self.label_issuer_name = QLabel()
        self.label_issuer_name.setText("Issuer name (optional)")
        layout = QVBoxLayout()
        layout.addWidget(self.label_token)
        layout.addWidget(self.edit_token)
        layout.addWidget(self.label_name)
        layout.addWidget(self.edit_name)
        layout.addWidget(self.label_issuer_name)
        layout.addWidget(self.edit_issuer_name)
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.button.clicked.connect(self.gen_token)
        buf = BytesIO()
        img = Image.new('RGB', (490, 490), color='red')
        img.save(buf, "PNG")

        qt_pixmap = QPixmap()
        qt_pixmap.loadFromData(buf.getvalue(), "PNG")
        self.label.setPixmap(qt_pixmap)

    def gen_token(self):
        buf = BytesIO()

        img = qrcode.make(pyotp.totp.TOTP(
            self.edit_token.text()
        ).provisioning_uri(
            self.edit_name.text(), self.edit_issuer_name.text()
        ))
        img.save(buf, "PNG")

        qt_pixmap = QPixmap()
        qt_pixmap.loadFromData(buf.getvalue(), "PNG")
        self.label.setPixmap(qt_pixmap)

def main():
    app = QApplication(sys.argv)
    form = QrCodeForm()
    form.show()
    sys.exit(app.exec_())   

if __name__ == '__main__':
    main()

