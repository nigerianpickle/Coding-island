from flask import Flask, render_template, request

app = Flask(
    __name__,
    template_folder="html_pages",  
    static_folder="assets"         
)



# Home page
@app.route("/")
def home():
    return render_template("index.html")



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/run-script")
def run_script():
    # Example Python logic (you can replace this with your own script)
    result = 2 * 5  # simple calculation
    return f"<h2>Result of Python script: {result}</h2>"