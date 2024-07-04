// 웹 페이지에 주입되어 사용자가 드래그한 텍스트를 분석하는 스크립트

function analyzeText(text) {
  return fetch("https://127.0.0.1:5000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  }).then((response) => response.json());
}

function addOverlay(risk, summary) {
  const existingOverlay = document.querySelector('.overlay');
  if (existingOverlay) {
    existingOverlay.remove();
  }

  const overlay = document.createElement("div");
  overlay.className = "overlay";
  overlay.textContent = risk === "High" ? summary : "문제 없음";
  overlay.style.position = "fixed";
  overlay.style.backgroundColor = risk === "High" ? "red" : "green";
  overlay.style.color = "white";
  overlay.style.padding = "5px";
  overlay.style.zIndex = "10000";
  overlay.style.bottom = "10px";
  overlay.style.right = "10px";
  overlay.style.maxWidth = "300px";
  overlay.style.borderRadius = "5px";
  document.body.appendChild(overlay);
}

let isMouseDown = false;
let selectedText = '';

document.addEventListener('mousedown', () => {
  isMouseDown = true;
  selectedText = '';
});

document.addEventListener('mouseup', () => {
  if (isMouseDown) {
    selectedText = window.getSelection().toString().trim();
    console.log(`Mouse up: ${selectedText}`);
    if (selectedText.length > 0) {
      console.log(`Selected text to analyze: ${selectedText}`);
      analyzeText(selectedText)
        .then((result) => {
          console.log(`Server response: ${JSON.stringify(result)}`);
          addOverlay(result.risk, result.summary);
        })
        .catch((error) => {
          console.error("Error analyzing text:", error);
        });
    } else {
      console.log("No text selected.");
    }
    isMouseDown = false;
  }
});
