"""Tests for UI theme generator and persona generator."""
import pytest
from forgix.interface.ui_generator import UIGenerator, THEMES, THEME_MAP
from forgix.persona.generator import PersonaGenerator, PERSONAS, PERSONA_MAP


class TestUIGenerator:
    def test_theme_selected_on_init(self):
        gen = UIGenerator()
        assert gen.current_theme is not None
        assert gen.current_theme["name"]

    def test_theme_has_required_keys(self):
        gen = UIGenerator()
        required = {"name", "bg", "surface", "accent", "text", "font"}
        assert required.issubset(gen.current_theme.keys())

    def test_force_theme_by_id(self):
        for theme in THEMES:
            gen = UIGenerator(force=theme["id"])
            assert gen.current_theme["id"] == theme["id"]

    def test_force_invalid_theme_falls_back_to_random(self):
        gen = UIGenerator(force="nonexistent_theme_xyz")
        assert gen.current_theme is not None

    def test_all_ten_themes_exist(self):
        assert len(THEMES) == 10

    def test_theme_ids_unique(self):
        ids = [t["id"] for t in THEMES]
        assert len(ids) == len(set(ids))

    def test_theme_map_has_all_ids(self):
        for theme in THEMES:
            assert theme["id"] in THEME_MAP

    def test_render_chat_page_returns_html(self):
        gen = UIGenerator()
        html = gen.render_chat_page(token="test-token", csrf="test-csrf", persona_name="Feynman")
        assert "<html" in html.lower() or "<!doctype" in html.lower()

    def test_render_chat_page_injects_token_as_json(self):
        import json
        gen = UIGenerator()
        token = "tok-123"
        csrf = "csrf-abc"
        html = gen.render_chat_page(token=token, csrf=csrf, persona_name="Test")
        assert json.dumps(token) in html
        assert json.dumps(csrf) in html

    def test_render_chat_page_contains_persona_name(self):
        gen = UIGenerator()
        html = gen.render_chat_page(token="x", csrf="y", persona_name="Ada Lovelace")
        assert "Ada Lovelace" in html

    def test_random_theme_varies_across_boots(self):
        themes_seen = set()
        for _ in range(50):
            gen = UIGenerator()
            themes_seen.add(gen.current_theme["id"])
        assert len(themes_seen) > 1

    def test_each_theme_renderable(self):
        for theme in THEMES:
            gen = UIGenerator(force=theme["id"])
            html = gen.render_chat_page(token="t", csrf="c", persona_name="Test")
            assert html and len(html) > 500


class TestPersonaGenerator:
    def test_persona_selected_on_init(self):
        gen = PersonaGenerator()
        assert gen.current_figure
        assert gen.current_description

    def test_system_prompt_not_empty(self):
        gen = PersonaGenerator()
        assert len(gen.system_prompt) > 100

    def test_system_prompt_contains_figure_name(self):
        gen = PersonaGenerator()
        assert gen.current_figure in gen.system_prompt

    def test_twenty_personas_exist(self):
        assert len(PERSONAS) == 20

    def test_persona_keys_unique(self):
        keys = [p.key for p in PERSONAS]
        assert len(keys) == len(set(keys))

    def test_persona_map_has_all_keys(self):
        for persona in PERSONAS:
            assert persona.key in PERSONA_MAP

    def test_force_persona_by_key(self):
        gen = PersonaGenerator(force="feynman")
        assert "Feynman" in gen.current_figure

    def test_force_invalid_falls_back_to_random(self):
        gen = PersonaGenerator(force="doesnotexist_xyz")
        assert gen.current_figure

    def test_random_persona_varies_across_boots(self):
        figures_seen = set()
        for _ in range(50):
            gen = PersonaGenerator()
            figures_seen.add(gen.current_figure)
        assert len(figures_seen) > 1

    def test_security_mode_in_system_prompt(self):
        gen = PersonaGenerator()
        assert "MAXIMUM" in gen.system_prompt or "jailbreak" in gen.system_prompt.lower()

    def test_all_personas_have_system_prompt(self):
        for persona in PERSONAS:
            gen = PersonaGenerator(force=persona.key)
            assert len(gen.system_prompt) > 200
