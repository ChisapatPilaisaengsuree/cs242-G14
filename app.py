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

#  สลับตรงนี้ตอน backend เสร็จ
USE_API = False
API_URL = "http://localhost:8000"

# ── mock state ─────────────────────────────
_places = [
    {**p, "toilets": [{**t} for t in p["toilets"]]}
    for p in PLACES
]
_last_updated = datetime.now().strftime("%H:%M:%S")

def flat():
    return flat_toilets(_places)

def maps_url(lat, lng):
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}&travelmode=walking"

# ── helper: ดึง data ───────────────────────
def get_places():
    if USE_API:
        return requests.get(f"{API_URL}/places").json()
    return _places

def get_all_toilets():
    if USE_API:
        return requests.get(f"{API_URL}/toilets").json()
    return flat()

# ── Auth ──────────────────────────────────
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

# ── Pages ─────────────────────────────────

@app.route("/home")
@login_required
def home():
    gender_filter = request.args.get("filter", "All")

    places = get_places()

    if not USE_API:
        # filter mock
        filtered = []
        for p in places:
            toilets = [
                t for t in p["toilets"]
                if gender_filter == "All" or t["gender"] == gender_filter
            ]
            if toilets:
                filtered.append({**p, "toilets": toilets})
        places = filtered

    return render_template("home.html",
        user=session["user"],
        places=places,
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
    q = request.args.get("q", "").strip().lower()
    gender = request.args.get("filter", "All")

    data = get_all_toilets()

    if not USE_API:
        results = [
            t for t in data
            if (q == "" or q in t["name"].lower() or q in t["place_name"].lower())
            and (gender == "All" or t["gender"] == gender)
        ]
    else:
        results = data

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
    data = get_all_toilets()

    toilet = next((x for x in data if x["id"] == tid), None)
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

# ── Mock API (ใช้ตอนยังไม่มี backend) ─────────

@app.route("/api/refresh", methods=["POST"])
@login_required
def api_refresh():
    global _last_updated
    if USE_API:
        return jsonify(ok=True)

    for p in _places:
        for t in p["toilets"]:
            t["occupancy"] = max(0, min(100, t["occupancy"] + random.randint(-9, 9)))

    _last_updated = datetime.now().strftime("%H:%M:%S")
    return jsonify(ok=True)

# ── Run ──────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)