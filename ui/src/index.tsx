import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./tailwind.css";
import type { SlippersError } from "./types";

const reportErrorsToConsole = (errors: SlippersError[]) => {
    console.group("Slippers: Failed prop types");
    errors.forEach((slippersError) => {
        console.groupCollapsed(
            `${slippersError.tag_name} in ${slippersError.template_name}:${slippersError.lineno}`
        );
        slippersError.errors.forEach((propError) => {
            if (propError.error === "invalid") {
                console.error(
                    `Invalid prop ${propError.name} set on ${slippersError.tag_name}. Expected ${propError.expected}, got ${propError.actual}.`
                );
            } else if (propError.error === "missing") {
                console.error(
                    `Required prop ${propError.name} of type ${propError.expected} not set on ${slippersError.tag_name}.`
                );
            } else if (propError.error === "extra") {
                console.error(
                    `Extra prop ${propError.name} of type ${propError.actual} set on ${slippersError.tag_name}.`
                );
            }
        });
        console.groupEnd();
    });
    console.groupEnd();
};

document.addEventListener("DOMContentLoaded", () => {
    const errors = window.slippersPropErrors || [];
    const typeCheckingOutput = JSON.parse(
        document.getElementById("slippers_type_checking_output")?.textContent ||
            "[]"
    );

    if (errors.length > 0) {
        // Report errors to console
        if (typeCheckingOutput.includes("console")) {
            reportErrorsToConsole(errors);
        }

        // Render overlay
        if (typeCheckingOutput.includes("overlay")) {
            const root = ReactDOM.createRoot(
                document.getElementById(
                    "slippers_errors_ui_root"
                ) as HTMLElement
            );
            root.render(
                <React.StrictMode>
                    <App errors={errors} />
                </React.StrictMode>
            );
        }
    }
});
