import os
import logging
from datetime import datetime

Log_file_format = "DATE"f"{datetime.now().strftime('%m_%d_%y')}"
log_file_path = os.path.join(os.getcwd(), "logs", Log_file_format)
os.makedirs(log_file_path, exist_ok=True)
log_file_name = f"{Log_file_format}.log" 
log_file = os.path.join(log_file_path, log_file_name)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)