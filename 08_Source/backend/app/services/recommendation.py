"""Rekomendasi berbasis aturan. AI tidak menentukan prioritas."""

from dataclasses import dataclass
from datetime import date, timedelta

ACTIONS: dict[str, dict[str, object]] = {
    "PSY-01": {
        "title": "Tegaskan tujuan usaha",
        "actions": [
            "Tulis tujuan usaha untuk enam bulan ke depan dalam satu kalimat.",
            "Hubungkan tujuan itu dengan keputusan stok dan harga mingguan.",
            "Tinjau tujuan setiap akhir bulan.",
        ],
    },
    "PSY-02": {
        "title": "Uji kesesuaian bidang usaha",
        "actions": [
            "Bandingkan keahlian dan pengalaman Anda dengan kebutuhan pelanggan.",
            "Tanyakan alasan pembelian kepada lima pelanggan terakhir.",
            "Catat satu penyesuaian produk atau layanan dari hasilnya.",
        ],
    },
    "PSY-03": {
        "title": "Buat daftar risiko dan batas kerugian",
        "actions": [
            "Daftar tiga risiko usaha yang paling mungkin terjadi.",
            "Tetapkan batas kerugian untuk tiap risiko.",
            "Uji satu keputusan kecil dengan batas tersebut sebelum menambah modal.",
        ],
    },
    "PAS-01": {
        "title": "Lengkapi identitas merek",
        "actions": [
            "Tetapkan logo dan satu warna merek yang dipakai konsisten.",
            "Rapikan kemasan atau tampilan produk.",
            "Samakan nama, bio, dan kontak di semua kanal penjualan.",
        ],
    },
    "PAS-02": {
        "title": "Buka satu saluran penjualan tambahan",
        "actions": [
            "Pilih satu kanal baru yang paling dekat dengan pelanggan Anda.",
            "Siapkan katalog dan stok untuk kanal tersebut.",
            "Jalankan dua minggu, lalu catat jumlah pesanan dan kendalanya.",
        ],
    },
    "PAS-03": {
        "title": "Perluas cakupan pasar bertahap",
        "actions": [
            "Tetapkan satu wilayah perluasan terdekat.",
            "Ukur permintaan dari wilayah itu selama satu bulan.",
            "Siapkan pengiriman atau penyaluran sebelum menambah wilayah lain.",
        ],
    },
    "PAS-04": {
        "title": "Pasang kanal digital dasar",
        "actions": [
            "Aktifkan satu media sosial dengan jadwal unggah mingguan.",
            "Daftarkan produk di satu marketplace atau katalog digital.",
            "Sediakan satu metode pembayaran digital dan catat transaksinya.",
        ],
    },
    "PAS-05": {
        "title": "Cari peluang sub-kontrak masuk",
        "actions": [
            "Daftar tiga usaha besar yang membutuhkan produk Anda.",
            "Ajukan penawaran singkat berisi kapasitas, harga, dan jadwal.",
            "Catat tanggapan dan alasan penolakan untuk perbaikan berikutnya.",
        ],
    },
    "PAS-06": {
        "title": "Rapikan kesiapan sub-kontrak keluar",
        "actions": [
            "Tulis kapasitas produksi yang bisa dipenuhi per bulan.",
            "Tetapkan standar mutu dan cara pemeriksaannya.",
            "Siapkan contoh kontrak kerja sama yang sederhana.",
        ],
    },
    "PAS-07": {
        "title": "Riset tiga pesaing terdekat",
        "actions": [
            "Catat harga dan produk tiga pesaing terdekat.",
            "Bandingkan saluran penjualan dan cara mereka menjangkau pelanggan.",
            "Tentukan satu pembeda yang bisa Anda pertahankan.",
        ],
    },
    "PAS-08": {
        "title": "Ikuti satu pameran lokal",
        "actions": [
            "Pilih satu pameran yang sesuai jenis usaha dan anggaran.",
            "Siapkan stan, contoh produk, dan materi kontak.",
            "Tetapkan target jumlah kontak baru dan tindak lanjutnya.",
        ],
    },
    "PAS-09": {
        "title": "Pelajari syarat ekspor",
        "actions": [
            "Daftar dokumen dan standar produk yang diminta negara tujuan.",
            "Konsultasi ke instansi pembina ekspor setempat.",
            "Hitung biaya dan risiko sebelum menerima pesanan pertama.",
        ],
    },
}


@dataclass(frozen=True)
class CriterionScore:
    criterion_id: int
    code: str
    question: str
    dimension_name: str
    score: float
    order_no: int


@dataclass(frozen=True)
class MilestonePlan:
    order_no: int
    title: str
    description: str
    action_items: list[str]
    due_date: date


def build_plan(
    criteria: list[CriterionScore], scored_on: date, limit: int = 3
) -> list[MilestonePlan]:
    ordered = sorted(criteria, key=lambda item: (item.score, item.order_no))[:limit]
    plans: list[MilestonePlan] = []
    for index, item in enumerate(ordered):
        action = ACTIONS.get(item.code, {})
        title = str(action.get("title") or f"Perbaiki {item.code}")
        actions = list(action.get("actions") or ["Tinjau kriteria ini bersama pendamping."])
        description = (
            f"Skor {round(item.score, 2)} dari 100 pada {item.dimension_name}. "
            f"Kriteria: {item.question}"
        )
        plans.append(
            MilestonePlan(
                order_no=index + 1,
                title=title,
                description=description,
                action_items=actions,
                due_date=scored_on + timedelta(days=14 * (index + 1)),
            )
        )
    return plans


def build_summary(plan: list[MilestonePlan], dimension_names: list[str]) -> str:
    aspects = " dan ".join(dict.fromkeys(dimension_names))
    titles = ", ".join(item.title.lower() for item in plan)
    return f"Tiga langkah prioritas dari aspek {aspects}: {titles}."
