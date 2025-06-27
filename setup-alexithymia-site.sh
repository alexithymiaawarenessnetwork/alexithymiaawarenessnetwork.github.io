#!/bin/bash

# Exit on error
set -e

# Set repo name
REPO_NAME="alexithymia-awareness-network"

echo "🚧 Creating project folder: $REPO_NAME"
mkdir $REPO_NAME && cd $REPO_NAME

echo "📦 Initializing Node project"
npm init -y

echo "📥 Installing Eleventy"
npm install --save-dev @11ty/eleventy

echo "🗂️ Creating folder structure"
mkdir -p src/advice _includes _data .github/workflows

echo "✍️ Creating Eleventy config file"
cat <<'EOF' > .eleventy.js
module.exports = function(eleventyConfig) {
  eleventyConfig.addPassthroughCopy("styles.css");

  eleventyConfig.addCollection("advice", function(collectionApi) {
    return collectionApi.getFilteredByGlob("./src/advice/*.md");
  });

  return {
    dir: {
      input: "src",
      includes: "../_includes",
      output: "_site"
    }
  };
};
EOF

echo "📄 Creating homepage"
cat <<'EOF' > src/index.md
---
layout: layout.njk
title: Alexithymia Awareness Network
---

# Welcome to the Alexithymia Awareness Network

This site is a curated guide for people exploring or living with alexithymia. It gathers trusted insights, practical advice, and shared experiences from the /r/alexithymia community.
EOF

echo "📄 Creating first advice content"
cat <<'EOF' > src/advice/recognizing-emotions.md
---
layout: layout.njk
title: Recognizing Emotions
---

## Recognizing Emotions When You Can’t Feel Them

- You may not feel sadness, but your body might.
- Cravings, fatigue, irritability, or numbness may be signs.
- Try body scans and journaling bodily sensations to start tracking.

> “I learned that when I start craving sugar and I’m snapping at people, I’m probably overwhelmed.” — /r/alexithymia user
EOF

echo "🧱 Creating basic layout"
cat <<'EOF' > _includes/layout.njk
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{{ title }}</title>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <header>
    <h1><a href="/">Alexithymia Awareness Network</a></h1>
    <nav>
      <a href="/">Home</a> | <a href="/advice/">Advice</a>
    </nav>
    <hr/>
  </header>
  <main>
    {{ content | safe }}
  </main>
</body>
</html>
EOF

echo "🎨 Creating minimal stylesheet"
cat <<'EOF' > styles.css
body {
  font-family: sans-serif;
  max-width: 700px;
  margin: 2rem auto;
  padding: 1rem;
  line-height: 1.6;
}
header a {
  text-decoration: none;
}
nav a {
  margin-right: 10px;
}
EOF

echo "⚙️ Creating GitHub Actions workflow"
cat <<'EOF' > .github/workflows/deploy.yml
name: Deploy Eleventy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  build-deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm install

      - name: Build site
        run: npx eleventy

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_site
EOF

echo "✅ Initial build"
npx eleventy

# Pause for user action
echo ""
echo "🧑‍💻 Next steps (Manual Actions Required):"
echo "1. Create a GitHub repo called: $REPO_NAME"
echo "2. Push this folder to GitHub:"
echo "   git init"
echo "   git remote add origin git@github.com:<your-username>/$REPO_NAME.git"
echo "   git add . && git commit -m 'Initial commit'"
echo "   git push -u origin main"
echo ""
echo "3. Go to GitHub ➝ Settings ➝ Pages:"
echo "   - Set Source = 'Deploy from a GitHub Action'"
echo ""
echo "4. (Optional) Configure custom domain:"
echo "   - Enter: alexithymiaawarenessnetwork.org"
echo "   - Add CNAME file if needed: echo 'alexithymiaawarenessnetwork.org' > CNAME"
echo ""
echo "When done, push any changes and your site will auto-deploy 🚀"

