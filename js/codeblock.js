import {hljs} from './highlight.min.js';

export function decorateCodeBlocks(target=document) {
  target.querySelectorAll("pre.codeblock").forEach((block)=>{
    var lang = [...[...block.classList].filter((clsname)=>clsname.startsWith("lang-")), "lang-text"][0].slice(5);

    if (hljs.getLanguage(lang) == undefined) {
      lang = "text";
    }

    let code = block.innerText;

    let result = hljs.highlight(code, {language: lang});

    block.innerHTML = result.value;

    let wrapper = document.createElement("div");
    wrapper.className="codeblock-wrapper";
    wrapper.innerHTML = "<div class=\"codeblock-header\">" +
      "<input type=\"button\" value=\"Copy\" onclick=\"navigator.clipboard.writeText(this.parentElement.nextElementSibling.innerText)\"></div>" +
      block.outerHTML;

    block.insertAdjacentElement("afterend", wrapper);
    block.remove();
  });
}