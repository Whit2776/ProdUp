(() => {
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

