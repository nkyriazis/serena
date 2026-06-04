#!/usr/bin/env python3
"""Detect project languages and emit --language flags for Serena.

Only returns languages that have runtimes available in the container.
Avoids languages like powershell, elixir, haskell, etc. that need
external binaries not present in the Serena image.
"""
import os
import sys
import subprocess
from pathlib import Path

# Languages Serena actually accepts via --language.
# Subset of those that work without extra runtime dependencies.
SAFE_LANGUAGES = frozenset({
    "python", "typescript", "bash", "json",
    "yaml", "markdown", "html", "toml",
    "vue", "svelte", "java", "c", "cpp", "go", "rust",
    "ruby", "php", "swift", "kotlin", "scala", "lua",
    "terraform", "zig", "r", "perl", "clojure", "dart",
    "crystal", "cue", "nix", "erlang", "ocaml", "fsharp",
    "rego", "julia", "fortran", "haskell", "haxe", "groovy",
    "angular", "scss", "ansible",
})

EXT_TO_LANG = {
    ".py": "python", ".pyi": "python",
    ".ts": "typescript", ".tsx": "typescript",
    # .js/.jsx -> no mapping; Serena has no 'javascript' language,
    # TypeScript LSP covers JS files when typescript is active
    ".sh": "bash", ".bash": "bash", ".zsh": "bash",
    ".json": "json", ".jsonc": "json",
    ".yml": "yaml", ".yaml": "yaml",
    ".md": "markdown",
    ".html": "html", ".htm": "html",
    ".scss": "scss", ".less": "scss",
    # .css -> no mapping (Serena has no 'css', only 'scss')
    ".toml": "toml",
    ".vue": "vue",
    ".svelte": "svelte",
    ".java": "java",
    ".c": "c", ".h": "c",
    ".cpp": "cpp", ".hpp": "cpp", ".cc": "cpp", ".cxx": "cpp",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin", ".kts": "kotlin",
    ".scala": "scala",
    ".lua": "lua",
    ".tf": "terraform", ".hcl": "terraform",
    ".zig": "zig",
    ".r": "r", ".R": "r",
    ".pl": "perl", ".pm": "perl",
    ".clj": "clojure", ".cljc": "clojure",
    ".dart": "dart",
    ".cr": "crystal",
    ".cue": "cue",
    ".nix": "nix",
    ".ex": "elixir", ".exs": "elixir",
    ".elm": "elm",
    ".fs": "fsharp", ".fsx": "fsharp",
    ".rs": "rust",
    ".jl": "julia",
    ".hs": "haskell",
    ".hx": "haxe",
    ".groovy": "groovy",
}

def detect(project_dir: str) -> list[str]:
    counts: dict[str, int] = {}
    skip_dirs = frozenset({
        "node_modules", "__pycache__", "dist", "build", ".git",
        ".venv", "venv", "env", ".env", ".tox", ".mypy_cache",
        ".next", ".nuxt", ".output", "storybook-static",
    })
    for root, dirs, files in os.walk(project_dir):
        # Prune walk to skip heavy directories
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in skip_dirs]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            lang = EXT_TO_LANG.get(ext)
            if lang:
                counts[lang] = counts.get(lang, 0) + 1

    # Filter to safe languages, return those with >0 files
    return [lang for lang, _ in sorted(counts.items(), key=lambda x: -x[1]) if lang in SAFE_LANGUAGES]


def main() -> None:
    project_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    langs = detect(project_dir)
    if not langs:
        # Fallback: let Serena auto-detect (it will prompt, but at least we
        # don't pass bad languages — the caller should handle this case)
        print("")
        return
    # Emit --language lang1 --language lang2 ...
    args = []
    for lang in langs:
        args.append(f"--language {lang}")
    print(" ".join(args))


if __name__ == "__main__":
    main()
