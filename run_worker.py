from app.worker import loop_worker
from app.logger import setup_logger

logger = setup_logger("robot-b-main")

if __name__ == "__main__":
    logger.info("🚀 Iniciando Robô B")
    loop_worker()
