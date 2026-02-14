import requests
import time

from .config import NGROK_BASE_URL, API_KEY, REQUEST_TIMEOUT
from .logger import setup_logger

logger = setup_logger("robot-b-client")

HEADERS = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json",
}


def obter_proxima_task():
    url = f"{NGROK_BASE_URL}/tasks/next"
    inicio = time.time()

    try:
        logger.info(f"🔎 Polling em {url}")

        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        elapsed = time.time() - inicio

        logger.info(f"📡 Status HTTP: {resp.status_code} ({elapsed:.2f}s)")

        resp.raise_for_status()
        data = resp.json()

        # 🔴 aqui está o ponto crítico
        if not data or data.get("task") is None:
            logger.info("📭 API respondeu sem tarefas")
            return None

        logger.info(f"📥 Task recebida do servidor: {data}")
        return data

    except Exception:
        logger.exception("❌ Falha ao buscar próxima task")
        return None


def concluir_task(task_id: int, status: str):
    url = f"{NGROK_BASE_URL}/tasks/{task_id}/complete"
    inicio = time.time()

    try:
        logger.info(f"📤 Enviando conclusão da task {task_id} → {status}")

        resp = requests.post(
            url,
            headers=HEADERS,
            json={"status": status},
            timeout=REQUEST_TIMEOUT,
        )

        elapsed = time.time() - inicio
        logger.info(f"📡 Status conclusão: {resp.status_code} ({elapsed:.2f}s)")

        resp.raise_for_status()
        logger.info(f"✅ Task {task_id} confirmada pelo servidor")

    except Exception:
        logger.exception(f"❌ Erro ao concluir task {task_id}")
