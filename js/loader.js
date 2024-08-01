import {doRequest, getBaseUrl} from './request.js';

function addHeader() {
  let promise = doRequest("get", "header.html");
  promise.then((headerHTML)=>{
    document.body.insertAdjacentHTML("afterbegin", headerHTML.replaceAll("%BASE%", getBaseUrl()));
  });
}

function addFooter() {
  let promise = doRequest("get", "footer.html");
  let lastElement = document.body.lastElementChild;
  promise.then((footerHTML)=>{
    console.log(lastElement);
    lastElement.insertAdjacentHTML("afterend", footerHTML.replaceAll("%BASE%", getBaseUrl()));
  });
}

function loadAll() {
  addHeader();
  addFooter();
}

document.addEventListener("DOMContentLoaded", loadAll);