import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask import jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, format_codLER, format_codLER_excel, format_ton

# Configure application
app = Flask(__name__)

app.jinja_env.filters["format_codLER"] = format_codLER
app.jinja_env.filters["format_codLER_excel"] = format_codLER_excel
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
            return apology("Faltou o nome do user", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Faltou a palavra-passe"), 400

        # Query database for username
        users_db = db.execute("""
        SELECT
            *
        FROM
            users
        WHERE
            username = ?""", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(users_db) != 1 or not check_password_hash(users_db[0]["hash"], request.form.get("password")):
            return apology("User e/ou password inválidas", 400)

        # Remember which user has logged in
        session["user_id"] = users_db[0]["id"]
        flash(f"Iniciou a sessão com: {users_db[0]['username']}","login")

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
            return apology("Deve escolher um nome de utilizador, uma palavra-passe e confirmar", 400)

        if not username:
            return apology("Deve escolher um nome de utilizador", 400)

        if not password:
            return apology("Deve escolher uma palavra-passe", 400)

        if not confirmation:
            return apology("Deve confirmar a palavra-passe escolhida", 400)

        # If all 3 inputs are met
        if password != confirmation:
            return apology("As palavras-passe não coincidem", 400)

        hashed_password = generate_password_hash(password)

        try:
            new_user = db.execute("""
            INSERT INTO
                users (username, hash) VALUES(?,?)
            """,username, hashed_password)
        except:
            # table users: username TEXT NOT NULL UNIQUE
            return apology("Desculpe, o nome de utilizador que escolheu já se encontra em uso", 409)

        session["user_id"] = new_user
        
        return redirect('/')

    else:
        return render_template("register.html")


@app.route("/insert", methods=["GET", "POST"])
@login_required
def insert():

    if request.method == "GET":
        contracts = db.execute("""
        SELECT
            contract_short FROM apa_code_contract
        ORDER BY
            contract_short ASC""")
        
        codes_LER = db.execute("""
        SELECT
            codLER FROM codler_description
        ORDER BY
            codLER ASC""")
        
        operations = db.execute("""
        SELECT
            *
        FROM
            operation_description
        ORDER BY
            operation DESC""")
        
        producers = db.execute("""
        SELECT
            username
        FROM
            users""")
       
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

        required_fields = [
            ("data", "Faltou a data"),
            ("egar", "Faltou número da e-GAR"),
            ("obra", "Faltou designação da obra"),
            ("apa_associado", "Faltou APA do produtor da e-GAR"),
            ("transp", "Faltou designação do transportador"),
            ("nif_transp", "Faltou NIF do transportador"),
            ("matricula", "Faltou a matrícula"),
            ("codLER", "Faltou código LER"),
            ("ton", "Faltou tonelagem"),
            ("dest_final", "Faltou destino final (ex: R12)"),
            ("dest", "Faltou designação do destinatário"),
            ("nif_dest", "Faltou NIF do destinatário"),
            ("apa_dest", "Faltou APA do destinatário"),
            ("produtor", "Faltou produtor do resíduo")
        ]
        
        for field, specific_error_message in required_fields:
            if not locals().get(field):
                flash(f"A e-GAR não foi inserida no sistema! - {specific_error_message} - Repita o processo")
                return redirect("/insert")
   
        # Find APA code from contract_short, depending on the APA associated with the e-GAR
        if apa_associado == 'GT':
            apa_estab = 'GT'
        elif apa_associado == 'estab':
            apa_estab_db = db.execute("""
            SELECT
                apa_code
            FROM
                apa_code_contract
            WHERE
                contract_short = ?
            """, obra)
    
            apa_estab = apa_estab_db[0]["apa_code"]
            
        else:
            flash("APA do produtor incorreto")
            return redirect("/insert")

        # Find waste name from codLER
        residuo_db = db.execute("""
        SELECT
            description
        FROM
            codler_description
        WHERE codLER = ?
        """, codLER)
        
        residuo = residuo_db[0]["description"]

        # Only parameter that can be missing
        if not apa_transp:
            apa_transp = "--"

        # Avoid duplicate e-GARs:
        egar_in_wastemap = db.execute("""
        SELECT
            *
        FROM
            wastemap
        WHERE
            wastemap.egar = ?
        """, egar)
        
        if egar_in_wastemap:
            flash(f"Uma e-GAR com o número {egar} já tinha sido submetida anteriormente, verifique no Mapa")
            return redirect("/insert")

        # Enter all the e-GAR parameters in the wastemap table
        db.execute("""
        INSERT INTO
            wastemap (data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor,empresa_id)\
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor,session["user_id"])
        
        return redirect('/insert')
                                 
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

        # Option to link e-GAR's
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
                    data ASC
                """,session["user_id"])

            elif obra != "todas" and ano == "todos":
                map = db.execute("""
                SELECT
                    id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor
                FROM 
                    wastemap 
                WHERE
                    wastemap.empresa_id = ? AND obra = ?
                ORDER BY
                    data ASC
                """,session["user_id"],obra)

            elif obra == "todas" and ano != "todos":
                map = db.execute("""
                SELECT 
                    id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor
                FROM 
                    wastemap    
                WHERE 
                    wastemap.empresa_id = ? AND strftime('%Y', data) = ?
                ORDER BY 
                    data ASC
                """,session["user_id"],ano)

            # contract(obra) != "all"/"todas" and year(ano) != "all"/"todos":
            else:
                map = db.execute("""
                SELECT
                    id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor
                FROM
                    wastemap
                WHERE
                    wastemap.empresa_id = ? AND obra = ? AND strftime('%Y', data) = ?
                ORDER BY
                    data ASC
                """,session["user_id"],obra, ano)

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
                    data ASC
                """,session["user_id"])

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

            # contract(obra) != "all"/"todas" and year(ano) != "all"/"todos":
            else:
                map = db.execute("""
                SELECT
                    id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor
                FROM
                    wastemap
                WHERE
                    wastemap.empresa_id = ? AND ((obra = ? AND dest_final = 'AP') OR apa_estab = 'APA00055104') AND strftime('%Y', data) = ?
                ORDER BY 
                    data ASC
                """,session["user_id"],obra,ano)

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
        SELECT
            *
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

# DELETE various information relating to several html files
@app.route("/delete", methods=["POST"])
@login_required
def delete():

    # from history.html:
    row_id_hist = request.form.get("row_id_hist")
    
    if row_id_hist:
        db.execute("""
        DELETE FROM
            wastemap WHERE wastemap.id = ? AND wastemap.empresa_id = ?
        """, row_id_hist, session["user_id"])

        obra = request.form.get("obra")
        map_exists = db.execute("""
        SELECT
            *
        FROM
            wastemap WHERE obra = ?
        """, obra)
        
        if map_exists:
            map = db.execute("""
            SELECT
                id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest
            FROM
                wastemap
            WHERE
                wastemap.empresa_id = ? AND obra = ?
            ORDER BY
                data ASC
            """,session["user_id"], obra)
            
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
            SELECT
                *
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

    # from establishments.html:
    row_id_estab = request.form.get("row_id_estab")

    if row_id_estab:
        db.execute("""
        DELETE FROM 
            apa_code_contract
        WHERE
            id = ?
        """, row_id_estab)
        return redirect("/establishments")
    
    # from codler_description.html:
    codLER = request.form.get("codLER")
    
    if codLER:
        db.execute("""
        DELETE FROM
            codler_description
        WHERE
            codLER = ?
        """, codLER)
        return redirect("/codler_description")
    
    # from operation_description.html:
    operation = request.form.get("operation")

    if operation:
        db.execute("""
        DELETE FROM
            operation_description
        WHERE
            operation = ?
        """, operation)
        return redirect("/operation_description")


# EDIT e-GARs from the history/database
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

        required_fields = [
            ("nova_data", "Faltou a data"),
            ("nova_egar", "Faltou número da e-GAR"),
            ("nova_obra", "Faltou designação da obra"),
            ("novo_apa_associado", "Faltou APA do produtor da e-GAR"),
            ("novo_transp", "Faltou designação do transportador"),
            ("novo_nif_transp", "Faltou NIF do transportador"),
            ("nova_matricula", "Faltou a matrícula"),
            ("novo_codLER", "Faltou código LER"),
            ("nova_ton", "Faltou tonelagem"),
            ("novo_dest_final", "Faltou destino final (ex: R12)"),
            ("novo_dest", "Faltou designação do destinatário"),
            ("novo_nif_dest", "Faltou NIF do destinatário"),
            ("novo_apa_dest", "Faltou APA do destinatário"),
            ("novo_produtor", "Faltou produtor do resíduo")
        ]

        for field, specific_error_message in required_fields:
            if not locals().get(field):
                flash(f"Não foram realizadas alterações! - {specific_error_message} - Repita o processo")
                return redirect("/history")

       # Find APA code from contract_short, depending on the APA associated with the e-GAR
        if novo_apa_associado == 'GT':
            apa_estab = 'GT'
        elif novo_apa_associado == 'estab':
            apa_estab_db = db.execute("""
            SELECT
                apa_code FROM apa_code_contract
            WHERE
                contract_short = ?
            """, nova_obra)
            apa_estab = apa_estab_db[0]["apa_code"]
        else:
            flash("APA do produtor incorreto")
            return redirect("/history")

        # Find new waste name from new codLER
        residuo_db = db.execute("""
        SELECT
            description
        FROM
            codler_description
        WHERE
            codLER = ?
        """, novo_codLER)
        residuo = residuo_db[0]["description"]

        # only parameter that can be missing
        if not novo_apa_transp:
            novo_apa_transp = "--"

        # eliminate the current one
        if row_id:
            db.execute("""
            DELETE FROM
                wastemap WHERE wastemap.id = ? AND wastemap.empresa_id = ?
            """,row_id, session["user_id"])

        # Avoid duplicate e-GARs:
        egar_in_wastemap = db.execute("""
        SELECT
            *
        FROM
            wastemap
        WHERE
            wastemap.egar = ?
        """, nova_egar)
        
        if egar_in_wastemap:
            flash(f"Não foram realizadas alterações! Uma e-GAR com o número {nova_egar} já tinha sido submetida anteriormente, verifique no Mapa")
            return redirect("/history")

        # Enter all the e-GAR parameters in the wastemap table
        db.execute("""
        INSERT INTO
            wastemap (data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor,empresa_id)\
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,nova_data,nova_egar,nova_obra,apa_estab,novo_transp,novo_nif_transp,nova_matricula,novo_apa_transp,\
            novo_codLER,residuo,nova_ton,novo_dest_final,novo_dest, novo_nif_dest,novo_apa_dest,novo_produtor,session["user_id"])

        # Show the Map of the contractor (or new contractor) that has been edited:
        map = db.execute("""
        SELECT 
            id,data,egar,obra,apa_estab,transp,nif_transp,matricula,apa_transp,codLER,residuo,ton,dest_final,dest,nif_dest,apa_dest,produtor
        FROM
            wastemap
        WHERE
            wastemap.empresa_id = ? AND obra = ?
        ORDER BY
            data ASC
        """,session["user_id"], nova_obra)

        # Prepare edit form always after the first and all subsequent edits
        contracts = db.execute("""
        SELECT
            contract_short FROM apa_code_contract
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
        SELECT
            *
        FROM
            operation_description
        ORDER BY
            operation DESC""")
        
        producers = db.execute("""
        SELECT
            username
        FROM
            users""")

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
        all_estab = db.execute("""
        SELECT 
            id,apa_code,contract_full,contract_short
        FROM
            apa_code_contract
        ORDER BY
            apa_code DESC""")

        return render_template("establishments.html", all_estab=all_estab)

    else:
        apa_code = request.form.get("apa_code")
        nome_estab = request.form.get("nome_estab")
        nome_estab_curto = request.form.get("nome_estab_curto")
        
        required_fields = [
            ("apa_code","Faltou o código APA"),
            ("nome_estab","Faltou nome completo do estabelecimento/obra"),
            ("nome_estab_curto","Faltou nome curto do estabelecimento/obra")
        ]

        for field, specific_error_message in required_fields:
            if not locals().get(field):
                flash(f"O estabelecimento não foi inserido no sistema! - {specific_error_message} - Repita o processo")
                return redirect("/establishments")
 
        # Delete whitespace at the beginning and end of a string using strip() method
        nome_estab = nome_estab.strip()
        nome_estab_curto = nome_estab_curto.strip()
        

        # Insert new establishment or contract. Ensure non-duplication of APA code, except for "GT"
        if apa_code != "GT" and apa_code[:3] != "APA":
            flash("Deve escrever um código APA que comece com 'APA' ou escrever 'GT' (referente a 'Geral Tecnorém')")
            return redirect("/establishments")

        all_apa_codes = db.execute("""
        SELECT
            apa_code
        FROM
            apa_code_contract""")
        
        if apa_code[:3] == "APA":
            for ac in all_apa_codes:
                if ac["apa_code"] == apa_code:
                    flash("Já existe um estabelecimento criado com esse código APA inserido")
                    return redirect("/establishments")

        
       # Avoid duplicating of the full and/or short name of the contractor
        repetition_contract = db.execute("""
        SELECT
            *
        FROM
            apa_code_contract
        WHERE
            contract_full = ? OR contract_short = ?
        """, nome_estab, nome_estab_curto)
        if repetition_contract:
            flash("Atenção, a designação (Completa ou Curta) da obra que tentou inserir já existe em sistema")
            return redirect("/establishments")
            

        #Insert a new establishment in database:
        db.execute("""
        INSERT INTO
            apa_code_contract (apa_code, contract_full,contract_short) VALUES(?,?,?)""", apa_code,nome_estab,nome_estab_curto)

        # Show all establishments
        all_estab = db.execute("""
        SELECT
            id,apa_code,contract_full,contract_short
        FROM
            apa_code_contract
        ORDER BY
            apa_code DESC""")
        
        return render_template("establishments.html", all_estab=all_estab)

# EDIT establishments created
@app.route("/edit_establishments", methods=["GET","POST"])
@login_required
def edit_establishments():

    if request.method == "GET":
        return render_template("establishments.html")

    else:
        antigo_apa = request.form.get("antigo_apa")
        novo_apa = request.form.get("novo_apa")
        antiga_design_longa = request.form.get("antiga_design_longa")
        nova_design_longa = request.form.get("nova_design_longa")
        antiga_design_curta = request.form.get("antiga_design_curta")
        nova_design_curta = request.form.get("nova_design_curta")
        
        required_fields = [
            ("novo_apa"," Faltou o código APA"),
            ("nova_design_longa","Faltou nome completo do estabelecimento/obra"),
            ("nova_design_curta","Faltou nome curto do estabelecimento/obra")
        ]

        for field, specific_error_message in required_fields:
            if not locals().get(field):
                flash(f"Não foram realizadas alterações! - {specific_error_message} - Repita o processo")
                return redirect("/establishments")

        # Delete whitespace at the beginning and end of a string using strip() method
        nova_design_longa = nova_design_longa.strip()
        nova_design_curta = nova_design_curta.strip()

        # Insert new establishment or contract. Ensure non-duplication of APA code, except for "GT"
        if novo_apa != "GT" and novo_apa[:3] != "APA":
            flash("Deve escrever um novo código APA que comece com 'APA' ou escrever 'GT' (referente a 'Geral Tecnorém')")
            return redirect("/establishments")

        # Check that the new APA is not already in the database:
        if novo_apa != antigo_apa:
            all_apa_codes = db.execute("SELECT apa_code FROM apa_code_contract")
            if novo_apa[:3] == "APA":
                for ac in all_apa_codes:
                    if ac["apa_code"] == novo_apa:
                        flash("Já existe um estabelecimento criado com esse código APA inserido")
                        return redirect("/establishments")
        
        # Avoid duplicating of the full and/or short name of the contractor
        repetition_contract = db.execute("""
        SELECT
            apa_code
        FROM
            apa_code_contract
        WHERE
            contract_full = ? OR contract_short = ?
        """, nova_design_longa, nova_design_curta)
        
        if repetition_contract:
            repeated_apa_code_list = []
            for estab in repetition_contract:
                repeated_apa_code_list.append(estab['apa_code'])
                if novo_apa not in repeated_apa_code_list:
                    for apa in repeated_apa_code_list:
                        flash(f"As alterações foram efetivadas, contudo pode existir um possível conflito com a(s) linha(s) do(s) seguinte(s) APA('s): {apa} - Corrija antes de avançar!")
    

        # Make changes to the establishment/contractor
        db.execute("""
        DELETE FROM
            apa_code_contract
        WHERE
            apa_code = ? AND contract_full = ? AND contract_short = ?
        """, antigo_apa, antiga_design_longa, antiga_design_curta)
        
        db.execute ("""
        INSERT INTO
            apa_code_contract (apa_code,contract_full,contract_short) VALUES(?,?,?)
        """, novo_apa, nova_design_longa, nova_design_curta)

        # Show all establishments (after changes)
        all_estab = db.execute("""
        SELECT
            apa_code,contract_full,contract_short
        FROM
            apa_code_contract
        ORDER BY
            apa_code DESC""")

        # Update wastemap: short name of the contractor and APA code of the establishment
        db.execute("""
        UPDATE 
            wastemap
        SET
            obra = ?, apa_estab = ?
        WHERE 
            obra = ? AND apa_estab = ?
        """,nova_design_curta,novo_apa,antiga_design_curta,antigo_apa)

        return render_template("establishments.html", all_estab=all_estab)

@app.route("/codler_description", methods=["GET", "POST"])
@login_required
def codler_description():

    if request.method == "GET":
        all_codLER = db.execute("""
        SELECT
            * 
        FROM
            codler_description""")

        return render_template("codler_description.html", all_codLER=all_codLER)

    else:
        codLER = request.form.get("codLER")
        description = request.form.get("description")

        if not codLER:
            flash("O LER não foi inserido no sistema! - Faltou código LER - Repita o processo")
            return redirect("/codler_description")

        codLER = format_codLER(codLER)
        if codLER == None:
            flash("O código LER inserido deve ter 6 dígitos no formato XX XX XX ou XXXXXX")
            return redirect("/codler_description")

        if not description:
            flash("O LER não foi inserido no sistema! - Faltou descrição do código LER - Repita o processo")
            return redirect("/codler_description")

        # Insert new code "LER" and description. Ensure non-duplication of code "LER"
        try:
            db.execute("""
            INSERT INTO
                codler_description (codLER, description) VALUES(?,?)
            """, codLER, description)
        except:
            # table codler_description: codLER TEXT NOT NULL UNIQUE
            flash("O código LER que tentou inserir já se encontra no sistema!")
            return redirect("/codler_description")

        # Show all codes "LER"
        all_codLER = db.execute("""
        SELECT
            * 
        FROM
            codler_description""")

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
            flash("Não foram realizadas alterações! - Faltou código LER - Repita o processo")
            return redirect("/codler_description")

        novo_codLER = format_codLER(novo_codLER)
        if novo_codLER == None:
            flash("Não foram realizadas alterações! - O código LER inserido deve ter 6 dígitos\
                no formato XX XX XX ou XXXXXX - Repita o processo")
            return redirect("/codler_description")

        if not nova_descrição:
            flash("Não foram realizadas alterações! - Faltou descrição do código LER - Repita o processo")
            return redirect("/codler_description")

        # Make changes to the codLER_description table
        db.execute("""
        DELETE FROM
            codler_description
        WHERE
            codler = ?""", antigo_codLER)
        
        db.execute ("""
        INSERT INTO
            codler_description (codLER,description) VALUES(?,?)
        """, novo_codLER, nova_descrição)

        # Show all LER and descriptions (after changes)
        all_codLER = db.execute("""
        SELECT
            *
        FROM
            codler_description
        ORDER BY
            codLER DESC""")

        # Update wastemap: LER code
        db.execute("""
        UPDATE
            wastemap
        SET
            codLER = ?,residuo = ?
        WHERE
            codLER = ?
        """,novo_codLER, nova_descrição, antigo_codLER)

        return render_template("codler_description.html", all_codLER=all_codLER)


@app.route("/operation_description", methods=["GET", "POST"])
@login_required
def operation_description():

    if request.method == "GET":
        all_operations = db.execute("""
        SELECT
            * 
        FROM
            operation_description""")

        return render_template("operation_description.html", all_operations=all_operations)

    else:
        operation = request.form.get("operation")
        description = request.form.get("description")

        if not operation:
            flash("A operação não foi inserida nos sistema! - Faltou operação de valorização/eliminação - \
                Repita o processo")
            return redirect("/operation_description")

        if not description:
            flash("A operação não foi inserida nos sistema! - Faltou descrição da operação\
                de valorização/eliminação - Repita o processo")
            return redirect("/operation_description")

        # Insert new operation and description. Ensure non-duplication
        try:
            db.execute("""
            INSERT INTO
                operation_description (operation, description) VALUES(?,?)
            """, operation, description)
        except:
            # table operation_description: operation TEXT NOT NULL UNIQUE,
            flash("A operação de valorização/eliminação que tentou inserir já se encontra no sistema!")
            return redirect("/operation_description")

        # Show all operations
        all_operations = db.execute("""
        SELECT
            *
        FROM
            operation_description""")

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
            flash("Não foram realizadas alterações! - Faltou operação de valorização/eliminação - \
                Repita o processo")
            return redirect("/operation_description")
        if not nova_descrição:
            flash("Não foram realizadas alterações! - Faltou descrição da operação de valorização/eliminação - \
                Repita o processo")
            return redirect("/operation_description")

        # Make changes to the valorization/elimination operation
        db.execute("""
        DELETE FROM
            operation_description WHERE operation = ?
        """, antiga_operação)
        
        db.execute ("""
        INSERT INTO
            operation_description (operation,description) VALUES(?,?)
        """, nova_operação, nova_descrição)

        # Show all operations (after changes)
        all_operations = db.execute("""
        SELECT
            *
        FROM
            operation_description
        ORDER BY
            operation DESC""")

        # Update wastemap: operation
        db.execute("""
        UPDATE
            wastemap
        SET
            dest_final = ?
        WHERE
            dest_final = ?
        """, nova_operação, antiga_operação)

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

    # All establishments and all contracts with APA "GENERAL TEC"
    if request.method == "GET":

        return render_template("mirr.html", mirr_options = mirr_options, years=years)

    else:
        estab_chosen = request.form.get("estab_chosen")
        year = request.form.get("year")

        # Given the user who is logged in, determine the producer's username:
        producer = db.execute ("""
        SELECT
            username
        FROM
            users
        WHERE
            users.id = ?
        """, session["user_id"])
            
        producer = producer[0]["username"]
        
        # Using Common Table Expression (CTE)
        # Sources:
        # https://www.sqlitetutorial.net/sqlite-cte/
        # https://learnsql.com/blog/cte-vs-subquery/
        # I also have used Chat GPT for a better explanation of CTE

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
                obra = :obra AND dest_final != 'AP' AND empresa_id = :empresa_id AND strftime('%Y', data) = :ano AND produtor = :produtor
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
                obra = :obra AND dest_final != 'AP' AND empresa_id = :empresa_id AND strftime('%Y', data) = :ano AND produtor = :produtor
            GROUP BY
                wastemap.codLER,
                wastemap.apa_dest,
                wastemap.dest,
                wastemap.transp,
                wastemap.dest_final
            """, **params_subset(["obra","empresa_id","ano","produtor"]))


    # For the MIRR, APA of the establishment GT - General Tecnorém
    else:
        mirr = db.execute("""
        WITH total_each_LER AS (
            SELECT
                wastemap.codLER,
                SUM(ton) AS total
            FROM
                wastemap
            WHERE
                apa_estab = 'GT' AND dest_final != 'AP' AND empresa_id = :empresa_id AND strftime('%Y', data) = :ano AND produtor = :produtor
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
                apa_estab = 'GT' AND dest_final != 'AP' AND empresa_id = :empresa_id AND strftime('%Y', data) = :ano AND produtor = :produtor
            GROUP BY
                wastemap.codLER,
                wastemap.apa_dest,
                wastemap.dest,
                wastemap.transp,
                wastemap.dest_final
            """, **params_subset(["empresa_id","ano","produtor"]))

    if not mirr:
        flash("Não existem registos para as opções selecionadas")
        return redirect("/mirr")

    return render_template("mirr.html", mirr=mirr, mirr_options = mirr_options, years=years)
