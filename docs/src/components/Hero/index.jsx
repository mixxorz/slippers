import React from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import CodeBlock from "@theme/CodeBlock";

import styles from "./styles.module.css";

const example = `
{% #quote %}
  {% quote_photo src="/django.jpg" %}

  {% #quote_text %}
    The Django template system recognizes that templates are most
    often written by designers, not programmers, and therefore
    should not assume Python knowledge.
  {% /quote_text %}

  {% #quote_attribution %}
    Design philosophies – Django
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
                                to="/docs/intro"
                            >
                                Get started
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
                    </div>
                    <div className={clsx("col col--6 example-column", styles.exampleColumn)}>
                        <CodeBlock className="language-django">
                            {example}
                        </CodeBlock>
                    </div>
                </div>
            </div>
        </main>
    );
}
