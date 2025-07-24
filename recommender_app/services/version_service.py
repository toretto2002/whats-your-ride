from recommender_app.repositories.version_repository_impl import VersionRepositoryImpl
from recommender_app.models.version import Version
from recommender_app.schemas.version_dto import VersionCreate, VersionOut

class VersionService:

    def __init__(self):
        self.version_repository = VersionRepositoryImpl()

    def create_version(self, version: Version) -> int:
        return self.version_repository.create_version(version)

    def get_version_by_id(self, version_id: int) -> VersionOut:
        return self.version_repository.get_by_id(version_id)

    def update_version(self, version_id: int, version_update: VersionCreate) -> VersionOut:
        return self.version_repository.update(version_id, version_update)

    def delete_version(self, version_id: int) -> None:
        return self.version_repository.delete(version_id)

    def list_versions(self) -> list[VersionOut]:
        return self.version_repository.list_all()