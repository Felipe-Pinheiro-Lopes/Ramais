from PyQt5 import uic,QtWidgets
import _sqlite3

con = _sqlite3.connect('Ramais.db')
cursor = con.cursor()

def funcao_principal():
    nome = formulario.lineEdit.text()
    telefone = formulario.lineEdit_2.text()
    observacao = formulario.lineEdit_3.text()
    setor = formulario.lineEdit_4.text()

    cursor.execute(f"INSERT INTO Ramais VALUES ('{nome}', '{telefone}', '{setor}', '{observacao}')")
    con.commit()

app=QtWidgets.QApplication([])
formulario=uic.loadUi("untitled.ui")
formulario.pushButton.clicked.connect(funcao_principal)

formulario.show()
app.exec()