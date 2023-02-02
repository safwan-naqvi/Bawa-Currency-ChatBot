from flask import Flask,request,jsonify
import requests
app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name'][0]
    print(str(source_currency) +"  "+str(amount)+"  "+str(target_currency)+"  cf = ")

    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount = amount*cf
    final_amount = round(final_amount,2)
    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }

    return jsonify(response)

def fetch_conversion_factor(source,target):
    url = "https://currency-exchange.p.rapidapi.com/exchange"

    querystring = {"from": str(source), "to": str(target), "q": "1.0"}

    headers = {
        "X-RapidAPI-Key": "979ef49584msh0c40f43733290e2p111861jsn1e5b8d23bb6a",
        "X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    return response

if __name__ == "__main__":
    app.run(debug=True)