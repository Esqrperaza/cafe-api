from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random
import os


app = Flask(__name__)


# Create database
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe Database Table Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=["GET"])
def get_random_cafe():
    if request.method == "GET":
        result = db.session.execute(db.select(Cafe))
        all_cafes = result.scalars().all()
        random_cafe = random.choice(all_cafes)
        return jsonify(cafe=random_cafe.to_dict())


# Read All Records
@app.route("/all", methods=["GET"])
def get_all_cafes():
    if request.method == "GET":
        result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
        all_cafes = result.scalars().all()
        return jsonify(cafe=[cafe.to_dict() for cafe in all_cafes])


# Search for Cafe using location
@app.route("/search", methods=["GET"])
def search_cafes():
    if request.method == "GET":
        loc = request.args.get('loc')
        result = db.session.execute(db.select(Cafe).where(Cafe.location.in_([loc])))
        all_results = result.scalars().all()
        if not all_results:
            return jsonify("error: Not found")
        else:
            return jsonify(cafe=[cafe.to_dict() for cafe in all_results])


# Create New Cafe Data
@app.route("/add", methods=["POST"])
def add_new_cafe():
    if request.method == "POST":
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        db.session.close()
        return jsonify(response={"success": "New cafe added"})


# Update Cafe Data
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_cafe(cafe_id):
    if request.method == "PATCH":
        new_price = request.args.get('new_price')
        cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        if cafe:
            cafe.coffee_price = new_price
            db.session.commit()
            return jsonify(response={"success": f"Successfully updated price for {cafe.name}"})
        else:
            return jsonify(error={"Coffee shop not found in database."})


# Delete Cafe Data with valid token
@app.route("/report-close/<int:cafe_id>", methods=["DELETE"])
def delete(cafe_id):
    cafe = db.session.execute(
        db.select(Cafe).where(Cafe.id == cafe_id)
    ).scalars().one_or_none()

    api_key = request.args.get("api_key")
    if api_key != os.environ.get("API_KEY"):
        return jsonify(error={"Forbidden": "Sorry, ensure API key is valid"}), 403
    if cafe is None:
        return jsonify(error={"message": f"CAFE NOT FOUND"}), 404
    try:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response={"SUCCESS": f"Cafe {cafe_id} has been deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error={"message": "Could not remove entry"}), 500


if __name__ == '__main__':
    app.run(debug=True)
