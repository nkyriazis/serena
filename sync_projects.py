#!/usr/bin/env python3
"""Sync global config projects list to match actually mounted repos.

Source of truth is /workspace/*/ (what compose mounts), NOT the persistent
config volume which may have stale entries from previous runs.

Serena expects absolute paths in the projects list, not bare names.
"""
import os

import yaml

CONFIG_PATH = "/workspaces/serena/config/serena_config.yml"
WORKSPACE_DIR = "/workspace"


def main():
    with open(CONFIG_PATH) as f:
        cfg = yaml.safe_load(f) or {}

    # What's actually mounted right now (as absolute paths)
    mounted_paths = {
        os.path.join(WORKSPACE_DIR, d)
        for d in os.listdir(WORKSPACE_DIR)
        if os.path.isdir(os.path.join(WORKSPACE_DIR, d))
    }

    # What the config currently says
    registered = set(cfg.get("projects", []) or [])

    # Add newly mounted projects
    for path in sorted(mounted_paths - registered):
        print(f"  >> Adding {path} to global projects list")

    # Remove unmounted projects
    for path in sorted(registered - mounted_paths):
        print(f"  >> Removing {path} from global projects list (no longer mounted)")

    cfg["projects"] = sorted(mounted_paths)

    with open(CONFIG_PATH, "w") as f:
        yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)

    print(f"  [{len(mounted_paths)} projects in global config]")


if __name__ == "__main__":
    main()
