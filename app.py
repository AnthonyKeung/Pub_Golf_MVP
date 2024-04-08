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
)
import flask_resize
from markupsafe import Markup 
import requests
from requests.auth import HTTPBasicAuth


import sendgrid
from datetime import date

# App setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "some_really_long_random_string_here"


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





# Routes
# All functions should have a page_title variables if they render templates

@app.route("/")
def index():
    """Function for Shirts4Mike Homepage"""
    context = {"page_title": "PubGolf", "current_year": date.today().year}
    counter = 0
    product_data = []
    context["product_data"] = Markup("".join(product_data))
    return render_template("index.html", **context)

@app.route("/termsandconditions")
def termsandconditions():
    return render_template("termsandconditions.html")
@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/payments/<order_id>/capture", methods=["POST"])
def capture_payment(order_id):  # Checks and confirms payment
    captured_payment = approve_payment(order_id)
    # print(captured_payment) # or you can do some checks from this captured data details
    return jsonify(captured_payment)
def approve_payment(order_id):
    api_link = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
    client_id = "Ae4YDp1BcCpDYnFZSvZzgEjiTQPMUSxVxEkPFFELIiFY9SHlR-WEsN-szQQunxA5DiDjVGh_1STCaGz7"
    secret = "EDfuxXiy0HIh3R8BWYIChfmTtme3Gbr20OQMK1vK6mTOJuHnV-OkrREXZrrJV5cjVzK7jL1IZxCzi2_4"
    basic_auth = HTTPBasicAuth(client_id, secret)
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url=api_link, headers=headers, auth=basic_auth)
    response.raise_for_status()
    json_data = response.json()
    return json_data



@app.route("/shirts")
def shirts():
    """Function for the Shirts Listing Page"""
    context = {"page_title": "PubGolf", "current_year": date.today().year}
    product_data = []
    for product in products_info:
        product_data.append(Markup(get_list_view_html(product)))
    context["product_data"] = Markup("".join(product_data))
    return render_template("shirts.html", **context)


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


# Route to send email
@app.route("/send", methods=['POST'])
def send():
    """Function to send email using sendgrid API"""
    sendgrid_object = sendgrid.SendGridClient(
        sendgrid_details[0], sendgrid_details[1])
    message = sendgrid.Mail()
    sender = request.form["email"]
    subject = request.form["name"]
    body = request.form["message"]
    message.add_to("charlie.thomas@attwoodthomas.net")
    message.set_from(sender)
    message.set_subject(subject)
    message.set_html(body)
    sendgrid_object.send(message)
    flash("Email sent.")
    return redirect(url_for("contact"))


# Run application
if __name__ == "__main__":
    app.run(debug=True)
