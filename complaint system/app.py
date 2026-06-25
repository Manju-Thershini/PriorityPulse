from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ---------------- #
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            complaint TEXT,
            priority TEXT,
            status TEXT
        )
    ''')
    conn.close()

# ---------------- PRIORITY LOGIC ---------------- #
def get_priority(text):
    text = text.lower()

    if "urgent" in text or "immediately" in text or "asap" in text:
        return "High"
    elif "soon" in text or "delay" in text:
        return "Medium"
    else:
        return "Low"

# ---------------- USER PAGE ---------------- #
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        complaint = request.form["complaint"]

        priority = get_priority(complaint)

        conn = sqlite3.connect('database.db')
        conn.execute(
            "INSERT INTO complaints (name, complaint, priority, status) VALUES (?, ?, ?, ?)",
            (name, complaint, priority, "Pending")
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("index.html")

# ---------------- ADMIN PAGE ---------------- #
@app.route("/admin")
def admin():
    conn = sqlite3.connect('database.db')
    data = conn.execute("SELECT * FROM complaints").fetchall()
    conn.close()

    return render_template("admin.html", data=data)

# ---------------- UPDATE STATUS ---------------- #
@app.route("/resolve/<int:id>")
def resolve(id):
    conn = sqlite3.connect('database.db')
    conn.execute("UPDATE complaints SET status='Resolved' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin")

# ---------------- DELETE ---------------- #
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect('database.db')
    conn.execute("DELETE FROM complaints WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin")

# ---------------- RUN ---------------- #
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
