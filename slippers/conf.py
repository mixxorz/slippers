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
    ) -> List[Literal["shell", "browser_console", "ui"]]:
        """Where to output type checking errors"""
        return getattr(
            django_settings,
            "SLIPPERS_TYPE_CHECKING_OUTPUT",
            ["shell", "browser_console", "ui"],
        )


settings = Settings()
