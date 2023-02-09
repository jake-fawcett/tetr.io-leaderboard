from flask import Flask, redirect, render_template, request, url_for
from helpers.utils import calc_mmr, get_leaderboard_data

app = Flask(__name__)


@app.route("/")
def index():
    print("Index page request recieved")
    return render_template("index.html")


@app.route("/leaderboard")
def leaderboard():
    get_leaderboard_data()
    print("Leaderboard page request recieved")
    return render_template("leaderboards.html", tables=[get_leaderboard_data()])


@app.route("/submit", methods=["GET", "POST"])
def submitPlayers():
    print("Submit page request recieved")
    if request.method == "POST":
        try:
            num_players = int(next(request.form.items())[1])
            return redirect(url_for("submitResults", num_players=num_players))
        except Exception as e:
            print(e)
            return render_template("submit.html", buttonStatus="Unsuccessful - please enter a valid input.")
    return render_template("submit.html", buttonStatus="")


@app.route("/submit-results", methods=["GET", "POST"])
def submitResults():
    print("Submit Results page request recieved")
    num_players = int(request.args.get("num_players", None))
    if request.method == "POST":
        usernames = list(request.form.values())
        if "" in usernames:
            return render_template("submit-results.html", num_players=num_players, buttonStatus="Unsuccessful - please enter a valid input.")
        result_string = "New MMRs \n" + "\n".join([user["User"] + ": " + user["MMR"] + "," for user in calc_mmr(usernames)])
        return render_template("submit-results.html", num_players=num_players, buttonStatus=result_string)
    return render_template("submit-results.html", num_players=num_players, buttonStatus="")


if __name__ == "__main__":
    app.run()
