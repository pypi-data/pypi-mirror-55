from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, Union, TYPE_CHECKING

from jinja2 import Template

from lightweight.template import template
from .content import Content

if TYPE_CHECKING:
    from lightweight import SitePath


@dataclass(frozen=True)
class JinjaPage(Content):
    template: Template
    path: Optional[Path]
    params: Dict[str, Any]

    def write(self, path: SitePath):
        path.create(self.template.render(
            site=path.site, source=self, **self.params
        ))


def jinja(template_path: Union[str, Path], **params) -> JinjaPage:
    """Renders the page at path with provided parameters.

    Templates are resolved from current directory (NOT `./templates/`)."""
    path = Path(template_path)
    return JinjaPage(
        template=template(path, base_dir='.'),
        path=path,
        params=params,
    )
