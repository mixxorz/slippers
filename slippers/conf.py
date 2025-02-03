from typing import List, Literal

from django.conf import settings as django_settings


class Settings:
    @property
    def SLIPPERS_RUNTIME_TYPE_CHECKING(self) -> bool:
        """Enable runtime type checking of props"""
        return getattr(django_settings, "SLIPPERS_RUNTIME_TYPE_CHECKING", django_settings.DEBUG)  # type: ignore

    @property
    def SLIPPERS_TYPE_CHECKING_OUTPUT(
        self,
    ) -> List[Literal["console", "overlay"]]:
        """Where to output type checking errors"""
        return getattr(
            django_settings,
            "SLIPPERS_TYPE_CHECKING_OUTPUT",
            ["console", "overlay"],
        )

    @property
    def SLIPPERS_PARAMS_VISIBLE_IN_CHILDREN(self) -> bool:
        """Make component parameters visible in children"""
        return getattr(django_settings, "SLIPPERS_PARAMS_VISIBLE_IN_CHILDREN", False)  # type: ignore

    @property
    def SLIPPERS_VARS_VISIBLE_IN_CHILDREN(self) -> bool:
        """Make component var declarations visible in children"""
        return getattr(django_settings, "SLIPPERS_VARS_VISIBLE_IN_CHILDREN", False)  # type: ignore


settings = Settings()
