"""
Forgix UI Generator — random aesthetic theme engine.

10 visual personalities, selected randomly each boot.
Seed is NOT persisted — you never know what you'll get.
"""
from __future__ import annotations

import random
from typing import Any

THEMES: list[dict[str, Any]] = [
    {
        "id": "brutalist_terminal",
        "name": "Brutalist Terminal",
        "vibe": "Hacker / matrix",
        "bg": "#0a0a0a", "surface": "#111", "accent": "#00ff41", "accent2": "#00cc33",
        "text": "#00ff41", "muted": "#005c17", "border": "#00ff41",
        "font": "'Courier New', monospace",
        "radius": "0px",
        "shadow": "0 0 10px #00ff4133",
        "send_label": "EXECUTE",
        "placeholder": "enter command...",
        "animation": "@keyframes blink { 50% { opacity: 0; } } .cursor { animation: blink 1s step-end infinite; }",
    },
    {
        "id": "pastel_dreamcore",
        "name": "Pastel Dreamcore",
        "vibe": "Soft / ethereal",
        "bg": "#fdf0ff", "surface": "#fff5fe", "accent": "#c77dff", "accent2": "#9b5de5",
        "text": "#4a3560", "muted": "#b89ec4", "border": "#e0b8ff",
        "font": "Georgia, 'Times New Roman', serif",
        "radius": "20px",
        "shadow": "0 4px 24px #c77dff22",
        "send_label": "✨ send",
        "placeholder": "whisper something...",
        "animation": "",
    },
    {
        "id": "retro_neon_arcade",
        "name": "Retro Neon Arcade",
        "vibe": "Synthwave / CRT",
        "bg": "#0d0221", "surface": "#160835", "accent": "#ff006e", "accent2": "#8338ec",
        "text": "#f8f8f2", "muted": "#6272a4", "border": "#ff006e",
        "font": "'Courier New', monospace",
        "radius": "4px",
        "shadow": "0 0 20px #ff006e55, 0 0 40px #8338ec33",
        "send_label": "INSERT COIN",
        "placeholder": "press start...",
        "animation": "@keyframes scanline { 0%,100%{opacity:.03} 50%{opacity:.08} } body::after{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.1) 2px,rgba(0,0,0,.1) 4px);pointer-events:none;animation:scanline 8s linear infinite;}",
    },
    {
        "id": "corporate_minimalist",
        "name": "Corporate Minimalist",
        "vibe": "Clean / professional",
        "bg": "#f5f7fa", "surface": "#ffffff", "accent": "#2563eb", "accent2": "#1d4ed8",
        "text": "#1e293b", "muted": "#94a3b8", "border": "#e2e8f0",
        "font": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "radius": "8px",
        "shadow": "0 1px 3px rgba(0,0,0,.1)",
        "send_label": "Send",
        "placeholder": "Message Forgix...",
        "animation": "",
    },
    {
        "id": "cottagecore",
        "name": "Cottagecore",
        "vibe": "Warm / organic",
        "bg": "#fdf6ec", "surface": "#fffaf3", "accent": "#7c6d4f", "accent2": "#5c4e35",
        "text": "#3d2b1f", "muted": "#b0956d", "border": "#e8d5b0",
        "font": "Palatino, 'Book Antiqua', serif",
        "radius": "12px",
        "shadow": "0 2px 12px rgba(124,109,79,.15)",
        "send_label": "🌿 send",
        "placeholder": "What's on your mind, dear?",
        "animation": "",
    },
    {
        "id": "y2k_chrome",
        "name": "Y2K Chrome",
        "vibe": "Silver / early web",
        "bg": "#e8f0ff", "surface": "#f0f4ff", "accent": "#0033cc", "accent2": "#0022aa",
        "text": "#000066", "muted": "#6680cc", "border": "#aabbdd",
        "font": "Arial, Helvetica, sans-serif",
        "radius": "6px",
        "shadow": "inset 0 1px 0 rgba(255,255,255,.8), 0 2px 4px rgba(0,0,0,.2)",
        "send_label": ">> GO",
        "placeholder": "Type here [AOL style]",
        "animation": "",
    },
    {
        "id": "solarpunk",
        "name": "Solarpunk",
        "vibe": "Green / hopeful",
        "bg": "#f0fce8", "surface": "#f8fff2", "accent": "#2d7d32", "accent2": "#1b5e20",
        "text": "#1a3320", "muted": "#81c784", "border": "#a5d6a7",
        "font": "'Trebuchet MS', sans-serif",
        "radius": "16px",
        "shadow": "0 3px 16px rgba(45,125,50,.12)",
        "send_label": "☘️ grow",
        "placeholder": "Plant a thought...",
        "animation": "",
    },
    {
        "id": "deep_space",
        "name": "Deep Space",
        "vibe": "Navy / stellar",
        "bg": "#020b18", "surface": "#071428", "accent": "#4fc3f7", "accent2": "#0288d1",
        "text": "#e1f5fe", "muted": "#4a6fa5", "border": "#1a3a5c",
        "font": "Consolas, 'Lucida Console', monospace",
        "radius": "4px",
        "shadow": "0 0 30px rgba(79,195,247,.1)",
        "send_label": "▶ transmit",
        "placeholder": "Signal across the void...",
        "animation": "@keyframes twinkle{0%,100%{opacity:1}50%{opacity:.3}} .star{animation:twinkle var(--d,2s) infinite;}",
    },
    {
        "id": "vaporwave",
        "name": "Vaporwave",
        "vibe": "Magenta / nostalgia",
        "bg": "#1a0030", "surface": "#2d0050", "accent": "#ff71ce", "accent2": "#b967ff",
        "text": "#fffde7", "muted": "#7b5ea7", "border": "#ff71ce",
        "font": "'VT323', 'Courier New', monospace",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');",
        "radius": "0px",
        "shadow": "0 0 15px #ff71ce44, 0 0 30px #b967ff22",
        "send_label": "A E S T H E T I C",
        "placeholder": "Ｗｈａｔ ｄｏ ｙｏｕ Ｗａｎｔ Ｔｏ Ｓａｙ？",
        "animation": "",
    },
    {
        "id": "ancient_codex",
        "name": "Ancient Codex",
        "vibe": "Parchment / ink",
        "bg": "#f5f0e8", "surface": "#faf7f0", "accent": "#3d2b1f", "accent2": "#5c3d2e",
        "text": "#2c1a0e", "muted": "#8b7355", "border": "#c8b48a",
        "font": "'IM Fell English', Georgia, serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=IM+Fell+English&display=swap');",
        "radius": "2px",
        "shadow": "2px 2px 8px rgba(60,40,20,.2)",
        "send_label": "❧ Inscribe",
        "placeholder": "Write thy query here...",
        "animation": "",
    },
]

THEME_MAP = {t["id"]: t for t in THEMES}

_CHAT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Forgix — {{ persona_name }}</title>
<style>
{{ font_import }}
{{ animation }}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: {{ bg }};
  color: {{ text }};
  font-family: {{ font }};
  height: 100dvh;
  display: flex;
  flex-direction: column;
}
#header {
  padding: 12px 16px;
  border-bottom: 1px solid {{ border }};
  background: {{ surface }};
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.85em;
  color: {{ muted }};
}
#header strong { color: {{ accent }}; font-size: 1.1em; }
#messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.msg {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: {{ radius }};
  line-height: 1.5;
  word-break: break-word;
  box-shadow: {{ shadow }};
}
.msg.user {
  align-self: flex-end;
  background: {{ accent }};
  color: {{ bg }};
}
.msg.assistant {
  align-self: flex-start;
  background: {{ surface }};
  border: 1px solid {{ border }};
}
.msg.system { align-self: center; font-size: 0.8em; color: {{ muted }}; }
#input-area {
  padding: 12px 16px;
  border-top: 1px solid {{ border }};
  background: {{ surface }};
  display: flex;
  gap: 8px;
}
#input {
  flex: 1;
  background: {{ bg }};
  color: {{ text }};
  border: 1px solid {{ border }};
  border-radius: {{ radius }};
  padding: 10px 14px;
  font-family: {{ font }};
  font-size: 1em;
  outline: none;
  resize: none;
  min-height: 42px;
  max-height: 120px;
}
#input:focus { border-color: {{ accent }}; box-shadow: {{ shadow }}; }
#send-btn {
  background: {{ accent }};
  color: {{ bg }};
  border: none;
  border-radius: {{ radius }};
  padding: 10px 18px;
  font-family: {{ font }};
  font-size: 0.9em;
  cursor: pointer;
  white-space: nowrap;
}
#send-btn:hover { background: {{ accent2 }}; }
#send-btn:disabled { opacity: 0.5; cursor: not-allowed; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: {{ bg }}; }
::-webkit-scrollbar-thumb { background: {{ border }}; border-radius: 3px; }
</style>
</head>
<body>
<div id="header">
  <strong>FORGIX</strong>
  <span>{{ persona_name }} &bull; private &bull; local</span>
</div>
<div id="messages"></div>
<div id="input-area">
  <textarea id="input" placeholder="{{ placeholder }}" rows="1"></textarea>
  <button id="send-btn">{{ send_label }}</button>
</div>
<script>
const TOKEN = {{ token_json }};
const CSRF = {{ csrf_json }};
const CONV_ID = localStorage.getItem('forgix_conv') || null;
let ws, currentDiv, convId = CONV_ID;

function connect() {
  const proto = location.protocol === 'https:' ? 'wss' : 'ws';
  ws = new WebSocket(`${proto}://${location.host}/ws`);
  ws.onopen = () => {
    ws.send(JSON.stringify({token: TOKEN, csrf: CSRF, conversation_id: convId}));
  };
  ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    if (msg.type === 'ready') {
      convId = msg.conversation_id;
      localStorage.setItem('forgix_conv', convId);
    } else if (msg.type === 'start') {
      currentDiv = addMsg('assistant', '');
    } else if (msg.type === 'chunk') {
      if (currentDiv) { currentDiv.textContent += msg.content; scrollDown(); }
    } else if (msg.type === 'end') {
      currentDiv = null;
    } else if (msg.type === 'error') {
      addMsg('system', '⚠ ' + msg.message);
    }
  };
  ws.onclose = () => setTimeout(connect, 2000);
  ws.onerror = () => ws.close();
}

function addMsg(role, text) {
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  div.textContent = text;
  document.getElementById('messages').appendChild(div);
  scrollDown();
  return div;
}

function scrollDown() {
  const m = document.getElementById('messages');
  m.scrollTop = m.scrollHeight;
}

function send() {
  const inp = document.getElementById('input');
  const text = inp.value.trim();
  if (!text || !ws || ws.readyState !== 1) return;
  addMsg('user', text);
  ws.send(JSON.stringify({message: text}));
  inp.value = '';
  inp.style.height = 'auto';
  document.getElementById('send-btn').disabled = true;
  setTimeout(() => document.getElementById('send-btn').disabled = false, 500);
}

document.getElementById('send-btn').addEventListener('click', send);
document.getElementById('input').addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
});
document.getElementById('input').addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

connect();
</script>
</body>
</html>
""".strip()


class UIGenerator:
    def __init__(self, force: str | None = None):
        if force and force in THEME_MAP:
            self.current_theme = THEME_MAP[force]
        else:
            self.current_theme = random.choice(THEMES)

    def render_chat_page(self, token: str = "", csrf: str = "", persona_name: str = "Forgix") -> str:
        t = self.current_theme
        html = _CHAT_TEMPLATE
        # Safe substitution — replace placeholders
        replacements = {
            "{{ persona_name }}": persona_name,
            "{{ font_import }}": t.get("font_import", ""),
            "{{ animation }}": t.get("animation", ""),
            "{{ bg }}": t["bg"],
            "{{ surface }}": t["surface"],
            "{{ accent }}": t["accent"],
            "{{ accent2 }}": t["accent2"],
            "{{ text }}": t["text"],
            "{{ muted }}": t["muted"],
            "{{ border }}": t["border"],
            "{{ font }}": t["font"],
            "{{ radius }}": t["radius"],
            "{{ shadow }}": t["shadow"],
            "{{ send_label }}": t["send_label"],
            "{{ placeholder }}": t["placeholder"],
            "{{ token_json }}": json.dumps(token),
            "{{ csrf_json }}": json.dumps(csrf),
        }
        import json
        for k, v in replacements.items():
            html = html.replace(k, v)
        return html
