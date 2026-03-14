"""TUI configuration schema definitions."""

from pydantic import BaseModel, Field


class ScrollAcceleration(BaseModel):
    """Scroll acceleration settings."""

    enabled: bool = Field(description="Enable scroll acceleration")


class TuiOptions(BaseModel):
    """TUI display options."""

    scroll_speed: float | None = Field(
        None,
        ge=0.001,
        description="TUI scroll speed",
    )
    scroll_acceleration: ScrollAcceleration | None = Field(
        None,
        description="Scroll acceleration settings",
    )
    diff_style: str | None = Field(
        None,
        description="Control diff rendering style: 'auto' adapts to terminal width, 'stacked' always shows single column",
    )

    class Config:
        extra = "forbid"


class TuiInfo(TuiOptions):
    """Complete TUI configuration including theme and keybinds."""

    schema_: str | None = Field(None, alias="$schema")
    theme: str | None = None
    keybinds: dict[str, str] | None = None

    class Config:
        extra = "forbid"
        populate_by_name = True
