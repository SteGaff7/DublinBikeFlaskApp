from flask import Flask, render_template
app = Flask(__name__)

@app.route("/home") # Tells the browser where to look
def home():
    return render_template('home.html') # This points to the html page

@app.route("/about") # Tells the browser where to look
def How_it_works():
    return render_template('how_it_works.html', title='About') # This points to the html page

@app.route("/subscription") # Tells the browser where to look
def subscription():
    return render_template('subscription.html', title='Subscriptions') # This points to the html page

@app.route("/contact") # Tells the browser where to look
def Contact():
    return render_template('contact.html', title='Contact') # This points to the html page

if __name__ == '__main__': # This will allow us to run the and change the page without restarting the server
    app.run(debug=True)
