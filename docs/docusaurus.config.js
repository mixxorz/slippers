const prismTheme = require("./src/prism-theme");

/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
    title: "slippers",
    tagline:
        "Build reusable components in Django without writing a single line of Python.",
    url: "https://mitchel.me",
    baseUrl: "/slippers/",
    onBrokenLinks: "throw",
    onBrokenMarkdownLinks: "warn",
    favicon: "img/favicon.ico",
    organizationName: "mixxorz",
    projectName: "slippers",
    trailingSlash: true,
    themeConfig: {
        image: "https://repository-images.githubusercontent.com/384881226/b3f17d7e-ba55-4470-b1ea-4c65c4ab2cde",
        navbar: {
            title: "",
            logo: {
                alt: "slippers",
                src: "img/slippers.svg",
            },
            items: [
                {
                    href: "/docs/introduction/",
                    label: "Docs",
                },
                {
                    href: "https://github.com/mixxorz/slippers",
                    label: "GitHub",
                    position: "right",
                },
            ],
        },
        footer: {
            style: "light",
            links: [
                {
                    title: "Docs",
                    items: [
                        {
                            label: "Introduction",
                            to: "/docs/introduction",
                        },
                        {
                            label: "Installation",
                            to: "/docs/installation",
                        },
                        {
                            label: "Getting started",
                            to: "/docs/getting-started",
                        },
                    ],
                },
                {
                    title: "More",
                    items: [
                        {
                            label: "GitHub",
                            href: "https://github.com/mixxorz/slippers",
                        },
                        {
                            label: "Twitter",
                            href: "https://twitter.com/mixxorz",
                        },
                    ],
                },
            ],
        },
        prism: {
            theme: prismTheme,
            darkTheme: prismTheme,
            additionalLanguages: ["django", "twig"],
        },
    },
    presets: [
        [
            "@docusaurus/preset-classic",
            {
                docs: {
                    sidebarPath: require.resolve("./sidebars.js"),
                    // Please change this to your repo.
                    editUrl:
                        "https://github.com/mixxorz/slippers/edit/main/docs/",
                },
                theme: {
                    customCss: require.resolve("./src/css/custom.css"),
                },
            },
        ],
    ],
};
