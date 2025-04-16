from flask import Flask, render_template, redirect, request
from cart import Cart
from billing import calculate_bill
from db import get_connection

app = Flask(__name__)
cart = Cart()

@app.route("/", methods=["GET"])
def home():
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
    return render_template("index.html", products=products)

@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    product_id = int(request.form["product_id"])
    quantity = int(request.form["quantity"])

    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            if product:
                cart.add_item(product, quantity)
    return redirect("/")

@app.route("/cart")
def view_cart():
    return render_template("cart.html", cart=cart.get_items())

@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):
    cart.remove_item(product_id)
    return redirect("/cart")

@app.route("/clear-cart")
def clear_cart():
    cart.clear_cart()
    return redirect("/cart")

@app.route("/bill")
def show_bill():
    cart_items = cart.get_items()
    connection = get_connection()

    with connection:
        with connection.cursor() as cursor:
            for item in cart_items:
                product_id = item['product']['id']
                quantity = item['quantity']

                cursor.execute("SELECT stock FROM products WHERE id = %s", (product_id,))
                stock = cursor.fetchone()['stock']

                if stock >= quantity:
                    cursor.execute("UPDATE products SET stock = stock - %s WHERE id = %s", (quantity, product_id))
                else:
                    item['quantity'] = 0  # mark as unfulfilled
            connection.commit()

    cart.items = [item for item in cart_items if item['quantity'] > 0]
    bill = calculate_bill(cart.get_items())
    cart.clear_cart()  # empty cart after billing
    return render_template("bill.html", bill=bill)

if __name__ == "__main__":
    app.run(debug=True)