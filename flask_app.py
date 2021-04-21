from flask import Flask, render_template
import dash_app_multipage_attempt
from

app = Flask(__name__)
app = create_dashboard(app)


@app.route('/')
def index():
    return render_template('index.html', title='Group 22 Home')


@app.route('/matplotlib')
def matplotlib():
    return render_template('matplotlib.html', title="Matplotlib charts")


@app.route('/express')
def express():
    return render_template('express.html', title="Plotly express charts")


@app.route('/dash')
def dash():
    return render_template('dash.html', title="Dash chart explanations")


if __name__ == '__main__':
    app.run()
