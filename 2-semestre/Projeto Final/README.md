# EduTrack — entrega acadêmica

**Site publicado:** <https://srv1834976.hstgr.cloud>. O banco público é novo; crie sua conta no site. As contas locais não foram migradas.

Gestão de estudos com React/TypeScript, API Python/FastAPI e SQL Server. Este pacote contém código-fonte, testes, documentação Markdown, modelo de dados, SQL e OpenSpec. Não contém banco de alunos, credenciais ou dependências instaladas.

## Estrutura

| Pasta | Conteúdo |
| --- | --- |
| `edutrack-app-completo` | Frontend e OpenSpec em `openspec/` |
| `edutrack-api` | API, agente de estudos, testes e migrações SQL |
| `edutrack-documentacao` | Explicações, DER, dicionário e roteiro de apresentação |
| `.github/workflows` | Modelo de CI; em repositório com subpasta, precisa ser instalado na raiz do repositório e ter os caminhos ajustados |

Abra `EduTrack.code-workspace` no VS Code. Leia primeiro [estado atual](edutrack-documentacao/ESTADO_ATUAL.md), [documentação](edutrack-documentacao/DOCUMENTACAO.md) e [validação](edutrack-documentacao/VALIDACAO_FINAL.md).

## Preparar o ambiente

1. Instale Node.js 22.13 ou superior, pnpm, Python 3.12, SQL Server e Microsoft ODBC Driver 18.
2. Em `edutrack-api`, crie o ambiente: `python -m venv .venv`.
3. Instale versões testadas: `.venv\Scripts\python.exe -m pip install -r requirements.lock.txt` e `.venv\Scripts\python.exe -m pip install --no-deps -e .`.
4. Em `edutrack-app-completo`, execute `pnpm install --frozen-lockfile`.
5. Configure o banco e segredos conforme os arquivos `.env.example`. Não copie os exemplos para um repositório com valores reais.
6. Para uma instalação **nova e vazia**, o SQL `migrations/000_schema_completo_banco_vazio.sql` descreve todas as tabelas. Sua execução exige autorização do responsável. Não execute esse arquivo no banco existente.
7. No frontend, `pnpm run dev:local` inicia site e API locais e abre o Chrome. Nenhuma migração é automática.

Site local: <http://localhost:3002/login>. Swagger: <http://127.0.0.1:8000/docs>. O terminal deve continuar aberto.

## Entrega e publicação

- O pacote é uma cópia organizada. O manifesto lista tamanho e SHA-256 de cada fonte.
- O site público anterior não é atualizado pela criação deste ZIP.
- A implantação na Hostinger foi autorizada e executada. Consulte [publicação e operação](edutrack-documentacao/PUBLICACAO_HOSTINGER.md).
- A Edu IA tem planejador por regras funcional; a conversa generativa aguarda chave e modelo. Não apresentar respostas de regras como chamadas a IA externa.
- O [roteiro dos vídeos](edutrack-documentacao/ROTEIRO_AVALIACAO_FINAL.md) cobre as três etapas da avaliação. Vídeos ainda precisam ser gravados e conferidos.

SMS, cobrança, aplicativo Flutter e administração completa de outras contas estão fora do escopo implementado.
