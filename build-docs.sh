#!/bin/bash
set -e

# Install dependencies
pip install mkdocs mkdocs-material pymdown-extensions

# Build the documentation
mkdocs build

# If this is running in a GitHub Action, deploy to GitHub Pages
if [ "$CI" = "true" ]; then
    echo "Deploying to GitHub Pages..."
    # Use the GitHub token to deploy
    mkdocs gh-deploy --force
fi

echo "Documentation built successfully!"
