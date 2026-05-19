#!/usr/bin/env bash

# AAN Site Deployment Script (gh-based)
# -----------------------------------------------------------------------------
# Alternative to deploy.sh. Uses the GitHub CLI (`gh`) for auth verification
# and routes the push through HTTPS so gh's credential helper handles
# authentication. Verifies that the active gh account can push to the AAN
# repo before doing anything destructive; if it can't, scans other
# logged-in gh accounts and offers to switch to one that can.
#
# Usage: ./deploy-gh.sh [options] "commit message"
#   -f, --fast    Skip local review server and deploy immediately
#   -h, --help    Show this help message

set -euo pipefail

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
REPO="alexithymiaawarenessnetwork/alexithymiaawarenessnetwork.github.io"
BRANCH="main"

# -----------------------------------------------------------------------------
# Output helpers
# -----------------------------------------------------------------------------
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'
info()   { echo -e "${BLUE}[INFO]${NC} $*"; }
ok()     { echo -e "${GREEN}[OK]${NC} $*"; }
warn()   { echo -e "${YELLOW}[WARN]${NC} $*"; }
err()    { echo -e "${RED}[ERROR]${NC} $*" >&2; }
review() { echo -e "${CYAN}[REVIEW]${NC} $*"; }

show_help() {
  cat <<'EOF'
AAN Site Deployment Script (gh-based)

Usage: ./deploy-gh.sh [options] "commit message"

Options:
  -f, --fast    Skip local review server and deploy immediately
  -h, --help    Show this help message

What it does, in order:
  1. Verifies the GitHub CLI (gh) is installed and an account is logged in.
  2. Confirms the currently-active gh account has push access to the AAN
     repo. If not, scans your other logged-in accounts (using per-account
     tokens, without changing your active account silently), and offers to
     switch to one that has push access.
  3. Ensures origin uses HTTPS so gh's credential helper handles auth.
     One-shot: if origin is already HTTPS, this is a no-op.
  4. Fetches origin and aborts if local main has diverged.
  5. Builds the MkDocs site with --strict (fails on broken links).
  6. Starts a local preview server for review (skip with -f).
  7. Shows what 'git add .' would stage, then commits and pushes.
EOF
}

# -----------------------------------------------------------------------------
# Arg parsing
# -----------------------------------------------------------------------------
FAST=false
COMMIT_MSG=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -f|--fast) FAST=true; shift ;;
    -h|--help) show_help; exit 0 ;;
    -*) err "Unknown option: $1"; show_help; exit 1 ;;
    *)  COMMIT_MSG="$1"; shift ;;
  esac
done
if [[ -z "$COMMIT_MSG" ]]; then
  COMMIT_MSG="Rebuild site - $(date '+%Y-%m-%d %H:%M:%S')"
fi

# -----------------------------------------------------------------------------
# Preflight: cwd + tools + branch
# -----------------------------------------------------------------------------
[[ -f aan/mkdocs.yml ]] || { err "Run this from the repo root (aan/mkdocs.yml not found)."; exit 1; }
command -v gh     >/dev/null 2>&1 || { err "GitHub CLI (gh) is not installed. https://cli.github.com/"; exit 1; }
command -v mkdocs >/dev/null 2>&1 || { err "MkDocs is not installed. Try: pip install -r requirements.txt"; exit 1; }

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" != "$BRANCH" ]]; then
  warn "You are on branch '$CURRENT_BRANCH', not '$BRANCH'."
  read -rp "Continue and push to '$BRANCH' anyway? (y/n) " yn
  [[ "$yn" =~ ^[Yy]$ ]] || { info "Aborted."; exit 0; }
fi

# -----------------------------------------------------------------------------
# gh auth verification
# -----------------------------------------------------------------------------
info "Checking GitHub CLI authentication..."
if ! gh auth status >/dev/null 2>&1; then
  err "No gh accounts are logged in. Run: gh auth login"
  exit 1
fi

ACTIVE_LOGIN=$(gh api user --jq .login 2>/dev/null || true)
if [[ -z "$ACTIVE_LOGIN" ]]; then
  err "Could not determine active gh account. Run: gh auth status"
  exit 1
fi
info "Active gh account: $ACTIVE_LOGIN"

# Returns "true"/"false" for whether a given gh-logged-in account can push.
# If $1 is empty, queries with the currently-active account (no token override).
check_push_perm() {
  local login="${1:-}"
  if [[ -z "$login" ]]; then
    gh api "repos/$REPO" --jq '.permissions.push // false' 2>/dev/null || echo false
  else
    local token
    token=$(gh auth token --user "$login" 2>/dev/null || true)
    [[ -z "$token" ]] && { echo false; return; }
    GH_TOKEN="$token" gh api "repos/$REPO" --jq '.permissions.push // false' 2>/dev/null || echo false
  fi
}

ACTIVE_CAN_PUSH=$(check_push_perm "")
if [[ "$ACTIVE_CAN_PUSH" != "true" ]]; then
  warn "$ACTIVE_LOGIN does NOT have push access to $REPO."
  info "Scanning other logged-in gh accounts..."

  # Parse other logged-in usernames from `gh auth status`. Recent gh versions
  # emit lines like: "  - Logged in to github.com account <login> (<source>)"
  OTHER_LOGINS=$(gh auth status 2>&1 \
    | awk '/Logged in to github\.com account/ {print $(NF-1)}' \
    | sort -u \
    | grep -v "^$ACTIVE_LOGIN$" || true)

  CANDIDATE=""
  for login in $OTHER_LOGINS; do
    info "  testing $login..."
    if [[ "$(check_push_perm "$login")" == "true" ]]; then
      CANDIDATE="$login"
      break
    fi
  done

  if [[ -z "$CANDIDATE" ]]; then
    err "None of your logged-in gh accounts can push to $REPO."
    err "Run: gh auth login   (and pick the account that owns/can-push to this repo)"
    exit 1
  fi

  warn "Found candidate with push access: $CANDIDATE"
  read -rp "Switch active gh account from '$ACTIVE_LOGIN' to '$CANDIDATE'? (y/n) " yn
  if [[ "$yn" =~ ^[Yy]$ ]]; then
    gh auth switch -u "$CANDIDATE" -h github.com
    ACTIVE_LOGIN="$CANDIDATE"
    info "Note: active gh account is now '$ACTIVE_LOGIN'. To switch back later:"
    info "      gh auth switch -u <previous-login>"
  else
    err "Aborted. Manually run: gh auth switch -u $CANDIDATE"
    exit 1
  fi
fi
ok "Push access confirmed: $ACTIVE_LOGIN -> $REPO"

# -----------------------------------------------------------------------------
# Ensure origin uses HTTPS so gh's credential helper handles auth
# -----------------------------------------------------------------------------
REMOTE_URL=$(git remote get-url origin)
if [[ "$REMOTE_URL" =~ ^git@ ]] || [[ "$REMOTE_URL" =~ ^ssh:// ]]; then
  warn "origin is currently SSH: $REMOTE_URL"
  info "Switching origin to HTTPS and configuring gh credential helper..."
  git remote set-url origin "https://github.com/$REPO.git"
  gh auth setup-git
  ok "origin is now https://github.com/$REPO.git (gh handles auth)."
else
  info "origin already uses HTTPS: $REMOTE_URL"
fi

# -----------------------------------------------------------------------------
# Fetch + ahead/behind check
# -----------------------------------------------------------------------------
info "Fetching origin/$BRANCH..."
git fetch --quiet origin "$BRANCH"
LOCAL_SHA=$(git rev-parse "$BRANCH")
REMOTE_SHA=$(git rev-parse "origin/$BRANCH")
BASE_SHA=$(git merge-base "$BRANCH" "origin/$BRANCH")

if [[ "$LOCAL_SHA" == "$REMOTE_SHA" ]]; then
  info "Local $BRANCH is in sync with origin/$BRANCH."
elif [[ "$LOCAL_SHA" == "$BASE_SHA" ]]; then
  err "Local $BRANCH is BEHIND origin/$BRANCH. Pull before deploying:  git pull --ff-only"
  exit 1
elif [[ "$REMOTE_SHA" == "$BASE_SHA" ]]; then
  AHEAD=$(git rev-list --count "origin/$BRANCH..$BRANCH")
  warn "Local $BRANCH is ahead of origin by $AHEAD commit(s) — they will go up with this push."
else
  err "Local $BRANCH has DIVERGED from origin/$BRANCH. Reconcile manually (rebase/merge) before deploying."
  exit 1
fi

# -----------------------------------------------------------------------------
# Build (strict)
# -----------------------------------------------------------------------------
info "Building MkDocs site (--strict --clean)..."
( cd aan && mkdocs build --strict --clean )
ok "Build OK."

# -----------------------------------------------------------------------------
# Anything to deploy?
# -----------------------------------------------------------------------------
if [[ -z "$(git status --porcelain)" ]]; then
  warn "No changes detected. Nothing to deploy."
  exit 0
fi

info "Files that would be staged by 'git add .':"
git status --short
echo ""

# -----------------------------------------------------------------------------
# Local review (skippable with -f) — with proper cleanup trap
# -----------------------------------------------------------------------------
SERVER_PID=""
cleanup() {
  if [[ -n "$SERVER_PID" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
    review "Stopping local server (pid $SERVER_PID)..."
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

if [[ "$FAST" = false ]]; then
  PORT=8000
  while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
    PORT=$((PORT + 1))
  done
  review "Starting local preview on port $PORT..."
  ( cd aan && mkdocs serve --dev-addr=127.0.0.1:$PORT ) >/dev/null 2>&1 &
  SERVER_PID=$!
  sleep 2

  LOCAL_URL="http://127.0.0.1:$PORT"
  review "Opening $LOCAL_URL"
  if   command -v open     >/dev/null 2>&1; then open "$LOCAL_URL"     2>/dev/null || true
  elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$LOCAL_URL" 2>/dev/null || true
  else review "Open manually: $LOCAL_URL"
  fi

  echo ""
  while true; do
    read -rp "$(echo -e "${CYAN}[REVIEW]${NC} Deploy these changes to production? (y/n): ")" yn
    case "$yn" in
      [Yy]*) ok "Proceeding with deployment..."; break ;;
      [Nn]*) warn "Deployment cancelled by user."; exit 0 ;;
      *)     echo "Please answer y or n." ;;
    esac
  done
fi

# -----------------------------------------------------------------------------
# Stage / commit / push
# -----------------------------------------------------------------------------
info "Staging changes..."
git add .

info "Committing..."
git commit -m "$COMMIT_MSG"

info "Pushing to origin/$BRANCH via gh-authenticated HTTPS..."
git push origin "$BRANCH"

ok "Deployed."
ok "Site: https://alexithymiaawarenessnetwork.org"
info "GitHub Pages may take a minute or two to refresh."
