# Dicionário de dados — EduTrack

Modelo alvo gerado do código, sem consultar valores de usuários. SQL Server; datas DATETIME2 seguem UTC.

A versão final contém nove tabelas. `recuperacoes_senha` depende da migração 003; a existência no modelo não comprova aplicação no banco.

CPF é validado e descartado. Senhas são armazenadas somente como hash Argon2; códigos de confirmação usam HMAC e tokens de recuperação usam SHA-256.

## usuarios

| Campo | Tipo SQL Server | Nulo | Chave / regra |
|---|---|---|---|
| `nome` | `NVARCHAR(150)` | Não | — |
| `email` | `NVARCHAR(255)` | Não | UNIQUE |
| `senha_hash` | `VARCHAR(255)` | Não | — |
| `role` | `VARCHAR(16)` | Não | — |
| `id` | `UNIQUEIDENTIFIER` | Não | PK |
| `criado_em` | `DATETIME2(3)` | Não | — |
| `atualizado_em` | `DATETIME2(3)` | Não | — |

Restrições: role IN ('student', 'admin').

## convites_administrador

| Campo | Tipo SQL Server | Nulo | Chave / regra |
|---|---|---|---|
| `email` | `NVARCHAR(255)` | Não | PK |
| `criado_em` | `DATETIME2(3)` | Não | — |
| `expira_em` | `DATETIME2(3)` | Não | — |
| `usado_em` | `DATETIME2(3)` | Sim | — |
| `usuario_id` | `UNIQUEIDENTIFIER` | Sim | FK → usuarios.id |

Restrições: (usado_em IS NULL AND usuario_id IS NULL) OR (usado_em IS NOT NULL AND usuario_id IS NOT NULL); expira_em > criado_em.

## cursos

| Campo | Tipo SQL Server | Nulo | Chave / regra |
|---|---|---|---|
| `usuario_id` | `UNIQUEIDENTIFIER` | Não | FK → usuarios.id |
| `nome` | `NVARCHAR(150)` | Não | — |
| `instituicao` | `NVARCHAR(200)` | Sim | — |
| `data_inicio` | `DATETIME` | Sim | — |
| `data_fim` | `DATETIME` | Sim | — |
| `id` | `UNIQUEIDENTIFIER` | Não | PK |
| `criado_em` | `DATETIME2(3)` | Não | — |
| `atualizado_em` | `DATETIME2(3)` | Não | — |

Restrições: data_inicio IS NULL OR data_fim IS NULL OR data_fim >= data_inicio.

## recuperacoes_senha

| Campo | Tipo SQL Server | Nulo | Chave / regra |
|---|---|---|---|
| `usuario_id` | `UNIQUEIDENTIFIER` | Não | FK → usuarios.id |
| `token_hash` | `VARCHAR(64)` | Não | UNIQUE |
| `criado_em` | `DATETIME2(3)` | Não | — |
| `expira_em` | `DATETIME2(3)` | Não | — |
| `usado_em` | `DATETIME2(3)` | Sim | — |
| `id` | `UNIQUEIDENTIFIER` | Não | PK |

Restrições: expira_em > criado_em.

## relatorios_semanais

| Campo | Tipo SQL Server | Nulo | Chave / regra |
|---|---|---|---|
| `usuario_id` | `UNIQUEIDENTIFIER` | Não | FK → usuarios.id |
| `periodo_inicio` | `DATETIME` | Não | — |
| `periodo_fim` | `DATETIME` | Não | — |
| `url_arquivo` | `NVARCHAR(2048)` | Sim | — |
| `gerado_em` | `DATETIME2(3)` | Não | — |
| `id` | `UNIQUEIDENTIFIER` | Não | PK |

Restrições: .

## verificacoes_email

| Campo | Tipo SQL Server | Nulo | Chave / regra |
|---|---|---|---|
| `usuario_id` | `UNIQUEIDENTIFIER` | Não | PK; FK → usuarios.id |
| `codigo_hash` | `VARCHAR(64)` | Sim | — |
| `expira_em` | `DATETIME2(3)` | Sim | — |
| `confirmado_em` | `DATETIME2(3)` | Sim | — |
| `enviado_em` | `DATETIME2(3)` | Sim | — |
| `janela_em` | `DATETIME2(3)` | Sim | — |
| `envios` | `INTEGER` | Não | — |
| `tentativas` | `INTEGER` | Não | — |
| `versao` | `INTEGER` | Não | — |

Restrições: .

## disciplinas

| Campo | Tipo SQL Server | Nulo | Chave / regra |
|---|---|---|---|
| `curso_id` | `UNIQUEIDENTIFIER` | Não | FK → cursos.id |
| `usuario_id` | `UNIQUEIDENTIFIER` | Não | FK → cursos.usuario_id; FK → usuarios.id |
| `nome` | `NVARCHAR(150)` | Não | — |
| `professor` | `NVARCHAR(150)` | Sim | — |
| `carga_horaria` | `INTEGER` | Sim | — |
| `id` | `UNIQUEIDENTIFIER` | Não | PK |
| `criado_em` | `DATETIME2(3)` | Não | — |
| `atualizado_em` | `DATETIME2(3)` | Não | — |

Restrições: carga_horaria IS NULL OR carga_horaria >= 0.

## tarefas_academicas

| Campo | Tipo SQL Server | Nulo | Chave / regra |
|---|---|---|---|
| `disciplina_id` | `UNIQUEIDENTIFIER` | Não | FK → disciplinas.id |
| `usuario_id` | `UNIQUEIDENTIFIER` | Não | FK → disciplinas.usuario_id; FK → usuarios.id |
| `titulo` | `NVARCHAR(200)` | Não | — |
| `descricao` | `NTEXT` | Sim | — |
| `data_prevista` | `DATETIME2(3)` | Sim | — |
| `status` | `VARCHAR(20)` | Não | — |
| `minutos_estimados` | `INTEGER` | Sim | — |
| `concluido_em` | `DATETIME2(3)` | Sim | — |
| `id` | `UNIQUEIDENTIFIER` | Não | PK |
| `criado_em` | `DATETIME2(3)` | Não | — |
| `atualizado_em` | `DATETIME2(3)` | Não | — |

Restrições: minutos_estimados IS NULL OR minutos_estimados >= 0; status <> 'concluida' OR concluido_em IS NOT NULL; status IN ('pendente', 'em_andamento', 'concluida', 'cancelada').

## registros_tempo_tarefa

| Campo | Tipo SQL Server | Nulo | Chave / regra |
|---|---|---|---|
| `tarefa_id` | `UNIQUEIDENTIFIER` | Não | FK → tarefas_academicas.id |
| `iniciado_em` | `DATETIME2(3)` | Não | — |
| `finalizado_em` | `DATETIME2(3)` | Sim | — |
| `duracao_minutos` | `INTEGER` | Sim | Calculado: CASE WHEN finalizado_em IS NULL THEN NULL ELSE DATEDIFF(minute, iniciado_em, finalizado_em) END |
| `criado_em` | `DATETIME2(3)` | Não | — |
| `id` | `UNIQUEIDENTIFIER` | Não | PK |

Restrições: .

## Integridade e uso

Os vínculos compostos de disciplina/curso e tarefa/disciplina incluem usuario_id para impedir associações entre contas. Exclusões com dependências são recusadas pela API. O agente consulta somente dados da conta autenticada.

`relatorios_semanais` é uma estrutura reservada para artefatos persistidos. Atualmente a tela calcula o relatório a partir das sessões e permite exportar CSV; ela não grava nessa tabela.

Ver [DER](MODELO_DE_DADOS.md) e [recuperação de senha](RECUPERACAO_DE_SENHA.md).