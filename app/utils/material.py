"""Utility helpers for working with material data."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Tuple

from flask import current_app

from ..models import (
    KomposisiMaterial,
    Material,
    MaterialProduk,
    Produk,
    db,
)


def _clean_cell(value: str | None) -> str:
    return value.strip() if value else ""


def _parse_float(value: str | None) -> float | None:
    if not value:
        return None

    normalised = value.replace(".", "").replace(",", ".").replace("%", "").strip()
    if not normalised:
        return None

    try:
        return float(normalised)
    except ValueError:
        return None


def _resolve_csv_path(filename: str) -> Path:
    path = Path(filename)
    if path.is_absolute():
        return path
    # CSV files are typically stored alongside the project root.
    project_root = Path(current_app.root_path).parent
    return project_root / filename


def baca_csv_material(filename: str) -> Tuple[bool, str]:
    """Import material composition data from a CSV file.

    The CSV structure can vary slightly between exports. The helper is resilient
    to both the legacy format (with material codes and percentage columns) and
    the simplified format used by the newer tooling. The function returns a
    ``(success, message)`` tuple so callers can surface useful error information
    without needing to raise exceptions.
    """

    try:
        csv_path = _resolve_csv_path(filename)
    except RuntimeError as exc:  # pragma: no cover - defensive
        return False, str(exc)

    if not csv_path.exists():
        return False, f"File '{filename}' tidak ditemukan"

    try:
        with csv_path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.reader(handle, delimiter=";")
            current_produk: Produk | None = None

            for raw_row in reader:
                row = [_clean_cell(cell) for cell in raw_row]
                if not any(row):
                    # Blank lines are used as separators between produk entries.
                    current_produk = None
                    continue

                if row and row[0]:
                    kode_produk = row[0]
                    nama_produk = row[1] if len(row) > 1 and row[1] else kode_produk

                    current_produk = Produk.query.filter_by(kode=kode_produk).first()
                    if current_produk is None:
                        current_produk = Produk(kode=kode_produk, nama=nama_produk)
                        db.session.add(current_produk)
                        db.session.flush()  # ensure the new ID is available
                    else:
                        current_produk.nama = nama_produk

                if current_produk is None:
                    # Material rows must always follow a produk header. If the file
                    # does not contain a header before material rows we simply skip
                    # the orphaned entries.
                    continue

                # Legacy exports contain up to seven columns, newer exports only
                # five. Extract the known fields defensively.
                kode_material = row[2] if len(row) > 2 else ""
                nama_material = row[3] if len(row) > 3 else ""
                jumlah_value = row[5] if len(row) > 5 else ""
                satuan = row[6] if len(row) > 6 else ""
                additional = row[4] if len(row) > 4 else ""

                if len(row) <= 4:
                    # Newer exports omit the material code column.
                    nama_material = row[2] if len(row) > 2 else nama_material
                    jumlah_value = row[3] if len(row) > 3 else jumlah_value
                    satuan = row[4] if len(row) > 4 else satuan
                    kode_material = ""
                    additional = ""

                if not nama_material:
                    # Some header rows only carry product information.
                    continue

                material: Material | None = None
                if kode_material:
                    material = Material.query.filter_by(kode=kode_material).first()

                if material is None:
                    material = Material.query.filter_by(nama=nama_material).first()

                if material is None:
                    material = Material(kode=kode_material or None, nama=nama_material)
                    db.session.add(material)
                    db.session.flush()
                else:
                    if kode_material and not material.kode:
                        material.kode = kode_material

                # Update shared material metadata.
                if satuan:
                    material.satuan = satuan
                if additional and not material.jenis:
                    # The "additional" column stores either a material category
                    # or the percentage contained in the pack depending on the
                    # CSV variant. We only copy it when the material has not been
                    # categorised yet.
                    material.jenis = additional

                persentase = _parse_float(additional) if "%" in additional else None
                jumlah_float = _parse_float(jumlah_value)

                komposisi = KomposisiMaterial.query.filter_by(
                    produk_id=current_produk.id, material_id=material.id
                ).first()
                if komposisi is None:
                    komposisi = KomposisiMaterial(
                        produk=current_produk,
                        material=material,
                    )
                    db.session.add(komposisi)

                if jumlah_float is not None:
                    komposisi.jumlah_per_pack = jumlah_float
                if persentase is not None:
                    komposisi.persentase = persentase
                if satuan:
                    komposisi.satuan = satuan

                material_produk = MaterialProduk.query.filter_by(
                    produk_id=current_produk.id, material_id=material.id
                ).first()
                if material_produk is None:
                    material_produk = MaterialProduk(
                        produk=current_produk,
                        material=material,
                    )
                    db.session.add(material_produk)

                if jumlah_float is not None:
                    material_produk.jumlah = jumlah_float
                if satuan:
                    material_produk.satuan = satuan

    except Exception as exc:  # pragma: no cover - defensive error handling
        current_app.logger.exception("Gagal membaca CSV material: %s", filename)
        db.session.rollback()
        return False, f"Gagal membaca file CSV: {exc}"

    return True, "Import material berhasil"
