from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    Response
) 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import re
import csv
import json

app = Flask(__name__)

app.secret_key = "uas_algoritma_pemrograman"

EMAIL_ADMIN = "admin@gmail.com"
PASSWORD_ADMIN = "admin123"


class Orang:

    def __init__(self, nama):
        self.__nama = nama

    @property
    def nama(self):
        return self.__nama

    def info(self):
        return "Ini Orang"


class Mahasiswa(Orang):

    def __init__(self, nim, nama, jurusan, ipk):

        super().__init__(nama)

        self.__nim = nim
        self.__jurusan = jurusan
        self.__ipk = ipk

    @property
    def nim(self):
        return self.__nim


    @property
    def jurusan(self):
        return self.__jurusan

    @property
    def ipk(self):
        return self.__ipk

    def info(self):
        return f"{self.nama} adalah mahasiswa"

    def to_list(self):
        return [
            str(self.nim),
            str(self.nama),
            str(self.jurusan),
            str(self.ipk)
        ]


def simpan_mahasiswa(mahasiswa):

    with open("mahasiswa.txt", "a") as file:
        file.write(
            f"{mahasiswa.nim},{mahasiswa.nama},{mahasiswa.jurusan},{mahasiswa.ipk}\n"
        )


def baca_mahasiswa():

    data = []

    if not os.path.exists("mahasiswa.txt"):
        return data

    with open("mahasiswa.txt", "r") as file:

        for baris in file:
            baris = baris.strip()

            if baris:
                nim, nama, jurusan, ipk = baris.split(",")

                mhs = Mahasiswa(nim, nama, jurusan, ipk)
                data.append(mhs)

    return data


# Linear Search
# Time Complexity: O(n)
def linear_search(data, keyword):

    hasil = []
    keyword = keyword.lower()

    for mahasiswa in data:
        if (keyword in mahasiswa.nim.lower() or
            keyword in mahasiswa.nama.lower() or
            keyword in mahasiswa.jurusan.lower()):
            hasil.append(mahasiswa)

    return hasil


def binary_search_nim(data, target):

    data.sort(key=lambda x: x.nim)

    kiri = 0
    kanan = len(data) - 1

    while kiri <= kanan:

        tengah = (kiri + kanan) // 2

        if data[tengah].nim == target:
            return [data[tengah]]

        elif data[tengah].nim < target:
            kiri = tengah + 1

        else:
            kanan = tengah - 1

    return []



def sequential_search(data, keyword):

    hasil = []

    i = 0

    while i < len(data):

        if (keyword.lower() in data[i].nim.lower() or
            keyword.lower() in data[i].nama.lower()):
            hasil.append(data[i])

        i += 1

    return hasil



    
    
@app.route('/sequential_search')
def sequential_search_route():

    if "user" not in session:
        return redirect('/')

    keyword = request.args.get('keyword', '').strip()

    if not keyword:
        flash("Keyword tidak boleh kosong!", "sequential")
        return redirect('/cari')

    data = baca_mahasiswa()
    hasil = sequential_search(data, keyword)

    if hasil:
        flash(f"Sequential Search berhasil! Ditemukan {len(hasil)} data.", "sequential")
    else:
        flash("Data tidak ditemukan.", "sequential")

    return render_template(
        'cari.html',
        hasil=hasil,
        title='Hasil Sequential Search'
    )


@app.route('/cek_polymorphism')
def cek_polymorphism():

    orang = Orang("Budi")
    mahasiswa = Mahasiswa("123", "Andi", "Informatika", 3.9)

    return f"""
    {orang.info()} <br>
    {mahasiswa.info()}
    """


@app.route('/')
def login():

    if "user" in session:
        return redirect('/dashboard')

    return render_template('login.html')


@app.route('/proses_login', methods=['POST'])
def proses_login():

    email = request.form['email']
    password = request.form['password']

    if email == EMAIL_ADMIN and password == PASSWORD_ADMIN:
        session['user'] = email
        return redirect('/dashboard')

    flash("Email atau password salah!")
    return redirect('/')


@app.route('/dashboard')
def dashboard():

    if "user" not in session:
        return redirect('/')

    data = baca_mahasiswa()
    total = len(data)

    ipk_list = [float(m.ipk) for m in data] if data else []

    ipk_tertinggi = max(ipk_list) if ipk_list else 0
    rata_rata = round(
    sum(ipk_list) / len(ipk_list),
    2
    ) if ipk_list else 0
    
    # Total jurusan unik
    total_jurusan = len(set(m.jurusan for m in data))

    # Mahasiswa IPK > 3.5
    ipk_tinggi = len([m for m in data if float(m.ipk) > 3.5])

    # Mahasiswa IPK < 2.5
    ipk_rendah = len([m for m in data if float(m.ipk) < 2.5])

    return render_template(
        'dashboard.html',
        email=session['user'],
        data=data,
        total=total,
        ipk_max=ipk_tertinggi,
        ipk_avg=rata_rata,
        total_jurusan=total_jurusan,
        ipk_tinggi=ipk_tinggi,
        ipk_rendah=ipk_rendah
    )
    
@app.route('/tambah')
def halaman_tambah():

    if "user" not in session:
        return redirect('/')

    return render_template('tambah.html')
    

@app.route('/cari')
def halaman_cari():

    if "user" not in session:
        return redirect('/')

    return render_template(
        'cari.html',
        hasil=None,
        title='Belum Ada Pencarian'
    )


@app.route('/sorting')
def sorting_page():
    if "user" not in session:
        return redirect('/')

    data = baca_mahasiswa()

    return render_template(
        'sorting.html',
        before_data=data
    )
    
@app.route('/data_mahasiswa')
def data_mahasiswa():
    if "user" not in session:
        return redirect('/')

    data = baca_mahasiswa()
    return render_template('data_mahasiswa.html', data=data)
    
    
@app.route('/linear_search')
def linear_search_route():

    if "user" not in session:
        return redirect('/')

    keyword = request.args.get('keyword', '').strip()

    if not keyword:
        flash("Keyword tidak boleh kosong!", "linear")
        return redirect('/cari')

    data = baca_mahasiswa()
    hasil = linear_search(data, keyword)

    if hasil:
        flash(f"Linear Search berhasil! Ditemukan {len(hasil)} data.", "linear")
    else:
        flash("Data tidak ditemukan.", "linear")

    return render_template(
        'cari.html',
        hasil=hasil,
        title='Hasil Linear Search'
    )
    
    
@app.route('/binary_search')
def binary_search_route():

    if "user" not in session:
        return redirect('/')

    keyword = request.args.get('keyword', '').strip()

    if not keyword:
        flash("Keyword tidak boleh kosong!", "binary")
        return redirect('/cari')

    data = baca_mahasiswa()
    hasil = binary_search_nim(data, keyword)

    if hasil:
        flash(f"Binary Search berhasil! Ditemukan {len(hasil)} data.", "binary")
    else:
        flash("Data tidak ditemukan.", "binary")

    return render_template(
        'cari.html',
        hasil=hasil,
        title='Hasil Binary Search'
    )
    
    
@app.route('/sort_ipk')
def sort_ipk():

    if "user" not in session:
        return redirect('/')

    before_data = baca_mahasiswa()
    data = baca_mahasiswa()
    
    if not data:
        flash("Belum ada data untuk di-sort.")
        return redirect('/sorting')

    n = len(data)

    for i in range(n):
        for j in range(0, n - i - 1):
            if float(data[j].ipk) < float(data[j + 1].ipk):
                data[j], data[j + 1] = data[j + 1], data[j]

    return render_template(
        'sorting.html',
        before_data=before_data,
        after_data=data,
        title='Hasil Bubble Sort'
    )


@app.route('/insertion_sort')
def insertion_sort():

    if "user" not in session:
        return redirect('/')

    before_data = baca_mahasiswa()
    data = baca_mahasiswa()
    
    if not data:
        flash("Belum ada data untuk di-sort.")
        return redirect('/sorting')

    for i in range(1, len(data)):

        key = data[i]
        j = i - 1

        while j >= 0 and float(data[j].ipk) < float(key.ipk):
            data[j + 1] = data[j]
            j -= 1

        data[j + 1] = key

    return render_template(
        'sorting.html',
        before_data=before_data,
        after_data=data,
        title='Hasil Insertion Sort'
    )


@app.route('/selection_sort')
def selection_sort():

    if "user" not in session:
        return redirect('/')

    before_data = baca_mahasiswa()
    data = baca_mahasiswa()

    if not data:
        flash("Belum ada data untuk di-sort.")
        return redirect('/sorting')

    n = len(data)

    for i in range(n):
        max_idx = i

        for j in range(i + 1, n):
            if float(data[j].ipk) > float(data[max_idx].ipk):
                max_idx = j

        data[i], data[max_idx] = data[max_idx], data[i]

    flash("Selection Sort berhasil!")

    return render_template(
        'sorting.html',
        before_data=before_data,
        after_data=data,
        title='Hasil Selection Sort'
    )


@app.route('/tambah_mahasiswa', methods=['POST'])
def tambah_mahasiswa():
    
    if "user" not in session:
        return redirect('/')

    nim = request.form['nim']
    nama = request.form['nama']
    jurusan = request.form['jurusan']
    ipk = request.form['ipk']
    
    data = baca_mahasiswa()
    
    if not re.match("^[0-9]+$", nim):
        flash("NIM harus angka!")
        return redirect('/tambah')

    if not re.match("^[a-zA-Z ]+$", nama):
        flash("Nama hanya boleh huruf!")
        return redirect('/data_mahasiswa')

    if not nim or not nama or not jurusan or not ipk:
        flash("Semua field wajib diisi!")
        return redirect('/data_mahasiswa')

    try:
        ipk = float(ipk)
    except:
        flash("IPK harus berupa angka!")
        return redirect('/data_mahasiswa')

    if ipk < 0 or ipk > 4:
        flash("IPK harus antara 0 - 4!")
        return redirect('/data_mahasiswa')


    for m in data:
        if m.nim == nim:
            flash("NIM sudah terdaftar!")
            return redirect('/tambah')
        
    mhs = Mahasiswa(nim, nama, jurusan, ipk)
    simpan_mahasiswa(mhs)
    

    flash("Data mahasiswa berhasil ditambahkan!")
    return redirect('/tambah')

    
@app.route('/hapus_mahasiswa/<nim>')
def hapus_mahasiswa(nim):

    if "user" not in session:
        return redirect('/')

    data = baca_mahasiswa()
    data_baru = []

    for m in data:
        if m.nim != nim:
            data_baru.append(m)

    with open("mahasiswa.txt", "w") as file:
        for m in data_baru:
            file.write(",".join(m.to_list()) + "\n")
            
    flash("Data berhasil dihapus!")
    return redirect('/data_mahasiswa')


@app.route('/edit_mahasiswa/<nim>')
def edit_mahasiswa(nim):

    if "user" not in session:
        return redirect('/')

    data = baca_mahasiswa()

    for m in data:
        if m.nim == nim:
            return render_template("edit.html", m=m)

    return redirect('/data_mahasiswa')


@app.route('/update_mahasiswa', methods=['POST'])
def update_mahasiswa():

    if "user" not in session:
        return redirect('/')

    nim_lama = request.form['nim_lama']
    nim = request.form['nim'].strip()
    nama = request.form['nama'].strip()
    jurusan = request.form['jurusan'].strip()
    ipk = request.form['ipk'].strip()

    data = baca_mahasiswa()

    # Validasi kosong
    if not nim or not nama or not jurusan or not ipk:
        flash("Semua field wajib diisi!")
        return redirect(f'/edit_mahasiswa/{nim_lama}')

    # Validasi NIM
    if not re.match("^[0-9]+$", nim):
        flash("NIM harus berupa angka!")
        return redirect(f'/edit_mahasiswa/{nim_lama}')

    # Validasi Nama
    if not re.match("^[a-zA-Z ]+$", nama):
        flash("Nama hanya boleh huruf dan spasi!")
        return redirect(f'/edit_mahasiswa/{nim_lama}')

    # Validasi duplicate NIM
    for m in data:
        if m.nim == nim and m.nim != nim_lama:
            flash("NIM sudah terdaftar!")
            return redirect(f'/edit_mahasiswa/{nim_lama}')

    # Validasi IPK
    try:
        ipk = float(ipk)
    except ValueError:
        flash("IPK harus berupa angka!")
        return redirect(f'/edit_mahasiswa/{nim_lama}')

    if ipk < 0 or ipk > 4:
        flash("IPK harus antara 0 - 4!")
        return redirect(f'/edit_mahasiswa/{nim_lama}')

    data_baru = []

    for m in data:
        if m.nim == nim_lama:
            data_baru.append(Mahasiswa(nim, nama, jurusan, ipk))
        else:
            data_baru.append(m)

    with open("mahasiswa.txt", "w") as file:
        for m in data_baru:
            file.write(f"{m.nim},{m.nama},{m.jurusan},{m.ipk}\n")

    flash("Data berhasil diupdate!")
    return redirect('/data_mahasiswa')


@app.route('/export_pdf')
def export_pdf():

    if "user" not in session:
        return redirect('/')

    data = baca_mahasiswa()

    from io import BytesIO
    buffer = BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, y, "Laporan Data Mahasiswa")

    y -= 40
    p.setFont("Helvetica", 12)

    for m in data:
        line = f"NIM: {m.nim} | Nama: {m.nama} | Jurusan: {m.jurusan} | IPK: {m.ipk}"
        p.drawString(50, y, line)
        y -= 20

        if y < 50:
            p.showPage()
            y = height - 50

    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    return Response(
        pdf,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': 'attachment; filename=data_mahasiswa.pdf'
        }
    )


@app.route('/export_json')
def export_json():

    if "user" not in session:
        return redirect('/')

    data = baca_mahasiswa()

    json_data = []

    for m in data:
        json_data.append({
            "nim": m.nim,
            "nama": m.nama,
            "jurusan": m.jurusan,
            "ipk": m.ipk
        })

    return Response(
        json.dumps(json_data, indent=4),
        mimetype="application/json",
        headers={
            "Content-Disposition": "attachment; filename=data_mahasiswa.json"
        }
    )


@app.route('/export_csv')
def export_csv():

    if "user" not in session:
        return redirect('/')

    data = baca_mahasiswa()

    csv_data = "NIM,Nama,Jurusan,IPK\n"

    for m in data:
        csv_data += f"{m.nim},{m.nama},{m.jurusan},{m.ipk}\n"

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=data_mahasiswa.csv"
        }
    )


@app.route('/logout')
def logout():
    session.clear()
    
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
