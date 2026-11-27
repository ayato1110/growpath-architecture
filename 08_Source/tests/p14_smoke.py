"""Smoke test black-box P14 lewat API.

Jalankan setelah database dimigrasi dan seed:
    python tests/p14_smoke.py --report ../07_Evidence/P14/smoke-report.json

Kredensial dibaca dari environment, bukan ditulis di file:
    SMOKE_EMAIL, SMOKE_PASSWORD
    SMOKE_OTHER_EMAIL, SMOKE_OTHER_PASSWORD  (opsional, untuk TC-02)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

import httpx

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

PROFILE = {
    "business_name": "Puding Coklat Pak Hambali",
    "owner_name": "Hambali Ambawirejo",
    "gender": "male",
    "age": 42,
    "whatsapp": "081234567890",
    "email": "hambali@example.com",
    "address": "Jl. Melati 12, Jambi",
    "sector": "kuliner",
    "established_year": 2018,
    "operation_months": 60,
    "business_description": "Puding coklat rumahan untuk pesanan harian.",
}

ANSWERS = [
    (1, {"option": "market"}),
    (2, {"option": "experience"}),
    (3, {"option": "balanced"}),
    (8, {"options": ["logo", "packaging"]}),
    (9, {"options": ["store", "marketplace", "reseller"]}),
    (10, {"option": "city"}),
    (11, {"options": ["social", "marketplace", "payment"]}),
    (12, {"option": "once"}),
    (13, {"option": "once"}),
    (14, {"option": "price"}),
    (15, {"option": "local"}),
    (16, {"option": "none"}),
]

EXPECTED_TOTAL = 47.92
EXPECTED_SEGMENT = "Branding Enthusiasts"
EXPECTED_MILESTONES = [
    "Pelajari syarat ekspor",
    "Ikuti satu pameran lokal",
    "Perluas cakupan pasar bertahap",
]


class Runner:
    def __init__(self, client: httpx.Client) -> None:
        self.client = client
        self.cases: list[dict[str, object]] = []

    def record(self, case_id: str, status: str, detail: str) -> None:
        self.cases.append({"id": case_id, "status": status, "detail": detail})
        print(f"[{status.upper():8}] {case_id}: {detail}")

    def lulus(self, case_id: str, detail: str) -> None:
        self.record(case_id, "lulus", detail)

    def gagal(self, case_id: str, detail: str) -> None:
        self.record(case_id, "gagal", detail)

    def skip(self, case_id: str, detail: str) -> None:
        self.record(case_id, "skip", detail)


def login(client: httpx.Client, email: str, password: str) -> dict:
    response = client.post(
        f"{BASE_URL}/auth/login", json={"email": email, "password": password}
    )
    response.raise_for_status()
    return response.json()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report",
        default=str(
            Path(__file__).resolve().parents[2]
            / "07_Evidence"
            / "P14"
            / "smoke-report.json"
        ),
    )
    args = parser.parse_args()

    email = os.getenv("SMOKE_EMAIL")
    password = os.getenv("SMOKE_PASSWORD")
    if not email or not password:
        print("SMOKE_EMAIL dan SMOKE_PASSWORD wajib diisi.", file=sys.stderr)
        return 2

    runner = Runner(httpx.Client(timeout=30.0, follow_redirects=True))
    client = runner.client
    headers: dict[str, str] = {}

    response = client.get(f"{BASE_URL}/health")
    if response.status_code == 200 and response.json().get("status") == "ok":
        runner.lulus("TC-00", "Health check merespons ok.")
    else:
        runner.gagal("TC-00", f"Health check gagal: {response.status_code}")

    body = login(client, email, password)
    headers = {"Authorization": f"Bearer {body['access_token']}"}
    if body["user"]["role"] == "umkm":
        runner.lulus("TC-01", "Login UMKM berhasil dan token diterima.")
    else:
        runner.gagal("TC-01", f"Peran bukan umkm: {body['user']['role']}")
        return 1

    profile = client.get(f"{BASE_URL}/me/profile", headers=headers)
    if profile.status_code == 404:
        runner.lulus("TC-03", "Profil kosong menjawab 404 dengan pesan jelas.")
    elif profile.status_code == 200:
        runner.skip("TC-03", "Profil sudah ada; state kosong tidak berlaku.")
    else:
        runner.gagal("TC-03", f"Status tak terduga: {profile.status_code}")

    bad_wa = client.put(
        f"{BASE_URL}/me/profile",
        headers=headers,
        json={**PROFILE, "whatsapp": "abc"},
    )
    runner.lulus("TC-05", "WhatsApp tidak valid ditolak.") if bad_wa.status_code == 422 else runner.gagal(
        "TC-05", f"Harusnya 422, dapat {bad_wa.status_code}"
    )

    bad_sector = client.put(
        f"{BASE_URL}/me/profile",
        headers=headers,
        json={**PROFILE, "sector": "tambang"},
    )
    runner.lulus("TC-06", "Sektor tidak valid ditolak.") if bad_sector.status_code == 422 else runner.gagal(
        "TC-06", f"Harusnya 422, dapat {bad_sector.status_code}"
    )

    saved = client.put(f"{BASE_URL}/me/profile", headers=headers, json=PROFILE)
    if saved.status_code == 200 and float(saved.json()["completeness_pct"]) >= 90:
        runner.lulus(
            "TC-04",
            f"Profil tersimpan, kelengkapan {saved.json()['completeness_pct']}%.",
        )
    else:
        runner.gagal("TC-04", f"Gagal simpan profil: {saved.status_code}")

    created = client.post(f"{BASE_URL}/assessments", headers=headers, json={})
    if created.status_code != 201:
        runner.gagal("TC-08", f"Gagal membuat asesmen: {created.status_code}")
        return report(runner, args.report)
    draft = created.json()
    assessment_id = draft["assessment"]["id"]
    criteria = draft["criteria"]
    psy = [item for item in criteria if item["dimension_code"] == "PSY"]
    pas = [item for item in criteria if item["dimension_code"] == "PAS"]
    if len(criteria) == 12 and len(psy) == 3 and len(pas) == 9:
        runner.lulus("TC-08", "Draf berisi 12 kriteria: Psikografi 3, Pasar 9.")
    else:
        runner.gagal(
            "TC-08",
            f"Komposisi kriteria salah: total {len(criteria)}, PSY {len(psy)}, PAS {len(pas)}",
        )

    first_batch = [
        {"criterion_id": criterion_id, "raw_value": raw}
        for criterion_id, raw in ANSWERS[:3]
    ]
    saved_answers = client.put(
        f"{BASE_URL}/assessments/{assessment_id}/answers",
        headers=headers,
        json={"answers": first_batch},
    )
    if saved_answers.status_code == 200:
        runner.lulus("TC-09", "Tiga jawaban Psikografi tersimpan.")
    else:
        runner.gagal("TC-09", f"Gagal simpan jawaban: {saved_answers.status_code}")

    invalid = client.put(
        f"{BASE_URL}/assessments/{assessment_id}/answers",
        headers=headers,
        json={"answers": [{"criterion_id": 1, "raw_value": {"option": "tidak_ada"}}]},
    )
    runner.lulus("TC-10", "Opsi tidak dikenal ditolak 422.") if invalid.status_code == 422 else runner.gagal(
        "TC-10", f"Harusnya 422, dapat {invalid.status_code}"
    )

    incomplete = client.post(
        f"{BASE_URL}/assessments/{assessment_id}/submit", headers=headers
    )
    detail = incomplete.json().get("detail", "") if incomplete.status_code == 422 else ""
    if incomplete.status_code == 422 and "PAS" in detail:
        runner.lulus("TC-11", "Submit belum lengkap ditolak dan menyebut kriteria kurang.")
    else:
        runner.gagal(
            "TC-11", f"Harusnya 422 dengan daftar kurang, dapat {incomplete.status_code}"
        )

    remaining = [
        {"criterion_id": criterion_id, "raw_value": raw}
        for criterion_id, raw in ANSWERS[3:]
    ]
    client.put(
        f"{BASE_URL}/assessments/{assessment_id}/answers",
        headers=headers,
        json={"answers": remaining},
    ).raise_for_status()

    submitted = client.post(
        f"{BASE_URL}/assessments/{assessment_id}/submit", headers=headers
    )
    if submitted.status_code != 200:
        runner.gagal("TC-12", f"Submit gagal: {submitted.status_code}")
        return report(runner, args.report)
    score = submitted.json()

    again = client.get(
        f"{BASE_URL}/assessments/{assessment_id}/scores", headers=headers
    )
    same = (
        again.status_code == 200
        and abs(float(again.json()["total_score"]) - float(score["total_score"])) < 0.01
        and again.json()["segment"]["name"] == score["segment"]["name"]
    )
    expected = abs(float(score["total_score"]) - EXPECTED_TOTAL) < 0.01
    if same and expected:
        runner.lulus(
            "TC-12",
            f"Skor {score['total_score']} dan segmen {score['segment']['name']} konsisten.",
        )
    else:
        runner.gagal(
            "TC-12",
            f"Skor tidak sesuai harapan: {score['total_score']} / {score['segment']['name']}",
        )

    if score["segment"]["name"] == EXPECTED_SEGMENT and 30 <= float(score["total_score"]) < 55:
        runner.lulus("TC-13", "Skor 47,92 masuk segmen 2 sesuai ambang.")
    else:
        runner.gagal("TC-13", f"Segmen tidak sesuai: {score['segment']['name']}")

    coverage = (
        score["criteria_answered"] == 12 and score["criteria_total"] == 31
    )
    if coverage and len(score["dimensions"]) == 2:
        runner.lulus("TC-14", "Hasil menampilkan 12 dari 31 kriteria dan 2 dimensi.")
    else:
        runner.gagal("TC-14", f"Cakupan salah: {score.get('criteria_answered')}/{score.get('criteria_total')}")

    roadmap = client.get(
        f"{BASE_URL}/assessments/{assessment_id}/roadmap", headers=headers
    )
    milestones = roadmap.json().get("milestones", []) if roadmap.status_code == 200 else []
    titles = [item["title"] for item in milestones]
    if titles == EXPECTED_MILESTONES:
        runner.lulus("TC-15", "Tiga langkah sesuai tiga kriteria terendah.")
        first = milestones[0]["id"]
        patched = client.patch(
            f"{BASE_URL}/milestones/{first}",
            headers=headers,
            json={"status": "done"},
        )
        reloaded = client.get(
            f"{BASE_URL}/assessments/{assessment_id}/roadmap", headers=headers
        )
        persisted = any(
            item["id"] == first and item["status"] == "done"
            for item in reloaded.json().get("milestones", [])
        )
        if patched.status_code == 200 and persisted:
            runner.lulus("TC-15b", "Status langkah selesai tersimpan setelah muat ulang.")
        else:
            runner.gagal("TC-15b", "Status langkah tidak tersimpan.")
    else:
        runner.gagal("TC-15", f"Judul langkah tidak sesuai: {titles}")

    other_email = os.getenv("SMOKE_OTHER_EMAIL")
    other_password = os.getenv("SMOKE_OTHER_PASSWORD")
    if other_email and other_password:
        other = login(client, other_email, other_password)
        other_headers = {"Authorization": f"Bearer {other['access_token']}"}
        denied = client.get(f"{BASE_URL}/me/profile", headers=other_headers)
        runner.lulus("TC-02", "Peran non-UMKM ditolak 403.") if denied.status_code == 403 else runner.gagal(
            "TC-02", f"Harusnya 403, dapat {denied.status_code}"
        )
    else:
        runner.skip("TC-02", "Kredensial akun non-UMKM tidak diisi.")
    runner.skip("TC-07", "Butuh akun tanpa profil; verifikasi manual.")

    return report(runner, args.report)


def report(runner: Runner, path: str) -> int:
    failed = [case for case in runner.cases if case["status"] == "gagal"]
    payload = {
        "base_url": BASE_URL,
        "finished_at": datetime.now(UTC).isoformat(),
        "summary": {
            "lulus": sum(1 for c in runner.cases if c["status"] == "lulus"),
            "gagal": len(failed),
            "skip": sum(1 for c in runner.cases if c["status"] == "skip"),
        },
        "cases": runner.cases,
    }
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nLaporan: {target}")
    print(f"Lulus {payload['summary']['lulus']} · Gagal {payload['summary']['gagal']} · Skip {payload['summary']['skip']}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
