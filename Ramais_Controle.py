from PyQt5 import uic,QtWidgets, QtCore, QtGui
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path
import os, openpyxl, _sqlite3

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
            formulario.tableWidget.setColumnWidth(0, 2)
            formulario.tableWidget.setColumnWidth(1, 160)
            formulario.tableWidget.setColumnWidth(2, 50)
            formulario.tableWidget.setColumnWidth(4, 200)

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
    setor = formulario.comboBox.currentText()
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
    ramal = formulario.lineEdit_9.text()
    cursor.execute(f"SELECT * FROM Ramais INNER JOIN Nomes ON Ramais.Nome=Nomes.ID INNER JOIN Telefones ON Ramais.Telefone=Telefones.ID INNER JOIN Setor ON Ramais.Setor=Setor.ID WHERE Nomes.nome LIKE '%{ramal}%' OR Telefones.numeros LIKE '%{ramal}%'")
    resultado = cursor.fetchone()
    formulario.lineEdit_9.setText("")
    if resultado:
        formulario.lineEdit_5.setText(obter_nome_nome(resultado[1]))
        formulario.lineEdit_6.setText(obter_numero_telefone(resultado[2]))
        formulario.lineEdit_7.setText(obter_nome_setor(resultado[3]))
        formulario.lineEdit_8.setText(resultado[4])
    else:
        QtWidgets.QMessageBox.warning(formulario, 'Aviso', 'Ramal não encontrado!')

#Função de Edição do Banco
def funcao_editar_ramal():
    linha_selecionada = formulario.tableWidget.currentRow()
    if linha_selecionada < 0:
        QtWidgets.QMessageBox.warning(formulario, 'Aviso', 'Selecione um registro para excluir!')
        formulario.Paginas.setCurrentWidget(formulario.Lista)
        return
    
    formulario.lineEdit_10.setText(formulario.tableWidget.item(linha_selecionada, 0).text())
    formulario.lineEdit_11.setText(formulario.tableWidget.item(linha_selecionada, 1).text())
    formulario.lineEdit_12.setText(formulario.tableWidget.item(linha_selecionada, 2).text())
    formulario.lineEdit_14.setText(formulario.tableWidget.item(linha_selecionada, 4).text())
    funcao_comboBox2_setor()

#Função para salvar a alteração de ramal
def salvar_alteracoes():
    id = formulario.lineEdit_10.text()
    nome = formulario.lineEdit_11.text()
    telefone = formulario.lineEdit_12.text()
    setor = formulario.comboBox_2.currentText()
    observacao = formulario.lineEdit_14.text()

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

    formulario.lineEdit_10.setText("")
    formulario.lineEdit_11.setText("")
    formulario.lineEdit_12.setText("")
    formulario.lineEdit_14.setText("")
    clear_combox()
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

def funcao_fechar():
    QtWidgets.QApplication.quit()

def funcao_comboBox_setor():
    formulario.comboBox.clear()
    cursor.execute("SELECT Nome FROM Setor")
    resultados = cursor.fetchall()
    nomes_setor = [resultado[0] for resultado in resultados]
    formulario.comboBox.addItems(nomes_setor)

def funcao_comboBox2_setor():
    linha_selecionada = formulario.tableWidget.currentRow()
    valor_selecionado = formulario.tableWidget.item(linha_selecionada, 3).text()
    cursor.execute("SELECT Nome FROM Setor")
    resultados = cursor.fetchall()
    nomes_setor = [resultado[0] for resultado in resultados]
    formulario.comboBox_2.addItems(nomes_setor)
    formulario.comboBox_2.setCurrentText(valor_selecionado)
    
def funcao_cadastro_setor():
    setor = formulario.lineEdit_15.text().upper()
    id_setor = obter_id_setor(setor)
    cursor.execute(f"SELECT * FROM Ramais WHERE Setor='{id_setor}'")
    resultado = cursor.fetchone()
    if resultado:
        QtWidgets.QMessageBox.warning(formulario, 'Aviso', 'Já existe um Setor com esse nome!')
        return

    cursor.execute(f"UPDATE Ramais SET Setor=(SELECT ID FROM Setor WHERE Nome='{setor}')")
    con.commit()
    funcao_comboBox_setor()

def clear_combox():
    formulario.comboBox_2.clear()

def pdf():
    desktop_path = str(Path.home() / "Desktop")
    pdf_path = os.path.join(desktop_path, "lista_ramais.pdf")
    pdf_canvas = canvas.Canvas(pdf_path, pagesize=letter)
    x = 50
    y = 750
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(x, y, "Lista de Ramais")
    x = 50
    y -= 50

    cursor.execute("SELECT r.ID, n.Nome, t.Numeros, s.Nome, r.Observacao FROM Ramais r JOIN Nomes n ON r.Nome = n.ID JOIN Telefones t ON r.Telefone = t.ID JOIN Setor s ON r.Setor = s.ID")
    resultados = cursor.fetchall()
    pdf_canvas.setFont("Helvetica", 10)
    for row in resultados:
        nome = f"Nome: {row[1]}"
        telefone = f"Telefone: {row[2]}"
        setor = f"Setor: {row[3]}"
        observacao = f"Observação: {row[4]}"

        if y < 50:
            pdf_canvas.showPage()
            y = 750
            pdf_canvas.setFont("Helvetica", 10)
            x = 50
            y -= 50


        pdf_canvas.drawString(x, y, nome)
        y -= 20
        pdf_canvas.drawString(x, y, telefone)
        y -= 20
        pdf_canvas.drawString(x, y, setor)
        y -= 20
        pdf_canvas.drawString(x, y, observacao)
        y -= 40
    pdf_canvas.save()
    QtWidgets.QMessageBox.information(formulario, 'Sucesso', 'Arquivo PDF salvo na área de trabalho!')

def excel():
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet['A1'] = 'Nome'
    sheet['B1'] = 'Telefone'
    sheet['C1'] = 'Setor'
    sheet['D1'] = 'Observação'
    cursor.execute("SELECT r.ID, n.Nome, t.Numeros, s.Nome, r.Observacao FROM Ramais r JOIN Nomes n ON r.Nome = n.ID JOIN Telefones t ON r.Telefone = t.ID JOIN Setor s ON r.Setor = s.ID")
    resultados = cursor.fetchall()
    row_num = 2 
    for row in resultados:
        nome = row[1]
        telefone = row[2]
        setor = row[3]
        observacao = row[4]
        sheet.cell(row=row_num, column=1, value=nome)
        sheet.cell(row=row_num, column=2, value=telefone)
        sheet.cell(row=row_num, column=3, value=setor)
        sheet.cell(row=row_num, column=4, value=observacao)
        row_num += 1
    desktop_path = str(Path.home() / "Desktop")
    excel_path = f"{desktop_path}/lista_ramais.xlsx"
    workbook.save(excel_path)
    QtWidgets.QMessageBox.information(formulario, 'Sucesso', 'Dados salvos em um arquivo Excel na sua área de trabalho!')

app=QtWidgets.QApplication([])
formulario=uic.loadUi("Style.ui") #Carrega o Visual
formulario.pushButton.clicked.connect(funcao_principal)         # Botão para Cadastro
formulario.pushButton_7.clicked.connect(funcao_pesquisar)       # Botão para Pesquisa
formulario.pushButton_11.clicked.connect(funcao_listar)          # Botão para Listar
formulario.pushButton_9.clicked.connect(lambda: formulario.Paginas.setCurrentWidget(formulario.Editar))
formulario.pushButton_9.clicked.connect(funcao_editar_ramal)
formulario.pushButton_10.clicked.connect(funcao_excluir_ramal)   # Botão para Excluir
formulario.pushButton_2.clicked.connect(salvar_alteracoes)   # Botão para Salvar Edição
formulario.pushButton_2.clicked.connect(lambda: formulario.Paginas.setCurrentWidget(formulario.Lista))
formulario.downloadpdf.clicked.connect(pdf)
formulario.downloadexcel.clicked.connect(excel)
#Validadores
validator = QtGui.QIntValidator()
formulario.lineEdit_2.setValidator(validator)
formulario.lineEdit_12.setValidator(validator)

nome_validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[A-Za-z ]+"))
formulario.lineEdit.setValidator(nome_validator)
formulario.comboBox.setValidator(nome_validator)
formulario.lineEdit_11.setValidator(nome_validator)

class validar_setor(QtGui.QValidator):
    def validate(self, text, pos):
        if text:
            for char in text:
                if not char.isalpha() and char != '/':
                    return (QtGui.QValidator.Invalid, text, pos)
        return (QtGui.QValidator.Acceptable, text, pos)
setor_validator = validar_setor()
formulario.comboBox.setValidator(setor_validator)
formulario.comboBox_2.setValidator(setor_validator)
formulario.lineEdit_15.setValidator(setor_validator)

formulario.lineEdit_5.setReadOnly(True)
formulario.lineEdit_6.setReadOnly(True)
formulario.lineEdit_7.setReadOnly(True)
formulario.lineEdit_8.setReadOnly(True)
formulario.lineEdit_10.setReadOnly(True)

#Botões do menu lateral
formulario.pushButton_cadastro.clicked.connect(lambda: formulario.Paginas.setCurrentWidget(formulario.Cadastro))
formulario.pushButton_cadastro.clicked.connect(lambda: formulario.CAD.setCurrentWidget(formulario.CAD_1))
formulario.pushButton_cadastro.clicked.connect(funcao_comboBox_setor)    # ComboBox
formulario.pushButton_buscar.clicked.connect(lambda: formulario.Paginas.setCurrentWidget(formulario.Pesquisa))
formulario.pushButton_listar.clicked.connect(lambda: formulario.Paginas.setCurrentWidget(formulario.Lista))
formulario.pushButton_listar.clicked.connect(clear_combox)
formulario.pushButton_fechar.clicked.connect(funcao_fechar)
formulario.pushButton_updates.clicked.connect(lambda: formulario.Paginas.setCurrentWidget(formulario.Updates))
formulario.pushButton_3.clicked.connect(lambda: formulario.CAD.setCurrentWidget(formulario.CAD_2))
formulario.pushButton_4.clicked.connect(funcao_cadastro_setor)
formulario.pushButton_4.clicked.connect(lambda: formulario.CAD.setCurrentWidget(formulario.CAD_1))


#Abre o aplicativo
formulario.show()
app.exec()

# Banco de Dados = SQLite3
# Visual = PyQt5 ("Qt Designer")
# Python 3.11.3