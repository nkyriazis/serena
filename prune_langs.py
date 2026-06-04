#!/usr/bin/env python3
"""Prune languages without runtimes from a Serena project.yml.

After Serena auto-detects languages (via `yes y | serena project create`),
this removes languages that need external runtimes not present in the
container (powershell, elixir, haskell, matlab, etc.).

Usage: prune_langs.py <project.yml>
"""
import re
import sys

# Languages that need external runtimes not in the Serena image.
# Serena will try to start their LSP servers and fail with errors.
NO_RUNTIME = frozenset({
    "powershell", "elixir", "haskell", "matlab", "msl", "bsl",
    "ada", "gdscript", "pascal", "lean4", "groovy",
    "clojure", "erlang", "ocaml", "fsharp", "al", "rego",
    "fortran", "haxe", "crystal", "cue", "nix", "luau",
    "julia", "perl", "r", "swift", "scala", "ruby", "dart",
    "php", "csharp", "java", "kotlin", "cpp_ccls", "typescript_vts",
    "python_jedi", "python_ty", "csharp_omnisharp", "ruby_solargraph",
    "php_phpactor", "hlsl", "systemverilog", "solidity", "ansible",
    "angular",
})


def prune(yml_path: str) -> None:
    with open(yml_path) as f:
        content = f.read()

    # Match the languages list: languages: {python, powershell, typescript, ...}
    m = re.search(r"(languages:\s*\{)([^}]+)(\})", content)
    if not m:
        return

    langs = {l.strip() for l in m.group(2).split(",") if l.strip()}
    kept = langs - NO_RUNTIME

    if kept == langs:
        return  # Nothing to prune

    with open(yml_path, "w") as f:
        f.write(m.group(1) + ", ".join(sorted(kept)) + m.group(3))


if __name__ == "__main__":
    prune(sys.argv[1])
