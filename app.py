from flask import Flask


app = Flask(__name__)

with app.app_context():
    import routes
    from dashf import histo_lstm


    app = histo_lstm.init_dash(app)

if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True, port=8080)
