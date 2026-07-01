from flask import Flask, render_template, request, jsonify
from funcoes import (
    carregar_pokemons, carregar_ginasios, selecionar_ginasios,
    executar_algoritmo_genetico, score_time_vs_ginasio, poder_total_ginasio,
    resultado_provavel
)

# inicializa o servidor Flask
app = Flask(__name__)

# carrega os dados uma unica vez ao iniciar o servidor
pokemons = carregar_pokemons()
ginasios = carregar_ginasios()

# rota principal da interface
@app.route("/")
def index():
    return render_template("index.html")

# rota que recebe a requisicao da interface e retorna o time gerado
@app.route("/gerar-time", methods=["POST"])
def gerar_time():
    dados = request.json
    quantidade = dados.get("quantidade", 0)

    ginasios_selecionados = selecionar_ginasios(ginasios, quantidade)
    time, fitness = executar_algoritmo_genetico(pokemons, ginasios_selecionados)

    ginasios_info = []
    for ginasio in ginasios_selecionados:
        score_time = score_time_vs_ginasio(time, ginasio)
        score_ginasio = poder_total_ginasio(time, ginasio)

        if score_time == -1000:
            resultado = "Derrota"
        else:
            resultado = resultado_provavel(score_time, score_ginasio)

        ginasios_info.append({
            "nome": ginasio.nome,
            "tipo": ginasio.tipo,
            "score_time": round(score_time, 2) if score_time != -1000 else 0,
            "score_ginasio": round(score_ginasio, 2),
            "resultado": resultado,
            "pokemons": [
                {"id": p.id, "nome": p.nome, "tipos": p.tipos}
                for p in ginasio.pokemons
            ]
        })

    return jsonify({
        "time": [
            {"id": p.id, "nome": p.nome, "tipos": p.tipos}
            for p in time
        ],
        "ginasios": ginasios_info,
        "fitness": fitness
    })

if __name__ == "__main__":
    app.run(debug=True)
