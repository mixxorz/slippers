from pathlib import Path, PosixPath

from django.apps import AppConfig
from django.template.loader import get_template, render_to_string
from django.utils.autoreload import autoreload_started, file_changed

import yaml

from slippers.templatetags.slippers import (
    register_block_components,
    register_inline_components,
)


def watch(sender, **kwargs):
    """Watch when component.yml changes"""
    template = get_template("components.yml")
    sender.extra_files.add(Path(template.origin.name))


def changed(sender, file_path: PosixPath, **kwargs):
    """Refresh tag registry when component.yml changes"""
    if file_path.name == "components.yml":
        print("components.yml changed. Updating component tags...")
        components = yaml.safe_load(render_to_string("components.yml"))
        register_inline_components(components["inline_components"])
        register_block_components(components["block_components"])


class SlippersConfig(AppConfig):
    name = "slippers"

    def ready(self):
        # Register tags from components.yml
        components = yaml.safe_load(render_to_string("components.yml"))
        register_inline_components(components["inline_components"])
        register_block_components(components["block_components"])

        autoreload_started.connect(watch)
        file_changed.connect(changed)
