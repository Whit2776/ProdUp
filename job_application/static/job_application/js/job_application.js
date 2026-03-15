(() => {
  const THEME_KEY = "ja_theme";

  function getSavedTheme() {
    const saved = localStorage.getItem(THEME_KEY);
    return saved === "light" || saved === "dark" ? saved : null;
  }

  function systemTheme() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function applyTheme(theme, save) {
    document.documentElement.dataset.theme = theme;
    if (save) localStorage.setItem(THEME_KEY, theme);
    const btn = document.getElementById("themeToggle");
    if (btn) btn.textContent = theme === "dark" ? "Light mode" : "Dark mode";
  }

  document.addEventListener("DOMContentLoaded", () => {
    const saved = getSavedTheme();
    applyTheme(saved || systemTheme(), false);

    // If there isn't a saved choice, keep following the OS preference.
    const mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
    if (!saved && mq && typeof mq.addEventListener === "function") {
      mq.addEventListener("change", () => applyTheme(systemTheme(), false));
    }

    const btn = document.getElementById("themeToggle");
    if (btn) {
      btn.addEventListener("click", () => {
        const current = document.documentElement.dataset.theme === "light" ? "light" : "dark";
        // First explicit click becomes the user's saved preference.
        applyTheme(current === "dark" ? "light" : "dark", true);
      });
    }

    const imageInput = document.querySelector('input[type="file"][name="image"]');
    const resumeInput = document.querySelector('input[type="file"][name="resume"]');
    const imagePreview = document.getElementById("imagePreview");
    const resumeHint = document.getElementById("resumeHint");
    let currentObjectUrl = null;

    function clearObjectUrl() {
      if (currentObjectUrl) {
        URL.revokeObjectURL(currentObjectUrl);
        currentObjectUrl = null;
      }
    }

    function humanBytes(n) {
      const units = ["B", "KB", "MB", "GB"];
      let size = Number(n || 0);
      let i = 0;
      while (size >= 1024 && i < units.length - 1) {
        size /= 1024;
        i += 1;
      }
      return `${size.toFixed(i === 0 ? 0 : 1)} ${units[i]}`;
    }

    function renderResumeHint() {
      if (!resumeInput || !resumeHint) return;
      const file = resumeInput.files && resumeInput.files[0];
      resumeHint.textContent = file ? `Selected: ${file.name} (${humanBytes(file.size)})` : "";
    }

    function renderImagePreview() {
      if (!imageInput || !imagePreview) return;
      const file = imageInput.files && imageInput.files[0];
      clearObjectUrl();
      if (!file) {
        imagePreview.innerHTML = '<div class="upload-preview-empty">No file selected yet.</div>';
        return;
      }

      currentObjectUrl = URL.createObjectURL(file);
      const lower = (file.name || "").toLowerCase();
      const meta = `<div class="upload-hint">Selected: ${file.name} (${humanBytes(file.size)})</div>`;
      if (lower.endsWith(".mp4")) {
        imagePreview.innerHTML = `<video src="${currentObjectUrl}" controls playsinline></video>${meta}`;
      } else {
        imagePreview.innerHTML = `<img src="${currentObjectUrl}" alt="Selected upload preview" />${meta}`;
      }
    }

    if (resumeInput) resumeInput.addEventListener("change", renderResumeHint);
    if (imageInput) imageInput.addEventListener("change", renderImagePreview);
    renderResumeHint();
    renderImagePreview();
    window.addEventListener("beforeunload", clearObjectUrl);
  });

  // Small UX: autofocus the first invalid field on form submit.
  document.addEventListener("submit", (e) => {
    const form = e.target;
    if (!(form instanceof HTMLFormElement)) return;

    // Let the server validate; if it returns errors the page reloads.
    // This hook is just for browser-level invalids (required, type).
    const firstInvalid = form.querySelector(":invalid");
    if (firstInvalid && firstInvalid instanceof HTMLElement) {
      firstInvalid.focus({ preventScroll: false });
    }
  });
})();

