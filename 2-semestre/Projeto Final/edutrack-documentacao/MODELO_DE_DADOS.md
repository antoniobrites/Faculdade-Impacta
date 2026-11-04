# Modelo de dados (DER)

Cardinalidades e vínculos do modelo alvo. O diagrama não contém dados dos alunos.

```mermaid
erDiagram
  usuarios ||--o{ cursos : possui
  cursos ||--o{ disciplinas : organiza
  disciplinas ||--o{ tarefas_academicas : contem
  tarefas_academicas ||--o{ registros_tempo_tarefa : acumula
  usuarios ||--o| verificacoes_email : verifica
  usuarios o|--o{ convites_administrador : consome
  usuarios ||--o{ recuperacoes_senha : solicita
  usuarios ||--o{ relatorios_semanais : possui
  usuarios {
    NVARCHAR nome
    NVARCHAR email
    VARCHAR senha_hash
    VARCHAR role
    UNIQUEIDENTIFIER id PK
    DATETIME2 criado_em
    DATETIME2 atualizado_em
  }
  convites_administrador {
    NVARCHAR email PK
    DATETIME2 criado_em
    DATETIME2 expira_em
    DATETIME2 usado_em
    UNIQUEIDENTIFIER usuario_id FK
  }
  cursos {
    UNIQUEIDENTIFIER usuario_id FK
    NVARCHAR nome
    NVARCHAR instituicao
    DATETIME data_inicio
    DATETIME data_fim
    UNIQUEIDENTIFIER id PK
    DATETIME2 criado_em
    DATETIME2 atualizado_em
  }
  recuperacoes_senha {
    UNIQUEIDENTIFIER usuario_id FK
    VARCHAR token_hash
    DATETIME2 criado_em
    DATETIME2 expira_em
    DATETIME2 usado_em
    UNIQUEIDENTIFIER id PK
  }
  relatorios_semanais {
    UNIQUEIDENTIFIER usuario_id FK
    DATETIME periodo_inicio
    DATETIME periodo_fim
    NVARCHAR url_arquivo
    DATETIME2 gerado_em
    UNIQUEIDENTIFIER id PK
  }
  verificacoes_email {
    UNIQUEIDENTIFIER usuario_id PK
    VARCHAR codigo_hash
    DATETIME2 expira_em
    DATETIME2 confirmado_em
    DATETIME2 enviado_em
    DATETIME2 janela_em
    INTEGER envios
    INTEGER tentativas
    INTEGER versao
  }
  disciplinas {
    UNIQUEIDENTIFIER curso_id FK
    UNIQUEIDENTIFIER usuario_id FK
    NVARCHAR nome
    NVARCHAR professor
    INTEGER carga_horaria
    UNIQUEIDENTIFIER id PK
    DATETIME2 criado_em
    DATETIME2 atualizado_em
  }
  tarefas_academicas {
    UNIQUEIDENTIFIER disciplina_id FK
    UNIQUEIDENTIFIER usuario_id FK
    NVARCHAR titulo
    NTEXT descricao
    DATETIME2 data_prevista
    VARCHAR status
    INTEGER minutos_estimados
    DATETIME2 concluido_em
    UNIQUEIDENTIFIER id PK
    DATETIME2 criado_em
    DATETIME2 atualizado_em
  }
  registros_tempo_tarefa {
    UNIQUEIDENTIFIER tarefa_id FK
    DATETIME2 iniciado_em
    DATETIME2 finalizado_em
    INTEGER duracao_minutos
    DATETIME2 criado_em
    UNIQUEIDENTIFIER id PK
  }
```

Curso e disciplina também possuem FK para usuarios. As FK compostas de organização acadêmica preservam a titularidade. Uma confirmação de e-mail pertence a uma única conta; um convite pode estar pendente, sem conta vinculada.
