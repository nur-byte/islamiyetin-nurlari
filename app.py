import datetime as dt_module
from datetime import datetime
import requests
from flask import Flask, render_template, request
from hijri_converter import Gregorian

app = Flask(__name__)

# Tarih hesaplama işlemini tek bir yerde toplayan yardımcı fonksiyon
def get_today_dates():
    today_date = dt_module.date.today()
    
    # Miladi -> Hicri Dönüşümü
    hijri_date = Gregorian(today_date.year, today_date.month, today_date.day).to_hijri()
    hijri_str = f"{hijri_date.day} {hijri_date.month_name()} {hijri_date.year}"
    
    # Türkçe Miladi Ay İsimleri
    aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    gregorian_str = f"{today_date.day} {aylar[today_date.month - 1]} {today_date.year}"
    
    return hijri_str, gregorian_str

@app.route('/')
def home():
    hijri_str, gregorian_str = get_today_dates()
    return render_template('index.html', hijri_date=hijri_str, gregorian_date=gregorian_str)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/hadisler')
def hadisler():
    return render_template('hadisler.html')

@app.route('/iletisim')
def iletisim():
    return render_template("iletisim.html")

@app.route('/aciklama')
def aciklama():
    hijri_str, gregorian_str = get_today_dates()
    return render_template('aciklama.html', hijri_date=hijri_str, gregorian_date=gregorian_str)



@app.route('/savas')
def savas():
    return render_template("savas.html")

@app.route('/namazvakitleri')
def namaz_vakitleri():
    sehir = request.args.get('sehir', 'Istanbul')
    tarih_bugun = datetime.now().strftime('%d.%m.%Y')
    
    api_url = f"http://api.aladhan.com/v1/timingsByCity?city={sehir}&country=Turkey&method=13"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        if 'data' in data:
            vakitler = data['data']['timings']
        else:
            vakitler = None
    except Exception as e:
        print(f"Hata: {e}")
        vakitler = None

    return render_template('namazvakitleri.html', vakitler=vakitler, sehir=sehir.capitalize(), tarih=tarih_bugun)

@app.route('/vakitnamazlar')
def vakitnamazlar():
    return render_template("vakitnamazlar.html")

@app.route('/digernamazlar')
def digernamazlar():
    return render_template("digernamazlar.html")

@app.route('/islamınsartlari')
def islamınsartlari():
    return render_template("islamınsartlari.html")

@app.route('/namazkılınısları')
def namazkılınısları():
    return render_template("namazkılınısları.html")

@app.route('/dorthalife')
def dorthaife():
    return render_template("dorthalife.html")

@app.route('/peygamber')
def peygamber():
    return render_template("peygamber.html")

@app.route('/dualar')
def dualar():
    return render_template("dualar.html")

@app.route('/namazdualari')
def namazdualari():
    return render_template("namazdualari.html")

@app.route('/aile')
def aile():
    return render_template("aile.html")

@app.route('/iyilik')
def iyilik():
    return render_template("iyilik.html")

@app.route('/kudsi')
def kudsi():
    return render_template("kudsi.html")

@app.route('/israf')
def israf():
    return render_template("israf.html")

@app.route('/hicritakvim')
def hicritakvim():
    return render_template("hicritakvim.html")

if __name__ == '__main__':
    app.run(debug=True)