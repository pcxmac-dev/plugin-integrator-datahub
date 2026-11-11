"""The Datahub plugin, run against the library installed beside it: its parsers, its class on the
plugin contract, and the app loading it from this package with its own version and the datasets it
declared as a built-in."""
from __future__ import annotations

from datetime import date
from importlib.metadata import version
from pathlib import Path

from liminal_libs.sources import publishers, registry
from liminal_libs.sources.publisher import PublisherPlugin

import plugin_integrator_datahub as datahub
from plugin_integrator_datahub import Datahub


def own_version(p) -> str:
    """The version the app shows for it: its checkout's pyproject.toml when it is loaded from the workspace's
    plugin directory (an editable install's metadata can lag behind a release), else its installed
    distribution's."""
    if p.origin.startswith("plugins/"):
        import tomllib

        pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
        return tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]["version"]
    return version("plugin-integrator-datahub")


def test_commodities_skip_missing_cells():
    parsed = datahub.parse_commodities("c.csv", b"Date,All Commodity Price Index,Gold\n1980-02-01,nan,35.2\n"
                                                 b"1980-03-01,101.5,\n")
    assert sorted((s, v) for s, _, v in parsed.values) == [("All Commodity Price Index", 101.5), ("Gold", 35.2)]
    assert parsed.series["Gold"][1] == "USD (nominal)" and parsed.series["All Commodity Price Index"][1] == "index (2005 = 100)"


def test_shiller_dates_in_every_format_the_files_have_used_and_zeros_are_missing():
    d = datahub.shiller_date
    assert [d("2026-09-01"), d("1871.01"), d("1871.1"), d("1871.04166"), d("1871.95833")] == [
        date(2026, 9, 1), date(1871, 1, 1), date(1871, 10, 1), date(1871, 1, 1), date(1871, 12, 1)]
    parsed = datahub.parse_shiller("s.csv", b"Date,SP500,Earnings,PE10\n1871-01-01,4.44,0.4,0\n2026-08-01,7711.32,0,0\n")
    assert sorted(parsed.series) == ["Earnings", "SP500"]  # PE10 had only zeros: no values, no series
    assert parsed.series["SP500"] == ("SP500", "index", "month") and len(parsed.values) == 3


def test_constituents_carry_the_market_maps_sector_names():
    blob = (b"Symbol,Security,GICS Sector,GICS Sub-Industry,Headquarters Location,Date added,CIK,Founded\n"
            b"AAPL,Apple Inc.,Information Technology,Technology Hardware,Cupertino,1982-11-30,0000320193,1977\n"
            b"JPM,JPMorgan Chase,Financials,Diversified Banks,New York,1975-06-30,0000019617,2000\n")
    rows = datahub.parse_constituents("c.csv", blob).constituents
    assert [(r["ticker"], r["sector"], r["industry"], r["added"]) for r in rows] == [
        ("AAPL", "Technology", "Technology Hardware", "1982-11-30"), ("JPM", "Financial", "Diversified Banks", "1975-06-30")]
    assert rows[0]["index"] == "S&P 500" and rows[0]["cik"] == "0000320193"
    old = datahub.parse_constituents("c.csv", b"Symbol,Name,Sector\nMSFT,Microsoft,Information Technology\n").constituents
    assert old == [{"index": "S&P 500", "ticker": "MSFT", "name": "Microsoft", "sector": "Technology", "industry": "",
                    "added": None, "cik": None}]  # the mirror's older versions: Name, Sector


def test_it_is_a_class_on_the_plugin_contract():
    """The publisher is an instance of its class (plugin API 2.2), what it declares its class's
    attributes, its hooks the contract's defaults; the app loads it as that class."""
    p = datahub.PUBLISHER
    assert type(p) is Datahub and issubclass(Datahub, PublisherPlugin) and not p.is_record
    assert p.api == "2.2" and Datahub.api == "2.2" and p.KIND == "publisher"
    assert not p.has_moments and not p.has_calendar and not p.reads_itself and not p.has_settings
    assert p.moments(date(2026, 11, 3)) == () and p.calendar(date(2026, 11, 3)) == []  # the contract's defaults
    assert Datahub.datasets is datahub.DATASETS and p.datasets == datahub.DATASETS
    moved = p.with_(order=1)  # a changed copy, the registry's way (its origin and version)
    assert type(moved) is Datahub and moved.order == 1 and p.order == 410 and moved.datasets == p.datasets
    registry.reload()
    loaded = publishers()["datahub"]
    assert type(loaded) is Datahub and loaded.api == "2.2" and loaded.version == own_version(loaded)
    assert registry.api_refusal(loaded.api, record=loaded.is_record) is None
    assert not [why for where, why in registry.errors() if "datahub" in where or "datahub" in why]


def test_the_app_loads_it_from_this_package_with_its_own_version():
    registry.reload()
    p = publishers().get("datahub")
    assert p is not None, dict(registry.errors())
    assert p.origin in {"package: plugin-integrator-datahub (plugin_integrator_datahub:PUBLISHER)", "plugins/plugin-integrator-datahub (plugin_integrator_datahub:PUBLISHER)"}  # its package, or its checkout in the workspace\'s plugin directory
    assert p.version == own_version(p) and datahub.PUBLISHER.version == ""
    assert registry.api_refusal(p.api) is None and p.api == "2.2"
    assert not [why for where, why in registry.errors() if "datahub" in where or "datahub" in why]
    assert (p.title, p.kind, p.feeds) == ("Datahub", "mirror", ())
    assert {d.name: (d.provider, d.git) for d in p.datasets} == {
        "sp500-constituents": ("sp500", ("datasets/s-and-p-500-companies", "data/constituents.csv")),
        "shiller-us-market-monthly": ("shiller", ("datasets/s-and-p-500", "data/data.csv")),
        "imf-commodities-monthly": ("imf", ("datasets/commodity-prices", "data/commodity-prices.csv"))}
    assert set(p.policy.hosts) == {"github.com", "raw.githubusercontent.com"}
    assert all(url.startswith("https://raw.githubusercontent.com/datasets/") for d in p.datasets
               for url, _ in d.files(date(2026, 11, 1)))
