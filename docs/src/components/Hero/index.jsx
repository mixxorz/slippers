import React from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import CodeBlock from "@theme/CodeBlock";

import styles from "./styles.module.css";

const example = `
{% #quote %}
  {% quote_photo src="/project-hail-mary.jpg" %}

  {% #quote_text %}
    “I penetrated the outer cell membrane with a nanosyringe."
    "You poked it with a stick?"
    "No!" I said. "Well. Yes. But it was a scientific poke
    with a very scientific stick.”
  {% /quote_text %}

  {% #quote_attribution %}
    Andy Weir, Project Hail Mary
  {% /quote_attribution %}
{% /quote %}
`.trim();

export default function Hero() {
    const { siteConfig } = useDocusaurusContext();
    return (
        <main className={clsx("hero hero--primary", styles.heroBanner)}>
            <div className="container">
                <div className="row">
                    <div className="col col--6">
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
                                to="/docs/getting-started"
                            >
                                Get started
                            </Link>
                            <Link
                                className={clsx(
                                    "button button--secondary button--lg margin-top--md",
                                    styles.secondaryButton
                                )}
                                to="/docs/introduction"
                            >
                                Learn more
                            </Link>
                        </div>
                        <CodeBlock className="margin-top--lg">
                            $ pip install slippers
                        </CodeBlock>
                    </div>
                    <div
                        className={clsx(
                            "col col--6 example-column",
                            styles.exampleColumn
                        )}
                    >
                        <CodeBlock className="language-twig">
                            {example}
                        </CodeBlock>
                    </div>
                </div>
            </div>
        </main>
    );
}
