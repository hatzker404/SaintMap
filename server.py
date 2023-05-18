from func import *


app = Flask(__name__)
app.secret_key = "admin_see"

app.permanent_session_lifetime = datetime.timedelta(days=1)


@app.route('/')
@app.route('/index')
@app.route('/welcome')
def index():
    if 'isLogged' not in session:
        session["isLogged"] = False
    if 'username' not in session:
        session["username"] = ""
    if 'fav_places' not in session:
        session["fav_places"] = False
    if 'place_name' not in session:
        session["place_name"] = ""
    if 'region' not in session:
        session["region"] = ""
    if 'category' not in session:
        session["category"] = ""

    weather = get_weather()
    if weather:
        if weather[0] >= 16:
            rec = "Прекрасное время для прогулки!"
        elif 16 > weather[0] >= 5:
            rec = "Оденьтесь теплее и вперед покорять Петербург!"
        elif 5 > weather[0] >= -10:
            rec = "Немного прохладно, но разве погода может испортить прогулку!"
        else:
            rec = " Ну и дубак..."
    else:
        rec = ""
    return render_template(
        "index.html", fact=get_facts(), username=session.get("username"), image=get_image(), weather=weather, rec=rec
    )


@app.route('/about')
def about():
    return render_template("about.html", username=session.get("username"), image=get_image())


@app.route('/user')
def user():
    if session["isLogged"]:
        name, email, password, fav_places_id = get_user_info(session.get("username"))
        user_fav_places = [get_places(i=int(x)) for x in fav_places_id.split()]
        for i in range(len(user_fav_places)):
            user_fav_places[i][0][4] = url_for(
                'static', filename='img/places/' + user_fav_places[i][0][4].split("/")[-1]
            )
        if session.get("username") == "admin":
            return render_template(
                "admin.html", username=session.get("username"), fav_places=user_fav_places, image=get_image()
            )
        else:
            return render_template(
                "user.html", username=session.get("username"), fav_places=user_fav_places, image=get_image()
            )
    else:
        return render_template("signin.html", error=False, image=get_image())


@app.route('/signup')
def signup():
    return render_template("signup.html", error="1000", image=get_image())


@app.route("/map")
def create_map():
    return render_template("map.html", username=session.get("username"), iframe=init_map())


@app.post('/signin')
def signin():
    if request.method == "POST":
        return check_valid_signin(request.form['username'], request.form['userpsw'])


@app.post('/signup_check')
def signup_check():
    if request.method == "POST":
        return check_code()


@app.post('/apply_changes')
def apply_changes():
    if request.method == "POST":
        session["place_name"] = request.form["place_name"]
        session["region"] = request.form["region"]
        session["category"] = request.form["category"]
        return redirect(url_for('create_map'))


@app.post('/logout')
def logout():
    if request.method == "POST":
        session["isLogged"] = False
        session["username"] = ""
        return redirect(url_for('user'))


@app.post('/add_to_fav')
def add_to_fav():
    if request.method == "POST":
        if session.get("isLogged"):
            new_id = request.form["new_id"]
            place = get_places(name=new_id)
            if place:
                new_id = str(place[0][0])
                update_user_fav_places_id(session.get("username"), new_id)
            return redirect(url_for('create_map'))
        return redirect(url_for('user'))


@app.post('/get_user_fav_places')
def get_user_fav_places():
    if request.method == "POST":
        if session. get("isLogged"):
            session["fav_places"] = True
            return redirect(url_for('create_map'))
        return redirect(url_for('user'))


@app.post('/delete_user_fav_places')
def delete_user_fav_places():
    if request.method == "POST":
        update_user_fav_places_id(session.get("username"), "", delete_all=True)
        return redirect(url_for('user'))


@app.post('/add_place_to_db')
def add_place_to_db():
    if request.method == "POST":
        region = request.form["region"]
        category = request.form["category"]
        name = request.form["name"]
        address = request.form["photo"]
        photo = request.form["address"]
        description = request.form["description"]
        coordinates = request.form["coordinates"]
        add_new_place_to_db(region, category, name, address, photo, description, coordinates)

        return redirect(url_for('user'))


@app.post('/delete_place')
def delete_place():
    if request.method == "POST":
        name = request.form["delete_id"]
        delete_place_from_db(name)
        return redirect(url_for('user'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
