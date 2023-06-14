#!/usr/bin/env python

from typing import List
from os import walk, getenv, path, remove


target_folders: List[str] = ['desktop']
raw_gh_user_content_url: str = 'https://raw.githubusercontent.com'


def main():
    repo_name = must_env('GITHUB_REPO_NAME')
    repo_owner = must_env('GITHUB_REPO_OWNER')
    repo_branch = must_env('GITHUB_REPO_BRANCH')

    for folder_path in target_folders:
        for subdirectory_info in walk(folder_path):
            subdirectory_path = subdirectory_info[0]
            subdirectory_files = subdirectory_info[2]

            if subdirectory_path == folder_path:
                continue

            folder_info = get_folder_info(
                repo_owner, repo_name, repo_branch, subdirectory_path, subdirectory_files)

            readme_file_path = '/'.join(['.', folder_info.path, 'README.md'])

            with open(readme_file_path, '+w') as file:
                file.write('# HEADER\n')

                for file_url in folder_info.url_files:
                    image = '![{}]({})\n'.format(
                        path.basename(file_url), file_url)

                    file.write(image)


class FolderInfo:
    path: str
    url_files: List[str]

    def __init__(self, path) -> None:
        self.url_files = []
        self.path = path


def get_folder_info(repo_owner: str, repo_name: str, repo_branch: str, subdirectory_path: str, subdirectory_files: List[str]) -> FolderInfo:
    folder_info = FolderInfo(subdirectory_path)

    for file_name in subdirectory_files:
        if file_name == 'README.md':
            continue

        file_url = '/'.join([raw_gh_user_content_url, repo_owner,
                            repo_name, repo_branch, subdirectory_path, file_name])

        folder_info.url_files.append(file_url)

    return folder_info


def must_env(name) -> str:
    value = getenv(name)

    match value:
        case None:
            raise Exception(f'Environment variable {name} is not set')
        case '':
            raise Exception(f'Environment variable {name} is empty')

    return value


if __name__ == '__main__':
    main()
