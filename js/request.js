export function doRequest(method, uri, payload) {
  method = (method || "get").toLowerCase();

  if (!["get"].includes(method)) {
    throw "method '" + method + "' is not supported";
  }

  let request = new XMLHttpRequest();

  let promise = new Promise((resolve, reject)=>{
    request.addEventListener("load", ()=>resolve(request.response));
    request.addEventListener("error", ()=>reject(request.responseText));
    request.addEventListener("abort", ()=>reject("Aborted"));
  });

  request.open(method, uri);
  request.send(payload || null);

  return promise;
}