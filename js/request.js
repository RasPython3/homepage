export function getBaseUrl() {
  let url = location.origin + location.pathname.replace(/\/articles\/[0-9]*\/.*$/, "/");
  return url.match("^.*/(?=[^/]*$)")[0];
}

export function doRequest(method, uri, payload) {
  method = (method || "get").toLowerCase();

  if (!["get"].includes(method)) {
    throw "method '" + method + "' is not supported";
  }

  let request = new XMLHttpRequest();

  let base = getBaseUrl();

  let url = new URL(uri, base);

  let promise = new Promise((resolve, reject)=>{
    request.addEventListener("load", ()=>resolve(request.response));
    request.addEventListener("error", ()=>reject(request.responseText));
    request.addEventListener("abort", ()=>reject("Aborted"));
  });

  request.open(method, url);
  request.send(payload || null);

  return promise;
}