import {doRequest, getBaseUrl} from './request.js';

function addHeader() {
  let promise = doRequest("get", "header.html");
  promise.then((headerHTML)=>{
    document.body.insertAdjacentHTML("afterbegin", headerHTML.replace(/%BASE%/g, getBaseUrl().slice(0, -1)));
  });
}

function addFooter() {
  let promise = doRequest("get", "footer.html");
  let lastElement = document.body.lastElementChild;
  promise.then((footerHTML)=>{
    console.log(lastElement);
    lastElement.insertAdjacentHTML("afterend", footerHTML.replace(/%BASE%/g, getBaseUrl().slice(0, -1)));
  });
}

function loadAll() {
  prompt("aaa");
  addHeader();
  addFooter();
}

document.addEventListener("DOMContentLoaded", loadAll);