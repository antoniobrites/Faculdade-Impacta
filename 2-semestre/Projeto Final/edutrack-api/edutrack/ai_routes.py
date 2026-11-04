from fastapi import APIRouter, HTTPException, Request

from edutrack.agent import require_ai, run_agent
from edutrack.planning import build_plan
from edutrack.routes import Db, Student
from edutrack.schemas import ChatInput, ChatMessage, ChatOutput, PlanInput, StudyPlan
from edutrack.study_context import study_context

router = APIRouter(prefix="/api/edu-ia", tags=["Edu IA"])


def rate_limit(request, student):
    request.app.state.limiter.check("ai:" + str(student.id), 8, 60)


@router.get("/status")
def status(request: Request, student: Student):
    return {"configured": request.app.state.settings.ai_configured, "planejador_por_regras": True}


@router.get("/context")
def context(db: Db, student: Student):
    return study_context(db, student.id)


@router.post("/chat", response_model=ChatOutput)
def chat(body: ChatInput, request: Request, db: Db, student: Student):
    rate_limit(request, student)
    settings = request.app.state.settings
    require_ai(settings, body.enviar_dados_ia)
    academic_context = study_context(db, student.id)
    return run_agent(settings, body.messages, academic_context)


@router.post("/study-plan", response_model=StudyPlan)
def plan(body: PlanInput, request: Request, db: Db, student: Student):
    rate_limit(request, student)
    context = study_context(db, student.id)
    proposal = build_plan(context, body)
    if not body.usar_ia:
        return proposal
    settings = request.app.state.settings
    require_ai(settings, body.enviar_dados_ia)
    result = run_agent(
        settings,
        [ChatMessage(role="user", text="Crie e explique meu plano de estudos: " + body.objetivo)],
        context,
        body,
    )
    if not result["plan"]:
        raise HTTPException(
            502, "A IA não gerou o plano. Tente novamente ou use o planejamento por regras."
        )
    proposal = result["plan"]
    proposal.origem = "ia"
    proposal.resumo = result["reply"]
    return proposal
