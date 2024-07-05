from flask import Flask, render_template, request, redirect, url_for
from helpers.validation import capitalize_desc
from storage.save_load import save, load
from helpers.variables import problems

PROBLEMS = problems
app = Flask(__name__)


cars = load()


@app.route("/")
def cars_list():
    return render_template("car_list.html", car_list=cars, current_page="home")


@app.route("/single_car/<id>")
def single_car(id):
    for car in cars:
        if car["id"] == id:
            return render_template("single_car.html", car=car)


@app.route("/add_car", methods=["POST", "GET"])
def add_car():
    if request.method == "POST":
        selected_problems = request.form.getlist("problems")
        car_problems = [
            problem for problem in PROBLEMS if problem["name"] in selected_problems
        ]
        cars.append(
            {
                "id": str(int(cars[-1]["id"]) + 1),
                "number": request.form["car_number"],
                "problems": car_problems,
                "img": request.form["image_url"],
                "description": capitalize_desc(request.form["description"]),
                "urgent": bool(request.form["is_urgent"]),
            }
        )
        save(cars)
        return redirect("/")
    return render_template("add_car.html", current_page="add_car", problems=PROBLEMS)


@app.route("/urgents")
def urgents():
    urgent_cars = []
    for car in cars:
        if car["urgent"] == True:
            urgent_cars.append(car)
    return render_template("urgents.html", car_list=urgent_cars, current_page="urgents")


@app.route("/delete_car/<id>")
def delete_car(id):
    for car in cars:
        if car["id"] == id:
            cars.remove(car)
            save(cars)
    return redirect(url_for("cars_list"))


@app.route("/edit_car/<id>", methods=["POST", "GET"])
def edit_car(id):
    for car in cars:
        if car["id"] == id:
            if request.method == "POST":
                selected_problems = request.form.getlist("problems")
                car_problems = [
                    problem
                    for problem in PROBLEMS
                    if problem["name"] in selected_problems
                ]
                index = cars.index(car)
                cars.pop(index)
                cars.insert(
                    index,
                    {
                        "id": id,
                        "number": request.form["car_number"],
                        "problems": car_problems,
                        "img": request.form["image_url"],
                        "description": capitalize_desc(request.form["description"]),
                        "urgent": bool(request.form["is_urgent"]),
                    },
                )
                save(cars)
                return redirect(url_for("cars_list"))
            else:
                return render_template(
                    "edit_car.html",
                    car=car,
                    urgency=car["urgent"],
                    car_problems=car["problems"],
                    problems=PROBLEMS,
                )


if __name__ == "__main__":
    app.run(debug=True, port=9000)
