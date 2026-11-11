"""What the plugin attaches to (plugin API 2.2, apis.py): the core datasets' card is sound, names the files the
plugin's datasets really read (their addresses) and the git history the app imports for them, among the core datasets'
others, and every address on it is the makers' own. The page check (each address asked once) runs only with
LIMINAL_VENDOR_PAGES=1, the weekly CI run's; nothing is sent otherwise. The user, 2026-11-11: "each plugin should
reflect the the API its attached to, and present links that provide documentation"."""
from __future__ import annotations

import os
from datetime import date
from urllib.parse import urlsplit

import pytest

from liminal_libs.sources.apis import dead_links, problems, urls

import plugin_integrator_datahub as datahub
from plugin_integrator_datahub.apis import APIS, CORE_DATASETS, HISTORY, RAW_FILES


def test_the_card_is_sound_and_is_the_plugins():
    assert problems(APIS, today=date(2026, 11, 11)) == []
    assert datahub.PUBLISHER.apis == APIS and datahub.Datahub.apis is APIS
    assert CORE_DATASETS.docs == "https://docs.datahub.io/core-data" and CORE_DATASETS.verified == "2026-11-11"
    assert datahub.PUBLISHER.interface()["apis"] == ["Datahub core datasets"]
    assert datahub.PUBLISHER.api_facts() == {}  # it learns nothing while it runs: the app reads its files


def test_the_card_names_the_files_and_the_history_the_plugin_really_reads():
    """Each raw file it reads is one of its datasets' files (by its address under the card's base), and each of
    those is a call on the card; each dataset's git history (the app's submodule) is the git calls'."""
    read = {url for d in datahub.DATASETS for url, _ in d.files(date(2026, 11, 11))}
    got = {CORE_DATASETS.base + c.name.removeprefix("GET ") for c in CORE_DATASETS.used if c.name.startswith("GET ")}
    assert got == read and CORE_DATASETS.base == datahub.RAW
    assert all(d.git and d.git[1] in {u.removeprefix(datahub.RAW).split("/main/")[1] for u in read}
               for d in datahub.DATASETS)  # each dataset's history is its raw file's
    git = [c for c in CORE_DATASETS.used if c.name.startswith("git ")]
    assert {c.name.split()[1] for c in git} == {"fetch", "log", "show", "checkout"} and all(c.area == HISTORY for c in git)
    covered = {a.name for a in CORE_DATASETS.covered}
    assert {RAW_FILES, HISTORY} <= covered and len(covered) == 5
    assert all(c.area in {a.name for a in CORE_DATASETS.areas} for c in CORE_DATASETS.calls)
    assert len(CORE_DATASETS.areas) > len(covered) and len(CORE_DATASETS.calls) > len(CORE_DATASETS.used)
    assert not any(c.writes or c.costs for c in CORE_DATASETS.calls)  # files read, nothing changed, nothing billed


def test_every_address_is_the_makers_own():
    hosts = {urlsplit(u).hostname for u in urls(APIS)}
    assert hosts == {"docs.datahub.io", "datahub.io", "github.com", "datapackage.org", "git-scm.com"}


@pytest.mark.skipif(not os.environ.get("LIMINAL_VENDOR_PAGES"),
                    reason="LIMINAL_VENDOR_PAGES=1 asks each address on the card (the weekly CI run)")
def test_every_address_on_the_card_answers():
    assert dead_links(APIS) == []
