import qrcode
from django.conf import settings
from .models import Subject
import os

# Define the path where QR codes will be saved
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
qr_code_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
os.makedirs(qr_code_path, exist_ok=True)

def generate_qr_code(subject_id):
    # Create the URL for the attendance form
    url = f"http://192.168.195.186/attendance-form/?subject_id={subject_id}"
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    
    # Save the QR code image
    file_path = os.path.join(qr_code_path, f'subject_{subject_id}.png')
    img.save(file_path)
    print(f"QR code saved to {file_path}")

def generate_all_qr_codes():
    subjects = Subject.objects.all()
    for subject in subjects:
        generate_qr_code(subject.id)

if __name__ == "__main__":
    generate_all_qr_codes()
