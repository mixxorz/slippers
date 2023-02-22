# Error UI

This directory contains the React app that display the prop errors.

## Development

Install the dependencies

```
npm install
```

Start the dev server

```
npm start
```

You will see a blank page because this is the behaviour when there are no
errors.

To work on errors, manually add some test errors to index.tsx.

```tsx
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

root.render(
  <React.StrictMode>
    <App errors={testErrors} />
  </React.StrictMode>
);
```

## Release

The release process is automated. When `npm run build` is run, the toolchain
compiles an optimized bundle and drops it in `slippers/static/slippers/`. The
`main.js` and `main.css` are then included in the Python bundle when `poetry build` is run.
