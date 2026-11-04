# Especificação da Edu IA

## Purpose

Definir o comportamento da assistente de estudos e sua integração segura com o contexto acadêmico.

## Requirements

### Requirement: Conversa contextual

A Edu IA SHALL responder perguntas de estudo usando apenas o contexto acadêmico autorizado do usuário.

#### Scenario: Pergunta sobre disciplina

- **WHEN** o estudante seleciona uma disciplina e envia uma pergunta
- **THEN** a API inclui somente dados necessários dessa conta e retorna uma resposta contextual

### Requirement: Transparência da integração

A interface SHALL informar quando a IA real estiver conectada e quando estiver usando orientação local de demonstração.

#### Scenario: API indisponível

- **WHEN** a integração externa não estiver configurada ou falhar
- **THEN** a interface apresenta o estado correto sem fingir que houve uma resposta da IA remota

### Requirement: Limites e segurança

A API SHALL limitar frequência e tamanho das mensagens, SHALL proteger dados pessoais e SHALL manter o aviso de que respostas podem conter erros.

#### Scenario: Solicitação acima do limite

- **WHEN** uma conta excede o limite definido para mensagens
- **THEN** a API recusa temporariamente a solicitação com uma orientação clara para tentar depois

