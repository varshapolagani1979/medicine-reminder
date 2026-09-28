from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "medicine.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dosage TEXT NOT NULL,
            time TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            instructions TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db_connection()

    medicines = conn.execute(
        "SELECT * FROM medicines ORDER BY time"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        medicines=medicines
    )


@app.route("/add", methods=["GET", "POST"])
def add_medicine():

    if request.method == "POST":

        name = request.form["name"]
        dosage = request.form["dosage"]
        time = request.form["time"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        instructions = request.form["instructions"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO medicines
            (name, dosage, time, start_date, end_date, instructions)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            dosage,
            time,
            start_date,
            end_date,
            instructions
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add_medicine.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_medicine(id):

    conn = get_db_connection()

    medicine = conn.execute(
        "SELECT * FROM medicines WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        name = request.form["name"]
        dosage = request.form["dosage"]
        time = request.form["time"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        instructions = request.form["instructions"]

        conn.execute("""
            UPDATE medicines
            SET name = ?,
                dosage = ?,
                time = ?,
                start_date = ?,
                end_date = ?,
                instructions = ?
            WHERE id = ?
        """, (
            name,
            dosage,
            time,
            start_date,
            end_date,
            instructions,
            id
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    conn.close()

    return render_template(
        "edit_medicine.html",
        medicine=medicine
    )


@app.route("/delete/<int:id>")
def delete_medicine(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM medicines WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    create_database()
    app.run(host="0.0.0.0", port=5000)