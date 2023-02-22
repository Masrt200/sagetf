#!/bin/bash

set -euxo pipefail

CTF_DIR="/home/ctf"
CHALLENGE_DIR="/challenge"
MAIN_PY="main.py"
MODULE_PY="echo.py"
CTF_USER="ctf"
CTF_CRACKED_USER="ctf-cracked"

reset_file () {
  file="${1}"
  if [ -e "${CTF_DIR}/${file}" ] && [ -L "${CTF_DIR}/${file}" ] || ! [ -f "${CTF_DIR}/${file}" ]; then
    rm -rf "${CTF_DIR}/${file}"
  fi
  if ! [ -e "${CTF_DIR}/${file}" ]; then
    touch "${CTF_DIR}/${file}"
  fi
  if ! diff --no-dereference "${CHALLENGE_DIR}/${file}" "${CTF_DIR}/${file}"; then
    rm -rf "${CTF_DIR}/${file}"
    cp "${CHALLENGE_DIR}/${file}" "${CTF_DIR}/${file}"
  fi
  chmod 644 "${CTF_DIR}/${file}"
}

reset_challenge () {
  reset_file "${MAIN_PY}"
  reset_file "${MODULE_PY}"
}

string="${1}"

chown -R "root:root" "${CTF_DIR}"
chmod 755 "${CTF_DIR}"
reset_challenge
chmod +x "${CTF_DIR}/${MAIN_PY}"
diff --no-dereference "${CHALLENGE_DIR}/${MAIN_PY}" "${CTF_DIR}/${MAIN_PY}"
diff --no-dereference "${CHALLENGE_DIR}/${MODULE_PY}" "${CTF_DIR}/${MODULE_PY}"
sudo -u "${CTF_CRACKED_USER}" "${CTF_DIR}/${MAIN_PY}" "${string}"
chown -R "${CTF_USER}:${CTF_USER}" "${CTF_DIR}"
