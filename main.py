from flask import Flask, render_template, request, jsonify
from roboflow import Roboflow
import cv2
import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_HOST = os.getenv("DATABASE_HOST")
# Konfigurasi Database (Gantilah URL database sesuai dengan pengaturan Anda)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

db = SQLAlchemy(app)

# Inisialisasi Roboflow
rf = Roboflow(api_key="pnqOcI04CFBKzFgbTloy")
project = rf.workspace().project("motocyclehelmet_detection")
model = project.version(3).model

def create_filename(prefix, directory, extension):
    """Membuat nama file unik berdasarkan timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    counter = 0
    while True:
        filename = f"{prefix}_{timestamp}_{counter}.{extension}"
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            return filepath
        counter += 1

# Sidebar
def load_sidebar():
    return render_template('sidebar.html')

# Model SQLAlchemy untuk tabel detection_result
class DetectionResult(db.Model):
    id_data = db.Column(db.Integer, primary_key=True)
    uploaded_image_path = db.Column(db.Text, nullable=True)
    helmet_count = db.Column(db.Integer, nullable=True)
    no_helmet_count = db.Column(db.Integer, nullable=True)
    detected_image_path = db.Column(db.Text, nullable=True)
    date_detection = db.Column(db.DateTime, default=datetime.datetime.now)
@app.route('/')
def home():
    # Mengambil data dari tabel detection_result
    detection_data = DetectionResult.query.all()

    # Membuat dictionary untuk mengelompokkan data berdasarkan tanggal
    grouped_data = {}
    helmet_count = 0
    no_helmet_count = 0

    for item in detection_data:
        date = item.date_detection.date()  # Mengambil tanggal saja (tanpa waktu)
        if date not in grouped_data:
            grouped_data[date] = {'helmet_count': 0, 'no_helmet_count': 0}
        grouped_data[date]['helmet_count'] += item.helmet_count
        grouped_data[date]['no_helmet_count'] += item.no_helmet_count

        # Menghitung jumlah deteksi helm dan tidak pakai helm secara keseluruhan
        helmet_count += item.helmet_count
        no_helmet_count += item.no_helmet_count

    return render_template('home.html', grouped_data=grouped_data, helmet_count=helmet_count, no_helmet_count=no_helmet_count, sidebar_content=load_sidebar())


@app.route('/upload')
def index():
    return render_template('index.html', sidebar_content=load_sidebar())


@app.route('/result', methods=['GET'])
def get_detection_data():
    # Mengambil data dari tabel detection_result
    detection_data = DetectionResult.query.all()

    # Mengonversi data menjadi format yang sesuai
    data = []
    for item in detection_data:
        data.append({
            'id_data': item.id_data,
            'uploaded_image_path': item.uploaded_image_path,
            'helmet_count': item.helmet_count,
            'no_helmet_count': item.no_helmet_count,
            'detected_image_path': item.detected_image_path,
            'date_detection': item.date_detection.strftime("%d-%m-%Y %H:%M:%S")
        })

    return render_template('data.html', detection_data=data)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        # Membuat nama file untuk file yang diunggah dan hasil deteksi
        upload_filepath = create_filename("upload", "static/uploads", "jpg")
        result_filepath = create_filename("result", "static/result", "jpg")

        # Menyimpan file yang diunggah
        file.save(upload_filepath)

        # Melakukan prediksi menggunakan model
        result = model.predict(upload_filepath, confidence=40, overlap=30)
        predictions = result.json()

        # Membaca gambar untuk visualisasi
        image = cv2.imread(upload_filepath)

        # Inisialisasi penghitung
        helmet_count = 0
        no_helmet_count = 0

        # Menggambar kotak pembatas dan label kelas, serta menghitung jumlah
        for bounding_box in predictions['predictions']:
            x0 = bounding_box['x'] - bounding_box['width'] / 2
            x1 = bounding_box['x'] + bounding_box['width'] / 2
            y0 = bounding_box['y'] - bounding_box['height'] / 2
            y1 = bounding_box['y'] + bounding_box['height'] / 2
            
            start_point = (int(x0), int(y0))
            end_point = (int(x1), int(y1))

            # Menentukan warna berdasarkan kelas dan menghitung
            if bounding_box["class"] == "pakai-helm":
                color = (0, 255, 0)  # Hijau
                helmet_count += 1
            else:
                color = (0, 0, 255)  # Merah
                no_helmet_count += 1

            cv2.rectangle(image, start_point, end_point, color=color, thickness=3)
            cv2.putText(
                image,
                bounding_box["class"],
                (int(x0), int(y0) - 10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0,
                color=(0,0,0),
                thickness=2
            )

        # Menyimpan gambar yang sudah diolah
        cv2.imwrite(result_filepath, image)

        # Simpan hasil deteksi ke database
        detection_data = DetectionResult(
            uploaded_image_path=upload_filepath.replace("\\", "/"),
            helmet_count=helmet_count,
            no_helmet_count=no_helmet_count,
            detected_image_path=result_filepath.replace("\\", "/")
        )
        db.session.add(detection_data)
        db.session.commit()

        # Membuat dictionary untuk hasil
        results = {
            'total_detections': len(predictions['predictions']),
            'helmet_count': helmet_count,
            'no_helmet_count': no_helmet_count,
            'uploaded_image_path': upload_filepath.replace("\\", "/"),  # Mengganti backslash menjadi garis miring
            'detected_image_path': result_filepath.replace("\\", "/")  # Mengganti backslash menjadi garis miring
        }

        return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
