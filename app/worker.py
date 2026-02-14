import time

from .api_client import obter_proxima_task, concluir_task
from .config import POLL_INTERVAL_IDLE, POLL_INTERVAL_ERROR
from .logger import setup_logger

logger = setup_logger("robot-b-worker")

# 🔴 estado em memória
ultimo_task_id = None


def processar_codigo(codigo: str) -> str:
    """
    🔥 SUBSTITUA pela lógica real do cliente.
    """
    logger.info(f"⚙️ Processando código: {codigo}")

    # simulação
    if str(codigo).endswith("0"):
        return "INVALIDO"

    return "OK"


def loop_worker():
    global ultimo_task_id

    logger.info("🤖 Worker iniciado")

    while True:
        try:
            task = obter_proxima_task()

            # -------------------------------------------------
            # 📭 SEM TASK
            # -------------------------------------------------
            if not task:
                if ultimo_task_id:
                    logger.info(
                        f"😴 Idle — nenhuma task (última processada: id={ultimo_task_id}) — aguardando {POLL_INTERVAL_IDLE}s"
                    )
                else:
                    logger.info(
                        f"😴 Idle — nenhuma task ainda — aguardando {POLL_INTERVAL_IDLE}s"
                    )

                time.sleep(POLL_INTERVAL_IDLE)
                continue

            # -------------------------------------------------
            # 📥 RECEBEU TASK
            # -------------------------------------------------
            task_id = task["id"]
            codigo = task["codigo"]

            logger.info(f"📥 Task recebida: id={task_id} codigo={codigo}")

            status = processar_codigo(codigo)

            concluir_task(task_id, status)

            ultimo_task_id = task_id

            logger.info(f"✅ Task {task_id} finalizada com status {status}")

        except Exception:
            logger.exception("❌ Erro inesperado no loop do worker")
            time.sleep(POLL_INTERVAL_ERROR)
