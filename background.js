// 확장 프로그램의 백그라운드 스크립트. API 요청 등을 처리

chrome.runtime.onInstalled.addListener(() => {
    console.log('Privacy Policy Analyzer installed.');
  });