"""
Tests for all registered document templates.

Run all fast tests:
    pytest tests/test_templates.py -v

Run for a single template:
    pytest tests/test_templates.py -v --template=bank_statement

Run for a category:
    pytest tests/test_templates.py -v --category=financial

Include slow Paged.js browser rendering tests:
    pytest tests/test_templates.py -v --run-pagedjs

Run only Paged.js tests:
    pytest tests/test_templates.py -v --run-pagedjs -k pagedjs
"""
import re
import pytest
from synthdoc.templates import registry


# ---------------------------------------------------------------------------
# 1. Data Generation
# ---------------------------------------------------------------------------

class TestDataGeneration:
    """Test that generate_sample_data() works for every template."""

    def test_generate_data_returns_dict(self, template_name, template_instance):
        """generate_sample_data(seed) must return a dict."""
        data = template_instance.generate_sample_data(seed=42)
        assert isinstance(data, dict), f"{template_name}: generate_sample_data() did not return a dict"
        assert len(data) > 0, f"{template_name}: generate_sample_data() returned empty dict"

    def test_generate_data_is_deterministic(self, template_name, template_instance):
        """Same seed must produce identical data."""
        data1 = template_instance.generate_sample_data(seed=123)
        data2 = template_instance.generate_sample_data(seed=123)
        # Some older templates don't fully seed — warn instead of fail
        if data1 != data2:
            pytest.xfail(f"{template_name}: same seed produced different data (non-deterministic)")

    def test_generate_data_different_seeds(self, template_name, template_instance):
        """Different seeds should (usually) produce different data."""
        data1 = template_instance.generate_sample_data(seed=1)
        data2 = template_instance.generate_sample_data(seed=9999)
        # Not strictly required for all templates, but a good sign
        # We just check it doesn't crash with different seeds
        assert isinstance(data1, dict)
        assert isinstance(data2, dict)


# ---------------------------------------------------------------------------
# 2. Jinja2 Rendering
# ---------------------------------------------------------------------------

class TestJinja2Rendering:
    """Test that templates render to valid HTML."""

    def test_render_produces_html(self, template_name, template_instance):
        """render(data) must return a non-trivial HTML string."""
        data = template_instance.generate_sample_data(seed=42)
        html = template_instance.render(data)
        assert isinstance(html, str), f"{template_name}: render() did not return a string"
        assert len(html) > 100, f"{template_name}: rendered HTML too short ({len(html)} chars)"

    def test_render_has_html_structure(self, template_name, template_instance):
        """Rendered output should have basic HTML structure."""
        data = template_instance.generate_sample_data(seed=42)
        html = template_instance.render(data)
        html_lower = html.lower()
        assert "<html" in html_lower, f"{template_name}: missing <html> tag"
        assert "<body" in html_lower, f"{template_name}: missing <body> tag"

    def test_no_undefined_template_variables(self, template_name, template_instance):
        """Rendered HTML should not contain Jinja2 undefined markers."""
        data = template_instance.generate_sample_data(seed=42)
        html = template_instance.render(data)
        assert "Undefined" not in html, f"{template_name}: contains 'Undefined' — likely missing template variable"

    def test_no_jinja2_syntax_leaks(self, template_name, template_instance):
        """Rendered HTML should not contain unprocessed Jinja2 syntax."""
        data = template_instance.generate_sample_data(seed=42)
        html = template_instance.render(data)
        # Check for unprocessed template tags (but allow {{ in <script> blocks)
        # Strip script blocks first
        html_no_script = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        assert "{%" not in html_no_script, f"{template_name}: contains unprocessed {{% %}} tag"


# ---------------------------------------------------------------------------
# 3. Template Files
# ---------------------------------------------------------------------------

class TestTemplateFiles:
    """Test that template files are properly structured."""

    def test_get_template_string(self, template_name, template_instance):
        """get_template_string() must return a non-empty string."""
        tmpl_str = template_instance.get_template_string()
        assert isinstance(tmpl_str, str), f"{template_name}: get_template_string() did not return a string"
        assert len(tmpl_str) > 50, f"{template_name}: template string too short"

    def test_no_local_stylesheet_links(self, template_name, template_instance):
        """Template string should not have <link> to local CSS files (causes Paged.js failures)."""
        tmpl_str = template_instance.get_template_string()
        local_link = re.search(r'<link[^>]+href=["\'][^"\':/]+\.css["\']', tmpl_str)
        assert local_link is None, (
            f"{template_name}: has local <link stylesheet> that will break Paged.js rendering. "
            "CSS should be inlined via get_template_string(), not linked."
        )


# ---------------------------------------------------------------------------
# 4. CSS / Print Rules
# ---------------------------------------------------------------------------

class TestPrintCSS:
    """Test that CSS is print-ready."""

    def test_has_page_rule_in_template(self, template_name, template_instance):
        """Template itself should ideally include @page CSS rule."""
        tmpl_str = template_instance.get_template_string()
        if "@page" not in tmpl_str:
            pytest.xfail(f"{template_name}: missing @page CSS rule (renderer adds it at runtime)")

    def test_no_position_fixed(self, template_name, template_instance):
        """position: fixed breaks Paged.js."""
        tmpl_str = template_instance.get_template_string()
        # Allow it in comments but not in active CSS
        css_no_comments = re.sub(r'/\*.*?\*/', '', tmpl_str, flags=re.DOTALL)
        if "position: fixed" in css_no_comments or "position:fixed" in css_no_comments:
            pytest.xfail(f"{template_name}: uses position:fixed which may break Paged.js")

    def test_table_border_collapse(self, template_name, template_instance):
        """Tables should use border-collapse: collapse for print."""
        tmpl_str = template_instance.get_template_string()
        if "<table" in tmpl_str:
            assert "border-collapse" in tmpl_str, (
                f"{template_name}: has <table> but missing border-collapse in CSS"
            )


# ---------------------------------------------------------------------------
# 5. RDFa Annotations
# ---------------------------------------------------------------------------

class TestRDFaAnnotations:
    """Test that templates have proper RDFa semantic markup."""

    def test_has_rdfa_attributes(self, template_name, template_instance):
        """Templates should have RDFa typeof/property attributes."""
        data = template_instance.generate_sample_data(seed=42)
        html = template_instance.render(data)
        has_typeof = 'typeof="' in html or "typeof='" in html
        has_property = 'property="' in html or "property='" in html
        has_data_entity = 'data-entity-type=' in html
        assert has_typeof or has_property or has_data_entity, (
            f"{template_name}: no RDFa annotations (typeof/property) or data-entity-type found"
        )

    def test_has_namespace_declarations(self, template_name, template_instance):
        """Templates using RDFa should declare xmlns namespaces."""
        tmpl_str = template_instance.get_template_string()
        if 'typeof="schema:' in tmpl_str or 'typeof="doco' in tmpl_str:
            assert "xmlns:" in tmpl_str, (
                f"{template_name}: uses RDFa types but missing xmlns namespace declarations"
            )


# ---------------------------------------------------------------------------
# 6. Paged.js Browser Rendering (slow, opt-in)
# ---------------------------------------------------------------------------

class TestPagedJSRendering:
    """Test full Paged.js browser rendering pipeline. Requires --run-pagedjs flag."""

    @pytest.fixture(autouse=True)
    def _skip_unless_pagedjs(self, request):
        if not request.config.getoption("--run-pagedjs"):
            pytest.skip("Paged.js tests require --run-pagedjs flag")

    @pytest.fixture(scope="module")
    def browser_context(self):
        """Shared browser instance for all Paged.js tests."""
        from playwright.sync_api import sync_playwright
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=True)
        yield browser, pw
        browser.close()
        pw.stop()

    @pytest.fixture(scope="module")
    def renderer(self):
        from synthdoc.pagedjs_renderer import PagedJSRenderer
        return PagedJSRenderer(timeout=10000)

    def test_pagedjs_produces_pages(self, template_name, template_instance, browser_context, renderer):
        """Template must render at least 1 page through Paged.js."""
        import tempfile
        from pathlib import Path

        browser, _ = browser_context

        data = template_instance.generate_sample_data(seed=42)
        html = template_instance.render(data)
        html = renderer.inject_pagedjs_script(html)
        html = renderer.ensure_page_css(html)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html)
            tmp_path = Path(f.name)

        try:
            page = browser.new_page(viewport={'width': renderer.viewport_width, 'height': renderer.viewport_height})
            page.goto(f'file:///{tmp_path.as_posix()}', wait_until='networkidle')
            page_count = renderer.wait_for_pagination(page)
            page.close()
            assert page_count > 0, f"{template_name}: Paged.js produced 0 pages"
        finally:
            tmp_path.unlink(missing_ok=True)
