import React from "react";
import Layout from "@theme/Layout";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";

import Hero from "@site/src/components/Hero";

export default function Home() {
    const { siteConfig } = useDocusaurusContext();
    return (
        <Layout title={siteConfig.tagline} description={siteConfig.tagline}>
            <Hero />
        </Layout>
    );
}
