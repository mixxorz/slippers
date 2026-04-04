(function () {
    "use strict";

    // ---------------------------------------------------------------------------
    // Escaping function for HTML content
    // ---------------------------------------------------------------------------

    function esc(value) {
        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#39;");
    }

    // ---------------------------------------------------------------------------
    // Styles
    // ---------------------------------------------------------------------------

    const STYLES = `
    #slippers_errors_ui_root {
        position: relative;
        z-index: 99999;
    }
    #slippers-overlay {
      position: fixed; inset: 0;
      background: rgba(0,0,0,0.92);
      color: #e4e4e7;
      font-family: sans-serif;
      padding: 3rem;
      overflow-y: auto;
      z-index: 99999;
    }
    #slippers-overlay h1 { color: #f87171; font-size: 1.5rem; margin: 0 0 2rem; }
    .slippers-close {
      margin-left: auto; padding: 0.5rem 1rem;
      background: #000; color: #fff; border: 1px solid #555; cursor: pointer;
    }
    .slippers-header { display: flex; align-items: flex-start; }
    .slippers-error-box { margin-bottom: 2rem; }
    .slippers-tag-label { font-size: 1.1rem; font-weight: bold; }
    .slippers-location { color: #a1a1aa; font-family: monospace; word-break: break-all; }
    .slippers-error-list {
      margin-top: 1rem; padding: 1rem;
      background: #27272a; list-style: disc; list-style-position: inside;
    }
    .slippers-error-list li + li { margin-top: 0.5rem; }
    .slippers-var  { color: #818cf8; font-family: monospace; }
    .slippers-tag  { color: #fb923c; font-family: monospace; }
    .slippers-type { color: #2dd4bf; font-family: monospace; }
  `;

    // ---------------------------------------------------------------------------
    // Components
    // ---------------------------------------------------------------------------

    function formatPropErrorMessage(propError, tagName) {
        if (propError.error === "invalid")
            return `Invalid prop ${propError.name} set on ${tagName}. Expected ${propError.expected}, got ${propError.actual}.`;
        if (propError.error === "missing")
            return `Required prop ${propError.name} of type ${propError.expected} not set on ${tagName}.`;
        if (propError.error === "extra")
            return `Extra prop ${propError.name} of type ${propError.actual} set on ${tagName}.`;
        return propError.error;
    }

    function renderPropError(propError, tagName) {
        const name = `<span class="slippers-var">${esc(propError.name)}</span>`;
        const tag = `<span class="slippers-tag">${esc(tagName)}</span>`;
        const exp = `<span class="slippers-type">${esc(propError.expected)}</span>`;
        const act = `<span class="slippers-type">${esc(propError.actual)}</span>`;

        if (propError.error === "invalid")
            return `Invalid prop ${name} set on ${tag}. Expected ${exp}, got ${act}.`;
        if (propError.error === "missing")
            return `Required prop ${name} of type ${exp} not set on ${tag}.`;
        if (propError.error === "extra")
            return `Extra prop ${name} of type ${act} set on ${tag}.`;
        return esc(propError.error);
    }

    function renderErrorBox(slippersError) {
        const items = slippersError.errors
            .map(
                (e) => `<li>${renderPropError(e, slippersError.tag_name)}</li>`,
            )
            .join("");

        return `
      <div class="slippers-error-box">
        <p class="slippers-tag-label">${esc(slippersError.tag_name)}</p>
        <p class="slippers-location">${esc(slippersError.template_name)}:${esc(slippersError.lineno)}</p>
        <ul class="slippers-error-list">${items}</ul>
      </div>`;
    }

    function renderOverlay(errors) {
        const boxes = errors.map(renderErrorBox).join("");
        return `
      <style>${STYLES}</style>
      <div id="slippers-overlay">
        <div class="slippers-header">
          <h1>Slippers: Failed prop types</h1>
          <button class="slippers-close" id="slippers-close-btn">Close</button>
        </div>
        ${boxes}
      </div>`;
    }

    // ---------------------------------------------------------------------------
    // Console reporting
    // ---------------------------------------------------------------------------

    function reportErrorsToConsole(errors) {
        console.group("Slippers: Failed prop types");
        errors.forEach(function (slippersError) {
            console.groupCollapsed(
                slippersError.tag_name +
                    " in " +
                    slippersError.template_name +
                    ":" +
                    slippersError.lineno,
            );
            slippersError.errors.forEach(function (propError) {
                console.error(formatPropErrorMessage(propError, slippersError.tag_name));
            });
            console.groupEnd();
        });
        console.groupEnd();
    }

    // ---------------------------------------------------------------------------
    // Entry point
    // ---------------------------------------------------------------------------

    document.addEventListener("DOMContentLoaded", function () {
        var errors = window.slippersPropErrors || [];
        var configEl = document.getElementById("slippers_type_checking_output");
        var config = JSON.parse((configEl && configEl.textContent) || "[]");

        if (errors.length === 0) return;

        if (config.includes("console")) reportErrorsToConsole(errors);

        if (config.includes("overlay")) {
            var root = document.getElementById("slippers_errors_ui_root");
            if (!root) return;

            root.innerHTML = renderOverlay(errors);

            function closeOverlay() {
                root.innerHTML = "";
                document.removeEventListener("keydown", onKey);
            }

            function onKey(ev) {
                if (ev.key === "Escape") closeOverlay();
            }

            document.getElementById("slippers-close-btn").addEventListener("click", closeOverlay);
            document.addEventListener("keydown", onKey);
        }
    });
})();
