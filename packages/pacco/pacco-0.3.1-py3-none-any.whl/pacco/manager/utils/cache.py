import os
from pathlib import Path

from typing import Dict

from pacco.manager.utils.clients import LocalClient


class Cache:
    def __init__(self, clean=False):
        self.client = LocalClient(os.path.join(str(Path.home()), '.pacco_cache'), clean=clean)

    @staticmethod
    def __serialize(registry_name: str, assignment: Dict[str, str]):
        assignment['__pacco_registry_name'] = registry_name
        sorted_assignment_tuple = sorted(assignment.items(), key=lambda x: x[0])
        zipped_assignment = ['='.join(pair) for pair in sorted_assignment_tuple]
        return '=='.join(zipped_assignment)

    def download_from_cache(self, registry_name: str, assignment: Dict[str, str], download_path: str) -> bool:
        dir_name = Cache.__serialize(registry_name, assignment)
        if dir_name in self.client.ls():
            self.client.dispatch_subdir(dir_name).download_dir(download_path)
            return True
        else:
            return False

    def upload_to_cache(self, registry_name: str, assignment: Dict[str, str], source_path: str) -> None:
        dir_name = Cache.__serialize(registry_name, assignment)
        os.makedirs(dir_name, exist_ok=True)
        self.client.dispatch_subdir(dir_name).upload_dir(source_path)

    def get_path(self, registry_name: str, assignment: Dict[str, str]) -> str:
        dir_name = Cache.__serialize(registry_name, assignment)
        if dir_name in self.client.ls():
            return self.client.dispatch_subdir(dir_name).bin_dir_for_cache
        raise ValueError("No cache found")
