import segno
from settings import qr_dir
import os


def make_qr_and_return_path(string):
    qrcode = segno.make(string, micro=False)
    if not(os.path.isdir(qr_dir)):
        os.mkdir(qr_dir)
    qr_path = os.path.join(qr_dir, f"{string}.png")
    qrcode.save(qr_path, scale=5)
    return qr_path
