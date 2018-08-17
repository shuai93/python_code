import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

static_dir = os.path.join(BASE_DIR, 'static')
print(BASE_DIR)
print(static_dir)