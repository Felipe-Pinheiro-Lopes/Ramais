from PyQt5 import uic,QtWidgets, QtCore, QtGui
import _sqlite3

# Conexão com o Banco de Dados
con = _sqlite3.connect('Ramais.db')
cursor = con.cursor()

#Função de Lista 
def funcao_listar():
    cursor.execute("SELECT r.ID, n.Nome, t.Numeros, s.Nome, r.Observacao FROM Ramais r JOIN Nomes n ON r.Nome = n.ID JOIN Telefones t ON r.Telefone = t.ID JOIN Setor s ON r.Setor = s.ID")
    resultados = cursor.fetchall()

    formulario.tableWidget.setRowCount(len(resultados))
    formulario.tableWidget.setColumnCount(5)

    for i, row in enumerate(resultados):
        for j, col in enumerate(row):
            formulario.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(col)))

#Funções para obiter os IDs das tabelas extrangeiras 
def obter_id_setor(setor):
    
    cursor.execute(f"SELECT id FROM Setor WHERE Nome = '{setor}'")
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        cursor.execute(f"INSERT INTO Setor (Nome) VALUES ('{setor}')")
        con.commit()
        return cursor.lastrowid

def obter_id_telefone(telefone):
    
    cursor.execute(f"SELECT id FROM Telefones WHERE Numeros = '{telefone}'")
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        cursor.execute(f"INSERT INTO Telefones (Numeros) VALUES ('{telefone}')")
        con.commit()
        return cursor.lastrowid

def obter_id_nome(nome):
    
    cursor.execute(f"SELECT id FROM Nomes WHERE Nome = '{nome}'")
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        cursor.execute(f"INSERT INTO Nomes (Nome) VALUES ('{nome}')")
        con.commit()
        return cursor.lastrowid

#Função de Cadastro 
def funcao_principal():
    nome = formulario.lineEdit.text()
    telefone = formulario.lineEdit_2.text()
    observacao = formulario.lineEdit_3.text()
    setor = formulario.lineEdit_4.text().upper()
    id_setor = obter_id_setor(setor)
    id_telefone = obter_id_telefone(telefone)
    id_nome = obter_id_nome(nome)

    cursor.execute(f"SELECT * FROM Ramais WHERE Nome='{id_nome}' AND Telefone='{id_telefone}' AND Setor='{id_setor}'")
    resultado = cursor.fetchone()
    if resultado:
        QtWidgets.QMessageBox.warning(formulario, 'Aviso', 'Já existe um ramal com esses valores!')
        return

    cursor.execute(f"INSERT INTO Ramais (Nome, Telefone, Observacao, Setor) VALUES ('{id_nome}', '{id_telefone}', '{observacao}', '{id_setor}')")
    con.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")
    formulario.lineEdit_4.setText("")

#Função de mostrar ramais existentes
def funcao_mostrar_setores():
    lista_de_ramal.show()
    cursor.execute("SELECT Nome FROM Setor")
    resultados = cursor.fetchall()

    lista_de_ramal.tableWidget.setRowCount(len(resultados))
    lista_de_ramal.tableWidget.setColumnCount(1)

    for i, row in enumerate(resultados):
        for j, col in enumerate(row):
            lista_de_ramal.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(col)))

#Funções para obiter os valores das tabelas extrangeiras 
def obter_nome_setor(id_setor):
    cursor.execute(f"SELECT Nome FROM Setor WHERE id = {id_setor}")
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        return None
    
def obter_numero_telefone(id_telefone):
    cursor.execute(f"SELECT Numeros FROM Telefones WHERE id = {id_telefone}")
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        return None
    
def obter_nome_nome(id_nome):
    cursor.execute(f"SELECT Nome FROM Nomes WHERE id = {id_nome}")
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        return None

#Função de Pesquisa
def funcao_pesquisar():
    ramal = formulario.lineEdit_13.text()
    cursor.execute(f"SELECT * FROM Ramais INNER JOIN Nomes ON Ramais.Nome=Nomes.ID INNER JOIN Telefones ON Ramais.Telefone=Telefones.ID INNER JOIN Setor ON Ramais.Setor=Setor.ID WHERE Nomes.nome LIKE '%{ramal}%' OR Telefones.numeros LIKE '%{ramal}%'")
    resultado = cursor.fetchone()
    formulario.lineEdit_13.setText("")
    if resultado:
        formulario.lineEdit_9.setText(obter_nome_nome(resultado[1]))
        formulario.lineEdit_10.setText(obter_numero_telefone(resultado[2]))
        formulario.lineEdit_11.setText(obter_nome_setor(resultado[3]))
        formulario.lineEdit_12.setText(resultado[4])
    else:
        QtWidgets.QMessageBox.warning(formulario, 'Aviso', 'Ramal não encontrado!')

#Função de Edição do Banco
def funcao_editar_ramal():
    editar_ramal.show()

    linha_selecionada = formulario.tableWidget.currentRow()
    if linha_selecionada < 0:
        QtWidgets.QMessageBox.warning(formulario, 'Aviso', 'Selecione um registro para excluir!')
        return

    editar_ramal.lineEdit_5.setText(formulario.tableWidget.item(linha_selecionada, 0).text())
    editar_ramal.lineEdit.setText(formulario.tableWidget.item(linha_selecionada, 1).text())
    editar_ramal.lineEdit_2.setText(formulario.tableWidget.item(linha_selecionada, 2).text())
    editar_ramal.lineEdit_3.setText(formulario.tableWidget.item(linha_selecionada, 3).text())
    editar_ramal.lineEdit_4.setText(formulario.tableWidget.item(linha_selecionada, 4).text())

#Função para salvar a alteração de ramal
def salvar_alteracoes():
    id = editar_ramal.lineEdit_5.text()
    nome = editar_ramal.lineEdit.text()
    telefone = editar_ramal.lineEdit_2.text()
    setor = editar_ramal.lineEdit_3.text().upper()
    observacao = editar_ramal.lineEdit_4.text()

    id_setor = obter_id_setor(setor)
    id_telefone = obter_id_telefone(telefone)
    id_nome = obter_id_nome(nome)

    cursor.execute(f"SELECT * FROM Ramais WHERE Nome='{id_nome}' AND Telefone='{id_telefone}' AND Setor='{id_setor}'")
    resultado = cursor.fetchone()
    if resultado:
        QtWidgets.QMessageBox.warning(formulario, 'Aviso', 'Já existe um ramal com esses valores!')
        return

    cursor.execute(f"UPDATE Ramais SET Nome='{id_nome}', Telefone='{id_telefone}', Observacao='{observacao}', Setor='{id_setor}' WHERE id = {id}")
    con.commit()

    editar_ramal.hide()
    funcao_listar()

#Função para Exclusão do Banco
def funcao_excluir_ramal():
    # Obtém a linha selecionada na tabela
    linha_selecionada = formulario.tableWidget.currentRow()

    # Verifica se alguma linha foi selecionada
    if linha_selecionada < 0:
        QtWidgets.QMessageBox.warning(formulario, 'Aviso', 'Selecione um registro para excluir!')
        return

    # Obtém o valor do ID na coluna 0 da linha selecionada
    id_ramal = formulario.tableWidget.item(linha_selecionada, 0).text()

    # Exclui o registro correspondente na tabela Ramais
    cursor.execute(f"DELETE FROM Ramais WHERE Id='{id_ramal}'")
    con.commit()

    funcao_listar()


app=QtWidgets.QApplication([])
formulario=uic.loadUi("untitled.ui") #Carrega o Visual
lista_de_ramal=uic.loadUi("listaderamal.ui") #Carrega o Visual
editar_ramal=uic.loadUi("editar.ui") #Carrega o Visual
formulario.pushButton.clicked.connect(funcao_principal)         # Botão para Cadastro
formulario.pushButton_3.clicked.connect(funcao_pesquisar)       # Botão para Pesquisa
formulario.pushButton_4.clicked.connect(funcao_mostrar_setores) # Botão para Mostrar todos os Setores cadastrados
formulario.pushButton_7.clicked.connect(funcao_listar)          # Botão para Listar
formulario.pushButton_9.clicked.connect(funcao_editar_ramal)    # Botão para Editar
formulario.pushButton_8.clicked.connect(funcao_excluir_ramal)   # Botão para Excluir
editar_ramal.pushButton_10.clicked.connect(salvar_alteracoes)   # Botão para Salvar Edição

#Validadores
validator = QtGui.QIntValidator()
formulario.lineEdit_2.setValidator(validator)
editar_ramal.lineEdit_2.setValidator(validator)

nome_validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[A-Za-z ]+"))
formulario.lineEdit.setValidator(nome_validator)
formulario.lineEdit_4.setValidator(nome_validator)
editar_ramal.lineEdit.setValidator(nome_validator)

class validar_setor(QtGui.QValidator):
    def validate(self, text, pos):
        if text:
            for char in text:
                if not char.isalpha() and char != '/':
                    return (QtGui.QValidator.Invalid, text, pos)
        return (QtGui.QValidator.Acceptable, text, pos)
setor_validator = validar_setor()
formulario.lineEdit_4.setValidator(setor_validator)
editar_ramal.lineEdit_3.setValidator(setor_validator)

formulario.lineEdit_9.setReadOnly(True)
formulario.lineEdit_10.setReadOnly(True)
formulario.lineEdit_11.setReadOnly(True)
formulario.lineEdit_12.setReadOnly(True)
editar_ramal.lineEdit_5.setReadOnly(True)

formulario.show()
app.exec()

# Banco de Dados = SQLite3
# Visual = PyQt5 ("Qt Designer")
# Python 3.11.3