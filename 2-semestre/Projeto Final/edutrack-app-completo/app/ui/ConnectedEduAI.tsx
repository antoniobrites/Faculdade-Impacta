'use client';

import { useEffect, useState, type FormEvent } from 'react';
import { Bot, CalendarDays, Send } from 'lucide-react';
import { api, localDateInput } from '../lib/academic-api';
import type { StudyPlan } from '../lib/academic-types';

export default function ConnectedEduAI() {
  const [configured, setConfigured] = useState<boolean | null>(null);
  const [consent, setConsent] = useState(false);
  const [useAI, setUseAI] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [plan, setPlan] = useState<StudyPlan | null>(null);
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant'; text: string }[]>([]);
  const [draft, setDraft] = useState('');
  useEffect(() => {
    let active = true;
    api<{ configured: boolean }>('edu-ia/status').then((result) => { if (active) setConfigured(result.configured); }).catch((cause) => { if (active) setError(cause.message); });
    return () => { active = false; };
  }, []);
  async function makePlan(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); if (busy) return;
    const data = new FormData(event.currentTarget);
    setBusy(true); setError(''); setPlan(null);
    try {
      setPlan(await api<StudyPlan>('edu-ia/study-plan', { method: 'POST', body: JSON.stringify({
        data_inicio: data.get('data_inicio'), dias: Number(data.get('dias')), minutos_por_dia: Number(data.get('minutos_por_dia')),
        objetivo: data.get('objetivo'), usar_ia: useAI, enviar_dados_ia: useAI && consent,
      }) }));
    } catch (cause) { setError(cause instanceof Error ? cause.message : 'Não foi possível gerar o plano.'); }
    finally { setBusy(false); }
  }
  async function send(event: FormEvent) {
    event.preventDefault();
    if (!draft.trim() || !configured || !consent || busy) return;
    const pending = [...messages, { role: 'user' as const, text: draft.trim() }];
    setBusy(true); setError('');
    try {
      const result = await api<{ reply: string; plan: StudyPlan | null }>('edu-ia/chat', { method: 'POST', body: JSON.stringify({ messages: pending.slice(-10), enviar_dados_ia: true }) });
      setMessages([...pending, { role: 'assistant', text: result.reply }]); setDraft('');
      if (result.plan) setPlan(result.plan);
    } catch (cause) { setError(cause instanceof Error ? cause.message : 'Não foi possível enviar.'); }
    finally { setBusy(false); }
  }
  return <div className="connected-ai">
    <header className="page-heading"><div><span className="eyebrow">Seu assistente de estudos</span><h1>Edu IA</h1><p>Planeje sua rotina usando os cursos, disciplinas e atividades da sua conta.</p></div><Bot size={38} /></header>
    <div className="connection-notice">{configured === null ? 'Verificando conexão com o agente…' : configured ? 'Agente conectado. Autorize o envio de contexto antes de conversar.' : 'IA generativa ainda não configurada no servidor. O planejador por regras já funciona com suas atividades, sem enviar dados a serviços de IA.'}</div>
    <section className="surface connected-plan"><h2><CalendarDays size={22} /> Criar plano de estudo</h2><form onSubmit={makePlan}>
      <fieldset className="connected-fields" disabled={busy}>
        <div className="connected-grid"><label>Começar em<input name="data_inicio" type="date" required defaultValue={localDateInput(new Date())} /></label><label>Período (dias)<input name="dias" type="number" min={1} max={14} required defaultValue={7} /></label><label>Minutos por dia<input name="minutos_por_dia" type="number" min={15} max={240} required defaultValue={60} /></label></div>
        <label>Seu objetivo<input name="objetivo" maxLength={1000} required defaultValue="Organizar minhas atividades pendentes" /></label>
        {configured && <><label className="checkbox-line"><input type="checkbox" checked={consent} onChange={(event) => { setConsent(event.target.checked); if (!event.target.checked) setUseAI(false); }} /> Autorizo o envio das mensagens e do contexto acadêmico desta conta ao provedor de IA para esta conversa. Não inclua dados sensíveis nos textos.</label><label className="checkbox-line"><input type="checkbox" checked={useAI} disabled={!consent} onChange={(event) => setUseAI(event.target.checked)} /> Usar também a IA generativa no plano</label></>}
        <button className="primary-button" disabled={busy}>{busy ? 'Processando…' : 'Gerar plano de estudo'}</button>
      </fieldset>
    </form></section>
    {error && <p className="form-error" role="alert">{error}</p>}
    {plan && <section className="surface connected-plan" aria-live="polite"><span className="eyebrow">{plan.origem === 'ia' ? 'Plano com IA' : 'Planejador por regras'}</span><h2>Seu plano proposto</h2><p className="preserve-lines">{plan.resumo}</p><small>Proposta para revisão. Não modifica tarefas, prazos nem agenda e não é salva ao sair desta tela.</small>{plan.alertas.map((alert, index) => <p className="connection-notice" key={index}>{alert}</p>)}<div className="plan-blocks">{plan.blocos.map((block, index) => <article key={index}><strong>{new Date(block.data + 'T12:00:00').toLocaleDateString('pt-BR')} · {block.minutos} min</strong><h3>{block.titulo}</h3><p>{block.orientacao}</p></article>)}</div>{!plan.blocos.length && <p>Cadastre tarefas pendentes e gere novamente seu plano.</p>}{plan.tarefas_nao_planejadas.length > 0 && <p>{plan.tarefas_nao_planejadas.length} tarefa(s) não couberam neste período. Revise os alertas ou amplie sua disponibilidade.</p>}</section>}
    <section className="surface connected-chat"><h2>Converse com a Edu IA</h2><p>Peça explicações, revisões ou ajuda para estudar suas matérias.</p><div className="connected-messages" role="log" aria-live="polite">{messages.map((message, index) => <article className={'message-' + message.role} key={index}><strong>{message.role === 'user' ? 'Você' : 'Edu IA'}</strong><p className="preserve-lines">{message.text}</p></article>)}</div><form onSubmit={send}><label htmlFor="edu-message">Sua pergunta</label><textarea id="edu-message" maxLength={2000} rows={3} value={draft} onChange={(event) => setDraft(event.target.value)} disabled={!configured || !consent || busy} placeholder={!configured ? 'Aguardando configuração da chave no servidor' : !consent ? 'Autorize o uso da IA acima para começar' : 'O que você gostaria de estudar?'} /><button className="primary-button" disabled={!configured || !consent || busy || !draft.trim()}><Send size={17} />{busy ? 'Aguarde…' : 'Enviar pergunta'}</button></form><small>Confira as respostas com seus materiais. A conversa não fica salva ao sair desta tela.</small></section>
  </div>;
}

