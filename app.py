from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

car1 = {
    "id": "1",
    "number": "123-456",
    "problems": [],
    "img": "https://platform.cstatic-images.com/in/v2/stock_photos/90884105-7fd5-4da9-8479-27e482a4e479/2b678835-3279-4de7-8047-36484d4e2900.png",
    "description": "Ford Mustang 2022",
}
car2 = {
    "id": "2",
    "number": "456-789",
    "problems": [],
    "img": "https://www.cars.com/i/large/in/v2/stock_photos/1fce77f4-454e-4338-b0ed-4b7c961910b2/c9dc2064-dd42-45ec-b973-c0a27688ed16.png",
    "description": "Toyota Corolla 2002",
}
cars = [car1, car2]


@app.route("/")
def cars_list():
    return render_template("car_list.html", car_list=cars)

    # final_str = ""
    # for car in cars:
    #     final_str += f"<p>{car['number']}</p>"

    # return final_str


@app.route("/single_car/<id>")
def single_car(id):
    for car in cars:
        if car["id"] == id:
            return render_template("single_car.html", car=car)


@app.route("/add_car", methods=["POST", "GET"])
def add_car():
    if request.method == "POST":
        cars.append(
            {
                "id": str(int(cars[-1]["id"]) + 1),
                "number": request.form["car_number"],
                "problems": [],
                "img": request.form["image_url"],
                "description": request.form["description"],
            }
        )
        return redirect("/")
    return render_template("add_car.html")


@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True, port=9000)
