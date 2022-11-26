// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const prismTheme = require("./src/prism-theme");

/** @type {import('@docusaurus/types').Config} */
const config = {
    title: "slippers",
    tagline:
        "Build reusable components in Django without writing a single line of Python.",
    url: "https://mitchel.me",
    baseUrl: "/slippers/",
    onBrokenLinks: "throw",
    onBrokenMarkdownLinks: "warn",
    favicon: "img/favicon.ico",

    // GitHub pages deployment config.
    // If you aren't using GitHub pages, you don't need these.
    organizationName: "mixxorz", // Usually your GitHub org/user name.
    projectName: "slippers", // Usually your repo name.

    // Even if you don't use internalization, you can use this field to set useful
    // metadata like html lang. For example, if your site is Chinese, you may want
    // to replace "en" with "zh-Hans".
    i18n: {
        defaultLocale: "en",
        locales: ["en"],
    },

    presets: [
        [
            "classic",
            /** @type {import('@docusaurus/preset-classic').Options} */
            ({
                docs: {
                    sidebarPath: require.resolve("./sidebars.js"),
                    // Please change this to your repo.
                    // Remove this to remove the "edit this page" links.
                    editUrl:
                        "https://github.com/mixxorz/slippers/edit/main/docs/",
                },
                theme: {
                    customCss: require.resolve("./src/css/custom.css"),
                },
            }),
        ],
    ],

    themeConfig:
        /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
        ({
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
                style: "dark",
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
                additionalLanguages: ["twig"],
            },
        }),
};

module.exports = config;
