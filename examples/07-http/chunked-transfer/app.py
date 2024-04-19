from flask import Flask, Response
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

def generate_numbers():
    """Generator function to yield numbers."""
    for number in range(1, 11):  # Example: generate numbers 1 to 10
        yield f"{number}\n"
        time.sleep(1)  # Simulate a delay

@app.route('/stream')
def stream():
    return Response(generate_numbers(), content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True)