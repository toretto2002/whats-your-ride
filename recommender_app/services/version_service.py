from recommender_app.repositories.version_repository_impl import VersionRepositoryImpl
from recommender_app.models.version import Version

class VersionService:

    def __init__(self):
        self.version_repository = VersionRepositoryImpl()

    def create_version(self, version: Version) -> Version:
        return self.version_repository.create(version)

    def get_version_by_id(self, version_id: int) -> Version:
        return self.version_repository.get_by_id(version_id)

    def update_version(self, version_id: int, version_update: dict) -> Version:
        return self.version_repository.update(version_id, version_update)

    def delete_version(self, version_id: int) -> None:
        return self.version_repository.delete(version_id)

    def list_versions(self) -> list[Version]:
        return self.version_repository.list_all()