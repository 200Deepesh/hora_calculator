from flask import Flask, request
from hora_calculator import genrateHoraChart

app = Flask(__name__)

def main():
    print("Hello World!")


@app.route("/", methods=["POST", "GET"])
def root():
    if request.method=="GET":
        return "<p>Hello, World!</p>"

    else:
        date = request.form["date"]
        location = request.form["location"]
        if not(date and location) :
            app.logger.error({"status": 400, "error": "invalid user input", "dateInput": date, "locationInput": location})
            return {"message": "date and location both are required"}, 400
        res = genrateHoraChart(date, location)
        if res["error"]:
            app.logger.error({"status": 400, "error": res["error"], "dateInput": date, "locationInput": location})
            return {"message":"Server Error."}, 500
        
        return {"response": res }
    
if __name__ == "__main__":
    main()