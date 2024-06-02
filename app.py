import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask import jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, format_codLER

# Configure application
app = Flask(__name__)

# APAGAR SE ACABAR POR NÃO UTILIZAR EM JINJA
app.jinja_env.filters["format_codLER"] = format_codLER


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


@app.route("/")
@login_required
def index():
    

    return render_template("layout.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Faltou o nome do user", 403)
    
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Faltou a palavra-passe", 403)
        
        # Creating users table
        # CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL UNIQUE, hash TEXT NOT NULL);
        
        # Query database for username
        users_db = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(users_db) != 1 or not check_password_hash(users_db[0]["hash"], request.form.get("password")):
            return apology("User e/ou password inválidas", 403)

        # Remember which user has logged in
        session["user_id"] = users_db[0]["id"]

        flash("USER ID: ", session["user_id"])

        # Redirect user to home page
        if not session["user_id"]:
            return redirect("/login")

        return redirect('/')

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # dealing with the case of the user clicking
        # on the “register” button without filling in the inputs
        if not username and not password and not confirmation:
            return apology("Deve escolher um nome de utilizador, uma palavra-passe e confirmar", 403)

        if not username:
            return apology("Deve escolher um nome de utilizador", 403)

        if not password:
            return apology("Deve escolher uma palavra-passe", 403)

        if not confirmation:
            return apology("Deve confirmar a palavra-passe escolhida", 403)

        # If all 3 inputs are met
        if password != confirmation:
            return apology("As palavras-passe não coincidem")

        hashed_password = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, hashed_password)
        except:
            # table users: username TEXT NOT NULL UNIQUE
            return apology("Desculpe, o nome de utilizador que escolheu já se encontra em uso")

        session["user_id"] = new_user
        # in login: session["user_id"] = rows[0]["id"]

        return redirect('/')

    else:
        return render_template("register.html")
    
    
@app.route("/insert", methods=["GET", "POST"])
@login_required
def insert():
    
    if request.method == "GET":
        contracts = db.execute("SELECT contract_short FROM apa_code_contract\
            ORDER BY contract_short ASC")
        codes_LER = db.execute("SELECT codLER FROM codler_description\
            ORDER BY codLER ASC")
        operations = db.execute("SELECT * FROM operation_description\
            ORDER BY operation DESC")
        return render_template("insert.html",
            obras = [contract["contract_short"]for contract in contracts],
            todos_codLer = [codLER["codLER"] for codLER in codes_LER],
            dest_finais = [operation["operation"] for operation in operations]
        )
        
    else:
        data = request.form.get("data")
        egar = request.form.get("egar")
        obra = request.form.get("obra")
        transp = request.form.get("transp")
        nif_transp = request.form.get("nif_transp")
        matricula = request.form.get("matricula")
        apa_transp = request.form.get("apa_transp")
        codLER = request.form.get("codLER")
        ton = request.form.get("ton")
        dest_final = request.form.get("dest_final")
        dest = request.form.get("dest")
        nif_dest = request.form.get("nif_dest")
        apa_dest = request.form.get("apa_dest")
        
        if not data:
            return apology("Faltou a data")
        if not egar:
            return apology("Faltou número da e-GAR")
        if not obra:
            return apology("Faltou designação da obra")
        if not transp:
            return apology("Faltou designação do transportador")
        if not nif_transp:
            return apology("Faltou NIF do transportador")
        if not matricula:
            return apology("Faltou a matrícula")
        if not codLER:
            return apology("Faltou código LER")
        if not ton:
            return apology("Faltou tonelagem")
        if not dest_final:
            return apology("Faltou destino final (ex: R12)")
        if not dest:
            return apology("Faltou designação do destinatário")
        if not nif_dest:
            return apology("Faltou NIF do destinatário")
        if not apa_dest:
            return apology("Faltou APA do destinatário")
        
        # Encontrar código apa a partir de contract_short

        apa_estab_db = db.execute("SELECT apa_code FROM apa_code_contract\
            WHERE contract_short = ?", obra)
        apa_estab = apa_estab_db[0]["apa_code"]
        
        # Encontrar designação do resíduo a partir de codLER
        
        residuo_db = db.execute("SELECT description FROM codler_description\
            WHERE codLER = ?", codLER)
        residuo = residuo_db[0]["description"]
            
        # Parametro que pode faltar
        if not apa_transp:
            apa_transp = "--"
            
        # Evitar duplicação de e-GAR's:
        egar_in_wastemap = db.execute("SELECT * FROM wastemap WHERE wastemap.egar = ?", egar)
        if egar_in_wastemap:
            return apology(f"Uma e-GAR com o número {egar} já tinha sido submetida anteriormente, verifique no Mapa",403)    
    
        # Inserir todos os parâmetros da e-GAR na tabela wastemap
        db.execute(
            "INSERT INTO wastemap (data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,empresa_id)\
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,session["user_id"])
        
        return redirect('/insert')
    
@app.route("/history", methods = ["GET", "POST"])
@login_required
def history(): 
    
    contracts = db.execute("SELECT contract_short FROM apa_code_contract\
        ORDER BY contract_short ASC")
    
    if request.method == "GET":

        return render_template("history.html",
                               obras_mapeadas = [contract["contract_short"] for contract in contracts])

    else:
        
        obra = request.form.get("obra")

        if obra == "todas":
            map = db.execute(
                "SELECT id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,\
                    codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest\
                        FROM wastemap WHERE wastemap.empresa_id = ?\
                            ORDER BY data ASC",session["user_id"])
        
        else:
            map = db.execute(
                "SELECT id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,\
                    codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest\
                        FROM wastemap WHERE wastemap.empresa_id = ? AND obra = ?\
                            ORDER BY data ASC",session["user_id"], obra)
            
        # All the "Select" options:
        contracts = db.execute("SELECT contract_short FROM apa_code_contract\
            ORDER BY contract_short ASC")
        codes_LER = db.execute("SELECT codLER FROM codler_description\
            ORDER BY codLER ASC")
        operations = db.execute("SELECT * FROM operation_description\
            ORDER BY operation DESC")
            
        return render_template("history.html", map=map,
                               obras_mapeadas = [contract["contract_short"] for contract in contracts],
                               obras = [contract["contract_short"]for contract in contracts],
                               todos_codLer = [codLER["codLER"] for codLER in codes_LER],
                               dest_finais = [operation["operation"] for operation in operations]
                               )

# APAGAR e-GARs do histórico/base de dados
@app.route("/delete", methods=["POST"])
@login_required
def delete():
    row_id = request.form.get("row_id")
    apa_code = request.form.get("apa_code")
    codLER = request.form.get("codLER")
    operation = request.form.get("operation")
    
    if row_id:
        db.execute("DELETE FROM wastemap WHERE wastemap.id = ?\
            AND wastemap.empresa_id = ?", row_id, session["user_id"])
        
        obra = request.form.get("obra")
        map_exists = db.execute("SELECT * FROM wastemap WHERE obra = ?", obra)
        if map_exists:
            map = db.execute(
                "SELECT id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,\
                    codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest\
                        FROM wastemap WHERE wastemap.empresa_id = ? AND obra = ?\
                            ORDER BY data ASC",session["user_id"], obra)
            return render_template("history.html", map=map)
        
        else:
            return redirect("/history")
        
    if apa_code:
        db.execute("DELETE FROM apa_code_contract WHERE apa_code = ?", apa_code)
        return redirect("/establishments")
    
    if codLER:
        db.execute("DELETE FROM codler_description WHERE codLER = ?", codLER)
        return redirect("/codler_description")
    
    if operation:
        db.execute("DELETE FROM operation_description WHERE operation = ?", operation)
        return redirect("/operation_description")
    
    
# EDITAR e-GARs do histórico/base de dados
@app.route("/edit_egar", methods=["GET","POST"])
@login_required
def edit_egar():
    
    if request.method == "GET":
        return render_template("edit_egar.html")
        
    else:      
        row_id = request.form.get("row_id")
        nova_data = request.form.get("nova_data")
        nova_egar = request.form.get("nova_egar")
        nova_obra = request.form.get("nova_obra")
        novo_transp = request.form.get("novo_transp")
        novo_nif_transp = request.form.get("novo_nif_transp")
        nova_matricula = request.form.get("nova_matricula")
        novo_apa_transp = request.form.get("novo_apa_transp")
        novo_codLER = request.form.get("novo_codLER")
        nova_ton = request.form.get("nova_ton")
        novo_dest_final = request.form.get("novo_dest_final")
        novo_dest = request.form.get("novo_dest")
        novo_nif_dest = request.form.get("novo_nif_dest")
        novo_apa_dest = request.form.get("novo_apa_dest")
            
        if not nova_data:
            return apology("Faltou a data")
        if not nova_egar:
            return apology("Faltou número da e-GAR")
        if not nova_obra:
            return apology("Faltou designação da obra")
        if not novo_transp:
            return apology("Faltou designação do transportador")
        if not novo_nif_transp:
            return apology("Faltou NIF do transportador")
        if not nova_matricula:
            return apology("Faltou a matrícula")
        if not novo_codLER:
            return apology("Faltou código LER")
        if not nova_ton:
            return apology("Faltou tonelagem")
        if not novo_dest_final:
            return apology("Faltou destino final (ex: R12)")
        if not novo_dest:
            return apology("Faltou designação do destinatário")
        if not novo_nif_dest:
            return apology("Faltou NIF do destinatário")
        if not novo_apa_dest:
            return apology("Faltou APA do destinatário")
            
        # Encontrar novo código apa a partir de novo contract_short
        apa_estab_db = db.execute("SELECT apa_code FROM apa_code_contract\
            WHERE contract_short = ?", nova_obra)
        apa_estab = apa_estab_db[0]["apa_code"]
                
        # Encontrar nova designação do resíduo a partir de novo codLER
        residuo_db = db.execute("SELECT description FROM codler_description\
            WHERE codLER = ?", novo_codLER)
        residuo = residuo_db[0]["description"]
                    
        # Parametro que pode faltar
        if not novo_apa_transp:
            novo_apa_transp = "--"
                
        # Eliminar a atual:
        if row_id:
            db.execute("DELETE FROM wastemap WHERE wastemap.id = ?\
                AND wastemap.empresa_id = ?", row_id, session["user_id"])
                    
        # Evitar duplicação de e-GAR's:
        egar_in_wastemap = db.execute("SELECT * FROM wastemap WHERE wastemap.egar = ?", nova_egar)
        if egar_in_wastemap:
            return apology(f"Uma e-GAR com o número {nova_egar} já tinha sido submetida anteriormente, verifique no Mapa",403)    
            
            
        # AVALIAR SE FAZ MAIS SENTIDO FAZER UPDATE AO INVÉS DE FAZER DELETE DA EGAR + NOVA INSERT
            
        # Inserir todos os parâmetros da e-GAR na tabela wastemap
        db.execute("INSERT INTO wastemap (data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,empresa_id)\
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            nova_data,nova_egar,nova_obra,apa_estab,novo_transp,novo_nif_transp,nova_matricula,novo_apa_transp,novo_codLER,residuo,nova_ton,novo_dest_final,
            novo_dest, novo_nif_dest,novo_apa_dest,session["user_id"])
                
        # Mostrar o Mapa da obra (ou da nova obra) que sofreu edição:
        map = db.execute(
            "SELECT id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,\
                codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest\
                    FROM wastemap WHERE wastemap.empresa_id = ? AND obra = ?\
                        ORDER BY data ASC",session["user_id"], nova_obra)

        print("TIPO DE MAP: ", type(map[0]))
            
        return render_template("history.html", map=map)

@app.route("/establishments", methods=["GET", "POST"])
@login_required
def establishments(): 
    
    if request.method == "GET":
        all_estab = db.execute("SELECT apa_code,contract_full,contract_short \
            FROM apa_code_contract ORDER BY apa_code DESC")
        
        return render_template("establishments.html", all_estab=all_estab)
    
    else:
        apa_code = request.form.get("apa_code")
        nome_estab = request.form.get("nome_estab")
        nome_estab_curto = request.form.get("nome_estab_curto")
        if not apa_code:
            return apology("Faltou o código APA", 403)
        if not nome_estab:
            return apology("Faltou nome completo do estabelecimento/obra", 403)
        if not nome_estab_curto:
            return apology("Faltou nome curto do estabelecimento/obra", 403)
        
        # Insert new establishment or contract. Ensure non-duplication of APA code
        try:
            db.execute("INSERT INTO apa_code_contract (apa_code, contract_full,contract_short)\
                VALUES(?,?,?)", apa_code,nome_estab,nome_estab_curto)
        except:
            # table apa_code_contract: apa_code TEXT NOT NULL UNIQUE
            flash("O código APA que tentou inserir já se encontra no sistema!")
            return redirect("/establishments")
    
        # INSERT INTO table_name (column_a, column_b)
        # VALUES ("value_a", "value_b");
                
        # Show all establishments
        all_estab = db.execute("SELECT apa_code,contract_full,contract_short \
            FROM apa_code_contract ORDER BY apa_code DESC")
        
        return render_template("establishments.html", all_estab=all_estab)

# EDITAR estabelecimentos criados
@app.route("/edit_establishments", methods=["GET","POST"])
@login_required
def edit_establishments():

    if request.method == "GET":
        return render_template("edit_establishments.html")
    
    else:
        antigo_apa = request.form.get("antigo_apa")
        novo_apa = request.form.get("novo_apa")
        nova_design_longa = request.form.get("nova_design_longa")
        antiga_design_curta = request.form.get("antiga_design_curta")
        nova_design_curta = request.form.get("nova_design_curta")
        
        if not novo_apa:
            return apology("Faltou APA")
        if not nova_design_longa:
            return apology("Faltou nome longo do estabelecimento/obra")
        if not nova_design_curta:
            return apology("Faltou nome curto do estabelecimento/obra")
        
        # Realizar as alterações no estabelecimento/obra
        db.execute("DELETE FROM apa_code_contract WHERE apa_code = ?", antigo_apa)
        db.execute ("INSERT INTO apa_code_contract (apa_code,contract_full,contract_short)\
            VALUES(?,?,?)", novo_apa, nova_design_longa, nova_design_curta)
        
        # Show all establishments (after changes)
        all_estab = db.execute("SELECT apa_code,contract_full,contract_short \
            FROM apa_code_contract ORDER BY apa_code DESC")
        
        # Atualizar wastemap: designação curta da obra e apa do estabelecimento
        db.execute("UPDATE wastemap SET obra = ?, apa_estab = ?\
            WHERE obra = ? AND apa_estab = ?",nova_design_curta,novo_apa,antiga_design_curta,antigo_apa)

        return render_template("establishments.html", all_estab=all_estab)
        
@app.route("/codler_description", methods=["GET", "POST"])
@login_required
def codler_description():

    if request.method == "GET":
        all_codLER = db.execute("SELECT * FROM codler_description")
        
        return render_template("codler_description.html", all_codLER=all_codLER)
    
    else:
        codLER = request.form.get("codLER")
        description = request.form.get("description")
        
        if not codLER:
            return apology("Faltou código LER", 403)
        
        codLER = format_codLER(codLER)
        print("CODLER LINHA 484: ", codLER)
        if codLER == None:
            return apology("O código LER inserido deve ter 6 dígitos no formato XX XX XX ou XXXXXX", 403)
             
        if not description:
            return apology("Faltou descrição do código LER", 403)
        
        # Insert new code "LER" and description. Ensure non-duplication of code "LER"
        try:
            db.execute("INSERT INTO codler_description (codLER, description)\
                VALUES(?,?)", codLER, description)
        except:
            # table codler_description: codLER TEXT NOT NULL UNIQUE
            flash("O código LER que tentou inserir já se encontra no sistema!")
            return redirect("/codler_description")
        
        # INSERT INTO table_name (column_a, column_b)
        # VALUES ("value_a", "value_b");
                
        # Show all codes "LER"
        all_codLER = db.execute("SELECT * FROM codler_description")
        
        return render_template("codler_description.html", all_codLER=all_codLER)

@app.route("/edit_codler_description", methods=["GET", "POST"])
@login_required
def edit_codler_description():
    
    if request.method == "GET":
        return render_template("edit_codler_description.html")
    
    else:
        antigo_codLER = request.form.get("antigo_codLER")
        novo_codLER = request.form.get("novo_codLER")
        nova_descrição = request.form.get("nova_descrição")
        
        if not novo_codLER :
            return apology("Faltou código LER", 403)
        
        novo_codLER = format_codLER(novo_codLER)
        if novo_codLER == None:
            return apology("O código LER inserido deve ter 6 dígitos no formato XX XX XX ou XXXXXX", 403)
        
        if not nova_descrição:
            return apology("Faltou descrição do código LER", 403)
        
        # Realizar as alterações na codLER_description table
        db.execute("DELETE FROM codler_description WHERE codler = ?", antigo_codLER)
        db.execute ("INSERT INTO codler_description (codLER,description)\
            VALUES(?,?)", novo_codLER, nova_descrição)
        
        # Show all LER and descriptions (after changes)
        all_codLER = db.execute("SELECT * FROM codler_description\
            ORDER BY codLER DESC")
        
        # Atualizar wastemap: código LER
        db.execute("UPDATE wastemap SET codLER = ?,residuo = ?\
            WHERE codLER = ?",novo_codLER, nova_descrição, antigo_codLER)
        
        return render_template("codler_description.html", all_codLER=all_codLER)
    

@app.route("/operation_description", methods=["GET", "POST"])
@login_required
def operation_description():

    if request.method == "GET":
        all_operations = db.execute("SELECT * FROM operation_description")
        
        return render_template("operation_description.html", all_operations=all_operations)
    
    else:
        operation = request.form.get("operation")
        description = request.form.get("description")
        
        if not operation:
            return apology("Faltou operação de valorização/eliminação", 403)
         
        if not description:
            return apology("Faltou descrição da operação de valorização/eliminação", 403)
        
        # Insert new operation and description. Ensure non-duplication
        try:
            db.execute("INSERT INTO operation_description (operation, description)\
                VALUES(?,?)", operation, description)
        except:
            # table operation_description: operation TEXT NOT NULL UNIQUE,
            flash("A operação de valorização/eliminação que tentou inserir já se encontra no sistema!")
            return redirect("/operation_description")

        # Show all operations
        all_operations = db.execute("SELECT * FROM operation_description")
        
        return render_template("operation_description.html", all_operations=all_operations)
    
@app.route("/edit_operation_description", methods=["GET", "POST"])
@login_required
def edit_operation_description():

    if request.method == "GET":
        return render_template("edit_operation_description.html")
    
    else:
        antiga_operação = request.form.get("antiga_operação")
        nova_operação = request.form.get("nova_operação")
        nova_descrição = request.form.get("nova_descrição")
        
        if not nova_operação :
            return apology("Faltou operação de valorização/eliminação", 403)
        if not nova_descrição:
            return apology("Faltou descrição da operação de valorização/eliminação", 403)
        
        # Realizar as alterações na operação de valorização/eliminação
        db.execute("DELETE FROM operation_description WHERE operation = ?", antiga_operação)
        db.execute ("INSERT INTO operation_description (operation,description)\
            VALUES(?,?)", nova_operação, nova_descrição)
        
        # Show all operations (after changes)
        all_operations = db.execute("SELECT * FROM operation_description\
            ORDER BY operation DESC")
        
        # Atualizar wastemap: operação
        db.execute("UPDATE wastemap SET dest_final = ?\
            WHERE dest_final = ?", nova_operação, antiga_operação)

        return render_template("operation_description.html", all_operations=all_operations)
    

@app.route("/mirr", methods=["GET", "POST"])
@login_required
def mirr():
    
    # Fazer tabelas do MIRR
    
    return apology("TODO")

# Avaliar inserir parametro "id" nas tabelas da base de dados que nao possuem.
# Exportar excel pdf do Mapa de resíduos - Mas talvez com os dados completos.
# Adicinar função de editar/eliminar nos Estabelecimentos e nos Códigos LER
# Adicinar função de editar/eliminar na History
# adicionar mais mensagens flash
# MIRR



# Mais tarde:
# Criar uma associação entre Armazenamento Preliminar na Sede e os resíduos que são recolhidos na sede. De forma a ligar e-GAR's

