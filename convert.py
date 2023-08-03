import os
import re
from flask import Flask, request, jsonify
import speech_recognition as sr
import requests

app = Flask("Conversao")

# @app.route('/convert',methods=['POST'])
# def retornaFraseNota():
#     body = request.get_json()
#     frase = body["frase"]
#     avalicacoes = [('um', 1), ('dois', 2), ('três', 3), ('tres', 3), ('quatro', 4), ('cinco', 5)]
#     newString = ""
#     i = 0
#     nota = 0
#     while i < len(avalicacoes):
#         if avalicacoes[i][0] in frase:
#             print("Palavra encontrada")
#             newString = frase.replace(avalicacoes[i][0], str(avalicacoes[i][1]))
#             nota = avalicacoes[i][1]
#             print(newString)
#             print("Nota", str(avalicacoes[i][1]) )
#             if nota < 3:
#                 qualidade = "RUIM"
#             elif nota  >= 3 and nota < 4:
#                 qualidade = "MEDIA"
#             elif nota >= 4 and nota < 5:
#                 qualidade = "BOA"
#             elif nota == 5:
#                 qualidade = "EXCELENTE"
#             break
#         else:
#             print("não encontrada")
#         i = i+1
#     return {"convertida": newString, "nota": nota, "qualidade": str(qualidade)}



@app.route("/convert", methods=["POST"])
def retornaFraseNota():
    body = request.get_json()
    frase = body["frase"]
    avalicacoes = ["0", "1", "2", "3", "4", "5"]
    i = 0
    nota = 0

    numero_encontrado = re.search(r'\b\d+(\.\d+)?\b', frase)
    if numero_encontrado:
        numero = float(
            numero_encontrado.group()
        )  # Converte o número encontrado para float
        nota = int(numero)  # Converte o número para inteiro
    else:
        return {"error": "Nenhum número de 1 a 5 encontrado na frase."}, 400

    if nota not in range(1, 6):
        return {"error": "Somente números de 1 a 5 são permitidos."}, 400

    # Agora que temos a nota, podemos determinar a qualidade
    if nota < 3:
        qualidade = "RUIM"
    elif nota >= 3 and nota < 4:
        qualidade = "MEDIA"
    elif nota >= 4 and nota < 5:
        qualidade = "BOA"
    elif nota == 5:
        qualidade = "EXCELENTE"

    return {"convertida": frase, "nota": nota, "qualidade": qualidade}

    # while i < len(avalicacoes):
    #     if avalicacoes[i] in frase:
    #         print("Palavra encontrada")
    #         nota = int(avalicacoes[i])
    #         print("Nota", str(avalicacoes[i]))
    #         if nota < 3:
    #             qualidade = "RUIM"
    #         elif nota >= 3 and nota < 4:
    #             qualidade = "MEDIA"
    #         elif nota >= 4 and nota < 5:
    #             qualidade = "BOA"
    #         elif nota == 5:
    #             qualidade = "EXCELENTE"
    #         break
    #     else:
    #         print("não encontrada")
    #     i = i + 1
    # if nota not in range(1, 6):
    #     return {"error": "Somente números de 1 a 5 são permitidos."}, 400

    # if not str(nota).isdigit():
    #     return {
    #         "error": "Números decimais não são permitidos. Somente números inteiros de 1 a 5 são aceitos."
    #     }, 400

    # return {"convertida": frase, "nota": nota, "qualidade": str(qualidade)}


@app.route("/audio-to-text", methods=["POST"])
def audio_to_text():
    # Verifica se o arquivo de áudio foi enviado na requisição
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]

    print(audio_file.filename)

    # Verifica se o arquivo enviado é do tipo permitido (áudio)
    if audio_file.filename == "" or not audio_file.filename.lower().endswith(
        (".wav", ".mp3", ".ogg")
    ):
        return (
            jsonify(
                {
                    "error": "Invalid audio file format. Only .wav, .mp3, and .ogg formats are supported."
                }
            ),
            400,
        )

    # Salva o arquivo de áudio temporariamente
    audio_path = "temp_audio.wav"
    audio_file.save(audio_path)

    # Inicia o reconhecimento de fala
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    # Realiza a transcrição do áudio em texto
    try:
        text = recognizer.recognize_google(
            audio, language="pt-BR"
        )  # Altere para 'en-US' se for em inglês
        return jsonify({"frase": text}), 200
    except sr.UnknownValueError:
        return jsonify({"error": "Unable to recognize speech"}), 500
    except sr.RequestError:
        return jsonify({"error": "Failed to request the API"}), 500
    finally:
        # Remove o arquivo temporário após o uso
        os.remove(audio_path)


port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
