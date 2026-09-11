"""UI themes must land next to the existing ones without moving the
Sortable script tag (S4 hashes that region) or dropping old option values.
"""
import os

from retro.interface.bridge import Api
from retro.utils.config import Config


UI_DIR = os.path.join(os.path.dirname(__file__), "..", "retro", "interface", "assets")
INDEX = os.path.join(UI_DIR, "index.html")
FONTS = os.path.join(UI_DIR, "fonts", "fonts")

KEPT_THEMES = ("legacy", "premium")
NEW_THEMES = ("cyberpunk", "nebula", "synthwave", "ember", "abyss", "plasma")
THEME_CLASSES = tuple(f"theme-{t}" for t in NEW_THEMES)
REQUIRED_FONTS = (
    "inter-400.woff2",
    "syne-700.woff2",
    "instrument-serif-400.woff2",
    "plus-jakarta-sans-400.woff2",
    "newsreader-400.woff2",
    "source-sans-3-400.woff2",
    "ibm-plex-mono-400.woff2",
    "space-grotesk.woff2",
    "outfit.woff2",
)


def _index_text():
    with open(INDEX, encoding="utf-8") as f:
        return f.read()


def _index_bytes():
    with open(INDEX, "rb") as f:
        return f.read()


def test_sortable_script_tag_untouched():
    data = _index_bytes()
    needle = b'<script src="Sortable.min.js"></script>'
    idx = data.find(needle)
    assert idx >= 0
    # S4 hashes 32 bytes before this tag through 224 bytes after it.
    region = data[max(0, idx - 32) : idx + 224]
    assert needle in region
    assert b"intersection-polyfill" not in region


def test_kept_theme_classes_and_options_present():
    html = _index_text()
    assert ".theme-legacy" in html
    assert 'value="legacy"' in html
    assert 'value="premium"' in html


def test_new_theme_classes_and_options_present():
    html = _index_text()
    for name in NEW_THEMES:
        assert f".theme-{name}" in html
        assert f'value="{name}"' in html
        assert f'"theme-{name}"' in html  # setUITheme classList.remove


def test_old_themes_removed():
    html = _index_text()
    removed = ("ignite", "matrix", "cherry", "studio", "nocturne", "mocha",
               "vellum", "aurora", "neko", "bw")
    for name in removed:
        assert f".theme-{name}" not in html, f".theme-{name} should be gone"
        assert f'value="{name}"' not in html, f'value="{name}" should be gone'


def test_new_theme_canvases_present():
    html = _index_text()
    for name in NEW_THEMES:
        assert f'id="{name}-canvas"' in html, name


def test_new_theme_animations_present():
    html = _index_text()
    for name in NEW_THEMES:
        cap = name.capitalize()
        assert f"toggle{cap}Anim" in html, name
        assert f"draw{cap}" in html, name
        assert f"resize{cap}" in html, name


def test_old_canvases_removed():
    html = _index_text()
    for cid in ("matrix-canvas", "petals-canvas", "aurora-canvas", "neko-canvas"):
        assert cid not in html, cid


def test_set_ui_theme_clears_every_skin_class():
    html = _index_text()
    start = html.find("function setUITheme")
    assert start > 0
    chunk = html[start : start + 1800]
    for cls in THEME_CLASSES:
        assert f'"{cls}"' in chunk, cls


def test_bundled_theme_fonts_exist():
    for name in REQUIRED_FONTS:
        path = os.path.join(FONTS, name)
        assert os.path.isfile(path), name
        assert os.path.getsize(path) > 1000, name


def test_set_ui_theme_persists_new_ids(monkeypatch):
    api = Api.__new__(Api)
    api.settings = {}
    monkeypatch.setattr(Config, "save_settings", lambda *_a, **_k: True)
    for name in NEW_THEMES:
        api.set_ui_theme(name)
        assert api.settings["ui_theme"] == name


def test_checker_compare_label_is_not_hash_compare():
    html = _index_text()
    assert "Comparing version hashes" not in html
    assert "Comparing Roblox vs offset dump" in html
    assert "CDN latest:" in html
    assert "Offset dump:" in html
    assert 'key: "compare"' in html
    assert "rvcGuidDetail" in html
