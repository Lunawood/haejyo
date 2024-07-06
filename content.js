// 웹 페이지에 주입되어 사용자가 드래그한 텍스트를 분석하는 스크립트

function loadWebFonts() {
  const link = document.createElement('link');
  link.href = 'https://fonts.googleapis.com/css2?family=Jua&display=swap';
  link.rel = 'stylesheet';
  document.head.appendChild(link);

  const style = document.createElement('style');
  style.textContent = `
    .overlay, .loading-button, .expand-button {
      font-family: 'Jua', sans-serif !important;
      font-weight: 400;
      font-style: normal;
    }
  `;
  document.head.appendChild(style);
}

loadWebFonts();

function analyzeText(text) {
  return fetch("https://127.0.0.1:5000/search", {
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

function analyzeRisk(text) {
  // 위험도 분석을 위해 두 번째 API 요청
  return fetch('https://127.0.0.1:5000/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  })
    .then(response => response.json())
    .then(result => {
      return result;
    })
    .catch(error => {
      console.error('Error analyzing risk:', error);
      return { error: "An unexpected error occurred" };
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
    button.classList.remove('high-risk', 'medium-risk', 'low-risk');
    
    // 새로운 위험도 클래스 추가
    if (highestRisk === "High") {
      button.classList.add('high-risk');
    } else if (highestRisk === "Medium") {
      button.classList.add('medium-risk');
    } else {
      button.classList.add('low-risk');
    }
    button.style.borderColor = highestRisk === 'High' ? 'red' : highestRisk === 'Medium' ? '#FFD400' : 'green';
  }
}

function addOverlay(risk, summary, x, y) {
  const existingOverlay = document.querySelector(".overlay");
  if (existingOverlay) {
    existingOverlay.remove();
  }

  let riskLabel = '';
  if (risk === "High") {
    riskLabel = '위험 🚨';
  } else if (risk === "Medium") {
    riskLabel = '주의 ⚠️';
  }

  const overlay = document.createElement("div");
  overlay.className = `overlay ${risk.toLowerCase()}-risk`;
  overlay.innerHTML = `
      <div>${risk === "Low" ? "문제 없음" : `<strong>${riskLabel}</strong><br>${summary}`}</div>
      ${risk !== "Low" ? '<button class="expand-button">펼치기</button>' : ""}
      ${risk !== "Low" ? `<div class="customer-analysis" style="display:none;"></div>` : ""}
    `;
  overlay.style.left = `${x}px`;
  overlay.style.top = `${y}px`;
  overlay.style.fontFamily= "Jua";
  document.body.appendChild(overlay);

  if (risk !== "Low") {
    const expandButton = overlay.querySelector(".expand-button");
    const analysisDiv = overlay.querySelector(".customer-analysis");

    expandButton.style.color = "gray";

    analyzeRisk(summary).then(riskResult => {
      analysisDiv.innerHTML = riskResult[0]?.customer_analysis || ''; // 받은 결과의 customer_analysis 사용
      console.log(analysisDiv.innerHTML);
      expandButton.style.color = "blue"; // 활성화 후 파란색 배경

      expandButton.addEventListener("mouseup", () => {
        console.log("클릭됨");
        const isVisible = analysisDiv.style.display === "block";
        analysisDiv.style.display = isVisible ? "none" : "block";
        expandButton.textContent = isVisible ? "펼치기" : "접기";
      });
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
          console.log("안전");
        } else {
          const highRiskCount = results.filter((r) => r.risk === "High").length;
          const mediumRiskCount = results.filter((r) => r.risk === "Medium").length;
          const highestRisk = highRiskCount > 0 ? "High" : mediumRiskCount > 0 ? "Medium" : "Low";

          const highestRiskResult = results.find((r) => r.risk === highestRisk);
          const highestRiskSummary = highestRiskResult?.summary || "문제 없음";
          
          if (loadingButton) {
            updateLoadingButton(loadingButton, highRiskCount + mediumRiskCount, highestRisk);
            loadingButton.addEventListener("click", () => {
              addOverlay(highestRisk, highestRiskSummary, x, y);
            });
          }

          if (highestRisk === "High") {
            console.log("위험");
          } else if (highestRisk === "Medium") {
            console.log("주의");
          } else {
            console.log("안전");
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