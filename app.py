# Main file for Shirts4Mike
from pathlib import Path
THIS_FOLDER = Path(__file__).parent.resolve()
sendgrid_file = THIS_FOLDER / "sendgrid.txt"

# Import statement
from flask import (
    Flask,
    render_template,
    url_for,
    flash,  
    redirect,
    request,
    jsonify,
    session
)
from markupsafe import Markup 
import requests
from requests.auth import HTTPBasicAuth
from flask_mail import Mail
from flask_mail import Message




import sendgrid
from datetime import date

# App setup
app = Flask(__name__)

app.config["SECRET_KEY"] = "some_really_long_random_string_here"

app.config['MAIL_SERVER']="smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "anthony@PubCrawlers.uk"
app.config['MAIL_PASSWORD'] = "bycc reor hqxx cycz"
app.config['MAIL_USE_TLS'] = True


mail = Mail(app)


# Get details for sendgrid details
sendgrid_details = []

with open(sendgrid_file) as f:
    sendgrid_details = f.readlines()
    sendgrid_details = [x.strip("\n") for x in sendgrid_details]

# Global Variables
products_info = [
    {
        "id": "101",
        "name": "Standard Package",
        "img": "branding-title.jpg",
        "price": 40,
        "quantity": ["1","2","3","4","5","6","7","8","9","10"],
        "paypal": "LNRBY7XSXS5PA",
        "description": "The Standard Package - 8 Holes, 8 Drinks"
    },
]

# Functions

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)



# Routes
# All functions should have a page_title variables if they render templates

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

@app.route("/termsandconditions")
def termsandconditions():
    return render_template("termsandconditions.html")
@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/formsubmit", methods=['POST'])
def formsubmit():
    name = request.form['name']
    email = request.form['email']
    society = request.form['society']
    home_email = 'events@pubcrawlers.uk'
    try:
        order_id = session['order']
    except:
        order_id=0
    try:
        amount = session['amount']
        quantity = str(float(amount) // 25)
    except:
        amount = 'NA'
        quantity = 'NA'

    send_email("PubCrawlers UK Order Confirmation",
                  sender="events@pubcrawlers.uk",
                  recipients=[email, home_email], text_body="", html_body=render_template('email_templates/confirmation_template.html', name=name, society=society, order_id=order_id, amount=amount, quantity=quantity))

    return render_template("index.html")

@app.route("/payments/<order_id>/capture", methods=["POST"])
def capture_payment(order_id):  # Checks and confirms payment
    captured_payment = approve_payment(order_id)
    session['order'] = order_id
    session['amount'] = captured_payment['purchase_units'][0]['payments']['captures'][0]['amount']['value']
    # print(captured_payment) # or you can do some checks from this captured data details
    return jsonify(captured_payment)
def approve_payment(order_id):
    #api_link = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
    api_link = f"https://api-m.paypal.com/v2/checkout/orders/{order_id}"
    #test_client_id = "Ae4YDp1BcCpDYnFZSvZzgEjiTQPMUSxVxEkPFFELIiFY9SHlR-WEsN-szQQunxA5DiDjVGh_1STCaGz7"
    #test_secret = "EDfuxXiy0HIh3R8BWYIChfmTtme3Gbr20OQMK1vK6mTOJuHnV-OkrREXZrrJV5cjVzK7jL1IZxCzi2_4"
    client_id = "AWLD1Wt0dWZAxm14AceDnqNrQJFmrvGMUTte9CQ6q9EX4pyowNNwxx1K9rmsqR70osnvCVHpBEwCQ_Yy"
    secret = "EOSD6rVl3yMZs5PMhu-MfYBwzuyH_MOnanLqIrCzxfL0Nugngok7lix5ElJcUF3a-xd7-bv0EPynw7cS"
    basic_auth = HTTPBasicAuth(client_id, secret)
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url=api_link, headers=headers, auth=basic_auth)
    response.raise_for_status()
    json_data = response.json()
    return json_data




@app.route("/checkout")
def checkout():
    """Function for checkout page"""
    return render_template("checkout.html",quantity=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'])


@app.route("/receipt")
def receipt():
    """Function to display receipt after purchase"""
    context = {"page_title": "PubGolf", "current_year": date.today().year}
    return render_template("receipt.html", **context)


@app.route("/contact")
def contact():
    """Function for contact page"""
    context = {"page_title": "PubGolf", "current_year": date.today().year}
    return render_template("contact.html", **context)





# Run application
if __name__ == "__main__":
    app.run(debug=True)
