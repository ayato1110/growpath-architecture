# SKEMA LOG JAWABAN AI GROWPATH

**Deliverable:** P13-17 dan P13-18
**Pemilik:** Ripa Bagaskara dengan Wisnu Nugroho
**Status:** v1.0, desain. Tabel mengikuti `../../08_Source/db/migrations/001_init.sql`.
**Sumber lengkap:** `P13-AI-Architecture.md` bagian 8.

## 1. Tabel `ai_answer_log`

| Kolom | Isi | Contoh |
|---|---|---|
| id | UUID log | `9f...` |
| consultation_id | UUID pertanyaan | `3a...` |
| model | Model yang dipanggil | diisi saat P14 |
| prompt_version | Versi prompt | `growpath-consult-v1` |
| answer | Jawaban atau pesan penolakan | teks |
| sources | Rujukan yang benar-benar dipakai | array JSON |
| guardrail_result | Hasil pemeriksaan | objek JSON |
| token_count | Total token input dan output | 2840 |
| latency_ms | Waktu panggilan model | 4120 |
| status | succeeded, blocked, failed | `succeeded` |
| feedback | helpful, not_helpful, atau null | `helpful` |
| feedback_at | Waktu umpan balik | timestamp |
| created_at | Waktu dibuat | timestamp |

## 2. Aturan log

- Satu pertanyaan bisa punya beberapa log jika percobaan pertama gagal.
- `answer` null hanya untuk status `failed`.
- Log tidak menyimpan prompt lengkap berisi data pribadi. Yang disimpan adalah versi prompt dan ringkasan konteks.
- `sources` tidak boleh berisi dokumen yang tidak ada di database.
- Setiap jawaban AI wajib punya log yang bisa dibuka lagi.
- Feedback pengguna disimpan di `ai_answer_log.feedback` dan `feedback_at`.

## 3. Batas

- Skema ini kontrak desain, bukan bukti implementasi.
- Model, prompt final, dan hasil uji guardrail masih menunggu P14.
