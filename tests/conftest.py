import sys
import os
from pathlib import Path

# Xác định thư mục gốc của project (thư mục cha của thư mục tests)
ROOT = Path(__file__).resolve().parent.parent

# Thêm thư mục gốc vào đầu sys.path nếu chưa có
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Đảm bảo các tiến trình Python con cũng có thể tìm thấy module
os.environ["PYTHONPATH"] = str(ROOT) + os.pathsep + os.environ.get("PYTHONPATH", "")
