# Custom Theme Documentation

This directory contains the custom theme components for the Alexithymia Awareness Network site.

## Structure

```
theme/
├── partials/
│   ├── gtm-head.html      # Google Tag Manager script for <head>
│   └── gtm-body.html      # Google Tag Manager noscript for <body>
├── main.html              # Main template override
└── README.md              # This documentation
```

## Google Analytics Implementation

The Google Analytics tracking is implemented using Google Tag Manager (GTM) with ID: `GTM-W3N69DDW`

### Components:

1. **gtm-head.html** - Contains the GTM JavaScript code that loads in the `<head>` section
2. **gtm-body.html** - Contains the GTM noscript fallback that loads immediately after `<body>`
3. **main.html** - Extends the Material theme's base template and includes both GTM partials

### Benefits:

- ✅ **Write once, use everywhere**: GTM code is written once in partials and automatically included on all pages
- ✅ **Theme agnostic**: Easy to switch MkDocs themes while keeping analytics
- ✅ **Easy maintenance**: Update GTM code in one place to change across entire site
- ✅ **Composable**: Other tracking codes or components can be added as additional partials

## Theme Switching

To switch themes while keeping analytics:

1. Change the theme name in `mkdocs.yml`:
   ```yaml
   theme:
     name: readthedocs  # or any other theme
     custom_dir: theme/
   ```

2. The custom partials will automatically be included in the new theme

## Adding New Components

To add new reusable components:

1. Create a new partial in `theme/partials/`
2. Include it in `main.html` using `{% include "partials/filename.html" %}`
3. The component will be available across all pages

## Configuration

The theme is configured in `mkdocs.yml`:

```yaml
theme:
  name: material
  custom_dir: theme/
```

This tells MkDocs to use the Material theme as the base and override/extend it with files from the `theme/` directory.
