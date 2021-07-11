from pathlib import Path, PosixPath

from django.apps import AppConfig
from django.core.checks import Warning, register
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.autoreload import autoreload_started, file_changed

import yaml

from slippers.templatetags.slippers import (
    register_block_components,
    register_inline_components,
)


def register_tags():
    """Register tags from components.yaml"""
    try:
        template = get_template("components.yaml")
        components = yaml.safe_load(template.template.source)
        register_inline_components(components.get("inline_components", {}))
        register_block_components(components.get("block_components", {}))
    except TemplateDoesNotExist:
        pass


def watch(sender, **kwargs):
    """Watch when component.yaml changes"""
    try:
        template = get_template("components.yaml")
        sender.extra_files.add(Path(template.origin.name))
    except TemplateDoesNotExist:
        pass


def changed(sender, file_path: PosixPath, **kwargs):
    """Refresh tag registry when component.yaml changes"""
    if file_path.name == "components.yaml":
        print("components.yaml changed. Updating component tags...")
        register_tags()


def checks(app_configs, **kwargs):
    """Warn if unable to find components.yaml"""
    try:
        get_template("components.yaml")
    except TemplateDoesNotExist:
        return [
            Warning(
                "Slippers was unable to find a components.yaml file.",
                hint="Make sure it's in a root template directory.",
                id="slippers.E001",
            )
        ]
    return []


class SlippersConfig(AppConfig):
    name = "slippers"

    def ready(self):
        register_tags()

        register(checks)

        autoreload_started.connect(watch)
        file_changed.connect(changed)
