from pathlib import Path

BASE_DIR = Path(__file__).parent

# 输入输出路径
INPUT_DIR = BASE_DIR / 'input'
OUTPUT_DIR = BASE_DIR / 'output'
IMAGE_DIR = OUTPUT_DIR / 'images'

# 创建必要的目录
for dir_path in [INPUT_DIR, OUTPUT_DIR, IMAGE_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# 文件路径
INPUT_FILE = INPUT_DIR / 'books.txt'
OUTPUT_FILE = OUTPUT_DIR / 'results.csv'  # 现在只包含书名和价格