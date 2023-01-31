from flask import Flask, render_template, request
from helpers.utils import get_leaderboard_data
app = Flask(__name__)


@app.route("/")
def tabletennis():
    print('Index page request recieved')
    return render_template('index.html')


@app.route("/leaderboard")
def leaderboard():
    get_leaderboard_data()
    print('Leaderboard page request recieved')
    return render_template('leaderboards.html', tables=[get_leaderboard_data()])


@app.route("/submit", methods=["GET", "POST"])
def submit():
    print('Submit page request recieved')
    if request.method == "POST":
        form_items = request.form.items()
        winner_name = next(form_items)[1]
        loser_name = next(form_items)[1]
        score = next(form_items)[1]
        return render_template('submit.html', buttonStatus=f"Success - {winner_name} {score} {loser_name}", error="")
    return render_template('submit.html', buttonStatus="", error="")


if __name__ == '__main__':
    app.run()
