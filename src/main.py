from flask import request, redirect

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        print(f"Novo cadastro: {nome}, {email}")  # Só para testar
        return redirect("/login")
    return render_template("cadastro.html")
