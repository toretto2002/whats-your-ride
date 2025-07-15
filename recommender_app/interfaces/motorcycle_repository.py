from typing import Protocol, List, Optional, Union

class MotorcycleRepository(Protocol):

    def get_motorcycle_by_id(self, motorcycle_id: int) -> Optional[dict]:
        """Retrieve a motorcycle by its ID."""
        pass
    
    def get_all_motorcycles(self) -> List[dict]:
        """Retrieve all motorcycles."""
        pass

    def get_all_motorcycles_by_brand(self, brand: str) -> List[dict]:
        """Retrieve all motorcycles by a specific brand."""
        pass
