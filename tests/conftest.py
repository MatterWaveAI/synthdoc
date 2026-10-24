"""Shared fixtures for template tests."""
import pytest
from synthdoc.templates import registry


def pytest_addoption(parser):
    parser.addoption(
        "--template",
        action="store",
        default=None,
        help="Run tests for a specific template name only",
    )
    parser.addoption(
        "--category",
        action="store",
        default=None,
        help="Run tests for a specific category only",
    )
    parser.addoption(
        "--run-pagedjs",
        action="store_true",
        default=False,
        help="Run slow Paged.js browser rendering tests",
    )


def get_template_names(config):
    """Get filtered list of template names based on CLI options."""
    names = sorted(registry.list_templates())

    selected = config.getoption("--template")
    if selected:
        names = [n for n in names if n == selected]

    category = config.getoption("--category")
    if category:
        names = [
            n for n in names
            if registry.get_category(n) == category
        ]

    return names


def pytest_generate_tests(metafunc):
    """Parametrize tests dynamically based on registered templates."""
    if "template_name" in metafunc.fixturenames:
        names = get_template_names(metafunc.config)
        metafunc.parametrize("template_name", names)


@pytest.fixture
def template_instance(template_name):
    """Create a template instance from its registered name."""
    return registry.get_template_instance(template_name)
