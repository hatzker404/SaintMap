
from global_import import *


def init_db():
    db_session.global_init("static/db/saintmap.db")


def add_new_place_to_db(region, category, name, address, photo, description, coordinates):
    db_sess = db_session.create_session()
    place = PLACE()

    place.region = region
    place.category = category
    place.name = name
    place.address = address
    place.photo = photo
    place.description = description
    place.coordinates = coordinates

    db_sess.add(place)
    db_sess.commit()


def get_places(i=0, region="", category="", name=""):
    db_sess = db_session.create_session()
    if i:
        places = db_sess.query(PLACE).filter(PLACE.id == i)
    elif name:
        places = db_sess.query(PLACE).filter(PLACE.name == name)
    elif region and category:
        places = db_sess.query(PLACE).filter(PLACE.region == region, PLACE.category == category)
    elif region:
        places = db_sess.query(PLACE).filter(PLACE.region == region)
    elif category:
        places = db_sess.query(PLACE).filter(PLACE.category == category)
    else:
        places = db_sess.query(PLACE).all()
    places = [
        [place.id, place.region, place.category, place.name,
            place.address, place.photo, place.description, place.coordinates]
        for place in places
    ]
    return places


def delete_place_from_db(place_name):
    db_sess = db_session.create_session()
    places = db_sess.query(PLACE).all()
    for place in places:
        if place.name == place_name:
            db_sess.delete(place)
            db_sess.commit()
            return


def add_new_user_to_db(name, email, password):
    db_sess = db_session.create_session()
    user = USER()

    user.name = name
    user.email = email
    user.password = password
    user.fav_places_id = ""

    db_sess.add(user)
    db_sess.commit()


def get_all_users():
    db_sess = db_session.create_session()
    users = db_sess.query(USER).all()
    return [[user.name, user.email, user.password, user.fav_places_id] for user in users]


def get_user_info(name):
    db_sess = db_session.create_session()
    users = db_sess.query(USER).all()
    for user in users:
        if user.name == name:
            return user.name, user.email, user.password, user.fav_places_id


def get_user_favorite_places(name):
    return [get_places(i=int(x))[0] for x in get_user_info(name)[3].split()]


def update_user_fav_places_id(name, new_id, delete_all=False):
    db_sess = db_session.create_session()
    users = db_sess.query(USER).all()
    if delete_all:
        for user in users:
            if user.name == name:
                user.fav_places_id = ""
                db_sess.commit()
    else:
        for user in users:
            if user.name == name:
                old_id = user.fav_places_id
                a = old_id.split()
                if new_id not in a:
                    user.fav_places_id = old_id + " " + new_id
                db_sess.commit()


def check_valid_signup(name, email, psw):
    users = get_all_users()

    users_name = [i[0] for i in users]
    users_email = [i[1] for i in users]

    if name in users_name:
        return "1001"
    if name == "":
        return "1011"
    if email in users_email:
        return "1002"
    if email == "":
        return "1012"
    if len(psw) < 8 or psw == "":
        return "1003"

    add_new_user_to_db(name, email, psw)
    return "1000"


def check_valid_signin(usname, uspsw):
    name, email, password, fav_places_id = get_user_info(usname)

    if password == uspsw:
        session["isLogged"] = True
        session["username"] = request.form['username']

        return redirect(url_for('index'))
    return render_template("signin.html", error=True, image=get_image())


def get_facts():
    return open("static/facts.txt", encoding='utf-8').readlines()[randint(0, 3)].rstrip("\n")


def get_image():
    name = open("static/images.txt", encoding='utf-8').readlines()[randint(0, 3)].rstrip("\n")
    return url_for('static', filename=f'img/{name}')


def get_weather():
    city_id = 498817
    appid = "50df2261e36a71d62ce37b1fb58d1722"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        return [
            round(data['main']['temp']),
            data['weather'][0]['description'],
            data['wind']['speed'],
            data['main']['humidity']
        ]
    except Exception as e:
        return []


def check_code():
    code = check_valid_signup(request.form['username'], request.form['useremail'], request.form['userpsw'])
    if code == "1000":
        return render_template("success_signup.html")
    if code == "1001":
        return render_template("signup.html", error="1001", image=get_image())
    if code == "1011":
        return render_template("signup.html", error="1011", image=get_image())
    if code == "1002":
        return render_template("signup.html", error="1002", image=get_image())
    if code == "1012":
        return render_template("signup.html", error="1012", image=get_image())
    return render_template("signup.html", error="1003", image=get_image())


def init_map():
    saintmap = folium.Map(
        location=[59.9386, 30.3141]
    )
    if session.get("fav_places"):
        places = get_user_favorite_places(session.get("username"))
        session["fav_places"] = False
    else:
        places = get_places(name=session.get("place_name"), region=session.get("region"), category=session.get("category"))
    for place in places:
        image = '/img/places/' + place[4].split("/")[-1]
        image = url_for('static', filename=image)
        coordes = list(map(float, place[7].split(", ")))
        folium.Marker(
            location=[coordes[0], coordes[1]],
            popup=f"""
                    <div class="card-content" style="
                    z-index: 999;
                    box-sizing: border-box;
                    margin: -30px;
                    padding: 20px;
                    background-color: black;
                    border: 2px solid white;
                    border-radius: 20px;
                    color: white;
                    ">
                        <div class="place-container" style="font-size: 20px;">
                            <h1 style="text-align: center; text-shadow: #FC0 1px 0 10px;">{place[3]}</h1>
                            <div class="place-img-container" style="background-image: url({image});
                            background-attachment: fixed;
                            background-size: 100%;
                            background-repeat: no-repeat;
                            width: 400px; height: 300px;">
                            </div>
                            <p style="text-shadow: #FC0 1px 0 10px; text-transform: uppercase;">Адрес:</p>
                            <p>{place[1]} район, {place[5]} </p>
                            <p style="text-shadow: #FC0 1px 0 10px; text-transform: uppercase;">Описание:</p>
                            <p>{place[6]}</p>
                        </div>
                    </div>
                    """,
            tooltip=place[3]
        ).add_to(saintmap)

    saintmap.get_root().width = "100%"
    saintmap.get_root().height = "100%"
    iframe = saintmap._repr_html_()
    return iframe



