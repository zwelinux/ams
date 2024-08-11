import qrcode
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from app.models import Subject

class Command(BaseCommand):
    help = 'Generate QR codes for each subject'

    def handle(self, *args, **kwargs):
        # Define the path where QR codes will be saved
        qr_code_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        os.makedirs(qr_code_path, exist_ok=True)

        subjects = Subject.objects.all()
        for subject in subjects:
            self.generate_qr_code(subject.id, qr_code_path)
        
        self.stdout.write(self.style.SUCCESS('Successfully generated QR codes'))

    def generate_qr_code(self, subject_id, qr_code_path):
        # Create the URL for the attendance form
        url = f"http://192.168.195.186:8000/attendance-form/?subject_id={subject_id}"
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill='black', back_color='white')
        
        # Save the QR code image
        file_path = os.path.join(qr_code_path, f'subject_{subject_id}.png')
        img.save(file_path)
        print(f"QR code saved to {file_path}")
