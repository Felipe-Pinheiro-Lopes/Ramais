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

def funcao_pesquisar():
    ramal = formulario.lineEdit_5.text()
    cursor.execute(f"SELECT * FROM Ramais WHERE nomes='{ramal}'")
    resultado = cursor.fetchone()
    if resultado:
        formulario.lineEdit_6.setText(resultado[0])
        formulario.lineEdit_7.setText(resultado[1])
        formulario.lineEdit_8.setText(resultado[2])
        formulario.lineEdit_9.setText(resultado[3])
    else:
        QtWidgets.QMessageBox.warning(formulario, 'Aviso', 'Ramal não encontrado!')

app=QtWidgets.QApplication([])
formulario=uic.loadUi("untitled.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(funcao_pesquisar)

formulario.show()
app.exec()