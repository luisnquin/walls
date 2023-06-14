#!/usr/bin/env python
"""Generate README files for all project folders."""

from typing import List
from os import walk, getenv, path


target_folders: List[str] = ['desktop']
raw_gh_user_content_url: str = 'https://raw.githubusercontent.com'


def main():
    repo_name = must_env('GITHUB_REPO_NAME')
    repo_owner = must_env('GITHUB_REPO_OWNER')
    repo_branch = must_env('GITHUB_REPO_BRANCH')

    for folder_path in target_folders:
        for subfolder_info in walk(folder_path):
            subfolder_path = subfolder_info[0]
            subfolder_files = subfolder_info[2]

            if subfolder_path == folder_path:
                continue

            folder_info = get_folder_info(
                repo_owner, repo_name, repo_branch, subfolder_path, subfolder_files)

            generate_readme_for_subfolder(folder_info)


class FolderInfo:
    """A class that represents information about a folder."""

    path: str
    url_files: List[str]

    def __init__(self, folder_path: str) -> None:
        self.url_files = []
        self.path = folder_path


def generate_readme_for_subfolder(folder_info: FolderInfo):
    readme_file_path = '/'.join(['.', folder_info.path, 'README.md'])

    with open(readme_file_path, '+w', encoding='utf-8') as file:
        file.write('# HEADER\n')

        for file_url in folder_info.url_files:
            file_name_no_ext = path.splitext(path.basename(file_url))[0]
            image = f'![{file_name_no_ext}]({file_url})\n'

            file.write(image)


def get_folder_info(repo_owner: str, repo_name: str, repo_branch: str,
                    subdirectory_path: str, subdirectory_files: List[str]) -> FolderInfo:
    folder_info = FolderInfo(subdirectory_path)

    for file_name in subdirectory_files:
        if file_name == 'README.md':
            continue

        file_url = '/'.join([raw_gh_user_content_url, repo_owner,
                            repo_name, repo_branch, subdirectory_path, file_name])

        folder_info.url_files.append(file_url)

    return folder_info


class EnvironmentVariableError(Exception):
    """Exception raised for errors related to environment variables."""

    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message
        super().__init__(self.message)


def must_env(name) -> str:
    """Retrieve the value of an environment variable."""

    value = getenv(name)

    match value:
        case None:
            raise EnvironmentVariableError(
                name, f'Environment variable {name} is not set')
        case '':
            raise EnvironmentVariableError(
                name, f'Environment variable {name} is not set')

    return value


if __name__ == '__main__':
    main()
