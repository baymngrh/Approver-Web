"""Database models for the Approver web application."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import synonym

from .. import db


class TimestampMixin:
    """Mixin that provides ``created_at`` and ``updated_at`` timestamps."""

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class Produk(TimestampMixin, db.Model):
    __tablename__ = "produk"

    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(64), unique=True, nullable=True)
    nama = db.Column(db.String(255), nullable=False)
    jenis = db.Column(db.String(120), nullable=True)
    kelompok = db.Column(db.String(120), nullable=True)

    komposisi_material = db.relationship(
        "KomposisiMaterial",
        back_populates="produk",
        cascade="all, delete-orphan",
        lazy=True,
    )
    stok = db.relationship(
        "StokProduk",
        back_populates="produk",
        cascade="all, delete-orphan",
        lazy=True,
    )
    target_pengiriman = db.relationship(
        "TargetPengiriman",
        back_populates="produk",
        cascade="all, delete-orphan",
        lazy=True,
    )
    rencana_produksi = db.relationship(
        "RencanaProduksi",
        back_populates="produk",
        cascade="all, delete-orphan",
        lazy=True,
    )
    material_produk = db.relationship(
        "MaterialProduk",
        back_populates="produk",
        cascade="all, delete-orphan",
        lazy=True,
    )
    produksi = db.relationship(
        "Produksi",
        back_populates="produk",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Produk {self.kode or self.id}: {self.nama}>"


class Material(TimestampMixin, db.Model):
    __tablename__ = "material"

    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(64), unique=True, nullable=True)
    nama = db.Column(db.String(255), nullable=False)
    satuan = db.Column(db.String(32), nullable=True)
    # Alias dengan huruf kapital diperlukan oleh beberapa skrip warisan yang
    # mengakses atribut ``Material.Satuan`` secara langsung.
    Satuan = synonym("satuan")
    stok = db.Column(db.Float, default=0, nullable=False)
    min_stok = db.Column(db.Float, default=0, nullable=False)
    status = db.Column(db.String(32), default="aktif", nullable=False)
    jenis = db.Column(db.String(120), nullable=True)
    kelompok = db.Column(db.String(120), nullable=True)

    komposisi_material = db.relationship(
        "KomposisiMaterial",
        back_populates="material",
        cascade="all, delete-orphan",
        lazy=True,
    )
    material_produk = db.relationship(
        "MaterialProduk",
        back_populates="material",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Material {self.kode or self.id}: {self.nama}>"


class KomposisiMaterial(TimestampMixin, db.Model):
    __tablename__ = "komposisi_material"
    __table_args__ = (
        UniqueConstraint("produk_id", "material_id", name="uq_komposisi_produk_material"),
    )

    id = db.Column(db.Integer, primary_key=True)
    produk_id = db.Column(db.Integer, db.ForeignKey("produk.id"), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey("material.id"), nullable=False)
    persentase = db.Column(db.Float, nullable=True)
    jumlah_per_pack = db.Column(db.Float, nullable=True)
    satuan = db.Column(db.String(32), nullable=True)

    produk = db.relationship("Produk", back_populates="komposisi_material")
    material = db.relationship("Material", back_populates="komposisi_material")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"<KomposisiMaterial produk={self.produk_id} material={self.material_id} "
            f"jumlah={self.jumlah_per_pack} {self.satuan}>"
        )


class MaterialProduk(TimestampMixin, db.Model):
    __tablename__ = "material_produk"
    __table_args__ = (
        UniqueConstraint("produk_id", "material_id", name="uq_material_produk"),
    )

    id = db.Column(db.Integer, primary_key=True)
    produk_id = db.Column(db.Integer, db.ForeignKey("produk.id"), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey("material.id"), nullable=False)
    jumlah = db.Column(db.Float, nullable=True)
    satuan = db.Column(db.String(32), nullable=True)

    produk = db.relationship("Produk", back_populates="material_produk")
    material = db.relationship("Material", back_populates="material_produk")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"<MaterialProduk produk={self.produk_id} material={self.material_id} "
            f"jumlah={self.jumlah} {self.satuan}>"
        )


class StokProduk(TimestampMixin, db.Model):
    __tablename__ = "stok_produk"

    id = db.Column(db.Integer, primary_key=True)
    produk_id = db.Column(db.Integer, db.ForeignKey("produk.id"), nullable=False)
    tanggal = db.Column(db.Date, nullable=True)
    jumlah = db.Column(db.Float, default=0, nullable=False)

    produk = db.relationship("Produk", back_populates="stok")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<StokProduk produk={self.produk_id} tanggal={self.tanggal} jumlah={self.jumlah}>"


class TargetPengiriman(TimestampMixin, db.Model):
    __tablename__ = "target_pengiriman"

    id = db.Column(db.Integer, primary_key=True)
    produk_id = db.Column(db.Integer, db.ForeignKey("produk.id"), nullable=False)
    tanggal = db.Column(db.Date, nullable=True)
    jumlah = db.Column(db.Float, default=0, nullable=False)

    produk = db.relationship("Produk", back_populates="target_pengiriman")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<TargetPengiriman produk={self.produk_id} tanggal={self.tanggal} jumlah={self.jumlah}>"


class RencanaProduksi(TimestampMixin, db.Model):
    __tablename__ = "rencana_produksi"

    id = db.Column(db.Integer, primary_key=True)
    produk_id = db.Column(db.Integer, db.ForeignKey("produk.id"), nullable=False)
    tanggal_mulai = db.Column(db.Date, nullable=True)
    tanggal_selesai = db.Column(db.Date, nullable=True)
    jumlah_karton = db.Column(db.Float, default=0, nullable=False)

    produk = db.relationship("Produk", back_populates="rencana_produksi")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"<RencanaProduksi produk={self.produk_id} jumlah={self.jumlah_karton} "
            f"mulai={self.tanggal_mulai} selesai={self.tanggal_selesai}>"
        )


class Produksi(TimestampMixin, db.Model):
    __tablename__ = "produksi"

    id = db.Column(db.Integer, primary_key=True)
    produk_id = db.Column(db.Integer, db.ForeignKey("produk.id"), nullable=False)
    tanggal = db.Column(db.Date, nullable=True)
    jumlah_karton = db.Column(db.Float, default=0, nullable=False)
    pack_per_karton = db.Column(db.Integer, default=0, nullable=False)

    produk = db.relationship("Produk", back_populates="produksi")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"<Produksi produk={self.produk_id} tanggal={self.tanggal} "
            f"jumlah_karton={self.jumlah_karton}>"
        )


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
