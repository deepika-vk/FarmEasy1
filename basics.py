from flask import Flask,render_template
app=Flask(__name__)

@app.route("/")
def deepika():
  return "hello Deepika"

@app.route("/deep")
def deep():
  return "hello Depika"

@app.route("/de")
def dep():
  name="Deepika"
  return render_template("index.html",name1=name)

app.run(debug=True)    