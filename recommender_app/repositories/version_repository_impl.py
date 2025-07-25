from recommender_app.interfaces.version_repository import VersionRepository
from recommender_app.models.version import Version
from typing import List, Optional
from recommender_app.extensions import db

class VersionRepositoryImpl(VersionRepository):

    def create_version(self, dto) -> int:
        version = Version(**dto)
        db.session.add(version)
        db.session.commit()
        db.session.refresh(version)
        return version.id
        

    def get_version(self, version_id: int) -> Optional[Version]:
        return db.session.query(Version).filter(Version.id == version_id).first()

    def update_version(self, version_id: int, dto) -> None:
        version = self.get_version(version_id)
        if not version:
            raise ValueError(f"Version with ID {version_id} does not exist.")
        
        for key, value in dto.items():
            setattr(version, key, value)
        
        db.session.commit()

    def delete_version(self, version_id: int) -> None:
        version = self.get_version(version_id)
        if not version:
            raise ValueError(f"Version with ID {version_id} does not exist.")
        
        db.session.delete(version)
        db.session.commit()

    def get_all_versions(self) -> List[Version]:
        return db.session.query(Version).all()