__project__ = "flupy"

__version__ = "1.0.10"

from flupy.fluent import flu, with_iter, Fluent
from flupy.cli.utils import walk_files, walk_dirs

__all__ = ["flu", "with_iter", "Fluent", "walk_files", "walk_dirs"]
