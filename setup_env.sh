#!/usr/bin/env bash
# setup_env.sh  –  create `.old_env` running on Python 3.10 and install mpqp 0.2.2
# Usage:  bash setup_old_env.sh
# This is a temporary fix for an issue concerning the simulation of
# controlled custom unitary gates using the qiskit-aer simulator
set -euo pipefail

# ─────────────────────────────── settings ──────────────────────────────
PY_SHORT="3.10"         # major.minor we require
PY_FULL="3.10.14"       # exact version to install with pyenv if missing
VENV_DIR=".old_env"

# ───────────────────── locate or install Python 3.10 ───────────────────
if command -v "python${PY_SHORT}" >/dev/null 2>&1 ; then
    PY_BIN="$(command -v python${PY_SHORT})"
    echo "[+] Found system interpreter: $PY_BIN"
else
    echo "[!] python${PY_SHORT} not found on PATH."

    if command -v pyenv >/dev/null 2>&1 ; then
        echo "[+] Using pyenv to provide Python ${PY_FULL} …"
        # Ensure pyenv’s shims are on PATH for this script
        export PATH="$(pyenv root)/shims:$PATH"

        # Install if absent (-s = skip if already there)
        pyenv install -s "${PY_FULL}"
        PY_BIN="$(pyenv root)/versions/${PY_FULL}/bin/python${PY_SHORT}"
    else
        cat <<EOF >&2
ERROR: No suitable Python ${PY_SHORT} interpreter found and 'pyenv' is not installed.
       Install Python ${PY_SHORT} (e.g. via your package manager, Homebrew,
       the official installer, or by installing pyenv) and re-run this script.
EOF
        exit 1
    fi
fi

echo "[+] Using interpreter: $PY_BIN"

# ─────────────────────────── create venv ───────────────────────────────
"$PY_BIN" -m pip install --quiet --upgrade pip virtualenv
"$PY_BIN" -m virtualenv "$VENV_DIR"
echo "[+] Virtual environment created at ./${VENV_DIR}"

# ────────────────────────── install packages ───────────────────────────
source "${VENV_DIR}/bin/activate"
pip install "mpqp==0.2.2"
echo "[+] mpqp 0.2.2 installed in ${VENV_DIR}"

echo
echo "Done!  Activate the environment with:"
echo "    source ${VENV_DIR}/bin/activate"
