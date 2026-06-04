#!/usr/bin/env python3
"""Write Serena global config with external .serena storage.

Mount this script into the container and run it before 'serena project create'.
Sets project_serena_folder_location so .serena data lives outside project dirs,
allowing read-only (:ro) mounts for the source repositories.
"""
import os

CONFIG_PATH = "/workspaces/serena/config/serena_config.yml"

def main():
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    # $projectFolderName is a Serena placeholder — written literally to the file.
    # Serena expands it per-project at runtime.
    config = (
        "# Serena global configuration\n"
        "# Project metadata stored externally to allow read-only repo mounts\n"
        'project_serena_folder_location: "/workspaces/serena/config/projects/$projectFolderName/.serena"\n'
        "\n"
        "# Registered projects (populated at startup)\n"
        "projects: []\n"
    )
    with open(CONFIG_PATH, "w") as f:
        f.write(config)
    print(f"Config written to {CONFIG_PATH}")
    print(f"  project_serena_folder_location: /workspaces/serena/config/projects/$projectFolderName/.serena")

if __name__ == "__main__":
    main()
