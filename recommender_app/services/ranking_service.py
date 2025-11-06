"""Servizio di ranking/deduplicazione modelli.

Responsabilità: prendere le versioni grezze (rows) e restituire al massimo
una versione per modello, selezionando quella "migliore" secondo criteri
euristici. Non applica limiti di brand (richiesto esplicitamente).

È pensato per modelli nuovi da listino, quindi ignora aspetti di usura.

Funzioni principali:
 - choose_best_version(versions)
 - deduplicate_versions(rows, limit=20)

Nota: Le euristiche sono semplici e pensate per essere facilmente estendibili.
"""

from __future__ import annotations
from collections import defaultdict
from typing import List, Dict, Any


KEY_FIELDS = ["power_hp", "torque_nm", "displacement", "price", "dry_weight", "average_consumption"]


def _median(values: List[float]) -> float:
	if not values:
		return 0.0
	s = sorted(values)
	return s[len(s)//2]


def choose_best_version(versions: List[Dict[str, Any]]) -> Dict[str, Any]:
	"""Sceglie la migliore versione di un singolo modello.

	Criteri (ordine di sorting decrescente):
	1. Completezza (numero campi chiave non null)
	2. Potenza (power_hp)
	3. Coppia (torque_nm)
	4. Distanza dalla mediana del prezzo del gruppo (più vicino è meglio)
	5. Prezzo più basso (tie-break finale)
	"""
	if not versions:
		return {}

	prices = [v.get("price") for v in versions if v.get("price") is not None]
	median_price = _median(prices)

	def score(v: Dict[str, Any]):
		filled = sum(1 for f in KEY_FIELDS if v.get(f) not in (None, ""))
		power = v.get("power_hp") or 0
		torque = v.get("torque_nm") or 0
		price = v.get("price") or 0
		dist_med = abs(price - median_price) if median_price else 0
		# Ritorniamo tupla per ordinamento: elementi più grandi (o più negativi dove previsto) preferiti
		return (
			filled,
			power,
			torque,
			-dist_med,  # più vicino alla mediana meglio
			-price      # preferisci prezzo più basso come tie-break finale
		)

	return max(versions, key=score)


def _global_version_score(v: Dict[str, Any]) -> float:
	"""Calcola un punteggio globale per ordinare i migliori modelli (versioni già scelte)."""
	power = (v.get("power_hp") or 0)
	torque = (v.get("torque_nm") or 0)
	price = v.get("price") or 0
	abs_bonus = 0.05 if v.get("abs") else 0
	tc_bonus = 0.05 if v.get("traction_control") else 0
	rbw_bonus = 0.05 if v.get("ride_by_wire") else 0
	filled = sum(1 for f in KEY_FIELDS if v.get(f) not in (None, ""))
	completeness = filled / len(KEY_FIELDS)
	eff = 0.0
	if v.get("displacement"):
		eff = power / v.get("displacement")
	price_component = 1 / (1 + (price / 10000))  # listino basso permanece vicino a 1
	return (
		0.35 * eff +
		0.25 * completeness +
		0.15 * (power / 20) +   # scala ipotetica per non dominare
		0.10 * (torque / 20) +
		0.10 * price_component +
		abs_bonus + tc_bonus + rbw_bonus
	)


def deduplicate_versions(rows: List[Dict[str, Any]], limit: int = 20) -> List[Dict[str, Any]]:
	"""Dato l'elenco di versioni (rows), restituisce al massimo una versione per modello.

	1. Raggruppa per model_id.
	2. Sceglie la migliore versione per ogni gruppo.
	3. Ordina le versioni scelte per punteggio globale e taglia a 'limit'.
	"""
	if not rows:
		return []
	by_model: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
	for r in rows:
		mid = r.get("model_id")
		if mid is None:
			# Se manca model_id, usa id() per mantenerlo unico
			mid = id(r)
		by_model[mid].append(r)

	best_versions = [choose_best_version(vs) for vs in by_model.values()]
	best_versions_sorted = sorted(best_versions, key=_global_version_score, reverse=True)
	return best_versions_sorted[:limit]


__all__ = ["deduplicate_versions", "choose_best_version"]

