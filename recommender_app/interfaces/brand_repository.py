from typing import Protocol, List, Optional
from recommender_app.models.brand import Brand


class BrandRepository(Protocol):

    def create_brand(self, name: str, url: str) -> None:
        """Create a new brand."""
        pass

    def get_brand(self, brand_id: int) -> Optional[Brand]:
        """Get a brand by its ID."""
        pass

    def update_brand(self, brand_id: int, name: str, url: str) -> None:
        """Update an existing brand."""
        pass

    def delete_brand(self, brand_id: int) -> None:
        """Delete a brand by its ID."""
        pass

    def get_all_brands(self) -> List[Brand]:
        """Get all brands."""
        pass
