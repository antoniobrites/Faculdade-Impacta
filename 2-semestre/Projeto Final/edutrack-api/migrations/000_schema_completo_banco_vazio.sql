-- Modelo completo para um banco EduTrackIA vazio, previamente criado pelo administrador.

-- Não executar no banco existente; nele use somente migrações revisadas.

USE [EduTrackIA];

GO

SET XACT_ABORT ON;

IF EXISTS (SELECT 1 FROM sys.tables WHERE is_ms_shipped = 0)

    THROW 50002, 'O banco deve estar vazio. Use migrações para um banco existente.', 1;

BEGIN TRANSACTION;

CREATE TABLE usuarios (
	nome NVARCHAR(150) NOT NULL, 
	email NVARCHAR(255) NOT NULL, 
	senha_hash VARCHAR(255) NOT NULL, 
	role VARCHAR(16) NOT NULL DEFAULT 'student', 
	id UNIQUEIDENTIFIER NOT NULL, 
	criado_em DATETIME2(3) NOT NULL, 
	atualizado_em DATETIME2(3) NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT [CK_usuarios_role] CHECK (role IN ('student', 'admin')), 
	UNIQUE (email)
);

CREATE TABLE convites_administrador (
	email NVARCHAR(255) NOT NULL, 
	criado_em DATETIME2(3) NOT NULL, 
	expira_em DATETIME2(3) NOT NULL, 
	usado_em DATETIME2(3) NULL, 
	usuario_id UNIQUEIDENTIFIER NULL, 
	PRIMARY KEY (email), 
	CONSTRAINT [CK_convites_admin_prazo] CHECK (expira_em > criado_em), 
	CONSTRAINT [CK_convites_admin_consumo] CHECK ((usado_em IS NULL AND usuario_id IS NULL) OR (usado_em IS NOT NULL AND usuario_id IS NOT NULL)), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE cursos (
	usuario_id UNIQUEIDENTIFIER NOT NULL, 
	nome NVARCHAR(150) NOT NULL, 
	instituicao NVARCHAR(200) NULL, 
	data_inicio DATETIME NULL, 
	data_fim DATETIME NULL, 
	id UNIQUEIDENTIFIER NOT NULL, 
	criado_em DATETIME2(3) NOT NULL, 
	atualizado_em DATETIME2(3) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id, usuario_id), 
	CHECK (data_inicio IS NULL OR data_fim IS NULL OR data_fim >= data_inicio), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE recuperacoes_senha (
	usuario_id UNIQUEIDENTIFIER NOT NULL, 
	token_hash VARCHAR(64) NOT NULL, 
	criado_em DATETIME2(3) NOT NULL, 
	expira_em DATETIME2(3) NOT NULL, 
	usado_em DATETIME2(3) NULL, 
	id UNIQUEIDENTIFIER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT [CK_recuperacoes_senha_prazo] CHECK (expira_em > criado_em), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id), 
	UNIQUE (token_hash)
);

CREATE INDEX ix_recuperacoes_senha_usuario_id ON recuperacoes_senha (usuario_id);

CREATE TABLE relatorios_semanais (
	usuario_id UNIQUEIDENTIFIER NOT NULL, 
	periodo_inicio DATETIME NOT NULL, 
	periodo_fim DATETIME NOT NULL, 
	url_arquivo NVARCHAR(2048) NULL, 
	gerado_em DATETIME2(3) NOT NULL, 
	id UNIQUEIDENTIFIER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE verificacoes_email (
	usuario_id UNIQUEIDENTIFIER NOT NULL, 
	codigo_hash VARCHAR(64) NULL, 
	expira_em DATETIME2(3) NULL, 
	confirmado_em DATETIME2(3) NULL, 
	enviado_em DATETIME2(3) NULL, 
	janela_em DATETIME2(3) NULL, 
	envios INTEGER NOT NULL, 
	tentativas INTEGER NOT NULL, 
	versao INTEGER NOT NULL, 
	PRIMARY KEY (usuario_id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE disciplinas (
	curso_id UNIQUEIDENTIFIER NOT NULL, 
	usuario_id UNIQUEIDENTIFIER NOT NULL, 
	nome NVARCHAR(150) NOT NULL, 
	professor NVARCHAR(150) NULL, 
	carga_horaria INTEGER NULL, 
	id UNIQUEIDENTIFIER NOT NULL, 
	criado_em DATETIME2(3) NOT NULL, 
	atualizado_em DATETIME2(3) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id, usuario_id), 
	FOREIGN KEY(curso_id, usuario_id) REFERENCES cursos (id, usuario_id), 
	CHECK (carga_horaria IS NULL OR carga_horaria >= 0), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE tarefas_academicas (
	disciplina_id UNIQUEIDENTIFIER NOT NULL, 
	usuario_id UNIQUEIDENTIFIER NOT NULL, 
	titulo NVARCHAR(200) NOT NULL, 
	descricao NTEXT NULL, 
	data_prevista DATETIME2(3) NULL, 
	status VARCHAR(20) NOT NULL, 
	minutos_estimados INTEGER NULL, 
	concluido_em DATETIME2(3) NULL, 
	id UNIQUEIDENTIFIER NOT NULL, 
	criado_em DATETIME2(3) NOT NULL, 
	atualizado_em DATETIME2(3) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(disciplina_id, usuario_id) REFERENCES disciplinas (id, usuario_id), 
	CHECK (status IN ('pendente', 'em_andamento', 'concluida', 'cancelada')), 
	CHECK (status <> 'concluida' OR concluido_em IS NOT NULL), 
	CHECK (minutos_estimados IS NULL OR minutos_estimados >= 0), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE registros_tempo_tarefa (
	tarefa_id UNIQUEIDENTIFIER NOT NULL, 
	iniciado_em DATETIME2(3) NOT NULL, 
	finalizado_em DATETIME2(3) NULL, 
	duracao_minutos AS (CASE WHEN finalizado_em IS NULL THEN NULL ELSE DATEDIFF(minute, iniciado_em, finalizado_em) END) PERSISTED, 
	criado_em DATETIME2(3) NOT NULL, 
	id UNIQUEIDENTIFIER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(tarefa_id) REFERENCES tarefas_academicas (id)
);

COMMIT TRANSACTION;

GO

