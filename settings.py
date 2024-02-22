from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
qr_dir = os.path.join(BASE_DIR, 'qr', 'qrcodes')
doc_dir = os.path.join(BASE_DIR, 'docs', 'documents')
tmp_files = os.path.join(BASE_DIR, 'docs', 'tmp_files')
admins = [1458263235,646951760]
