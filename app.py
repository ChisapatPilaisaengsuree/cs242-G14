from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
from datetime import datetime
from data.mock_data import PLACES, USERS, flat_toilets, get_status, get_status_label, get_status_color, get_gender_icon, get_gender_label, get_gender_color

app = Flask(__name__)
app.secret_key = "toiletfinder-secret-2024"

# ── in-memory state (per-process; resets on restart) ──────────────────────────
_places = [
    {**p, "toilets": [{**t} for t in p["toilets"]]}
    for p in PLACES
]
_last_updated = datetime.now().strftime("%H:%M:%S")

def flat():
    return flat_toilets(_places)

def maps_url(lat, lng):
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}&travelmode=walking"

# ── Auth ────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        user = next((u for u in USERS if u["email"] == email and u["password"] == password), None)
        if user:
            session["user"] = user
            session["favorites"] = []
            session["ratings"]   = {}
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

# ── Pages ────────────────────────────────────────────────────────────────────
@app.route("/home")
@login_required
def home():
    gender_filter = request.args.get("filter", "All")
    places = []
    for p in _places:
        toilets = [t for t in p["toilets"] if gender_filter == "All" or t["gender"] == gender_filter]
        if toilets:
            places.append({**p, "toilets": toilets})
    return render_template("home.html",
        user=session["user"],
        places=places,
        all_count=len(flat()),
        place_count=len(_places),
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
    q      = request.args.get("q", "").strip().lower()
    gender = request.args.get("filter", "All")
    results = [
        t for t in flat()
        if (q == "" or q in t["name"].lower() or q in t["place_name"].lower())
        and (gender == "All" or t["gender"] == gender)
    ]
    return render_template("search.html",
        user=session["user"],
        results=results,
        q=request.args.get("q", ""),
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
    t = next((x for x in flat() if x["id"] == tid), None)
    if not t:
        return redirect(url_for("home"))
    favs    = session.get("favorites", [])
    ratings = session.get("ratings", {})
    is_fav  = tid in favs
    rating  = ratings.get(str(tid), 0)
    return render_template("detail.html",
        user=session["user"],
        t=t,
        is_fav=is_fav,
        rating=rating,
        last_updated=_last_updated,
        maps_url=maps_url(t["lat"], t["lng"]),
        get_status_color=get_status_color,
        get_status_label=get_status_label,
        get_gender_icon=get_gender_icon,
        get_gender_label=get_gender_label,
        get_gender_color=get_gender_color,
    )

@app.route("/profile")
@login_required
def profile():
    favs    = session.get("favorites", [])
    ratings = session.get("ratings", {})
    return render_template("profile.html",
        user=session["user"],
        fav_count=len(favs),
        ratings=ratings,
        last_updated=_last_updated,
    )

@app.route("/admin")
@login_required
def admin():
    if session["user"].get("role") != "admin":
        return redirect(url_for("home"))
    tab     = request.args.get("tab", "status")
    all_t   = flat()
    av  = sum(1 for t in all_t if get_status(t["occupancy"]) == "available")
    bu  = sum(1 for t in all_t if get_status(t["occupancy"]) == "busy")
    cr  = sum(1 for t in all_t if get_status(t["occupancy"]) == "crowded")
    avg = round(sum(t["occupancy"] for t in all_t) / len(all_t)) if all_t else 0
    return render_template("admin.html",
        user=session["user"],
        tab=tab,
        places=_places,
        all_t=all_t,
        av=av, bu=bu, cr=cr, avg=avg,
        last_updated=_last_updated,
        get_status_color=get_status_color,
        get_status_label=get_status_label,
        get_gender_icon=get_gender_icon,
        get_gender_label=get_gender_label,
        get_gender_color=get_gender_color,
        get_status=get_status,
    )

# ── API actions ──────────────────────────────────────────────────────────────
@app.route("/api/refresh", methods=["POST"])
@login_required
def api_refresh():
    global _last_updated
    for p in _places:
        for t in p["toilets"]:
            delta = random.randint(-9, 9)
            t["occupancy"] = max(0, min(100, t["occupancy"] + delta))
    _last_updated = datetime.now().strftime("%H:%M:%S")
    return jsonify(ok=True)

@app.route("/api/favorite/<int:tid>", methods=["POST"])
@login_required
def api_favorite(tid):
    favs = session.get("favorites", [])
    if tid in favs:
        favs.remove(tid)
        added = False
    else:
        favs.append(tid)
        added = True
    session["favorites"] = favs
    return jsonify(ok=True, added=added)

@app.route("/api/rate/<int:tid>", methods=["POST"])
@login_required
def api_rate(tid):
    star    = int(request.json.get("star", 0))
    ratings = session.get("ratings", {})
    ratings[str(tid)] = star
    session["ratings"] = ratings
    return jsonify(ok=True)

@app.route("/api/admin/save_status", methods=["POST"])
@login_required
def api_save_status():
    if session["user"].get("role") != "admin":
        return jsonify(ok=False), 403
    global _last_updated
    data = request.json  # {id: occupancy, ...}
    for p in _places:
        for t in p["toilets"]:
            key = str(t["id"])
            if key in data:
                t["occupancy"] = max(0, min(100, int(data[key])))
    _last_updated = datetime.now().strftime("%H:%M:%S")
    return jsonify(ok=True)

@app.route("/api/admin/add_toilet", methods=["POST"])
@login_required
def api_add_toilet():
    if session["user"].get("role") != "admin":
        return jsonify(ok=False), 403
    d = request.json
    all_ids = [t["id"] for p in _places for t in p["toilets"]]
    new_id  = max(all_ids, default=0) + 1
    new_t   = {
        "id": new_id, "name": d["name"], "floor": d.get("floor", "ชั้น 1"),
        "gender": d["gender"], "distance": int(d.get("distance", 100)),
        "occupancy": 0, "capacity": int(d.get("capacity", 6)),
    }
    for p in _places:
        if p["id"] == d["place_id"]:
            p["toilets"].append(new_t)
            break
    return jsonify(ok=True)

@app.route("/api/admin/delete_toilet/<int:tid>", methods=["POST"])
@login_required
def api_delete_toilet(tid):
    if session["user"].get("role") != "admin":
        return jsonify(ok=False), 403
    for p in _places:
        p["toilets"] = [t for t in p["toilets"] if t["id"] != tid]
    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)