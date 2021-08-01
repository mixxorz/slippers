var theme = {
    plain: {
        backgroundColor: "#2a2734",
        color: "#ffffff",
    },
    styles: [
        {
            types: ["comment", "prolog", "doctype", "cdata"],
            style: {
                color: "#4a5f78",
            },
        },
        {
            types: ["namespace"],
            style: {
                opacity: 0.7,
            },
        },
        {
            types: ["tag", "operator", "number", "punctuation"],
            style: {
                color: "#0aa370",
            },
        },
        {
            types: ["property", "function"],
            style: {
                color: "#57718e",
            },
        },
        {
            types: ["tag-id", "selector", "atrule-id"],
            style: {
                color: "#ebf4ff",
            },
        },
        {
            types: ["attr-name"],
            style: {
                color: "#7eb6f6",
            },
        },
        {
            types: [
                "boolean",
                "string",
                "entity",
                "url",
                "attr-value",
                "control",
                "directive",
                "unit",
                "statement",
                "regex",
                "at-rule",
            ],
            style: {
                color: "#47ebb4",
            },
        },
        {
            types: ["placeholder", "plain", "keyword", "variable"],
            style: {
                color: "#ffffff",
            },
        },
        {
            types: ["deleted"],
            style: {
                textDecorationLine: "line-through",
            },
        },
        {
            types: ["inserted"],
            style: {
                textDecorationLine: "underline",
            },
        },
        {
            types: ["italic"],
            style: {
                fontStyle: "italic",
            },
        },
        {
            types: ["important", "bold"],
            style: {
                fontWeight: "bold",
            },
        },
        {
            types: ["important"],
            style: {
                color: "#c4b9fe",
            },
        },
    ],
};

module.exports = theme;
