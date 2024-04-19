from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

@app.route('/set-cookie')
def set_cookie():
    response = make_response("<h2>Cookie Set!</h2><p>A cookie has been set.</p>")
    # Set a harmless cookie
    response.set_cookie('supersecret', 'information')
    return response

@app.route('/')
def home():
    user_input = request.args.get('input', 'No input provided')  # Get user input from query parameter
    # The user_input is directly rendered into the HTML template below, which is vulnerable to XSS
    response = make_response(render_template_string(f"""
    <h2>Reflected XSS Example</h2>
    <p>Your input was: {user_input}</p>
    <form method="get">
        <input type="text" name="input" placeholder="Enter something here..." />
        <input type="submit" />
    </form>
    """))
    return response

if __name__ == "__main__":
    app.run(port=5000)
