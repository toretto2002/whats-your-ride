class BotService:
    
    def handle_bot_request(self, data):
        print("Handling bot request with data:", data)
        return {"received": data}