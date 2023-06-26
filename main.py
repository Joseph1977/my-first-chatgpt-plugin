import os
from waitress import serve
from flask import Flask, jsonify, send_from_directory
import requests

API_KEY = os.environ['EXCHANGERATE-API-KEY']

app = Flask(__name__)


def convert_currency(amount, base_currency, target_currency):
  url = f"https://api.apilayer.com/exchangerates_data/convert?from={base_currency}&to={target_currency}&amount={amount}"

  headers = {"apikey": API_KEY}
  response = requests.request("GET", url, headers=headers)
  print (response)
  if response.status_code == 200:
    data = response.json()
    return data["result"]
  else:
    raise Exception(f"Error: {response.status_code}, {response.text}")


@app.route('/convert/<amount>/<base_currency>/<target_currency>')
def get_conversion_rate(amount, base_currency, target_currency):

  try:
    converted_amount = convert_currency(amount, base_currency, target_currency)

    if converted_amount:
      response = {
        'amount': amount,
        'base_currency': base_currency,
        'target_currency': target_currency,
        'converted_amount': converted_amount
      }
      return jsonify(response), 200
    else:
      error_message = "Currency conversion failed."
      return jsonify({'error': error_message}), 500
  except Exception as e:
    return jsonify({"error": str(e)}), 400


@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
  return send_from_directory('.',
                             'ai-plugin.json',
                             mimetype='application/json')


@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
  return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')


if __name__ == '__main__':
  serve(app, host="0.0.0.0", port=8080)
