# plugin-integrator-datahub

Datahub's core datasets (datahub.io; github.com/datasets) for
[Liminal](https://github.com/pcxmac-dev/liminal-charts): free reference data kept as CSV files in public
GitHub repositories (ODC PDDL), each a mirror of someone else's data:

- the S&P 500's members with their GICS sector and sub-industry (`sp500-constituents`): the market
  map's sectors;
- Robert J. Shiller's US stock market data (`shiller-us-market-monthly`): the S&P composite,
  dividends, earnings, CPI, rates and CAPE, monthly from 1871;
- the IMF's primary commodity prices (`imf-commodities-monthly`): 53 commodities and 10 indexes,
  monthly 1980-2017, a frozen mirror (an archive, closed once imported; IMF terms: personal,
  non-commercial use).

Each repository is a git submodule of the app's repository (`data/github/datasets/`, where the
app's `LIMINAL_DATA_REPOS` points) whose whole commit history is imported, each commit a published
version; downloaded from raw.githubusercontent.com where the submodule is not checked out. No key.

A Liminal publisher plugin released on its own. The app finds it through the entry point group
`liminal.providers` and lists it on the Plugins view and in `liminal-charts plugins`
as `package: plugin-integrator-datahub`, with this package's version.

## Install

Into the app's environment, from the app's folder:

```powershell
.venv\Scripts\python.exe -m pip install "plugin-integrator-datahub @ git+https://github.com/pcxmac-dev/plugin-integrator-datahub@v0.3.0"
```

or with the app's plugins (`pip install -e ".[plugins]"` in liminal-charts). The app loads it on its next
start.

## Its API

There is no query API: Datahub's [core datasets](https://datahub.io/core/) ([Core Data](https://docs.datahub.io/core-data))
are data packages, each a public repository of the [`datasets` organization](https://github.com/datasets) on GitHub
holding CSV files and a `datapackage.json` ([the Data Package standard](https://datapackage.org/)), versioned with git.
The plugin reads three of them: [s-and-p-500-companies](https://github.com/datasets/s-and-p-500-companies),
[s-and-p-500](https://datahub.io/core/s-and-p-500) and [commodity-prices](https://datahub.io/core/commodity-prices),
each file's every commit through the app's submodule, or its latest from raw.githubusercontent.com. No key, no
published limit (the plugin keeps to 40 requests a day, an hour apart), nothing to pay.

`Datahub.apis` (`apis.py`, plugin API 2.2) says this on the plugin's page: the makers' pages, the core datasets' parts
(the ones read first, then the data packages' descriptions, Datahub's stable file links and the other finance
datasets: listings, S&P 500 financials, CPI, bond yields, commodities, exchange rates) and the calls made for it (the
three files, the four git commands) among the others, as read on 2026-11-11.

## Compatibility

It is written for plugin API 2.2, the class contract of liminal-libs 1.49.0 (`PUBLISHER.api`; the
publisher is `Datahub`, a `PublisherPlugin` subclass declaring its datasets and what it attaches to,
`PUBLISHER` its instance). An app offering 2.2 or a later 2.x loads it; an app of another major, or an
older 2.x, leaves it out and says why on the Plugins view.

## Develop

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install "liminal-libs @ git+https://github.com/pcxmac-dev/liminal-libs@release/0.2.0"
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe -m pytest -q
```

Tests never send requests and never read your keys.
