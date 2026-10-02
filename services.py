from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/eleicoes/velas', methods=['GET'])
def get_eleicoes_data():
    dados = {
      "eleicao": {
        "data_eleicao": "04/10/2026",
        "dia_semana": "Domingo",
        "inicio_votacao": "08:00",
        "fim_votacao": "17:00 (Sujeito a tolerância de filas)",
        "inicio_apuracao": "Imediatamente após o encerramento geral das urnas"
      },
      "status_conexao": "TSE_SINCRONIZADO",
      "totalizacao": {
        "status_geral": "Contagem oficial iniciará após o encerramento da votação."
      },
      "candidatos": [
        {
          "nome": "Luiz Inácio Lula da Silva",
          "partido": "PT",
          "numero": 13,
          "posicao": 1,
          "percentual": 0,
          "votos": "0",
          "status_texto": "⚠️ ELEIÇÃO NESTE DOMINGO (04/10/2026) — PREPARAÇÃO EM ANDAMENTO",
          "cor_vela": "#CC0000",
          "cor_badge": "#F59E0B"
        },
        {
          "nome": "Flávio Bolsonaro",
          "partido": "PL",
          "numero": 22,
          "posicao": 2,
          "percentual": 0,
          "votos": "0",
          "status_texto": "⚠️️ ELEIÇÃO NESTE DOMINGO (04/10/2026) — PREPARAÇÃO EM ANDAMENTO",
          "cor_vela": "#002D62",
          "cor_badge": "#F59E0B"
        }
      ]
    }
    return jsonify(dados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
