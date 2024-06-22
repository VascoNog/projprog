import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask import jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, format_codLER, format_ton

# Configure application
app = Flask(__name__)

# APAGAR SE ACABAR POR NÃO UTILIZAR EM JINJA
app.jinja_env.filters["format_codLER"] = format_codLER
app.jinja_env.filters["format_ton"] = format_ton


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
        producers = db.execute("SELECT username FROM users")
        
        # pré-preencher os vários parâmetros a partir da última e-GAR inserida
        # pre_fill = db.execute("""
        #     SELECT *
        #     FROM
        #         wastemap
        #     WHERE
        #         empresa_id = ?
        #     ORDER BY
        #         id DESC
        #     LIMIT 1
        #     """, session["user_id"])
        # if not pre_fill:
        #     return apology("Não existem e-GAR's inseridas no sistema")
        
        # print("PRE-FILL: ", pre_fill)
        
        
        return render_template("insert.html",
            obras = [contract["contract_short"]for contract in contracts],
            todos_codLer = [codLER["codLER"] for codLER in codes_LER],
            dest_finais = [operation["operation"] for operation in operations],
            produtores = [prod["username"] for prod in producers],
        )

    else:
        data = request.form.get("data")
        egar = request.form.get("egar")
        obra = request.form.get("obra")
        apa_associado = request.form.get("apa_associado")
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
        produtor = request.form.get("produtor")

        if not data:
            return apology("Faltou a data")
        if not egar:
            return apology("Faltou número da e-GAR")
        if not obra:
            return apology("Faltou designação da obra")
        if not apa_associado:
            return apology("Faltou APA do produtor da e-GAR")
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
        if not produtor:
            return apology("Faltou produtor do resíduo")

        # Encontrar código APA a partir de contract_short, consoante o APA associado à e-GAR
        if apa_associado == 'GT':
            apa_estab = 'GT'
        elif apa_associado == 'estab':
            apa_estab_db = db.execute("SELECT apa_code FROM apa_code_contract\
                WHERE contract_short = ?", obra)
            apa_estab = apa_estab_db[0]["apa_code"]
        else:
            return apology ("APA do produtor incorreto")

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
            "INSERT INTO wastemap (data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor,empresa_id)\
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor,session["user_id"])
        
        return redirect('/insert')
        
        # return render_template("insert.html", pre_fill=pre_fill)
                               

@app.route("/history", methods = ["GET", "POST"])
@login_required
def history():

    contracts = db.execute("""
        SELECT
            contract_short
        FROM
            apa_code_contract
        ORDER BY
            contract_short ASC""")

    years = db.execute("""
        SELECT DISTINCT
            strftime('%Y', data) AS year
        FROM
            wastemap
        WHERE
            dest_final != 'AP' AND empresa_id = ? AND strftime('%Y', data) != 'None'
        ORDER BY
            strftime('%Y', data) DESC
        """, session["user_id"])

    if request.method == "GET":

        return render_template("history.html",
                               obras_mapeadas = [contract["contract_short"] for contract in contracts],
                               years=years)
    else:
        obra = request.form.get("obra")
        ano = request.form.get("year")

        # Opção de ligar e-GAR's
        ligar_egars = request.form.get("ligar_egars")

        if ligar_egars == "NA":
            if obra == "todas" and ano == "todos":
                map = db.execute("""
                    SELECT
                        id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor
                    FROM 
                        wastemap 
                    WHERE
                        wastemap.empresa_id = ?
                    ORDER BY
                        data ASC""",session["user_id"])

            elif obra != "todas" and ano == "todos":
                map = db.execute("""
                    SELECT
                        id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor
                    FROM 
                        wastemap 
                    WHERE
                        wastemap.empresa_id = ? AND obra = ?
                    ORDER BY
                        data ASC""",session["user_id"],obra)

            elif obra == "todas" and ano != "todos":
                map = db.execute("""
                    SELECT 
                        id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor
                    FROM 
                        wastemap    
                    WHERE 
                        wastemap.empresa_id = ? AND strftime('%Y', data) = ?
                    ORDER BY 
                        data ASC""",session["user_id"],ano)

            # obra != "todas" and ano != "todos":
            else:
                map = db.execute("""
                    SELECT
                        id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor
                    FROM
                        wastemap
                    WHERE
                        wastemap.empresa_id = ? AND obra = ? AND strftime('%Y', data) = ?
                    ORDER BY
                        data ASC""",session["user_id"],obra, ano)

        if ligar_egars == "Ligar":

            if obra == "todas" and ano == "todos":
                map = db.execute("""
                    SELECT
                        id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor
                    FROM
                        wastemap
                    WHERE
                        wastemap.empresa_id = ? AND (dest_final = 'AP' OR apa_estab = 'APA00055104')
                    ORDER BY
                        data ASC""",session["user_id"])

            elif obra != "todas" and ano == "todos":
                
                map = db.execute("""
                    SELECT
                        id, data, egar, obra, apa_estab, transp, nif_transp, matricula, apa_transp, codLER, residuo, ton, dest_final, dest, nif_dest, apa_dest, produtor
                    FROM
                        wastemap
                    WHERE
                        wastemap.empresa_id = ? AND ((obra = ? AND dest_final = 'AP') OR apa_estab = 'APA00055104')
                    ORDER BY
                        data ASC
                """, session["user_id"],obra)


            elif obra == "todas" and ano != "todos":
                map = db.execute("""
                    SELECT
                        id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor
                    FROM 
                        wastemap
                    WHERE
                        wastemap.empresa_id = ? AND (dest_final = 'AP' OR apa_estab = 'APA00055104') AND strftime('%Y', data) = ?
                    ORDER BY
                        data ASC
                    """,session["user_id"],ano)

            # obra != "todas" and ano != "todos":
            else:
                map = db.execute("""
                    SELECT
                        id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor
                    FROM
                        wastemap
                    WHERE
                        wastemap.empresa_id = ? AND ((obra = ? AND dest_final = 'AP') OR apa_estab = 'APA00055104') AND strftime('%Y', data) = ?
                    ORDER BY 
                        data ASC""",session["user_id"],obra,ano)

        # All the "Select" options:
        contracts = db.execute("""
            SELECT 
                contract_short 
            FROM
                apa_code_contract
            ORDER BY 
                contract_short ASC""")
        
        codes_LER = db.execute("""
            SELECT
                codLER
            FROM
                codler_description
            ORDER BY
                codLER ASC""")
        
        operations = db.execute("""
            SELECT * 
            FROM 
                operation_description
            ORDER BY 
                operation DESC""")
        
        producers = db.execute("""
            SELECT
                username
            FROM
                users""")

        return render_template("history.html", map=map,
                               obras_mapeadas = [contract["contract_short"] for contract in contracts],
                               todos_codLer = [codLER["codLER"] for codLER in codes_LER],
                               dest_finais = [operation["operation"] for operation in operations],
                               produtores = [prod["username"] for prod in producers],
                               years=years)

# APAGAR diversas informações - relativo a vários html's
@app.route("/delete", methods=["POST"])
@login_required
def delete():

    # from history.html:
    row_id = request.form.get("row_id")
        
    # from establishments.html:
    apa_code = request.form.get("apa_code")
    c_full = request.form.get("c_full")
    c_short = request.form.get("c_short")

    # from codler_description.html:
    codLER = request.form.get("codLER")

    # from operation_description.html:
    operation = request.form.get("operation")

    # history.html:
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
            
            # All the "Select" options:
            contracts = db.execute("""
                SELECT
                    contract_short
                FROM
                    apa_code_contract
                ORDER BY
                    contract_short ASC""")
            
            codes_LER = db.execute("""
                SELECT
                    codLER FROM codler_description
                ORDER BY
                    codLER ASC""")
            
            operations = db.execute("""
                SELECT *
                FROM
                    operation_description
                ORDER BY
                    operation DESC""")
            
            producers = db.execute("""
                SELECT
                    username
                FROM
                    users""")
            years = db.execute("""
                SELECT DISTINCT
                    strftime('%Y', data) AS year
                FROM
                    wastemap""")

            return render_template("history.html", map=map,
                                obras_mapeadas = [contract["contract_short"] for contract in contracts],
                                todos_codLer = [codLER["codLER"] for codLER in codes_LER],
                                dest_finais = [operation["operation"] for operation in operations],
                                produtores = [prod["username"] for prod in producers],
                                years=years)
        else:
            return redirect("/history")

    # establishments.html:
    if apa_code and c_full and c_short:
        db.execute("DELETE FROM apa_code_contract WHERE apa_code = ?\
            AND contract_full = ?\
                AND contract_short = ?", apa_code, c_full, c_short)
        return redirect("/establishments")

    # codler_description.html:
    if codLER:
        db.execute("DELETE FROM codler_description WHERE codLER = ?", codLER)
        return redirect("/codler_description")

    # operation_description.html:
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
        novo_apa_associado = request.form.get("novo_apa_associado")
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
        novo_produtor = request.form.get("novo_produtor")

        if not nova_data:
            return apology("Faltou a data")
        if not nova_egar:
            return apology("Faltou número da e-GAR")
        if not nova_obra:
            return apology("Faltou designação da obra")
        if not novo_apa_associado:
            return apology("Faltou APA do produtor da e-GAR LINHA 361 EDIT EGAR")
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
        if not novo_produtor:
            return apology("Faltou produtor do resíduo")

        # Encontrar código APA a partir de contract_short, consoante o APA associado à e-GAR
        if novo_apa_associado == 'GT':
            apa_estab = 'GT'
        elif novo_apa_associado == 'estab':
            apa_estab_db = db.execute("SELECT apa_code FROM apa_code_contract\
                WHERE contract_short = ?", nova_obra)
            apa_estab = apa_estab_db[0]["apa_code"]
        else:
            return apology ("APA do produtor incorreto")

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
        db.execute("INSERT INTO wastemap (data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor,empresa_id)\
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            nova_data,nova_egar,nova_obra,apa_estab,novo_transp,novo_nif_transp,nova_matricula,novo_apa_transp,novo_codLER,residuo,nova_ton,novo_dest_final,
            novo_dest, novo_nif_dest,novo_apa_dest,novo_produtor,session["user_id"])

        # Mostrar o Mapa da obra (ou da nova obra) que sofreu edição:
        map = db.execute(
            "SELECT id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,\
                codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor\
                    FROM wastemap WHERE wastemap.empresa_id = ? AND obra = ?\
                        ORDER BY data ASC",session["user_id"], nova_obra)

        # Preparar formulário de edição sempre após a primeira e todas as seguintes edições
        contracts = db.execute("SELECT contract_short FROM apa_code_contract\
            ORDER BY contract_short ASC")
        codes_LER = db.execute("SELECT codLER FROM codler_description\
            ORDER BY codLER ASC")
        operations = db.execute("SELECT * FROM operation_description\
            ORDER BY operation DESC")
        producers = db.execute("SELECT username FROM users")

        return render_template("history.html",
            map = map,
            obras_mapeadas = [contract["contract_short"]for contract in contracts],
            todos_codLer = [codLER["codLER"] for codLER in codes_LER],
            dest_finais = [operation["operation"] for operation in operations],
            produtores = [prod["username"] for prod in producers]
        )

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

        # Insert new establishment or contract. Ensure non-duplication of APA code, except for "GT"
        if apa_code != "GT" and apa_code[:3] != "APA":
            flash("Deve escrever um código APA que comece com 'APA' ou escrever 'GT' (referente a 'Geral Tecnorém')")
            return redirect("/establishments")

        all_apa_codes = db.execute("SELECT apa_code FROM apa_code_contract")
        print("ALL APA CODES: ", all_apa_codes)
        if apa_code[:3] == "APA":
            for ac in all_apa_codes:
                if ac["apa_code"] == apa_code:
                    flash("Já existe um estabelecimento criado com esse código APA inserido")
                    return redirect("/establishments")


        #Insert a new establishment in database:
        db.execute("INSERT INTO apa_code_contract (apa_code, contract_full,contract_short)\
                VALUES(?,?,?)", apa_code,nome_estab,nome_estab_curto)

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
        antiga_design_longa = request.form.get("antiga_design_longa")
        nova_design_longa = request.form.get("nova_design_longa")
        antiga_design_curta = request.form.get("antiga_design_curta")
        nova_design_curta = request.form.get("nova_design_curta")

        if not novo_apa:
            return apology("Faltou APA")
        if not nova_design_longa:
            return apology("Faltou nome longo do estabelecimento/obra")
        if not nova_design_curta:
            return apology("Faltou nome curto do estabelecimento/obra")

        # Insert new establishment or contract. Ensure non-duplication of APA code, except for "GT"
        if novo_apa != "GT" and novo_apa[:3] != "APA":
            flash("Deve escrever um novo código APA que comece com 'APA' ou escrever 'GT' (referente a 'Geral Tecnorém')")
            return redirect("/establishments")

        # Verificar se o novo APA não se encontra já inserido na base de dados:
        if novo_apa != antigo_apa:
            all_apa_codes = db.execute("SELECT apa_code FROM apa_code_contract")
            print("ALL APA CODES EDIT ESTABLISHMENTS: ", all_apa_codes)
            if novo_apa[:3] == "APA":
                for ac in all_apa_codes:
                    if ac["apa_code"] == novo_apa:
                        flash("Já existe um estabelecimento criado com esse código APA inserido")
                        return redirect("/establishments")

        # Realizar as alterações no estabelecimento/obra
        db.execute("DELETE FROM apa_code_contract WHERE apa_code = ?\
            AND contract_full = ?\
                AND contract_short = ?", antigo_apa, antiga_design_longa, antiga_design_curta)
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
        db.execute ("INSERT INTO operation_description (operation,description) VALUES(?,?)", nova_operação, nova_descrição)

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

    mirr_options = db.execute("""
    SELECT
        contract_short
    FROM
        apa_code_contract
    WHERE
        apa_code != 'GT'
    ORDER BY
        contract_short ASC""")

    years = db.execute("""
    SELECT DISTINCT
        strftime('%Y', data) AS year
    FROM
        wastemap
    WHERE
        dest_final != 'AP' AND empresa_id = ? AND strftime('%Y', data) != 'None'
    ORDER BY
        strftime('%Y', data) DESC
    """, session["user_id"])

    print("TODOS OS ANOS POSSÍVEIS: ", years)


    # Todos os estabelecimentos e todas as obras com APA "GERAL TEC"

    if request.method == "GET":

        return render_template("mirr.html", mirr_options = mirr_options, years=years)

    else:
        estab_chosen = request.form.get("estab_chosen")
        year = request.form.get("year")

        print("TYPE OF ESTAB CHOSEN: ", type(estab_chosen))
        print("TYPE OF YEAR: ", type(year))

        # Face ao user que se encontra logado, determinar o username do produtor:
        producer = db.execute ("SELECT username FROM users\
            WHERE users.id = ?", session["user_id"])
        producer = producer[0]["username"]
        print("TYPE OF PRODUCER: ", type(producer))


        # Fazendo recurso a Common Table Expression (CTE)
        # Fontes:
        # https://www.sqlitetutorial.net/sqlite-cte/
        # https://learnsql.com/blog/cte-vs-subquery/

    params = {"obra":estab_chosen,"empresa_id":session["user_id"],"ano":year,"produtor":producer}
    def params_subset(keys):
        return {k:v for (k,v) in params.items() if k in keys}

    if estab_chosen != 'GT':
        mirr = db.execute("""
        WITH total_each_LER AS (
            SELECT
                wastemap.codLER,
                SUM(ton) AS total
            FROM
                wastemap
            WHERE
                obra = :obra AND dest_final != 'AP' AND empresa_id = :empresa_id AND (substr(data, 7, 4) = :ano OR strftime('%Y', data) = :ano) AND (produtor = :produtor OR produtor = 'Produtor Tecnorém')
            GROUP BY
                codLER
            )
            SELECT
                wastemap.codLER,
                total_each_LER.total,
                dest,
                nif_dest,
                apa_dest,
                dest_final,
                SUM(ton) AS subtotal,
                transp,
                nif_transp,
                apa_transp
            FROM
                wastemap
            JOIN
                total_each_LER ON wastemap.codLER = total_each_LER.codLER
            WHERE
                obra = :obra AND dest_final != 'AP' AND empresa_id = :empresa_id AND (substr(data, 7, 4) = :ano OR strftime('%Y', data) = :ano) AND (produtor = :produtor OR produtor = 'Produtor Tecnorém')
            GROUP BY
                wastemap.codLER,
                wastemap.dest_final,
                wastemap.transp
            """, **params_subset(["obra","empresa_id","ano","produtor"]))


        print("MIRR NÃO GT: ", mirr)

    # Para os MIRR, APA do estabelecimento GT - Geral Tecnorém
    else:
        mirr = db.execute("""
        WITH total_each_LER AS (
            SELECT
                wastemap.codLER,
                SUM(ton) AS total
            FROM
                wastemap
            WHERE
                apa_estab = 'GT' AND dest_final != 'AP' AND empresa_id = :empresa_id AND (substr(data, 7, 4) = :ano OR strftime('%Y', data) = :ano) \
                    AND (produtor = :produtor OR produtor = 'Produtor Tecnorém')
            GROUP BY
                codLER
            )
            SELECT
                wastemap.codLER,
                total_each_LER.total,
                dest,
                nif_dest,
                apa_dest,
                dest_final,
                SUM(ton) AS subtotal,
                transp,
                nif_transp,
                apa_transp
            FROM
                wastemap
            JOIN
                total_each_LER ON wastemap.codLER = total_each_LER.codLER
            WHERE
                apa_estab = 'GT' AND dest_final != 'AP' AND empresa_id = :empresa_id AND (substr(data, 7, 4) = :ano OR strftime('%Y', data) = :ano)\
                    AND (produtor = :produtor OR produtor = 'Produtor Tecnorém')
            GROUP BY
                wastemap.codLER,
                wastemap.dest_final,
                wastemap.transp
            """, **params_subset(["empresa_id","ano","produtor"]))

    if not mirr:
        flash("Não existem registos para as opções selecionadas")
        return redirect("/mirr")


    print("MIRR: ", mirr)

    return render_template("mirr.html", mirr=mirr, mirr_options = mirr_options, years=years)



# A FAZER:
# Avaliar inserir parametro "id" nas tabelas da base de dados que nao possuem.
# Exportar excel pdf do Mapa de resíduos - Mas talvez com os dados completos.
# adicionar mais mensagens flash
# MIRR

# Adicionar no MIRR "Produtor Tecnorém" - talvez escolher num SELECT

# QUERY DO MIRR:
# NAS LINHAS obra = ? AND NOT dest_final == 'AP' AND empresa_id = ? AND (substr(data, 7, 4) = ? OR strftime('%Y', data) = ?)
# Colocar depois apenas strftime('%Y', data) = ?, o website da-nos a data no formato aaaa-mm-dd, mas para já temos também no formato dd-mm-aaaa devido ao "upload" feito a partir do original
# o mesmo para (produtor = ? OR produtor = 'Produtor Tecnorém') - só interessa produtor = ?

# Formatar todas as queries no código. Mudar os NOT para !=

# No final devo alterar a tabela wastemap na parte do produtor de "Produtor Tecnorém" para "Tecnorém apenas"

# Pode existir a hipótese de uma obra ter estabelecimento criado mas as e-GAR's por lapso saírem com GT - Prevêr essa situação
