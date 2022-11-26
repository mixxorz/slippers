// Define slippers language based on twig
Prism.languages.slippers = Prism.languages.extend("twig", {});

Prism.languages.insertBefore("slippers", "tag-name", {
    // Token for component tags
    "component-name": {
        pattern: /(^\{%-?\s*)[\#\/]*[A-Z]\w+/,
        lookbehind: true,
        alias: "class-name",
    },
});

// Define slippers-markup language based on markup
Prism.languages["slippers-markup"] = Prism.languages.extend("markup", {});

// Add token for front matter
Prism.languages.insertBefore("slippers-markup", "comment", {
    "front-matter-block": {
        pattern: /(^(?:\s*[\r\n])?)---(?!.)[\s\S]*?[\r\n]---(?!.)/,
        lookbehind: true,
        greedy: true,
        inside: {
            punctuation: /^---|---$/,
            "front-matter": {
                pattern: /\S+(?:\s+\S+)*/,
                inside: Prism.languages.python,
            },
        },
    },
});

// Copied from twig. It:
// 1. It transforms template tags, vars, and comments into placeholders
// 2. Renders the code as "slippers-markup"
// 3. Replaces the placeholders with the original code and runs them through the
// slippers language
Prism.hooks.add("before-tokenize", function (env) {
    if (env.language !== "slippers") {
        return;
    }

    var pattern = /\{(?:#[\s\S]*?#|%[\s\S]*?%|\{[\s\S]*?\})\}/g;
    Prism.languages["markup-templating"].buildPlaceholders(
        env,
        "slippers",
        pattern
    );

    env.grammar = Prism.languages["slippers-markup"];
});

Prism.hooks.add("after-tokenize", function (env) {
    Prism.languages["markup-templating"].tokenizePlaceholders(env, "slippers");
});
