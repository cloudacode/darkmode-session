import datetime
import redis
from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)

app.secret_key = 'SECRET_KEY'

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://127.0.0.1:6379')
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=5)

server_session = Session(app)

@app.route('/', methods=['GET', 'POST'])
def hello():

    # Dummy messages
    messages = ['Welcome',
                'Let\'s switch the mode',
                ]

    # Init theme session object
    if session.get('theme') is None:
        session['theme'] = 'light-mode'

    # Save the form data to the session object
    if request.method == 'POST':
        if session['theme'] == "light-mode":
            session['theme'] = "dark-mode"
        else:
            session['theme'] = "light-mode"

        session['mode'] = request.form['switch']

    theme = session['theme']
    # print(theme)

    # Render template to display objects
    return render_template('switchmode.html', mode=theme, messages=messages, utc_dt=datetime.datetime.utcnow())

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port='8080')
