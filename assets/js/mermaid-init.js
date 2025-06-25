
// Upewniamy się, że mermaid.patch1() i mermaid.initialize() odbędą się dopiero
// gdy biblioteka mermaid.min.js jest załadowana.
document.addEventListener("DOMContentLoaded", function () {
  // Inicjalizujemy Mermaid z opcją startOnLoad: true, securityLevel: 'loose' i htmlLabels: true
  mermaid.initialize({
    startOnLoad: true,
    securityLevel: 'loose',
    flowchart: {
      htmlLabels: true
    }
    // Możesz tu dopisać inne opcje: theme, logLevel itp.
  });
  console.log("mermaid.init: Mermaid został zainicjalizowany (startOnLoad: true)");
});