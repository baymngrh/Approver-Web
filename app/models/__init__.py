"""Convenience imports for the ORM models."""

from .. import db
from .models import (
    db as _db_instance,
    KomposisiMaterial,
    Material,
    MaterialProduk,
    Produk,
    Produksi,
    RencanaProduksi,
    StokProduk,
    TargetPengiriman,
)

# Ensure that ``db`` exported from this module is the same instance as the one
# defined in :mod:`app.__init__`. The ``_db_instance`` import will raise an
# ImportError if the models module is imported before the database is created,
# providing fast feedback during development.
assert _db_instance is db

__all__ = [
    "db",
    "Produk",
    "Material",
    "KomposisiMaterial",
    "StokProduk",
    "TargetPengiriman",
    "RencanaProduksi",
    "MaterialProduk",
    "Produksi",
]
