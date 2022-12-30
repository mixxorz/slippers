import React from "react";
import { render, screen } from "@testing-library/react";
import App from "./App";

const testErrors = [
    {
        tag_name: "Button",
        template_name: "pattern-library/pages/home_page/home_page.html",
        lineno: 23,
        errors: [
            {
                error: "invalid" as "invalid",
                name: "color",
                expected: "string",
                actual: "number",
            },
            {
                error: "missing" as "missing",
                name: "href",
                expected: "string",
            },
        ],
    },
    {
        tag_name: "CardLink",
        template_name: "pattern-library/pages/home_page/home_page.html",
        lineno: 24,
        errors: [
            {
                error: "extra" as "extra",
                name: "variant",
                actual: "string",
            },
        ],
    },
];

test("Do not display overlay when there are no errors", () => {
    render(<App errors={[]} />);
    const header = screen.queryByText("Slippers: Failed prop types");
    expect(header).not.toBeInTheDocument();
});

test("Display errors in overlay", () => {
    render(<App errors={testErrors} />);
    const header = screen.queryByText("Slippers: Failed prop types");
    expect(header).toBeInTheDocument();

    const errorBoxes = screen.getAllByTestId("error-box");

    // Assert there are two error boxes
    expect(errorBoxes).toHaveLength(2);

    // Assert the first error box is for Button
    const buttonErrorBox = errorBoxes[0];
    expect(buttonErrorBox).toHaveTextContent(
        "Invalid prop color set on Button."
    );
    expect(buttonErrorBox).toHaveTextContent(
        "Required prop href of type string not set on Button."
    );

    // Assert the second error box is for Button
    const cardLinkErrorBox = errorBoxes[1];
    expect(cardLinkErrorBox).toHaveTextContent(
        "Extra prop variant of type string set on CardLink."
    );
});
