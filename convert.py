import os
from flask import Flask, request

app = Flask("Conversao")

@app.route('/convert',methods=['POST'])
def retornaFraseNota():
    body = request.get_json()
    frase = body["frase"]
    avalicacoes = [('um', 1), ('dois', 2), ('três', 3), ('tres', 3), ('quatro', 4), ('cinco', 5)]
    newString = ""
    i = 0
    nota = 0
    while i < len(avalicacoes):  
        if avalicacoes[i][0] in frase:
            print("Palavra encontrada")
            newString = frase.replace(avalicacoes[i][0], str(avalicacoes[i][1]))
            nota = avalicacoes[i][1]
            print(newString)
            print("Nota", str(avalicacoes[i][1]) )
            if nota < 3:
                qualidade = "RUIM"
            elif nota  >= 3 and nota < 4:
                qualidade = "MEDIA"
            elif nota >= 4 and nota < 5:
                qualidade = "BOA"
            elif nota == 5:
                qualidade = "EXCELENTE"
            break
        else:
            print("não encontrada")
        i = i+1
    return {"convertida": newString, "nota": nota, "qualidade": str(qualidade)}


port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)