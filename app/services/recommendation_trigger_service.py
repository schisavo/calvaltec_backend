import json
import logging
import urllib.error
import urllib.request
from typing import Any

from app.core.config import settings
from app.repositories.recommendation_repository import create_recommendation
from app.schemas.recommendation import RecommendationCreate, RecommendationOut
from app.services.assessment_service import get_assessment_data
from app.services.recommendation_service import _to_out
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def build_fallback_report(
    *,
    puntaje: float,
    estado: str,
    brechas: list[str],
    recomendaciones: list[str],
    empresa: str | None = None,
) -> dict[str, Any]:
    nivel = "Alto" if puntaje < 60 else "Medio" if puntaje < 80 else "Bajo"
    return {
        "empresa": empresa,
        "analisis_general": (
            f"La evaluación registró un cumplimiento del {round(puntaje)}% ({estado}). "
            f"Se identificaron {len(brechas)} área(s) de mejora según el autodiagnóstico Ley 1581."
        ),
        "fortalezas": [],
        "debilidades": brechas,
        "nivel_riesgo": nivel,
        "recomendaciones": recomendaciones
        or ["Elaborar un plan de acción para cerrar las brechas identificadas."],
    }


def _should_trigger_n8n() -> bool:
    public_url = (settings.BACKEND_PUBLIC_URL or "").strip()
    webhook = (settings.N8N_RECOMMENDATIONS_WEBHOOK_URL or "").strip()
    return bool(webhook) and public_url.startswith("https://")


def _trigger_n8n_async(assessment_id: int, assessment_payload: dict[str, Any]) -> None:
    webhook = settings.N8N_RECOMMENDATIONS_WEBHOOK_URL
    public_url = (settings.BACKEND_PUBLIC_URL or "").rstrip("/")
    body = json.dumps(
        {
            "assessment_id": assessment_id,
            "api_base_url": public_url,
            "assessment": assessment_payload,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        webhook,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        logger.warning("n8n recommendations webhook HTTP %s: %s", exc.code, detail)
    except Exception as exc:
        logger.warning("n8n recommendations webhook failed: %s", exc)


def generate_recommendations_for_assessment(
    db: Session,
    assessment_id: int,
    *,
    puntaje: float,
    estado: str,
    brechas: list[str],
    recomendaciones: list[str],
    empresa: str | None = None,
) -> RecommendationOut:
    assessment_out = get_assessment_data(db, assessment_id)
    report = build_fallback_report(
        puntaje=puntaje,
        estado=estado,
        brechas=brechas,
        recomendaciones=recomendaciones,
        empresa=empresa or assessment_out.company.name,
    )
    rec = create_recommendation(
        db,
        RecommendationCreate(assessment_id=assessment_id, report=report),
    )

    if _should_trigger_n8n():
        assessment_payload = assessment_out.model_dump(mode="json")
        _trigger_n8n_async(assessment_id, assessment_payload)

    return _to_out(rec)
