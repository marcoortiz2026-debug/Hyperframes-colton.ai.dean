#!/bin/bash
# Reinstalls the video toolchain in fresh Claude Code cloud containers.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# Node's built-in fetch ignores HTTPS_PROXY unless told otherwise; hyperframes
# uses it for model downloads (Parakeet, Whisper fallback).
export NODE_USE_ENV_PROXY=1
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export NODE_USE_ENV_PROXY=1" >> "$CLAUDE_ENV_FILE"
fi

# Workspace deps: Playwright, local GSAP + Inter (CDNs may be blocked in the sandbox)
npm install --no-audit --no-fund

# yt-dlp for /study-creator; Kokoro for local TTS
pip install -q --disable-pip-version-check yt-dlp kokoro-onnx soundfile

# Chrome Headless Shell for rendering (no-op when already cached)
npx --yes hyperframes browser ensure

# whisper-cli for transcription. Hyperframes' own auto-build is skipped in the sandbox,
# so build it here into the path the CLI already checks
# (~/.cache/hyperframes/whisper/whisper.cpp/build/bin). Runs in the background
# (several minutes) so it never delays session start; log in build.log.
WHISPER_DIR="$HOME/.cache/hyperframes/whisper/whisper.cpp"
if ! command -v whisper-cli >/dev/null && [ ! -x "$WHISPER_DIR/build/bin/whisper-cli" ]; then
  mkdir -p "$HOME/.cache/hyperframes/whisper"
  nohup bash -c "
    [ -d '$WHISPER_DIR/.git' ] || git clone --depth 1 https://github.com/ggml-org/whisper.cpp '$WHISPER_DIR'
    cmake -S '$WHISPER_DIR' -B '$WHISPER_DIR/build' -DCMAKE_BUILD_TYPE=Release -DWHISPER_BUILD_TESTS=OFF
    cmake --build '$WHISPER_DIR/build' -j\$(nproc) --config Release --target whisper-cli
  " >"$HOME/.cache/hyperframes/whisper/build.log" 2>&1 &
fi

# Whisper model for transcription — only succeeds once huggingface.co is allowed
# by the environment's network policy; never blocks session start.
if [ ! -s "$HOME/.cache/hyperframes/whisper/models/ggml-small.en.bin" ]; then
  curl -fsSL -m 300 -o "$HOME/.cache/hyperframes/whisper/models/ggml-small.en.bin.tmp" --create-dirs \
    https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin \
    && mv "$HOME/.cache/hyperframes/whisper/models/ggml-small.en.bin.tmp" "$HOME/.cache/hyperframes/whisper/models/ggml-small.en.bin" \
    || echo "session-start: Whisper model download skipped (huggingface.co not reachable)" >&2
fi

# Parakeet ASR (~640 MB): accurate word start times, used by scripts/detect-edits.py
# for rough cuts. Background so session start isn't delayed; no-op once installed.
nohup npx --yes hyperframes models install parakeet \
  >"$HOME/.cache/hyperframes/parakeet-install.log" 2>&1 &
