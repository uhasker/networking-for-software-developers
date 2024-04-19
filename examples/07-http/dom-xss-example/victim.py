from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    # The page includes a JavaScript that takes URL parameters and uses them unsafely in the DOM.
    return render_template_string("""
    <html>
    <head><title>DOM XSS Example</title></head>
    <body>
        <h2>DOM-Based XSS Demonstration</h2>
        <input id="data" type="text" placeholder="Enter your data here" />
        <button onclick="updateContent()">Update Content</button>
        <script>
            function getDataFromURL() {
                var url = document.location.href;
                var start = url.indexOf("data=") + 5;  // Find the start of the value and adjust to get the position right after "data="
                if (start === 4) {  // if index returned is -1 (not found) and adjusted by +5 it becomes 4
                    return "";  // No "data" parameter found
                }
                var end = url.indexOf("&", start);
                if (end === -1) {  // Check if the "data" parameter is the last in the URL
                    end = url.length;---------.....v
                }
                return decodeURIComponent(url.substring(start, end));
            }

            function updateContent() {
                var data = getDataFromURL();
                document.getElementById('data').value = data;
            }

            window.onload = function() {
                updateContent();
            };
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(port=5000)