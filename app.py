from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

matriz = None
solucao = None
n = 0

def gerarProblema(n):
    matriz = np.random.randint(low=10, high=100, size=(n,n))
    np.fill_diagonal(matriz, 0)
    return matriz

def gerarSolucao(n):
    return np.random.permutation(n)

def avaliar(n, solucao, matriz):
    distancia = 0
    for i in range(n-1):
        distancia += matriz[solucao[i]][solucao[i+1]]
    distancia += matriz[solucao[n-1]][solucao[0]]
    return distancia

@app.route("/", methods=["GET", "POST"])
def index():
    global matriz, solucao, n
    distancia = None

    if request.method == "POST":
        acao = request.form.get("acao")

        if acao == "problema":
            if request.form.get("n"):
                n = int(request.form.get("n"))
            matriz = gerarProblema(n)
            solucao = None

        elif acao == "solucao" and matriz is not None and n > 0:
            solucao = gerarSolucao(n)

        elif acao == "avaliar" and matriz is not None and solucao is not None:
            distancia = avaliar(n, solucao, matriz)

    return render_template("index.html",
                           matriz=matriz,
                           solucao=solucao,
                           distancia=distancia)

if __name__ == "__main__":
    app.run(debug=True)