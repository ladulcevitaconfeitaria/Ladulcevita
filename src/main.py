from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        print(f"Novo cadastro: {nome}, {email}")
        return redirect("/login")
    return render_template("cadastro.html")

if __name__ == "__main__":
    app.run()
