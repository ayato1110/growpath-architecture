# Dokumentasi Route dan Endpoint

**Sumber kontrak:** `03_Application/openapi.yaml`  
**Base URL lokal:** `http://127.0.0.1:8000`  
**Base URL staging:** `https://growpath-api.vercel.app`  
**Autentikasi:** Bearer token dari `POST /auth/login`

## 1. Aturan umum

- Semua endpoint data memakai `Authorization: Bearer <token>`.
- `tenant_id` dan `user_id` diambil dari token, bukan dari body.
- Endpoint data usaha, asesmen, dan konsultasi hanya untuk peran `umkm`.
- Error memakai `application/problem+json` dengan `title`, `status`, `code`, dan `detail`.
- Validasi gagal menjawab `422`; konflik status `409`; kuota `429`.

## 2. Ringkasan endpoint

| # | Method | Path | Peran | Fungsi |
|---:|---|---|---|---|
| 1 | POST | `/auth/login` | publik | Masuk dan dapat token |
| 2 | GET | `/auth/me` | semua | Identitas pengguna aktif |
| 3 | GET | `/health` | publik | Status layanan |
| 4 | GET | `/me/profile` | umkm | Baca data usaha |
| 5 | PUT | `/me/profile` | umkm | Simpan/ganti seluruh data usaha |
| 6 | PATCH | `/me/profile` | umkm | Perbarui data usaha |
| 7 | GET | `/assessments` | umkm | Daftar asesmen pengguna |
| 8 | POST | `/assessments` | umkm | Buat atau lanjutkan draf asesmen |
| 9 | GET | `/assessments/{id}` | umkm | Detail asesmen, kriteria, jawaban |
| 10 | PUT | `/assessments/{id}/answers` | umkm | Simpan batch jawaban |
| 11 | POST | `/assessments/{id}/submit` | umkm | Hitung skor, segmen, dan roadmap |
| 12 | GET | `/assessments/{id}/scores` | umkm | Baca skor dan cakupan |
| 13 | GET | `/assessments/{id}/roadmap` | umkm | Baca roadmap dan milestone |
| 14 | PATCH | `/milestones/{id}` | umkm | Ubah status milestone |
| 15 | POST | `/consultations` | umkm | Kirim pertanyaan ke AI |
| 16 | GET | `/consultations` | umkm | Daftar log konsultasi |
| 17 | GET | `/consultations/{id}` | umkm | Detail pertanyaan dan jawaban |
| 18 | POST | `/consultations/{id}/feedback` | umkm | Tandai jawaban berguna |

## 3. Auth

### POST `/auth/login`

```json
{"email": "umkm@growpath.id", "password": "..."}
```

Respons `200`:

```json
{"access_token": "...", "token_type": "Bearer", "expires_in": 3600, "user": {"id": "...", "role": "umkm"}}
```

Kode error: `401 AUTH_INVALID_CREDENTIALS`.

## 4. Data usaha

### GET `/me/profile`

Respons `200` berisi 10 field demografi, `completeness_pct`, dan timestamp. Jika belum ada: `404 PROFILE_NOT_FOUND`.

### PUT/PATCH `/me/profile`

```json
{
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
  "business_description": "Puding coklat rumahan."
}
```

Wajib: `business_name`, `owner_name`, `sector`, `established_year`, `operation_months`. WhatsApp harus format Indonesia. Error: `422 VALIDATION_FAILED`.

## 5. Asesmen

### POST `/assessments`

Body `{}` atau `{"profile_id": "..."}`. Membuat draf jika belum ada, atau mengembalikan draf aktif. Respons `201` berisi `assessment`, 12 `criteria`, dan `answers`.

Error: `404 PROFILE_NOT_FOUND`, `409 PROFILE_INCOMPLETE`.

### PUT `/assessments/{id}/answers`

```json
{"answers": [
  {"criterion_id": 1, "raw_value": {"option": "market"}},
  {"criterion_id": 8, "raw_value": {"options": ["logo", "packaging"]}}
]}
```

Tipe jawaban: `option` untuk pilihan tunggal, `options` untuk multi-pilih, `value` untuk angka/boolean. Error `422 ANSWER_INVALID` atau `CRITERION_NOT_ASSESSED`; `409 ASSESSMENT_LOCKED` bila sudah dinilai.

### POST `/assessments/{id}/submit`

Menghitung skor deterministik, segmen, dan roadmap dalam satu transaksi. Respons `200`:

```json
{
  "assessment_id": "...",
  "total_score": 47.92,
  "segment": {"id": 2, "code": "S2", "name": "Branding Enthusiasts"},
  "dimensions": [{"dimension_code": "PSY", "weighted_score": 66.67}],
  "criteria_answered": 12,
  "criteria_total": 31
}
```

Error: `422 ASSESSMENT_INCOMPLETE` dengan daftar kriteria yang belum dijawab.

### GET `/assessments/{id}/scores`

Mengembalikan skor, segmen, dimensi yang dinilai, dan cakupan. `409 ASSESSMENT_NOT_SCORED` bila belum dikirim.

### GET `/assessments/{id}/roadmap`

Mengembalikan roadmap aktif dan milestone. `404 ROADMAP_NOT_FOUND` bila belum dibuat.

### PATCH `/milestones/{id}`

```json
{"status": "done", "note": "opsional"}
```

Status: `pending`, `in_progress`, `done`, `skipped`. Menulis `progress_log`.

## 6. Konsultasi AI

### POST `/consultations`

```json
{"assessment_id": "...", "question": "Bagaimana cara menaikkan penjualan di marketplace?"}
```

Alur: cek asesmen sudah dinilai → cek kuota → guardrail → panggil Gemini → guardrail hasil → simpan `consultation` dan `ai_answer_log`.

Respons `201`:

```json
{
  "id": "...",
  "status": "completed",
  "answer": {
    "status": "succeeded",
    "answer": "Berdasarkan hasil asesmen...",
    "sources": [{"source_id": "dimension:PAS", "label": "Skor aspek Pasar"}],
    "model": "gemini-3.5-flash-lite",
    "prompt_version": "growpath-consult-v1"
  }
}
```

Error:
- `409 ASSESSMENT_NOT_SCORED`
- `429 AI_QUOTA_EXCEEDED` atau `AI_RATE_LIMITED`, dengan `reset_at`
- `502 AI_PROVIDER_ERROR`, pertanyaan tersimpan
- `503 AI_NOT_CONFIGURED`

Guardrail yang berhenti sebelum model: minta skor, kepastian hukum, data sensitif. Jawaban model yang menolak disimpan dengan status `blocked`.

### GET `/consultations`

Query: `from`, `to`, `page`, `limit` (maks 50). Respons berisi `items`, `page`, `limit`, `total`.

### GET `/consultations/{id}`

Detail pertanyaan, jawaban, sumber, dan feedback. `404 CONSULTATION_NOT_FOUND`.

### POST `/consultations/{id}/feedback`

```json
{"value": "helpful"}
```

Nilai: `helpful` atau `not_helpful`. `409 CONSULTATION_NOT_ANSWERED` untuk jawaban gagal.

## 7. Kuota dan batas

| Batas | Nilai |
|---|---:|
| Konsultasi per pengguna per hari | 10 |
| Pertanyaan per menit | 3 |
| Panjang pertanyaan | 3–1000 karakter |
| Panjang jawaban | 180 kata |
| Timeout model | 20 detik |
| Retry | 1 kali |
| Reset kuota | 00.00 Asia/Jakarta |

## 8. Catatan operasional

- Staging backend dilindungi Vercel Authentication; frontend server mengirim header `x-vercel-protection-bypass`. Header ini tidak boleh dipakai di browser pengguna.
- `POST /assessments/{id}/submit` memakai satu commit; kegagalan di tengah membatalkan skor dan roadmap.
- Endpoint konsultasi belum memakai RAG chunk; sumber berasal dari skor dimensi dan milestone.
