// ==UserScript==
// @name        KlawaClient
// @namespace   Violentmonkey Scripts
// @match       *://www.klawiaturowe-wyzwanie.pl/*
// @grant       GM.xmlHttpRequest
// @version     1.11
// @author      Kostek001
// @description 14.11.2023, 08:34:27
// ==/UserScript==


let text = "";

onElementUpdate("#displaytext", function (element) {
  if (text != element.innerText){
    text = element.innerText;
    GM.xmlHttpRequest({
      method: "POST",
      headers: {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
      },
      url: "http://127.0.0.1:5000/text",
      data: `data=${encodeURIComponent(element.innerText)}`,
      fetch: true
    });
    console.log("Text sended!");
  }
});

function waitForElement(selector) {
  return new Promise(resolve => {
    if (document.querySelector(selector) && !document.querySelector(selector).innerText.includes("--")) {
      return resolve(document.querySelector(selector));
    }

    const observer = new MutationObserver(mutations => {
      if (document.querySelector(selector) && !document.querySelector(selector).innerText.includes("--")) {
        observer.disconnect();
        resolve(document.querySelector(selector));
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  });
}

function onElementUpdate(selector, func){
  waitForElement(selector).then((element) => {
    const observer = new MutationObserver((records, observer) => {
      func(element);
    });
    const config = {
      subtree: true,
      childList: true,
      characterData: true
    };

    observer.observe(element, config);
    func(element);
  });
}