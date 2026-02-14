import requests
from .config import NGROK_BASE_URL, API_KEY, REQUEST_TIMEOUT
from .logger import setup_logger

logger = setup_logger("robot-b-client")

HEADERS = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json",
}


def obter_proxima_task():
    try:
        url = f"{NGROK_BASE_URL}/tasks/next"
        logger.debug(f"GET {url}")

        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        data = resp.json()

        if not data or data.get("task") is None:
            return None

        return data

    except Exception:
        logger.exception("Erro ao buscar próxima task")
        return None


def concluir_task(task_id: int, status: str):
    try:
        url = f"{NGROK_BASE_URL}/tasks/{task_id}/complete"

        logger.debug(f"POST {url}")

        resp = requests.post(
            url,
            headers=HEADERS,
            json={"status": status},
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()

        logger.info(f"Task {task_id} enviada como {status}")

    except Exception:
        logger.exception(f"Erro ao concluir task {task_id}")
