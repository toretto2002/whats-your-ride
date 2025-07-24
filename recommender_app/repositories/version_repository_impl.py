from recommender_app.interfaces.version_repository import VersionRepository
from recommender_app.models.version import Version
from typing import List, Optional

class VersionRepositoryImpl(VersionRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    def create_version(self, dto) -> int:
        version = Version(**dto)
        self.db_session.add(version)
        self.db_session.commit()
        self.db_session.refresh(version)
        return version.id
        

    def get_version(self, version_id: int) -> Optional[Version]:
        return self.db_session.query(Version).filter(Version.id == version_id).first()

    def update_version(self, version_id: int, dto) -> None:
        version = self.get_version(version_id)
        if not version:
            raise ValueError(f"Version with ID {version_id} does not exist.")
        
        for key, value in dto.items():
            setattr(version, key, value)
        
        self.db_session.commit()

    def delete_version(self, version_id: int) -> None:
        version = self.get_version(version_id)
        if not version:
            raise ValueError(f"Version with ID {version_id} does not exist.")
        
        self.db_session.delete(version)
        self.db_session.commit()

    def get_all_versions(self) -> List[Version]:
        return self.db_session.query(Version).all()