from flask import Flask, render_template
from flask import Flask, request, jsonify
from flask import redirect, url_for
import stepper
import threading


app = Flask(__name__)

running = False

def manual_loop(axis, speed):
    global running
    while running:
        stepper.get_position(axis, speed)
        time.sleep(0.001)


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/manual', methods=['POST'])
def manual():
    global running

    manual_axis = request.form.get("manual_axis")
    manual_speed = request.form.get("manual_speed")

    running = True
    Thread(target=manual_loop, args=(manual_axis, manual_speed), daemon=True).start()

    return redirect(url_for("home"))


@app.route('/manual/stop', methods=['POST'])
def manual_stop():
    global running
    running = False
    return "Stopped"


if __name__ == "__main__":
    app.run(debug=True)
