from flask import Flask, render_template_string, make_response, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a very very secret key'  # Necessary for session management and CSRF protection
csrf = CSRFProtect(app)  # Initialize CSRF protection

class TransferForm(FlaskForm):
    amount = StringField('Amount', validators=[DataRequired()])
    to_account = StringField('To Account', validators=[DataRequired()])
    submit = SubmitField('Transfer')

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
    <form method="POST" action="/">
        {{ form.hidden_tag() }}
        <input type="text" name="amount" placeholder="Amount" required>
        <input type="text" name="to_account" placeholder="To Account Number" required>
        <button type="submit">Transfer</button>
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TransferForm()
    if form.validate_on_submit():  # Correct use of validate_on_submit to check form validation and CSRF token
        amount = form.amount.data
        to_account = form.to_account.data
        return f"Transferred ${amount} to account {to_account}."
    # Render the page with the form
    return render_template_string(HTML, form=form)

@app.route('/set-cookie')
def set_cookie():
    response = make_response("<h2>Cookie Set!</h2><p>A cookie has been set.</p>")
    response.set_cookie('authcookie', 'authentication')
    return response

if __name__ == '__main__':
    app.run(debug=True)
