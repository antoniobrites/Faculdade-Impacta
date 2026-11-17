# Tarefa 13 — APIs CRUD de disciplinas

EduTrack · Innovation Lab · Faculdade Impacta · 17/11/2026

**Situação:** Executado no FastAPI.

## Entrega e explicação

Rotas preservadas: GET /api/disciplines; POST /api/disciplines; PUT /api/disciplines/{id}; DELETE /api/disciplines/{id}. O PUT mantém o contrato existente em lugar do PATCH ilustrativo do enunciado.

O usuário vem da autenticação do servidor. O curso precisa pertencer à mesma conta, e consultas e alterações são restritas ao proprietário. IDs de outra conta não conferem autorização. O teste cobre criação, leitura, edição, exclusão e isolamento.

Swagger de QA: http://127.0.0.1:8014/docs enquanto a prévia estiver em execução. Instalação local normal: http://127.0.0.1:8000/docs. O OpenAPI exportado permite examinar o contrato mesmo com o servidor desligado.

## Fontes e evidências

- [edutrack-api/edutrack/routes.py](https://github.com/antoniobrites/Faculdade-Impacta/blob/codex/innovation-lab-16-tarefas/2-semestre/Projeto%20Final/edutrack-api/edutrack/routes.py)
- [edutrack-api/docs/openapi.json](https://github.com/antoniobrites/Faculdade-Impacta/blob/codex/innovation-lab-16-tarefas/2-semestre/Projeto%20Final/edutrack-api/docs/openapi.json)

Consulte também o índice, a matriz de adaptações e os arquivos em `evidencias/` deste pacote.
