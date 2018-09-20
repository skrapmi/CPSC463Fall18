from flask import Flask
import webbrowser

app = Flask(__name__)
url = "localhost:3000"

@app.route(url)

if __name__ == '__main__':
    app.run()