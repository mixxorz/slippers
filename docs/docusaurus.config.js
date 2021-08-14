const prismTheme = require("./src/prism-theme");

/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
    title: "slippers",
    tagline:
        "Build reusable components in Django without writing a single line of Python.",
    url: "https://mixxorz.github.io",
    baseUrl: "/slippers/",
    onBrokenLinks: "throw",
    onBrokenMarkdownLinks: "warn",
    favicon: "img/favicon.ico",
    organizationName: "mixxorz", // Usually your GitHub org/user name.
    projectName: "slippers", // Usually your repo name.
    themeConfig: {
        navbar: {
            title: "",
            logo: {
                alt: "slippers",
                src: "img/slippers.svg",
            },
            items: [
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
                    title: "Community",
                    items: [
                        {
                            label: "Stack Overflow",
                            href: "https://stackoverflow.com/questions/tagged/docusaurus",
                        },
                        {
                            label: "Discord",
                            href: "https://discordapp.com/invite/docusaurus",
                        },
                        {
                            label: "Twitter",
                            href: "https://twitter.com/docusaurus",
                        },
                    ],
                },
                {
                    title: "More",
                    items: [
                        {
                            label: "Blog",
                            to: "/blog",
                        },
                        {
                            label: "GitHub",
                            href: "https://github.com/slippers/mixxorz",
                        },
                    ],
                },
            ],
            copyright: `Copyright © ${new Date().getFullYear()} My Project, Inc. Built with Docusaurus.`,
        },
        prism: {
            theme: prismTheme,
            darkTheme: prismTheme,
            additionalLanguages: ["django"],
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
                blog: {
                    showReadingTime: true,
                    // Please change this to your repo.
                    editUrl:
                        "https://github.com/mixxorz/slippers/edit/main/docs/blog/",
                },
                theme: {
                    customCss: require.resolve("./src/css/custom.css"),
                },
            },
        ],
    ],
};