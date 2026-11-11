# Changelog

## 0.3.0 (2026-11-11)

Its API on its page (plugin API 2.2, liminal-libs 1.49.0; the user: "each plugin should reflect the the API its
attached to, and present links that provide documentation, the plugin interface should more or less contain what it
already has, BUT, it should also expose more of what the API is about"). `Datahub.apis` (apis.py) is the card of
Datahub's core datasets: data packages in the `datasets` organization's GitHub repositories, read as raw files or as
their git history, with Datahub's and GitHub's pages (Core Data, the core datasets, the organization, the curators'
guide, the Data Package standard, the terms), its parts (the three datasets it reads, the raw files and the commit
history; the data packages' descriptions, Datahub's file links and the other finance datasets it does not read) and
its calls (the three files and the four git commands the app makes for it, and the others), verified 2026-11-11.
Nothing it reads or does changes; it learns nothing while it runs, so `api_facts()` says nothing. Needs
liminal-libs>=1.49.0. A test checks that the card names the files and the history the plugin really reads;
`LIMINAL_VENDOR_PAGES=1` asks each address on it.

## 0.2.0 (2026-11-03)

Renamed `plugin-integrator-datahub` (the package `plugin_integrator_datahub`; it was `liminal-plugin-datahub`) on 2026-11-03: the naming by system (plugins are `plugin-<app>-<name>`), on liminal-libs 1.4.0 (`liminal_libs`, the library renamed with it).

A class on plugin API 2.0 (liminal-libs 1.3.0; the user: "all the plugins under liminal should basically
follow inheritance/oop paradigm"): `Datahub`, a `PublisherPlugin` subclass, declares what the `Publisher`
record held (its name, kind, datasets and scrape checks, as class attributes); `PUBLISHER` is its instance,
the entry point as before. Nothing it does or says changes. Version 0.2.0: every Liminal distribution is
released at 0.2.0 together, tested against the library's `release/0.2.0` branch until the release.

## 1.1.1 (2026-11-02)

The plugin imports the library as `liminal_libs` and depends on liminal-libs (the app, renamed liminal-charts, is no longer needed to run the tests; the user, 2026-11-02: "lets rename the app to liminal-charts").

## 1.1.0 (2026-11-01)

- Released as its own package, `plugin-integrator-datahub`, registered under the entry point group
  `liminal.providers`; its version is the distribution's. The mirrors' git submodules stay with the
  app (`data/github/datasets/`, `LIMINAL_DATA_REPOS`): the plugin names each repository and file.
- Plugin API 1.4.

## 1.0.0 (2026-10-31)

- Built into the app (then massive-collate): the three mirrors declared by this plugin (plugin API
  1.4).
