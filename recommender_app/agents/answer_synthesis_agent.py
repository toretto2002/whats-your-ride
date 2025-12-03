"""Answer Synthesis Agent

Scopo: dato l'input utente (prompt originale) e una lista di versioni moto
già filtrate/rankate (tipicamente max 20, deduplicate per model_id) produce
una risposta naturale riassuntiva in italiano.

Non genera query SQL, non chiama altri agenti: prende solo dati già calcolati.

INPUT ATTESO (passato come stringa all'agente):
Un blocco JSON serializzato o testo strutturato contenente:
{
  "user_message": <string>,
  "items": [ { ... versione ... }, ... ],
  "meta": { "total_raw": int, ... }
}

OUTPUT: oggetto AnswerSynthesisOutput
  - answer: testo finale (max ~600 parole) con:
	  * breve intro che richiama need dell'utente
	  * elenco puntato con: Modello, motore (cc), potenza (se presente), peso (dry o wet), prezzo, feature chiave (ABS, traction_control, ride_by_wire)
	  * Poi aggiungi un raggionamento il cui obiettivo principale è aiutare l'utente a comprendere i dati messi a disposizione in relazione alle èreferenze espresse, se le preferenze sono espresse espilicitamente parti da quelle evidenzia come i modelli rispondono a tali preferenze
		se  invece non sono espresse preferenze specifiche, evidenzia le caratteristiche salienti dei modelli elencati prendendo in esame tutti i dati che ogni modello fornisce.
	  * invito a chiedere raffinamenti (es. "Puoi chiedermi di restringere per peso, potenza o budget") a partire dal ragionamento che hai appena prodotto.
	  * interpreta al meglio le richieste dell'utente ovvero l'analisi deve essere basata anche sulle domande implicite ad esempio se il discorso verte sugli scooter comodità e consumi possono essere aspetti importanti da evidenziare mentre se si parla di sportive potenza e prestazioni sono più rilevanti.
  - reasoning: spiegazione sintetica (2-3 frasi) su come è stato composto l'elenco (NON ripetere tutta la lista)

REGOLE
  - NON inventare campi mancanti; se un campo è None/non presente, omettilo.
  - Usa solo i campi realmente presenti in ciascun dict.
  - Prezzo: mostra come "€ {valore}" (se < 10 es. 2.499 interpretalo come 2.499 -> €2.499). Non formattare con separatore migliaia se già decimale.
  - Motore: usa displacement (cc) e power_hp (CV) se entrambi presenti, formato "{displacement:.0f}cc / {power_hp:.0f} CV".
  - Peso: preferisci dry_weight, altrimenti wet_weight.
  - Feature: mostra solo quelle True tra ABS, traction_control, ride_by_wire.
  - Se non ci sono elementi -> answer deve essere: "Non ho trovato modelli che soddisfano i criteri indicati. Prova a rilassare qualche filtro (es. prezzo o cilindrata)."
  - Non ripetere più di una volta il brand se presenti più modelli dello stesso brand.
  - Lingua italiana, tono neutro-professionale.
  - Non aggiungere markup HTML, solo testo/markdown semplice.

ESEMPI ELENCO PUNTI
 - Piaggio Liberty 125: 125cc / 11 CV, peso 106 kg, €2.999, ABS
 - Vespa GTS 125 Super: 125cc / 14 CV, €6.299, ABS, Traction Control

Se l'utente chiede "le più leggere" e i dati peso mancano per alcune, ammetti la mancanza ("Alcuni modelli non riportano il peso e sono stati esclusi dal confronto peso.").

Non superare 10 modelli nell'elenco; se items >10 seleziona i primi 10 nell'ordine fornito (non ricalcolare ranking qui).
"""

from agents import Agent
from agents.run import Runner
from pydantic import BaseModel
import json


class AnswerSynthesisOutput(BaseModel):
	answer: str
	reasoning: str


answer_synthesis_agent = Agent(
	name="Answer Synthesis Agent",
	instructions=__doc__,
	output_type=AnswerSynthesisOutput,
)


def _build_prompt(user_message: str, items: list[dict], meta: dict) -> str:
	"""Costruisce il payload testuale da passare all'agente LLM.
	Serializza in JSON assicurando che i numeri rimangano tali.
	"""
	payload = {
		"user_message": user_message,
		"items": items,
		"meta": meta,
	}
	# Usa ensure_ascii False per preservare accenti
	return json.dumps(payload, ensure_ascii=False)


async def answer_synthesis_agent_runner(user_message: str, items: list[dict], meta: dict) -> AnswerSynthesisOutput:
	"""Esegue l'agente di sintesi risposta.

	Args:
		user_message: Messaggio originale dell'utente.
		items: lista di versioni moto già filtrate/deduplicate.
		meta: dizionario con info (es. total_raw_results)
	Returns:
		AnswerSynthesisOutput
	"""
	runner = Runner()
	input_text = _build_prompt(user_message, items, meta)
	result = await runner.run(starting_agent=answer_synthesis_agent, input=input_text)
	return result.final_output_as(AnswerSynthesisOutput)


__all__ = ["answer_synthesis_agent", "answer_synthesis_agent_runner", "AnswerSynthesisOutput"]

