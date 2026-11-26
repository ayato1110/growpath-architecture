"""Skor deterministik. Tidak ada pemanggilan AI di modul ini."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Any


class ScoringError(ValueError):
    """Input jawaban tidak sesuai aturan kriteria."""


@dataclass(frozen=True)
class AnswerScore:
    raw_value: dict[str, Any]
    numeric_value: float | None
    score: float


def score_answer(
    input_type: str, scoring_rule: dict[str, Any], raw_value: Any
) -> AnswerScore:
    if input_type in {"enum", "scale"}:
        return _score_single_choice(scoring_rule, raw_value)
    if input_type == "multi_select":
        return _score_multi_select(scoring_rule, raw_value)
    if input_type == "number":
        return _score_number(scoring_rule, raw_value)
    if input_type == "boolean":
        return _score_boolean(raw_value)
    raise ScoringError(f"Tipe input '{input_type}' tidak dapat dinilai.")


def _score_single_choice(
    scoring_rule: dict[str, Any], raw_value: Any
) -> AnswerScore:
    option = _raw_dict(raw_value).get("option")
    if not isinstance(option, str):
        raise ScoringError("Jawaban pilihan tunggal wajib memuat 'option'.")
    points = _option_points(scoring_rule, option)
    return AnswerScore({"option": option}, None, points)


def _score_multi_select(
    scoring_rule: dict[str, Any], raw_value: Any
) -> AnswerScore:
    options = _raw_dict(raw_value).get("options")
    if not isinstance(options, list) or not options:
        raise ScoringError("Jawaban multi-pilih wajib memuat minimal satu 'options'.")
    if not all(isinstance(item, str) for item in options):
        raise ScoringError("Setiap opsi multi-pilih harus berupa kode teks.")
    chosen = list(dict.fromkeys(options))
    points = {item["code"]: float(item["points"]) for item in scoring_rule["options"]}
    unknown = [code for code in chosen if code not in points]
    if unknown:
        raise ScoringError("Opsi tidak dikenal: " + ", ".join(unknown))
    exclusive = set(scoring_rule.get("exclusive_codes", []))
    if exclusive & set(chosen) and len(chosen) > 1:
        raise ScoringError("Opsi 'tidak ada' tidak boleh digabung dengan opsi lain.")
    total = min(100.0, sum(points[code] for code in chosen))
    return AnswerScore({"options": chosen}, None, total)


def _score_number(scoring_rule: dict[str, Any], raw_value: Any) -> AnswerScore:
    value = _raw_dict(raw_value).get("value")
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ScoringError("Jawaban angka wajib memuat 'value' berupa angka.")
    if value < 0:
        raise ScoringError("Nilai angka tidak boleh negatif.")
    buckets = scoring_rule.get("buckets") or []
    for bucket in buckets:
        lower = float(bucket.get("min", 0))
        upper = bucket.get("max")
        if value >= lower and (upper is None or value < float(upper)):
            return AnswerScore({"value": float(value)}, float(value), float(bucket["points"]))
    raise ScoringError("Nilai angka di luar rentang yang dikonfigurasi.")


def _score_boolean(raw_value: Any) -> AnswerScore:
    value = _raw_dict(raw_value).get("value")
    if not isinstance(value, bool):
        raise ScoringError("Jawaban ya/tidak wajib memuat 'value' boolean.")
    return AnswerScore({"value": value}, None, 100.0 if value else 0.0)


def _option_points(scoring_rule: dict[str, Any], code: str) -> float:
    for option in scoring_rule.get("options", []):
        if option.get("code") == code:
            return float(option["points"])
    raise ScoringError(f"Opsi '{code}' tidak ada pada kriteria ini.")


def _raw_dict(raw_value: Any) -> dict[str, Any]:
    if not isinstance(raw_value, dict):
        raise ScoringError("Jawaban harus berupa objek JSON.")
    return raw_value


def weighted_average(pairs: list[tuple[float, float]]) -> float:
    total_weight = sum(weight for weight, _ in pairs)
    if total_weight <= 0:
        return 0.0
    return sum(weight * score for weight, score in pairs) / total_weight


def round_score(value: float) -> float:
    return float(Decimal(str(value)).quantize(Decimal("0.01")))


def segment_for(
    total_score: float, segments: list[tuple[int, str, float, float]]
) -> tuple[int, str, float, float]:
    """Segments: (id, code, min, max). Batas bawah inklusif, batas atas eksklusif."""
    for segment in segments:
        _, _, lower, upper = segment
        if upper >= 100 and lower <= total_score <= upper:
            return segment
        if lower <= total_score < upper:
            return segment
    raise ScoringError("Segmen untuk skor ini tidak ditemukan.")
