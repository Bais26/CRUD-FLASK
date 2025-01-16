from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.secret_key = "secretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model Database
class Buah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)

# Route Home
@app.route('/')
def index():
    buah_list = Buah.query.all()
    return render_template('index.html', buah_list=buah_list)

# Route Tambah Buah
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        jumlah = request.form['jumlah']
        buah = Buah(nama=nama, harga=harga, jumlah=jumlah)
        db.session.add(buah)
        db.session.commit()
        flash("Data berhasil ditambahkan!")
        return redirect(url_for('index'))

# Route Edit Buah
@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    buah = Buah.query.get(id)
    if request.method == 'POST':
        buah.nama = request.form['nama']
        buah.harga = request.form['harga']
        buah.jumlah = request.form['jumlah']
        db.session.commit()
        flash("Data berhasil diperbarui!")
        return redirect(url_for('index'))
    return render_template('edit.html', buah=buah)

# Route Hapus Buah
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    buah = Buah.query.get(id)
    db.session.delete(buah)
    db.session.commit()
    flash("Data berhasil dihapus!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
