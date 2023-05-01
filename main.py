from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    open = StringField("Opening Time e.g. 8AM", validators=[DataRequired()])
    close = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating", choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi_rating = SelectField("Wifi Strength Rating", choices=["✘", "📶", "📶📶", "📶📶📶", "📶📶📶📶", "📶📶📶📶📶"], validators=[DataRequired()])
    power_rating = SelectField("Power Socket Availability", choices=["✘", "⚡", "⚡⚡", "⚡⚡⚡", "⚡⚡⚡⚡", "⚡⚡⚡⚡⚡"], validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    cafe = CafeForm()
    if cafe.validate_on_submit():
        with open("Day 62 Coffe Project/Coffee/cafe-data.csv", mode="a", encoding='utf-8') as csv_file:
            csv_file.write(f"\n{cafe.cafe.data},"
                           f"{cafe.location.data},"
                           f"{cafe.open.data},"
                           f"{cafe.close.data},"
                           f"{cafe.coffee_rating.data},"
                           f"{cafe.wifi_rating.data},"
                           f"{cafe.power_rating.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=cafe)

@app.route('/delete', methods=["GET", "POST"])
def delete_cafe():
    cafe_name = request.form["cafe_name"]
    with open('Day 62 Coffe Project/Coffee/cafe-data.csv', 'r', newline='', encoding='utf-8') as csv_file:
        csv_data = list(csv.reader(csv_file))
    with open('Day 62 Coffe Project/Coffee/cafe-data.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for row in csv_data:
            if row[0] != cafe_name:
                writer.writerow(row)
    return redirect(url_for('cafes'))

@app.route('/cafes')
def cafes():
    with open('Day 62 Coffe Project/Coffee/cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)

if __name__ == '__main__':
    app.run(debug=True)
