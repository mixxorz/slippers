from pathlib import Path, PosixPath

from django.apps import AppConfig
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.autoreload import autoreload_started, file_changed

import yaml

from slippers.templatetags.slippers import (
    register_block_components,
    register_inline_components,
)


def register_tags():
    """Register tags from components.yml"""
    try:
        template = get_template("components.yml")
        components = yaml.safe_load(template.template.source)
        register_inline_components(components.get("inline_components", {}))
        register_block_components(components.get("block_components", {}))
    except TemplateDoesNotExist:
        pass


def watch(sender, **kwargs):
    """Watch when component.yml changes"""
    try:
        template = get_template("components.yml")
        sender.extra_files.add(Path(template.origin.name))
    except TemplateDoesNotExist:
        pass


def changed(sender, file_path: PosixPath, **kwargs):
    """Refresh tag registry when component.yml changes"""
    if file_path.name == "components.yml":
        print("components.yml changed. Updating component tags...")
        register_tags()


class SlippersConfig(AppConfig):
    name = "slippers"

    def ready(self):
        register_tags()

        autoreload_started.connect(watch)
        file_changed.connect(changed)
