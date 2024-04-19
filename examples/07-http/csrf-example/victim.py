from flask import Flask, request, render_template_string, make_response

app = Flask(__name__)

# Inline HTML Template for the form
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bank Transfer</title>
</head>
<body>
    <h1>Transfer Money</h1>
    <form action="http://localhost:5000/transfer" method="POST">
        <input type="text" name="amount" placeholder="Amount" required>
        <input type="text" name="to_account" placeholder="To Account Number" required>
        <button type="submit">Transfer</button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/set-cookie')
def set_cookie():
    response = make_response("<h2>Cookie Set!</h2><p>A cookie has been set.</p>")
    # Set a harmless cookie
    response.set_cookie('authcookie', 'authentication')
    return response

@app.route('/transfer', methods=['POST'])
def transfer():
    # Check if the correct authentication cookie is present
    if request.cookies.get('authcookie') == 'authentication':
        amount = request.form['amount']
        to_account = request.form['to_account']
        return f"Transferred ${amount} to account {to_account}."
    else:
        return "Authentication failed.", 403

if __name__ == '__main__':
    app.run(debug=True)
