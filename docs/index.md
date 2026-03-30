---
title: "slippers — Build reusable components in Django without writing a single line of Python."
description: "Build reusable components in Django without writing a single line of Python."
hide:
  - navigation
  - toc
---

<div class="sl-hero">
  <div class="sl-hero__inner">
    <div class="sl-hero__left">
      <img src="img/slippers.svg" alt="Slippers logo" class="sl-hero__logo">
      <p class="sl-hero__tagline">Build reusable components in Django without writing a single line of Python.</p>
      <div class="sl-hero__buttons">
        <a href="getting-started/" class="md-button md-button--primary">Get started</a>
        <a href="introduction/" class="md-button">Learn more</a>
      </div>
      <div class="sl-hero__install">
        <code>$ pip install slippers</code>
      </div>
    </div>
    <div class="sl-hero__right">

```slippers
{% #Quote %}
  {% QuotePhoto src="/project-hail-mary.jpg" %}

  {% #QuoteText %}
    "I penetrated the outer cell membrane with a nanosyringe."
    "You poked it with a stick?"
    "No!" I said. "Well. Yes. But it was a scientific poke
    with a very scientific stick."
  {% /QuoteText %}

  {% #QuoteAttribution %}
    Andy Weir, Project Hail Mary
  {% /QuoteAttribution %}
{% /Quote %}
```

</div>
  </div>
</div>

<style>
:root {
  --sl-almost-black: #0d1117;
}

.md-content h1:first-child {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.md-main,
.md-content,
.md-content__inner {
  background-color: var(--sl-almost-black) !important;
}

.sl-hero {
  padding: 2rem 0;
}

@media screen and (min-width: 997px) {
  .sl-hero {
    padding: 8rem 0;
  }
}

.sl-hero__inner {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: flex-end;
}

@media screen and (max-width: 996px) {
  .sl-hero__inner {
    grid-template-columns: 1fr;
  }
}

.sl-hero__logo {
  display: block;
  width: 100%;
  max-width: 480px;
  margin-bottom: 1.5rem;
}

.sl-hero__tagline {
  font-size: 1.1rem;
  line-height: 1.25;
  color: #fff;
  margin-bottom: 1.5rem;
  max-width: 480px;
}

.sl-hero__buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

@media screen and (min-width: 480px) {
  .sl-hero__buttons {
    flex-direction: row;
  }
}

.sl-hero__install {
  display: inline-block;
  background-color: #161b22;
  border-radius: 4px;
  padding: 0.75rem 1.25rem;
  max-width: 480px;
  width: 100%;
  box-sizing: border-box;
}

.sl-hero__install code {
  font-size: 0.9rem;
  color: #ccc;
  background: none;
  padding: 0;
}

.sl-hero__right {
  min-width: 0;
  --md-hue: 232;
  --md-code-fg-color: hsla(var(--md-hue), 18%, 86%, 0.82);
  --md-code-bg-color: hsla(var(--md-hue), 15%, 18%, 1);
  --md-default-fg-color--light: hsla(var(--md-hue), 15%, 90%, 0.56);
  --md-code-hl-number-color: #e6695b;
  --md-code-hl-special-color: #f06090;
  --md-code-hl-function-color: #c973d9;
  --md-code-hl-constant-color: #9383e2;
  --md-code-hl-keyword-color: #6791e0;
  --md-code-hl-string-color: #2fb170;
  --md-code-hl-name-color: var(--md-code-fg-color);
  --md-code-hl-operator-color: var(--md-default-fg-color--light);
  --md-code-hl-punctuation-color: var(--md-default-fg-color--light);
  --md-code-hl-comment-color: var(--md-default-fg-color--light);
  --md-code-hl-generic-color: var(--md-default-fg-color--light);
  --md-code-hl-variable-color: var(--md-default-fg-color--light);
}

.sl-hero__right .highlight {
  margin: 0;
}

.sl-hero__right pre {
  margin: 0 !important;
  border-radius: 8px;
}
</style>
