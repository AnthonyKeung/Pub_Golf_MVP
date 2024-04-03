# Main file for Shirts4Mike

# Import statement
from flask import (
    Flask,
    render_template,
    Markup,
    url_for,
    flash,
    redirect,
    request
)

import sendgrid
from datetime import date

# App setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "some_really_long_random_string_here"

# Get details for sendgrid details
sendgrid_file = "sendgrid.txt"
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


def get_list_view_html(product):
    """Function to return html for given shirt

    The product argument should be a dictionary in this structure:
    {
        "id": "shirt_id",
        "name": "name_of_shirt",
        "img": "image_name.jpg",
        "price": price_of_shirt_as_int_or_flat,
        "paypal": "paypal_id"
        "sizes": ["array_of_sizes"]
    }

    The html is returned in this structure:
    <li>
      <a href="shirt/shirt_id">
        <img src="/static/shirt_img" alt="shirt_name">
        <p>View Details</p>
      </a>
    </li>
    """
    output = ""
    image_url = url_for("static", filename=product["img"])
    shirt_url = url_for("shirt", product_id=product["id"])
    output = output + "<li>"
    output = output + '<a href="' + shirt_url + '">'
    output = (
        output + '<img src="' + image_url +
        '" al  t="' + product["name"] + '">')
    output = output + "<p>View Details</p>"
    output = output + "</a>"
    output = output + "</li>"

    return output


# Routes
# All functions should have a page_title variables if they render templates

@app.route("/")
def index():
    """Function for Shirts4Mike Homepage"""
    context = {"page_title": "PubGolf", "current_year": date.today().year}
    counter = 0
    product_data = []
    for product in products_info:
        counter += 1
        if counter < 5:  # Get first 4 shirts
            product_data.append(
                Markup(get_list_view_html(product))
            )
    context["product_data"] = Markup("".join(product_data))
    return render_template("index.html", **context)


@app.route("/shirts")
def shirts():
    """Function for the Shirts Listing Page"""
    context = {"page_title": "PubGolf", "current_year": date.today().year}
    product_data = []
    for product in products_info:
        product_data.append(Markup(get_list_view_html(product)))
    context["product_data"] = Markup("".join(product_data))
    return render_template("shirts.html", **context)


@app.route("/shirt/<product_id>")
def shirt(product_id):
    """Function for Individual Shirt Page"""
    context = {"page_title": "PubGolf", "current_year": date.today().year}
    my_product = ""
    for product in products_info:
        if product["id"] == product_id:
            my_product = product
    context["product"] = my_product
    return render_template("shirt.html", **context)


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
