import time
from .api_client import obter_proxima_task, concluir_task
from .config import POLL_INTERVAL_IDLE, POLL_INTERVAL_ERROR
from .logger import setup_logger

logger = setup_logger("robot-b-worker")


def processar_codigo(codigo: str) -> str:
    """
    🔥 SUBSTITUA pela lógica real do cliente.
    """
    logger.info(f"Processando código: {codigo}")

    # simulação
    if str(codigo).endswith("0"):
        return "INVALIDO"

    return "OK"


def loop_worker():
    logger.info("🤖 Worker iniciado")

    while True:
        try:
            task = obter_proxima_task()

            if not task:
                logger.info("Nenhuma task disponível — aguardando...")
                time.sleep(POLL_INTERVAL_IDLE)
                continue

            task_id = task["id"]
            codigo = task["codigo"]

            logger.info(f"Task recebida: id={task_id} codigo={codigo}")

            status = processar_codigo(codigo)

            concluir_task(task_id, status)

        except Exception:
            logger.exception("Erro inesperado no loop do worker")
            time.sleep(POLL_INTERVAL_ERROR)
