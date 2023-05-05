from PyQt5 import uic,QtWidgets
import _sqlite3

con = _sqlite3.connect('Ramais.db')
cursor = con.cursor()

def obter_id_setor(setor):
    
    cursor.execute(f"SELECT id FROM Setor WHERE Nome = '{setor}'")
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        cursor.execute(f"INSERT INTO Setor (Nome) VALUES ('{setor}')")
        con.commit()
        return cursor.lastrowid
    
def funcao_principal():
    nome = formulario.lineEdit.text()
    telefone = formulario.lineEdit_2.text()
    observacao = formulario.lineEdit_3.text()
    setor = formulario.lineEdit_4.text().upper()
    id_setor = obter_id_setor(setor)
    cursor.execute(f"INSERT INTO Ramais (Nome, Telefone, Observacao, Setor) VALUES ('{nome}', '{telefone}', '{observacao}', '{id_setor}')")
    con.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")
    formulario.lineEdit_4.setText("")

def obter_nome_setor(id_setor):
    cursor.execute(f"SELECT Nome FROM Setor WHERE id = {id_setor}")
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        return None

def funcao_pesquisar():
    ramal = formulario.lineEdit_5.text()
    cursor.execute(f"SELECT * FROM Ramais WHERE nome LIKE '%{ramal}%'")
    resultado = cursor.fetchone()
    formulario.lineEdit_5.setText("")
    if resultado:
        formulario.lineEdit_6.setText(resultado[1])
        formulario.lineEdit_7.setText(resultado[2])
        formulario.lineEdit_8.setText(obter_nome_setor(resultado[3]))
        formulario.lineEdit_9.setText(resultado[4])
    else:
        QtWidgets.QMessageBox.warning(formulario, 'Aviso', 'Ramal não encontrado!')
    
app=QtWidgets.QApplication([])
formulario=uic.loadUi("untitled.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(funcao_pesquisar)

formulario.show()
app.exec()