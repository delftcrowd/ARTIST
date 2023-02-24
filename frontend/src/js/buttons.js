/**
 * asynchronous method that copies the Original Text into the clipboard.
 */
export async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
  } catch ($e) {
    alert("Cannot copy");
  }
}
