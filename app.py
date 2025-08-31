from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-started')
def get_started():
    # Redirect or render a page to onboard user
    return "Get Started Page (Under Construction)"

@app.route('/schedule-consultation')
def schedule_consultation():
    # Redirect or render a form/page to schedule consultation
    return "Schedule Consultation Page (Under Construction)"

if __name__ == '__main__':
    app.run(debug=True)
