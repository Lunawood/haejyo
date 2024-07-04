// 웹 페이지에 주입되어 사용자가 드래그한 텍스트를 분석하는 스크립트

function analyzeText(text) {
  // 위험 옵션 분석 로직 (모델 API 호출)
  return fetch('https://127.0.0.1:5000/analyze', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
  })
  .then(response => response.json())
  .then(result => {
      if (result.risk === 'High') {
          console.log('위험');
      } else {
          console.log('안전');
      }
      return result; // 여기서 result 반환
  })
  .catch(error => {
      console.error('Error analyzing text:', error);
  });
}

function addOverlay(risk, summary, x, y) {
  const existingOverlay = document.querySelector('.overlay');
  if (existingOverlay) {
      existingOverlay.remove();
  }

  const overlay = document.createElement("div");
  overlay.className = "overlay";
  overlay.textContent = risk === "High" ? summary : "문제 없음";
  overlay.style.position = "fixed";
  overlay.style.backgroundColor = risk === "High" ? "rgba(255, 0, 0, 0.5)" : "rgba(0, 128, 0, 0.5)";
  overlay.style.color = "white";
  overlay.style.padding = "10px";
  overlay.style.zIndex = "10000";
  overlay.style.left = `${x}px`;
  overlay.style.top = `${y}px`;
  overlay.style.maxWidth = "300px";
  overlay.style.borderRadius = "8px";
  overlay.style.fontFamily = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
  overlay.style.fontSize = "14px";
  overlay.style.boxShadow = "0px 0px 10px rgba(0, 0, 0, 0.5)";
  document.body.appendChild(overlay);
}

document.addEventListener('mouseup', function(event) {
  const selectedText = window.getSelection().toString().trim();
  if (selectedText.length > 0) {
      analyzeText(selectedText).then(result => {
          if (result) {
              const { clientX: x, clientY: y } = event;
              addOverlay(result.risk, result.summary, x, y);
          }
      }).catch(error => {
          console.error('Error analyzing text:', error);
      });
  }
});

document.addEventListener('mouseup', function(event) {
  const existingOverlay = document.querySelector('.overlay');
  if (existingOverlay) {
      existingOverlay.remove();
  }
});
