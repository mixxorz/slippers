import React from "react";
import clsx from "clsx";
import Layout from "@theme/Layout";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import styles from "./index.module.css";
import HomepageFeatures from "../components/HomepageFeatures";

function HomepageHeader() {
    const { siteConfig } = useDocusaurusContext();
    return (
        <header className={clsx("hero hero--primary", styles.heroBanner)}>
            <div className="container">
                <img src="img/slippers.svg" alt="slippers" />
                <p
                    className={clsx(
                        "hero__subtitle margin-top--md",
                        styles.heroSubtitle
                    )}
                >
                    {siteConfig.tagline}
                </p>
                <div className={clsx("margin-top--lg", styles.buttons)}>
                    <Link
                        className="button button--primary button--lg"
                        to="/docs/intro"
                    >
                        Quick start
                    </Link>
                    <Link
                        className="button button--secondary button--lg margin-left--md"
                        to="/docs/intro"
                    >
                        Docs
                    </Link>
                </div>
            </div>
        </header>
    );
}

export default function Home() {
    return (
        <Layout
            title={
                "Build reusable components in Django without writing a single line of Python."
            }
            description="Build reusable components in Django without writing a single line of Python."
        >
            <HomepageHeader />
            <main>
                <HomepageFeatures />
            </main>
        </Layout>
    );
}
