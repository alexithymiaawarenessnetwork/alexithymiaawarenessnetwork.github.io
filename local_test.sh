#!/bin/bash

# Local Test Script for Alexithymia Awareness Network
# This script builds the site and starts a local development server.
# Usage: ./local_test.sh [starting_port]

set -u

START_PORT="${1:-${PORT:-8000}}"
MAX_ATTEMPTS=20
HOST="127.0.0.1"
READY_PATH="/treatment/"
READY_MARKER="Alexithymia Awareness Network"

if ! [[ "$START_PORT" =~ ^[0-9]+$ ]] || [ "$START_PORT" -lt 1 ] || [ "$START_PORT" -gt 65535 ]; then
    echo "❌ Invalid port: $START_PORT"
    echo "💡 Usage: ./local_test.sh [starting_port]"
    exit 1
fi

echo "🚀 Starting local development server for AAN site..."
echo "📁 Changing to aan directory..."

cd aan || exit 1

echo "🔧 Building site with current configuration..."
if mkdocs build; then
    echo "✅ Build successful!"
    echo "🌐 Starting development server..."
    echo ""
    echo "💡 Tips:"
    echo "   - The server will auto-reload when you make changes"
    echo "   - Press Ctrl+C to stop the server"
    echo "   - Check browser developer tools to verify GTM is loading"
    echo ""
    echo "🔍 To verify Google Analytics:"
    echo "   1. Open browser developer tools (F12)"
    echo "   2. Go to Network tab"
    echo "   3. Look for requests to googletagmanager.com"
    echo "   4. Check Console for any GTM-related messages"
    echo ""

    attempt=0
    while [ "$attempt" -lt "$MAX_ATTEMPTS" ]; do
        PORT_TO_TRY=$((START_PORT + attempt))
        if [ "$PORT_TO_TRY" -gt 65535 ]; then
            break
        fi

        if lsof -nP -iTCP:"$PORT_TO_TRY" -sTCP:LISTEN >/dev/null 2>&1; then
            echo "⚠️  Port $PORT_TO_TRY is already busy before start. Trying the next port..."
            echo ""
            attempt=$((attempt + 1))
            continue
        fi

        echo "📋 Attempt $((attempt + 1))/$MAX_ATTEMPTS: starting server at http://$HOST:$PORT_TO_TRY"
        echo ""

        log_file="$(mktemp)"
        mkdocs serve -a "$HOST:$PORT_TO_TRY" > >(tee "$log_file") 2>&1 &
        server_pid=$!

        ready=0
        for _ in $(seq 1 50); do
            if ! kill -0 "$server_pid" 2>/dev/null; then
                break
            fi

            if curl -fsS --max-time 1 "http://$HOST:$PORT_TO_TRY$READY_PATH" 2>/dev/null | grep -q "$READY_MARKER"; then
                ready=1
                break
            fi

            sleep 0.2
        done

        if [ "$ready" -eq 1 ]; then
            echo "READY: http://$HOST:$PORT_TO_TRY$READY_PATH"
            wait "$server_pid"
            status=$?
        else
            wait "$server_pid"
            status=$?
        fi

        if [ "$status" -eq 0 ]; then
            rm -f "$log_file"
            exit 0
        fi

        if grep -qiE 'Address already in use|\[Errno 48\]|port .* in use|OSError: \[Errno 48\]' "$log_file"; then
            echo "⚠️  Port $PORT_TO_TRY became busy during startup. Trying the next port..."
            echo ""
            rm -f "$log_file"
            attempt=$((attempt + 1))
            continue
        fi

        echo "❌ Development server exited with an unexpected error on port $PORT_TO_TRY."
        rm -f "$log_file"
        exit "$status"
    done

    echo "❌ Unable to start mkdocs serve after $MAX_ATTEMPTS attempts beginning at port $START_PORT."
    exit 1
else
    echo "❌ Build failed! Please check the errors above."
    echo "💡 Common issues:"
    echo "   - Check mkdocs.yml syntax"
    echo "   - Verify all referenced files exist"
    echo "   - Ensure theme files are properly formatted"
    exit 1
fi
