document.addEventListener("click", async (event) => {
  const button = event.target.closest(".copy-btn");
  if (!button) {
    return;
  }

  const promptText = button.dataset.copy || "";
  const originalLabel = button.textContent;

  try {
    await navigator.clipboard.writeText(promptText);
    button.textContent = "Copied!";
    button.classList.remove("bg-indigo-600", "hover:bg-indigo-700");
    button.classList.add("bg-emerald-600", "hover:bg-emerald-700");
  } catch (error) {
    button.textContent = "Copy failed";
    button.classList.remove("bg-indigo-600", "hover:bg-indigo-700");
    button.classList.add("bg-rose-600", "hover:bg-rose-700");
  }

  setTimeout(() => {
    button.textContent = originalLabel;
    button.classList.remove("bg-emerald-600", "hover:bg-emerald-700", "bg-rose-600", "hover:bg-rose-700");
    button.classList.add("bg-indigo-600", "hover:bg-indigo-700");
  }, 1500);
});
