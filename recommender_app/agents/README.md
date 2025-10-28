# Motorcycle Recommendation Agents

Questa cartella contiene gli agenti che sostituiscono la logica di llama-index con `openai-agents`.

## 📋 Architettura

```
┌─────────────────────────────────────────────────────────────┐
│         Motorcycle Recommendation Orchestrator              │
│                  (Agent principale)                         │
└─────────────────┬───────────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│ SQL Query        │  │ Answer Synthesis │
│ Generator Agent  │  │ Agent            │
└──────────────────┘  └──────────────────┘
```

## 🤖 Agenti Disponibili

### 1. **MotorcycleRecommendationOrchestrator** 
**File:** `motorcycle_recommendation_orchestrator_agent.py`

Agent principale che coordina l'intero flusso di raccomandazione.

**Sostituisce:** 
- `MotoItOpenAiBotService.ask()`

**Responsabilità:**
- Gestione sessioni conversazione
- Coordinamento tra SQL Generator e Answer Synthesis
- Retry logic con exponential backoff
- Fallback a GPT-3.5 in caso di rate limit

**Tabella:** `versions_enriched`

---

### 2. **SQLQueryGeneratorAgent**
**File:** `sql_query_generator_agent.py`

Genera query SQL da domande in linguaggio naturale.

**Sostituisce:**
- `NLSQLRetriever` di llama-index
- `NLSQLTableQueryEngine.retriever`

**Responsabilità:**
- Analisi domanda utente
- Generazione query SQL
- Gestione case-insensitive (ILIKE, LOWER)
- Validazione sicurezza query

**Tabelle:** `versions_enriched` o `motorcycles`

---

### 3. **AnswerSynthesisAgent**
**File:** `answer_synthesis_agent.py`

Sintetizza risposte naturali dai risultati SQL.

**Sostituisce:**
- `MotoItOpenAiBotService._synthesize_answer()`
- `AnswerBotService.compress_results()`

**Responsabilità:**
- Formattazione risultati in linguaggio naturale
- Compressione dati per ridurre token
- Generazione tabelle e statistiche
- Gestione storico conversazione

---

### 4. **SimpleMotorcycleChatAgent**
**File:** `simple_motorcycle_chat_agent.py`

Versione semplificata per chat sulla tabella `motorcycles`.

**Sostituisce:**
- `OpenAiBotService.ask()`

**Responsabilità:**
- Query semplici su motorcycles
- Nessuna gestione sessioni complessa
- Schema più semplice

**Tabella:** `motorcycles`

---

### 5. **OllamaMotorcycleQueryAgent**
**File:** `ollama_motorcycle_query_agent.py`

Agent per modelli locali Ollama (opzionale).

**Sostituisce:**
- `BotService` (se si vuole eliminare llama-index completamente)

**Responsabilità:**
- Query usando modelli locali Ollama
- Privacy-focused (nessun dato inviato a OpenAI)
- Riduzione costi

**Tabella:** `motorcycles`

**NOTA:** Può mantenere llama-index se necessario per modelli locali.

---

## 🔧 Implementazione

### Dipendenze
```bash
poetry add openai-agents
```

### Ordine di Implementazione Consigliato

1. ✅ **Creare skeleton degli agenti** (FATTO)
2. ⏳ **SQLQueryGeneratorAgent** - Inizia da qui, è il più critico
3. ⏳ **AnswerSynthesisAgent** - Secondo passo
4. ⏳ **MotorcycleRecommendationOrchestrator** - Combina i precedenti
5. ⏳ **SimpleMotorcycleChatAgent** - Versione semplificata
6. ⏳ **OllamaMotorcycleQueryAgent** - Opzionale, solo se necessario

### Pattern OpenAI Agents

```python
from agents import Agent, Runner

# Definire un agent
agent = Agent(
    name="sql_generator",
    instructions="Genera query SQL da domande in linguaggio naturale...",
    tools=[...]
)

# Eseguire con Runner
runner = Runner(agent)
result = await runner.run("Trova naked leggere")
```

### Tools da Implementare

- **Database Schema Tool**: Espone schema tabelle
- **SQL Execution Tool**: Esegue query in modo sicuro
- **Category Lookup Tool**: Recupera categorie disponibili
- **Result Compression Tool**: Comprime dati per ridurre token

---

## 📊 Mapping Servizi → Agenti

| Servizio Vecchio | Agente Nuovo | Priorità |
|-----------------|--------------|----------|
| `MotoItOpenAiBotService` | `MotorcycleRecommendationOrchestrator` | 🔴 Alta |
| `OpenAiBotService` | `SimpleMotorcycleChatAgent` | 🟡 Media |
| `BotService` (Ollama) | `OllamaMotorcycleQueryAgent` | 🟢 Bassa |
| `AnswerBotService` (helper) | `AnswerSynthesisAgent` | 🟡 Media |

---

## 🗄️ Schema Database

### `versions_enriched` (View)
Vedi: `utils/prompts/moto_it/versions_enriched_table_info.txt`

Campi principali:
- `brand`, `model`, `version`, `category`
- `power_hp`, `torque_nm`, `dry_weight`, `wet_weight`
- `displacement_cc`, `engine_configuration`
- `price`, `year`

### `motorcycles` (Tabella)
Vedi: `services/open_ai_bot_service.py` (custom_table_info)

Schema completo con 100+ campi tecnici.

---

## 📝 TODO

- [ ] Implementare SQLQueryGeneratorAgent
- [ ] Implementare AnswerSynthesisAgent
- [ ] Implementare MotorcycleRecommendationOrchestrator
- [ ] Implementare SimpleMotorcycleChatAgent
- [ ] Testing end-to-end
- [ ] Decidere se mantenere OllamaMotorcycleQueryAgent
- [ ] Rimuovere servizi vecchi dopo migrazione
- [ ] Aggiornare routes per usare nuovi agenti

---

## 🚀 Test Rapido

Dopo l'implementazione, testa con:

```python
from recommender_app.agents.motorcycle_recommendation_orchestrator_agent import (
    MotorcycleRecommendationOrchestrator
)

orchestrator = MotorcycleRecommendationOrchestrator(...)
result = await orchestrator.process_request(
    message="Cerco una naked leggera sotto i 180kg",
    session_id=None
)

print(result['answer'])
```
