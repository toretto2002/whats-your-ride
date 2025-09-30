

class AnswerBotService:
    MAX_ROWS_FOR_MODEL = 240
    TOP_TABLE_ROWS = 50
    NUMERIC_FIELDS = ["power_hp", "torque_nm", "dry_weight", "wet_weight", "displacement", "price", "seat_height_min", "seat_height_max"]

    def __init__(self):
        pass

    def score_row_relevance(self, row: dict[str, any], message: str) -> float:
        
        """
        È una funzione euristica: semplice, veloce, senza usare embeddings o modelli ML, ma utile per ordinare i risultati più probabili.
        Score the relevance of a database row to a given question.
        """
        
        keys = list(row.keys())

        text = " ".join(str(row.get(k)) for k in keys).lower()
        
        user_message = message.lower()
        key_words_count = 0
        
        for token in user_message.split():
            if token.lower() in text.lower():
                key_words_count += 1
                
        num_bonus = 0
        for field in self.NUMERIC_FIELDS:
            value = row.get(field)
            if value not in (None, "", 0):
                num_bonus += 1
        
        return key_words_count + (0.1 * num_bonus)
    
    def compress_results(self, rows: list[dict[str, any]], user_message: str) -> dict[str, any]:
        """
        Compress the results to fit within the model's input limits.
        """
        
        if not rows:
            return {"rows": [], "stats": {}, "groups": {}}
        
        ranked = sorted(rows, key= lambda r: self.score_row_relevance(r, user_message), reverse=True)[:self.MAX_ROWS_FOR_MODEL]
        
        def field_stats(field: str):
            
            values = [float(r[field]) for r in ranked if r.get(field) not in [None, "", "NA"]]
            
            if not values:
                return None
            
            values.sort()
            n = len(values)
            avg = sum(values) / n
            med = values[n // 2] if n % 2 == 1 else (values[n // 2 - 1] + values[n // 2]) / 2
            
            return {
                "min": min(values),
                "max": max(values),
                "avg": avg,
                "med": med,
            }
            
        stats = {field: field_stats(field) for field in self.NUMERIC_FIELDS}
        
        groups: dict[str, dict[str, int]] = {
            "by_category": {},
            "by_brand": {},
        }
        
        for r in ranked:
            brand = r.get("brand_name") or r.get("brand") 
            category = r.get("category_name") or r.get("category")
            if brand:
                groups["by_brand"][brand] = groups["by_brand"].get(brand, 0) + 1
            
            if category:
                groups["by_category"][category] = groups["by_category"].get(category, 0) + 1
        
        # Ordina i risultati per displacement in ordine decrescente (mancanti/non numerici in fondo)
        def _to_float(x):
            try:
                return float(x)
            except (TypeError, ValueError):
                return float('-inf')

        sorted_by_displacement = sorted(
            ranked,
            key=lambda r: _to_float(r.get("displacement")),
            reverse=True,
        )

        table_fields = ["brand", "model", "version", "year_start", "year_end", "category_name", "displacement", "power_hp", "torque_nm", "dry_weight", "wet_weight", "price"]               

        table = [
            {k: r.get(k) for k in table_fields} 
            for r in sorted_by_displacement
        ]
        
        for r in sorted_by_displacement:
            r["_evidence_id"] = f"{r.get('brand','?')}|{r.get('model','?')}|{r.get('version','?')}"
        
        return {
            "rows": sorted_by_displacement,
            "table": table,
            "stats": stats,
            "groups": groups
        }


    def summarize_history(self, messages: list[dict[str, any]], max_chars: int = 2000) -> str:
        """
        Summarize the chat history to provide context for the LLM.
        """
        
        if not messages:
            return ""
        
        tail = messages[-12:]
        
        s = []
        
        for m in tail:
            role = m.get("sender", "user")
            text = m.get("message", "")
            s.append(f"{str(role).upper()}:\n{text}\n")
            
        joined = "\n".join(s)
        return joined[-max_chars:]
    
        
