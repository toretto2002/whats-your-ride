from typing import Protocol, List, Optional
from recommender_app.models.version import Version

class VersionRepository(Protocol):

    def create_version(self, dto) -> None:
        """Create a new version."""
        pass

    def get_version(self, version_id: int) -> Optional[Version]:
        """Get a version by its ID."""
        pass

    def update_version(self, version_id: int, dto) -> None:
        """Update an existing version."""
        pass

    def delete_version(self, version_id: int) -> None:
        """Delete a version by its ID."""
        pass

    def get_all_versions(self) -> List[Version]:
        """Get all versions."""
        pass
    
    def get_version_by_name(self, name: str) -> Optional[Version]:
        """Get a version by its name."""
        pass