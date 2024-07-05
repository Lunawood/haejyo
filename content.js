// 웹 페이지에 주입되어 사용자가 드래그한 텍스트를 분석하는 스크립트

function analyzeText(text) {
  return fetch("https://127.0.0.1:5000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error("Error analyzing text:", error);
      return []; // 에러가 발생하면 빈 리스트 반환
    });
}

function createLoadingButton(x, y) {
  const existingButton = document.querySelector(".loading-button");
  if (existingButton) {
    existingButton.remove();
  }

  const button = document.createElement("div");
  button.className = "loading-button";
  button.style.left = `${x}px`;
  button.style.top = `${y}px`;
  button.innerHTML = '<div class="spinner"></div>';
  document.body.appendChild(button);
}

function updateLoadingButton(button, count, highestRisk) {
  if (button) {
    button.textContent = `${count}`;
    button.style.borderColor = highestRisk === "High" ? "red" : highestRisk === "Medium" ? "yellow" : "green";
    button.style.color = highestRisk === "High" ? "red" : highestRisk === "Medium" ? "yellow" : "green";
  }
}

function addOverlay(risk, summary, customerAnalysis, x, y) {
  const existingOverlay = document.querySelector(".overlay");
  if (existingOverlay) {
    existingOverlay.remove();
  }

  const overlay = document.createElement("div");
  overlay.className = `overlay ${risk.toLowerCase()}-risk`;
  overlay.innerHTML = `
      <div>${risk === "Low" ? "문제 없음" : summary}</div>
      ${risk !== "Low" ? '<button class="expand-button">펼치기</button>' : ""}
      ${risk !== "Low" ? `<div class="customer-analysis">${customerAnalysis}</div>` : ""}
    `;
  overlay.style.left = `${x}px`;
  overlay.style.top = `${y}px`;
  document.body.appendChild(overlay);

  if (risk !== "Low") {
    const expandButton = overlay.querySelector(".expand-button");
    const analysisDiv = overlay.querySelector(".customer-analysis");
    expandButton.addEventListener("click", () => {
      const isVisible = analysisDiv.style.display === "block";
      analysisDiv.style.display = isVisible ? "none" : "block";
      expandButton.textContent = isVisible ? "펼치기" : "접기";
    });
  }
}

document.addEventListener("mouseup", function (event) {
  const selectedText = window.getSelection().toString().trim();
  if (selectedText.length > 0) {
    const { clientX: x, clientY: y } = event;
    createLoadingButton(x, y);

    analyzeText(selectedText)
      .then((results) => {
        const loadingButton = document.querySelector(".loading-button");
        if (!Array.isArray(results) || results.length === 0) {
          if (loadingButton) {
            updateLoadingButton(loadingButton, 0, "Low");
            loadingButton.addEventListener("click", () => {
              addOverlay("Low", "문제 없음", "", x, y);
            });
          }
          console.log("%c안전", "color: green;");
        } else {
          const highRiskCount = results.filter((r) => r.risk === "High").length;
          const mediumRiskCount = results.filter((r) => r.risk === "Medium").length;
          const highestRisk = highRiskCount > 0 ? "High" : mediumRiskCount > 0 ? "Medium" : "Low";

          const highestRiskSummary = results.find((r) => r.risk === highestRisk)?.summary || "문제 없음";
          const highestRiskCustomerAnalysis = results.find((r) => r.risk === highestRisk)?.customer_analysis || "";

          if (loadingButton) {
            updateLoadingButton(loadingButton, highRiskCount + mediumRiskCount, highestRisk);
            loadingButton.addEventListener("click", () => {
              addOverlay(highestRisk, highestRiskSummary, highestRiskCustomerAnalysis, x, y);
            });
          }

          if (highestRisk === "High") {
            console.log("%c위험", "color: red;");
          } else if (highestRisk === "Medium") {
            console.log("%c주의", "color: yellow;");
          } else {
            console.log("%c안전", "color: green;");
          }
        }
      })
      .catch((error) => {
        console.error("Error analyzing text:", error);
      });
  }
});

document.addEventListener("mouseup", function (event) {
  const existingOverlay = document.querySelector(".overlay");
  if (existingOverlay) {
    existingOverlay.remove();
  }
});
