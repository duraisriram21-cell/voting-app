from flask import Flask, request, jsonify

app = Flask(__name__)

# in-memory dictionary to keep votes
votes = {"cats": 0, "dogs": 0}

@app.get("/")
def home():
    # just return the current counts as JSON
    return jsonify(votes)

@app.post("/vote")
def vote():
    # read the choice from request (default to cats)
    choice = request.form.get("choice", "cats")
    if choice not in ("cats", "dogs"):
        choice = "cats"
    # increment the chosen counter
    votes[choice] += 1
    # return updated counts
    return jsonify(votes)

if __name__ == "__main__":
    # run app on port 8080
    app.run(host="0.0.0.0", port=8080)
