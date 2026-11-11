"""What the plugin attaches to (plugin API 2.2, liminal_libs.sources.apis), as Datahub's and GitHub's own pages describe
it (read 2026-11-11): Datahub's core datasets, each a data package in a public GitHub repository of the `datasets`
organization, read as raw files from raw.githubusercontent.com or, where the app has the repository as a git submodule,
from its whole commit history. The three datasets the plugin reads come first, then the rest of what the core
datasets offer. The user, 2026-11-11: "each plugin should reflect the the API its attached to, and present links that
provide documentation ... it should also expose more of what the API is about"."""
from __future__ import annotations

from liminal_libs.sources.apis import Api, Area, Call, Link

RAW = "https://raw.githubusercontent.com/datasets/"  # each dataset repository's files (the plugin's RAW)
GITHUB = "https://github.com/datasets"
CORE = "https://datahub.io/core/"
DOCS = "https://docs.datahub.io/"
GIT = "https://git-scm.com/docs/"
VERIFIED = "2026-11-11"  # the day these facts were read from the makers' pages

COMPANIES = "S&P 500 companies"
SHILLER = "S&P 500 and Shiller's data"
COMMODITIES = "Commodity prices"
RAW_FILES = "Raw files"
HISTORY = "Commit history"

CORE_DATASETS = Api(
    name="Datahub core datasets",
    maker="Datahub's Core Data Curators (the datasets organization on GitHub)",
    about=("Datahub's core datasets are commonly used reference data (indexes and their members, prices, rates, codes) "
           "kept as open data packages: each a public GitHub repository holding CSV files and a datapackage.json that "
           "describes them, versioned with git so every change is a commit. They are read as files, from GitHub's raw "
           "host or from the repository itself, or through datahub.io's stable file links; there is no query API."),
    kind="feed",
    base=RAW,
    version="the data packages' main branch (CSV files described by datapackage.json)",
    auth="none: public repositories and files",
    limits=("none published for these files; the plugin keeps its own: at most 40 requests a day, an hour apart at "
            "least, from github.com and raw.githubusercontent.com only"),
    costs="",
    links=(
        Link("Core Data", DOCS + "core-data", "docs"),
        Link("Core datasets", CORE, "reference"),
        Link("The datasets organization on GitHub", GITHUB, "source"),
        Link("Core Data Curators Guide", DOCS + "core-data/curators-guide", "guide"),
        Link("Data Package standard", "https://datapackage.org/", "spec"),
        Link("Datahub terms of service", DOCS + "terms-of-service", "terms"),
    ),
    areas=(
        Area(COMPANIES, "the S&P 500's members with their GICS sector and sub-industry, date added and CIK "
                        "(datasets/s-and-p-500-companies)", GITHUB + "/s-and-p-500-companies",
             covered="sp500-constituents: the market map's sectors for S&P 500 members, every version"),
        Area(SHILLER, "Robert J. Shiller's monthly S&P composite, dividends, earnings, CPI, long rate and CAPE from 1871 "
                      "(datasets/s-and-p-500)", CORE + "s-and-p-500",
             covered="shiller-us-market-monthly, every version"),
        Area(COMMODITIES, "the IMF's primary commodity prices and indexes, monthly from 1980, a mirror no longer updated "
                          "(datasets/commodity-prices)",
             CORE + "commodity-prices", covered="imf-commodities-monthly, an archive closed once imported"),
        Area(RAW_FILES, "each repository's files at raw.githubusercontent.com/datasets/<repository>/main/<path>",
             GITHUB, covered="each dataset's file, where its submodule is not checked out"),
        Area(HISTORY, "each repository's git history: every commit of a file a version of it", GITHUB,
             covered="every commit of each file imported as a published version, where the app's data/github/datasets/ "
                     "submodule is checked out"),
        Area("Data packages", "datapackage.json: each dataset's files, fields, types, sources and licence",
             "https://datapackage.org/"),
        Area("Datahub file links", "a stable address on datahub.io for each file of a dataset "
                                   "(datahub.io/core/<dataset>/_r/-/<path>)", CORE + "s-and-p-500"),
        Area("Nasdaq and NYSE listings", "the listed companies of Nasdaq, the NYSE and the other US exchanges",
             CORE + "nasdaq-listings"),
        Area("S&P 500 companies with financials", "the S&P 500's members with financial information",
             CORE + "s-and-p-500-companies-financials"),
        Area("US Consumer Price Index", "the US consumer price index and inflation", CORE + "cpi-us"),
        Area("US 10-year bond yields", "the 10-year US government bond yield (the long-term interest rate)",
             CORE + "bond-yields-us-10y"),
        Area("Gold, oil and natural gas prices", "gold prices, Brent and WTI spot prices, natural gas prices",
             CORE + "gold-prices"),
        Area("Exchange rates and Euribor", "the US dollar to euro exchange rate since 1999, and the Euribor benchmark rates",
             CORE + "exchange-rates"),
    ),
    calls=(
        Call("GET s-and-p-500-companies/main/data/constituents.csv", "the S&P 500's members", COMPANIES,
             used="sp500-constituents (its latest version)", docs=GITHUB + "/s-and-p-500-companies"),
        Call("GET s-and-p-500/main/data/data.csv", "Shiller's monthly data from 1871", SHILLER,
             used="shiller-us-market-monthly (its latest version)", docs=CORE + "s-and-p-500"),
        Call("GET commodity-prices/main/data/commodity-prices.csv", "the IMF's commodity prices", COMMODITIES,
             used="imf-commodities-monthly (final: closed once imported)", docs=CORE + "commodity-prices"),
        Call("git fetch --quiet origin", "the submodule's newest commits from github.com", HISTORY,
             used="each dataset's history brought up to date (every 7 or 30 days)", docs=GIT + "git-fetch"),
        Call("git log --reverse --format=%H %cI <ref> -- <path>", "every commit of the dataset's file, oldest first",
             HISTORY, used="the versions not imported yet", docs=GIT + "git-log"),
        Call("git show <commit>:<path>", "the file as one commit left it", HISTORY,
             used="each version's rows", docs=GIT + "git-show"),
        Call("git checkout --quiet --detach <ref>", "the submodule at the repository's newest commit", HISTORY,
             used="the file's latest version left checked out", docs=GIT + "git-checkout"),
        Call("GET <repository>/main/datapackage.json", "a dataset's description: its files, fields and licence",
             "Data packages", docs="https://datapackage.org/"),
        Call("GET datahub.io/core/<dataset>/_r/-/<path>", "a dataset's file by its stable Datahub link",
             "Datahub file links", docs=CORE + "s-and-p-500"),
        Call("GET nasdaq-listings/main/data/nasdaq-listed.csv", "Nasdaq's listed companies",
             "Nasdaq and NYSE listings", docs=CORE + "nasdaq-listings"),
    ),
    verified=VERIFIED,
)

APIS = (CORE_DATASETS,)
