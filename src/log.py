import logging
import pytz
from datetime import datetime

# Configuración del timezone de Colombia
colombia_tz = pytz.timezone('America/Bogota')

class ColombiaTimeFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, colombia_tz)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()

# Configuración básica del logger
def setup_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evitar que los mensajes se propaguen al logger raíz
    logger.propagate = False
    
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        
        # Configurar el formateador
        formatter = ColombiaTimeFormatter(
            fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger


logger = setup_logger()
