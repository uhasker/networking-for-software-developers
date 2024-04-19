from flask import Flask, Response
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

def event_stream():
    for count in range(5):  # Limit the number of messages
        time.sleep(1)  # simulate some work being done
        yield f"data: Message {count} at {time.ctime()}\n\n"
    # After sending the last message, you could send a special event to tell the client to close the connection
    yield "event: close\n\n"

@app.route('/events')
def sse_request():
    return Response(event_stream(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)