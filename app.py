from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
from datetime import datetime
import requests

from data.mock_data import (
    PLACES, USERS, flat_toilets,
    get_status, get_status_label, get_status_color,
    get_gender_icon, get_gender_label, get_gender_color
)

app = Flask(__name__)
app.secret_key = "toiletfinder-secret-2024"

# ใช้ backend จริง
USE_API = True
API_URL = "http://localhost:8000/api"

# ── mock fallback ─────────────────────────
_places = [
    {**p, "toilets": [{**t} for t in p["toilets"]]}
    for p in PLACES
]
_last_updated = datetime.now().strftime("%H:%M:%S")

def flat():
    return flat_toilets(_places)

def maps_url(lat, lng):
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}&travelmode=walking"

# ── FIX สำคัญอยู่ตรงนี้ ─────────────────
def convert_crowd(level):
    return {
        "low": 20,
        "medium": 50,
        "high": 80
    }.get(level, 0)

def map_data(data):
    result = []
    for x in data:
        # รองรับทั้ง crowd_level และ crowd
        crowd = x.get("crowd_level") or x.get("crowd") or "low"

        result.append({
            "id": x["id"],
            "name": f"{x['building']} ชั้น {x['floor']}",
            "place_name": x["building"],
            "gender": x["type"],
            "occupancy": convert_crowd(crowd),
            "lat": x["latitude"],
            "lng": x["longitude"]
        })
    return result

# ── helper ───────────────────────────────
def get_all_toilets():
    if USE_API:
        try:
            res = requests.get(f"{API_URL}/restrooms")
            return map_data(res.json())
        except Exception as e:
            print("API error:", e)
            return []
    return flat()

def get_toilet(tid):
    if USE_API:
        try:
            res = requests.get(f"{API_URL}/restrooms/{tid}")
            return map_data([res.json()])[0]
        except Exception as e:
            print("Detail error:", e)
            return None
    data = flat()
    return next((x for x in data if x["id"] == tid), None)

def search_toilets(q):
    if USE_API:
        try:
            res = requests.post(f"{API_URL}/search", json={"keyword": q})
            return map_data(res.json())
        except Exception as e:
            print("Search error:", e)
            return []
    data = flat()
    return [
        t for t in data
        if q.lower() in t["name"].lower() or q.lower() in t["place_name"].lower()
    ]

# ── Auth ─────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        user = next((u for u in USERS if u["email"] == email and u["password"] == password), None)
        if user:
            session["user"] = user
            session["favorites"] = []
            session["ratings"] = {}
            return redirect(url_for("home"))
        else:
            error = "อีเมลหรือรหัสผ่านไม่ถูกต้อง"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

# ── Pages ───────────────────────────────

@app.route("/home")
@login_required
def home():
    gender_filter = request.args.get("filter", "All")

    data = get_all_toilets()

    if gender_filter != "All":
        data = [t for t in data if t["gender"] == gender_filter]

    return render_template("home.html",
        user=session["user"],
        toilets=data,
        gender_filter=gender_filter,
        last_updated=_last_updated,
        maps_url=maps_url,
        get_status_color=get_status_color,
        get_status_label=get_status_label,
        get_gender_icon=get_gender_icon,
        get_gender_label=get_gender_label,
        get_gender_color=get_gender_color,
    )

@app.route("/search")
@login_required
def search():
    q = request.args.get("q", "").strip()
    gender = request.args.get("filter", "All")

    results = search_toilets(q)

    if gender != "All":
        results = [t for t in results if t["gender"] == gender]

    return render_template("search.html",
        user=session["user"],
        results=results,
        q=q,
        gender_filter=gender,
        last_updated=_last_updated,
        get_status_color=get_status_color,
        get_status_label=get_status_label,
        get_gender_icon=get_gender_icon,
        get_gender_label=get_gender_label,
        get_gender_color=get_gender_color,
    )

@app.route("/detail/<int:tid>")
@login_required
def detail(tid):
    toilet = get_toilet(tid)

    if not toilet:
        return redirect(url_for("home"))

    favs = session.get("favorites", [])
    ratings = session.get("ratings", {})

    return render_template("detail.html",
        user=session["user"],
        toilet=toilet,
        is_fav=tid in favs,
        rating=ratings.get(str(tid), 0),
        last_updated=_last_updated,
        mapsurl=maps_url(toilet["lat"], toilet["lng"]),
        get_status_color=get_status_color,
        get_status_label=get_status_label,
        get_gender_icon=get_gender_icon,
        get_gender_label=get_gender_label,
        get_gender_color=get_gender_color,
    )

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html",
        user=session["user"],
        fav_count=len(session.get("favorites", [])),
        ratings=session.get("ratings", {}),
        last_updated=_last_updated,
    )

# ── Run ─────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)