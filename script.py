from flask import Flask, render_template, request
import StockFunctions3 as stkF

# This is the API between HTML and Python
app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/plot/", methods=['POST'])
def plot():
    if request.method == 'POST':
        stk_symbol = request.form["stk_symbol"]
        years_back = request.form["years_back"]
        try:
            dfResult = stkF.getStock(stk_symbol, years_back)
            htmlGraph = stkF.graphByYears(dfResult, stk_symbol)
            return render_template("graph.html", htmlGraph=htmlGraph)
        except Exception as e:
            error = str(e)
            message = "PLEASE INSERT A VALID STOCK SYMBOL."
            htmlGraph = message
            return render_template("index.html", error=message)
        # return render_template("graph.html", htmlGraph=htmlGraph)

if __name__ == '__main__':
    app.debug = True
    app.run()