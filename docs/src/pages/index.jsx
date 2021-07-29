import React from "react";
import clsx from "clsx";
import Layout from "@theme/Layout";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import styles from "./index.module.css";

export default function Home() {
    const { siteConfig } = useDocusaurusContext();
    return (
        <Layout
            title={
                "Build reusable components in Django without writing a single line of Python."
            }
            description="Build reusable components in Django without writing a single line of Python."
        >
            <main className={clsx("hero hero--primary", styles.heroBanner)}>
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
                    <div className={styles.buttons}>
                        <Link
                            className="button button--primary button--lg margin-top--md"
                            to="/docs/intro"
                        >
                            Quick start
                        </Link>
                        <Link
                            className={clsx(
                                "button button--secondary button--lg margin-top--md",
                                styles.secondaryButton
                            )}
                            to="/docs/intro"
                        >
                            Docs
                        </Link>
                    </div>
                    <div className="row margin-top--lg">
                        <div className="col col--4">
                            <pre>
                                <span>$</span> pip install slippers
                            </pre>
                        </div>
                    </div>
                </div>
            </main>
        </Layout>
    );
}
