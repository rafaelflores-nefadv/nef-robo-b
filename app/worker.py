import time

from .api_client import obter_proxima_task, concluir_task
from .config import POLL_INTERVAL_IDLE, POLL_INTERVAL_ERROR
from .logger import setup_logger

logger = setup_logger("robot-b-worker")

ultimo_task_id = None
total_processadas = 0


def processar_codigo(codigo: str) -> str:
    """
    Processa o código.
    Retorna:
      - PROCESSADO → sucesso
      - ERRO → falha técnica
    """
    logger.info(f"⚙️ Processando código: {codigo}")

    try:
        # 🔥 AQUI entra sua lógica real depois
        time.sleep(1)

        # ✅ enquanto não há regra de negócio:
        logger.info(f"✅ Código processado com sucesso: {codigo}")
        return "PROCESSADO"

    except Exception as e:
        logger.exception(f"💥 Falha ao processar código: {codigo}")
        return "ERRO"




def loop_worker():
    global ultimo_task_id, total_processadas

    logger.info("🤖 Worker iniciado — aguardando tarefas")

    while True:
        try:
            logger.debug("🔎 Iniciando polling...")

            task = obter_proxima_task()

            # -------------------------------------------------
            # 📭 SEM TASK
            # -------------------------------------------------
            if not task:
                logger.info(
                    f"😴 Idle — nenhuma task | última={ultimo_task_id} | total={total_processadas} | aguardando {POLL_INTERVAL_IDLE}s"
                )
                time.sleep(POLL_INTERVAL_IDLE)
                continue

            # -------------------------------------------------
            # 📥 RECEBEU TASK
            # -------------------------------------------------
            task_id = task["id"]
            codigo = task["codigo"]

            logger.info("--------------------------------------------------")
            logger.info(f"📥 NOVA TASK RECEBIDA → id={task_id}")
            logger.info(f"🔢 Código: {codigo}")

            inicio = time.time()

            status = processar_codigo(codigo)

            duracao = time.time() - inicio
            logger.info(f"⏱️ Processamento levou {duracao:.2f}s")

            logger.info(f"📤 Enviando resultado → {status}")
            concluir_task(task_id, status)

            ultimo_task_id = task_id
            total_processadas += 1

            logger.info(
                f"✅ Task {task_id} concluída | total processadas={total_processadas}"
            )
            logger.info("--------------------------------------------------")

        except Exception:
            logger.exception("❌ Erro inesperado no loop do worker")
            time.sleep(POLL_INTERVAL_ERROR)
