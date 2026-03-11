document.addEventListener("DOMContentLoaded", () => {
  const items = document.querySelectorAll(".js-reveal");
  items.forEach((el, i) => {
    el.animate(
      [
        { opacity: 0, transform: "translateY(20px)" },
        { opacity: 1, transform: "translateY(0px)" }
      ],
      {
        duration: 480,
        delay: i * 70,
        fill: "both",
        easing: "cubic-bezier(0.22, 1, 0.36, 1)"
      }
    );
  });
});
