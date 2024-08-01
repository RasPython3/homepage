export function getBaseUrl() {
  return location.origin + location.pathname.match("^(.*?)(?:/articles/[0-9]*/.*)?$")[1];
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