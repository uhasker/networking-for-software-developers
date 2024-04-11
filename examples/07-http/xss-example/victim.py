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

    # response.headers['Content-Security-Policy'] = "script-src 'self'"

    return response

if __name__ == "__main__":
    app.run(port=5000)
