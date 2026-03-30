from datetime import datetime
from flask import Flask, jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec

app = Flask(__name__)

spec = FlaskPydanticSpec('flask',
                         title='Cashback API - SENAI-SP',
                         version='1.0')
spec.register(app)


@app.route('/', methods=['GET'])
def principal():
    dados = {
        "mensagem": "Sua API esta online",
    }
    return jsonify(dados), 200


@app.route('/desconto/<primeira_compra>/<valor>', methods=['GET'])
def desconto(primeira_compra, valor):
    try:
        valor = float(valor)
        if valor <= 100:
            desconto = 0

        elif 101 <= valor <= 500:
            desconto = (valor * 5) / 100
        else:
            desconto = (valor * 10) / 100

        vf1 = valor - desconto
        if primeira_compra == "True":
            if vf1 > 50:
                total_desconto = desconto + 25
            else:
                total_desconto = desconto
        else:
            total_desconto = desconto

        valor_total = valor - (total_desconto)

        data_hj = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        dados = {
            "data_processamento:": data_hj,
            "valor_original:": valor,
            "total_desconto": total_desconto,
            "valor_final:": valor_total
        }

        return jsonify(dados), 200

    except ValueError:
        dados = {
            "status": "error",
            "msg": "Dados invalidos"
        }
        return jsonify(dados), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)