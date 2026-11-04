"""Contexto acadêmico sempre obtido no servidor a partir do usuário autenticado."""

from sqlalchemy import select

from edutrack.models import Course, Discipline, Task

CONTEXT_LIMIT = 200


def study_context(db, user_id):
    def rows(model, *conditions):
        return list(
            db.scalars(
                select(model)
                .where(model.usuario_id == user_id, *conditions)
                .order_by(model.id)
                .limit(CONTEXT_LIMIT + 1)
            )
        )

    courses = rows(Course)
    disciplines = rows(Discipline)
    tasks = rows(Task, Task.status.in_(["pendente", "em_andamento"]))
    # A chave de titularidade nunca vem do navegador nem de argumentos sugeridos pela IA.
    return {
        "cursos": [{"id": str(c.id), "nome": c.nome} for c in courses[:CONTEXT_LIMIT]],
        "disciplinas": [
            {"id": str(d.id), "curso_id": str(d.curso_id), "nome": d.nome}
            for d in disciplines[:CONTEXT_LIMIT]
        ],
        "tarefas": [
            {
                "id": str(t.id),
                "disciplina_id": str(t.disciplina_id),
                "titulo": t.titulo,
                "descricao": (t.descricao or "")[:300],
                "status": t.status,
                "data_prevista": t.data_prevista.isoformat() + "Z" if t.data_prevista else None,
                "minutos_estimados": t.minutos_estimados,
            }
            for t in tasks[:CONTEXT_LIMIT]
        ],
        "limite_atingido": any(
            len(items) > CONTEXT_LIMIT for items in (courses, disciplines, tasks)
        ),
        "aviso_privacidade": "Somente contexto acadêmico da conta autenticada; sem e-mail, CPF ou senha.",
    }
