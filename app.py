import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask import jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

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
        
        x = request.form.get("username")    
        print("NOME USER: ", x)
    
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
        return render_template("insert.html")
    
    else:
        data = request.form.get("data")
        egar = request.form.get("egar")
        obra = request.form.get("obra")
        apa_estab = request.form.get("apa_estab")
        transp = request.form.get("transp")
        nif_transp = request.form.get("nif_transp")
        matricula = request.form.get("matricula")
        apa_transp = request.form.get("apa_transp")
        codLER = request.form.get("codLER")
        residuo = request.form.get("residuo")
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
        if not apa_estab:
            return apology("Faltou APA do estabelecimento/obra")
        if not transp:
            return apology("Faltou designação do transportador")
        if not nif_transp:
            return apology("Faltou NIF do transportador")
        if not matricula:
            return apology("Faltou a matrícula")
        if not codLER:
            return apology("Faltou LER")
        if not residuo:
            return apology("Faltou designação do resíduo")
        if not ton:
            return apology("Faltou tonelagem")
        if not dest_final:
            return apology("Faltou destino final (ex: R12)")
        if not dest:
            return apology("Faltou designação do destinatário")
        if not apa_dest:
            return apology("Faltou APA do destinatário")
        if not nif_dest:
            return apology("Faltou NIF do destinatário")
        
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
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,session["user_id"])
        
        return redirect('/insert')
    
@app.route("/history")
@login_required
def history(): 
    
    # map = db.execute(
    #     "SELECT data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest\
    #         FROM wastemap WHERE wastemap.empresa_id = ? ORDER BY data ASC", session["user_id"])
    
    # Forma reduzida:
    map = db.execute(
        "SELECT data,egar,obra,transp,codLER,ton,dest_final,dest\
            FROM wastemap WHERE wastemap.empresa_id = ?\
                ORDER BY data ASC", session["user_id"])
    
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
            return apology("Faltou o código APA")
        if not nome_estab:
            return apology("Faltou nome completo do estabelecimento/obra")
        if not nome_estab_curto:
            return apology("Faltou nome curto do estabelecimento/obra")
        
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
        
@app.route("/mirr", methods=["GET", "POST"])
@login_required
def mirr():
    
    # Fazer tabelas do MIRR
    
    return apology("TODO")



# Fazer os selects ao inserir e-GAR's - Ver situações idênticas
# Exportar excel pdf do Mapa de resíduos - Mas talvez com os dados completos.
# Adicinar função de editar/eliminar nos Estabelecimentos
# Adicinar função de editar/eliminar na History
# Fazer MIRR


# Fazer os selects ao inserir e-GAR's - Ver situações idênticas
# Exportar excel pdf do Mapa de resíduos - Mas talvez com os dados completos.
# Adicinar função de editar/eliminar nos Estabelecimentos
# Adicinar função de editar/eliminar na History
# Fazer MIRR