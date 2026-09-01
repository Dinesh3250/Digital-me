"""Styling constants for the digital twin Gradio app."""

GOLD = "#ecad0a"
BLUE = "#209dd7"
PURPLE = "#753991"

EXAMPLES = [
    "Tell me about your background and experience.",
    "What kinds of projects are you working on now?",
    "What are your strongest technical skills?",
    "How can I get in touch with you?",
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --twin-gold: #ecad0a;
  --twin-blue: #209dd7;
  --twin-purple: #753991;

  --twin-bg: #0b0b0e;
  --twin-surface: #141418;
  --twin-surface-2: #1b1b21;
  --twin-surface-3: #232329;
  --twin-border: #26262e;
  --twin-border-strong: #37373f;
  --twin-text: #f0f0f2;
  --twin-text-dim: #b8b8c2;
  --twin-muted: #7d7d87;
}

body:not(.dark) {
  --twin-bg: #f6f6f8;
  --twin-surface: #ffffff;
  --twin-surface-2: #f0f0f3;
  --twin-surface-3: #e8e8ec;
  --twin-border: #e0e0e6;
  --twin-border-strong: #c6c6d0;
  --twin-text: #17171b;
  --twin-text-dim: #46464f;
  --twin-muted: #7a7a84;
}

footer, .built-with, .show-api, .api-docs { display: none !important; }
html, body, gradio-app { background: var(--twin-bg) !important; }

/* ---------- Layout ---------- */
.gradio-container {
  background: var(--twin-bg) !important;
  color: var(--twin-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
  width: 100% !important;
  max-width: 760px !important;
  min-width: 0 !important;
  margin: 0 auto !important;
  padding: 56px 24px 48px !important;
}
.gradio-container .main, .gradio-container .contain, .gradio-container .wrap {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 0 !important;
}
.gradio-container * { min-width: 0; }

/* ---------- Header block ---------- */
.gradio-container h1 {
  color: var(--twin-text) !important;
  font-size: 32px !important;
  font-weight: 800 !important;
  letter-spacing: -0.02em !important;
  line-height: 1.15 !important;
  margin: 0 0 10px !important;
  text-align: left !important;
  position: relative;
  padding-left: 16px !important;
}
.gradio-container h1::before {
  content: "";
  position: absolute;
  left: 0; top: 3px; bottom: 3px;
  width: 3px;
  background: linear-gradient(180deg, var(--twin-gold), var(--twin-blue));
}

/* Description line under the title */
.gradio-container > .main > .wrap > .contain > div:first-child .prose,
.gradio-container .app > .prose {
  color: var(--twin-text-dim) !important;
  font-size: 15px !important;
  line-height: 1.6 !important;
  padding-left: 16px !important;
  margin: 0 0 32px !important;
  max-width: 52ch;
}

/* ---------- Sharp corners on structural pieces ---------- */
.chatbot, .chatbot *, .block, .form,
button, input, textarea,
.examples button {
  border-radius: 0 !important;
}

.block, .form { background: transparent !important; box-shadow: none !important; }

/* ---------- Hide the Chatbot label / header strip ---------- */
.chatbot > .block-label,
.chatbot > label,
.chatbot .label-wrap,
.chatbot .block-label,
.chatbot > .label-container {
  display: none !important;
}

/* ---------- Chatbot frame ---------- */
.chatbot, .chatbot.block {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  min-height: 440px !important;
  box-shadow: 0 1px 0 var(--twin-border), 0 12px 32px -20px rgba(0,0,0,0.6) !important;
}
.chatbot .placeholder, .chatbot .placeholder * { color: var(--twin-muted) !important; }

/* ---------- Message rows ---------- */
.message-row,
.message-row > div,
.message-row .role,
.message-wrap, .bubble-wrap {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  border: 0 !important;
  box-shadow: none !important;
  padding: 10px 14px !important;
  margin: 3px 0 !important;
}

/* ---------- Bubble backgrounds ---------- */
.message-row.user-row .message,
.message-row.user-row .message-bubble,
.message-row.user-row .bubble,
.message-row[data-role="user"] .message,
.message-row[data-role="user"] .message-bubble {
  background: var(--twin-blue) !important;
  color: #ffffff !important;
}

.message-row.bot-row .message,
.message-row.bot-row .message-bubble,
.message-row.bot-row .bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .message-bubble {
  background: var(--twin-surface-2) !important;
  color: var(--twin-text) !important;
  border-left: 2px solid var(--twin-purple) !important;
}

/* prevent stripe doubling on nested elements */
.message-row.bot-row .message .message,
.message-row.bot-row .message .bubble,
.message-row.bot-row .bubble .message,
.message-row.bot-row .bubble .bubble,
.message-row[data-role="assistant"] .message .message,
.message-row[data-role="assistant"] .bubble .bubble {
  border-left: 0 !important;
}

/* ---------- Metadata / titled blocks (e.g. Dinesh's direct replies) ---------- */
.message-row .metadata,
.message-row [class*="metadata"] {
  color: var(--twin-gold) !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  opacity: 0.9 !important;
  border-bottom: 1px solid var(--twin-border) !important;
  padding-bottom: 6px !important;
  margin-bottom: 6px !important;
}

/* ---------- Typography inside bubbles ---------- */
.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  font-size: 14.5px !important;
  line-height: 1.6 !important;
}
.message-row .message p,
.message-row .message-bubble p,
.message-row .bubble p,
.message-row .prose p {
  font-size: 14.5px !important;
  line-height: 1.6 !important;
  margin: 0 0 8px !important;
  color: inherit !important;
}
.message-row .message p:last-child,
.message-row .message-bubble p:last-child,
.message-row .bubble p:last-child,
.message-row .prose p:last-child { margin-bottom: 0 !important; }

.message-row .message *,
.message-row .message-bubble *,
.message-row .bubble * {
  background: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
  color: inherit !important;
}
.message-row .message a,
.message-row .message-bubble a {
  color: var(--twin-gold) !important;
  text-decoration: underline;
  text-underline-offset: 2px;
}

/* ---------- Input row ---------- */
.input-row,
.gr-input-row,
.chat-input-row,
form[class*="input"] { align-items: stretch !important; gap: 8px !important; }

textarea, input[type="text"] {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  color: var(--twin-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 14.5px !important;
  padding: 13px 16px !important;
  line-height: 1.4 !important;
  min-height: 48px !important;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
textarea:focus, input[type="text"]:focus {
  border-color: var(--twin-gold) !important;
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(236, 173, 10, 0.18) !important;
}
textarea::placeholder, input::placeholder { color: var(--twin-muted) !important; }

/* ---------- Buttons ---------- */
button {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
  border: 1px solid var(--twin-border) !important;
  background: var(--twin-surface) !important;
  color: var(--twin-text) !important;
  padding: 0 18px !important;
  min-height: 48px !important;
  align-self: stretch !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}
button:hover { border-color: var(--twin-gold) !important; color: var(--twin-gold) !important; }

button.primary,
button[variant="primary"],
button.submit,
button.submit-button,
.submit-button,
button.lg.primary {
  background: var(--twin-gold) !important;
  border: 1px solid var(--twin-gold) !important;
  color: #14110a !important;
  font-weight: 700 !important;
  min-height: 48px !important;
  align-self: stretch !important;
  padding: 0 16px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
button.primary:hover,
button.submit:hover,
.submit-button:hover,
button.lg.primary:hover {
  background: #ffc42e !important;
  border-color: #ffc42e !important;
  color: #14110a !important;
}

button.submit svg,
button.submit-button svg,
.submit-button svg,
button.primary svg,
button[variant="primary"] svg {
  width: 18px !important;
  height: 18px !important;
  margin: 0 auto !important;
  display: block !important;
  align-self: center !important;
  color: #14110a !important;
  fill: currentColor !important;
  stroke: currentColor !important;
}

/* ---------- Examples ---------- */
.examples, .examples-holder, [data-testid="examples"] {
  background: transparent !important;
  padding: 0 !important;
  margin-top: 16px !important;
}
.examples table, .examples-table { background: transparent !important; border: 0 !important; }
.examples button, .example, .examples td button, [data-testid="examples"] button {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  color: var(--twin-text-dim) !important;
  font-weight: 400 !important;
  font-size: 13px !important;
  padding: 10px 14px !important;
  text-align: left !important;
  min-height: 0 !important;
  align-self: auto !important;
  display: inline-block !important;
}
.examples button:hover, .example:hover, [data-testid="examples"] button:hover {
  border-color: var(--twin-blue) !important;
  color: var(--twin-blue) !important;
  background: var(--twin-surface) !important;
}

/* ---------- Icon buttons (clear, retry, copy) ---------- */
.icon-button, .chatbot .icon-button {
  color: var(--twin-muted) !important;
  background: transparent !important;
  border: 0 !important;
  min-height: 0 !important;
  align-self: auto !important;
  padding: 4px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.icon-button:hover, .chatbot .icon-button:hover { color: var(--twin-gold) !important; }

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--twin-bg); }
::-webkit-scrollbar-thumb { background: var(--twin-border-strong); }
::-webkit-scrollbar-thumb:hover { background: var(--twin-purple); }

::selection { background: var(--twin-gold); color: #14110a; }

/* ---------- Mobile ---------- */
@media (max-width: 640px) {
  .gradio-container { padding: 40px 16px 36px !important; }
  .gradio-container h1 { font-size: 24px !important; }
  .chatbot, .chatbot.block { min-height: 380px !important; }
}
"""

JS = """
() => {
  document.title = 'Digital Twin';

  const focusInput = () => {
    const areas = document.querySelectorAll('textarea');
    if (areas.length) areas[areas.length - 1].focus();
  };
  setTimeout(focusInput, 300);

  const watchTextarea = (area) => {
    if (area.dataset.twinWatched) return;
    area.dataset.twinWatched = '1';
    let wasDisabled = area.disabled || area.readOnly;
    new MutationObserver(() => {
      const isDisabled = area.disabled || area.readOnly;
      if (wasDisabled && !isDisabled) area.focus();
      wasDisabled = isDisabled;
    }).observe(area, { attributes: true, attributeFilter: ['disabled', 'readonly'] });
  };

  const scan = () => document.querySelectorAll('textarea').forEach(watchTextarea);
  setTimeout(scan, 500);
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
}
"""