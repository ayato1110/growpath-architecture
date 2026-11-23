# KAMUS DATA P13 GROWPATH

**Deliverable:** P13-10, P13-18
**Pemilik:** Wisnu Nugroho dan Ripa Bagaskara
**Disusun oleh:** Tim Growpath P13, 22 November 2026
**Status:** v1.0, 23 entitas

## 1. Kedudukan dokumen

Dokumen ini adalah kamus data resmi P13 dan P14 untuk 23 entitas. Dokumen ini:

1. Menetapkan 23 entitas, termasuk `Consultation` dan `AIAnswerLog`.
2. Mencatat kolom, enum, dan aturan null.
3. Menjadi rujukan `../08_Source/db/migrations/001_init.sql`.

Kamus lama tidak dipakai sebagai acuan P13/P14. Jika ada perbedaan, dokumen ini yang berlaku.

## 2. Konvensi

- Nama logis memakai PascalCase. Nama fisik memakai snake_case.
- Tabel `User` ditulis `"user"` karena `user` adalah kata kunci PostgreSQL.
- Primary key transaksional memakai `uuid` dengan `gen_random_uuid()`.
- Primary key tabel referensi memakai `smallint`.
- Semua waktu memakai `timestamptz` dan disimpan UTC. Tampilan memakai Asia/Jakarta.
- Semua tabel tenant-scoped memuat `tenant_id`, termasuk tabel anak, untuk RLS dan query agregat.
- `created_at` dan `updated_at` memakai `now()`. Tabel append-only tidak punya `updated_at`.
- Nama constraint ditulis eksplisit agar mudah dirujuk saat migrasi.

## 3. Entitas baru

### 3.1 Consultation

Satu pertanyaan pengguna dalam satu sesi konsultasi. Satu baris untuk satu pertanyaan, bukan satu percakapan panjang.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | tidak | default gen_random_uuid() |
| tenant_id | uuid | FK | tidak | tenant.id, on delete cascade |
| user_id | uuid | FK | tidak | "user".id, on delete cascade |
| assessment_id | uuid | FK | tidak | assessment.id, on delete restrict |
| question | text | - | tidak | panjang 3 sampai 1000 karakter |
| status | enum | - | tidak | pending, processing, completed, failed |
| created_at | timestamptz | - | tidak | default now() |
| updated_at | timestamptz | - | tidak | default now() |

Indeks: `(user_id, created_at desc)`, `(tenant_id, created_at desc)`, `(assessment_id)`.

Aturan:

- `assessment_id` wajib menunjuk asesmen milik pengguna yang sama. Ini diperiksa di application layer karena tidak bisa dijaga satu FK.
- Pertanyaan disimpan walaupun kuota habis atau model gagal.
- `status` berubah menjadi `completed` hanya jika ada `AIAnswerLog` berstatus `succeeded` atau `blocked`.

### 3.2 AIAnswerLog

Satu jawaban atau satu percobaan jawaban untuk satu pertanyaan. Satu consultation dapat punya beberapa baris jika percobaan pertama gagal.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | tidak | default gen_random_uuid() |
| consultation_id | uuid | FK | tidak | consultation.id, on delete cascade |
| model | varchar(80) | - | tidak | nama model yang dipanggil |
| prompt_version | varchar(32) | - | tidak | misalnya growpath-consult-v1 |
| answer | text | - | ya | null bila status failed |
| sources | jsonb | - | tidak | default '[]', daftar rujukan |
| guardrail_result | jsonb | - | tidak | default '{}', hasil pemeriksaan |
| token_count | integer | - | ya | >= 0 |
| latency_ms | integer | - | ya | >= 0 |
| status | enum | - | tidak | succeeded, blocked, failed |
| feedback | enum | - | ya | helpful, not_helpful |
| feedback_at | timestamptz | - | ya | wajib bila feedback terisi |
| created_at | timestamptz | - | tidak | default now() |

Indeks: `(consultation_id, created_at desc)`, `(status)`.

Aturan:

- `answer` null hanya boleh untuk status `failed`.
- `sources` tidak boleh berisi dokumen yang tidak ada di `knowledge_document`. Validasi di application layer.
- `feedback` hanya boleh diisi untuk status `succeeded` atau `blocked`.
- Data pribadi tidak dimasukkan ke `sources` atau `guardrail_result`.

Contoh `sources`:

```json
[
  {"type": "assessment", "ref": "dimension:PAS"},
  {"type": "document", "document_id": "uuid", "chunk_id": 12, "title": "Kurikulum UMKM Naik Kelas", "section": "Pasar"}
]
```

Contoh `guardrail_result`:

```json
{
  "checks": {
    "in_scope": true,
    "has_source": true,
    "no_legal_certainty": true,
    "no_sensitive_data": true,
    "length_ok": true
  },
  "blocked_reason": null
}
```

## 4. Perubahan entitas lama

| Entitas | Perubahan | Alasan |
|---|---|---|
| UMKMProfile | Field demografi diselaraskan menjadi 10 field: business_name, owner_name, gender, age, whatsapp, email, address, sector, established_year, operation_months | Mengikuti katalog DEM-01 sampai DEM-10 |
| UMKMProfile | `city`, `province`, `monthly_revenue_band`, `employees_count` dihapus | Diganti `address`, dan omzet atau SDM sudah diukur sebagai kriteria |
| Criterion | `input_type` menambah nilai `multi_select` | Katalog memakai SC, MA, NM, BL |
| Criterion | `scoring_rule` JSONB memuat opsi dan poin | Bobot dan poin adalah konfigurasi, bukan kode |
| Dimension | `weight` untuk Demografi 0, lima dimensi lain 20 | Demografi non-scoring, lima dimensi dinilai |
| Assessment | Menambah `started_at`, `scored_at`, dan `scoring_version` | Melacak durasi dan versi aturan skor |
| Roadmap | Menambah `model_name` dan `prompt_version` | Menjaga provenance bila narasi dibantu model |
| AIAnswerLog | Menyimpan `feedback` dan `feedback_at` | Umpan balik melekat pada satu jawaban |
| Semua tabel tenant | `tenant_id` tetap diulang | RLS dan query agregat |

## 5. Enum

| Enum | Nilai |
|---|---|
| tenant_type | platform, institution, partner |
| tenant_status | active, suspended, inactive |
| user_role | umkm, pendamping, mentor, admin_b2g, admin_platform |
| user_status | active, invited, suspended, deleted |
| gender_value | male, female, undisclosed |
| profile_sector | kuliner, fashion, kriya, pertanian, perdagangan, jasa, teknologi, kesehatan, pendidikan, lainnya |
| assessment_status | draft, submitted, scored, archived |
| input_type | boolean, scale, enum, number, text, multi_select |
| roadmap_status | draft, active, completed, superseded |
| roadmap_generated_by | rule, llm, hybrid, manual |
| milestone_status | pending, in_progress, done, skipped |
| consultation_status | pending, processing, completed, failed |
| ai_log_status | succeeded, blocked, failed |
| feedback_value | helpful, not_helpful |
| document_type | regulation, guideline, faq, template, other |
| document_status | draft, review, published, archived |
| plan_audience | umkm, institution |
| subscription_status | trialing, active, past_due, cancelled, expired |
| invoice_status | draft, issued, paid, void, overdue |
| mentor_session_status | requested, confirmed, completed, cancelled, no_show |
| report_type | monthly, quarterly, impact, custom |
| report_status | queued, generating, ready, failed |
| notification_channel | in_app, email, whatsapp |
| notification_status | queued, sent, failed, read |

Catatan: enum `gender_value` memakai bahasa Inggris di database, label Indonesia ada di UI. Ini menjaga nilai database stabil saat copy berubah.

## 6. Aturan null dan validasi utama

| Tabel | Aturan |
|---|---|
| tenant | slug unik, type dan status wajib |
| "user" | email unik, tenant_id wajib, role wajib |
| umkm_profile | user_id unik, completeness_pct 0 sampai 100, established_year 1900 sampai 2100, age 15 sampai 100 |
| assessment | total_score 0 sampai 100; status scored wajib punya segment_id dan total_score |
| assessment_answer | unik (assessment_id, criterion_id); score 0 sampai 100 |
| dimension_score | primary key gabungan; raw_score dan weighted_score 0 sampai 100 |
| segment | min_score < max_score; rentang 0 sampai 100 |
| roadmap | unik (assessment_id, version); satu roadmap active per assessment |
| milestone | unik (roadmap_id, order_no); estimated_cost >= 0 |
| progress_log | progress_pct 0 sampai 100; append-only |
| consultation | question 3 sampai 1000 karakter |
| ai_answer_log | answer null hanya untuk failed; feedback_at wajib bila feedback terisi |
| knowledge_document | expiry_date > effective_date bila keduanya ada |
| knowledge_chunk | unik (document_id, chunk_index); token_count > 0 |
| subscription | tepat satu owner, tenant_id atau user_id; period_start < period_end |
| invoice | number unik; due_at >= issued_at; amount >= 0 |
| report | period_start <= period_end |
| audit_log | append-only |

## 7. Retensi dan privasi

| Data | Retensi | Catatan |
|---|---|---|
| AuditLog | 24 bulan | Asumsi desain, belum diuji |
| Assessment dan jawaban | 5 tahun | Untuk reproduksi skor |
| Roadmap dan progres | 5 tahun | Untuk bukti dampak |
| Consultation dan AIAnswerLog | 24 bulan | Cukup untuk audit dan umpan balik |
| Invoice | 7 tahun | Fase 2 |
| Profil UMKM | selama akun aktif, anonimisasi 90 hari setelah permintaan | Belum diimplementasikan |
| Log aplikasi | 30 hari | Sesuai paket hosting |

Data pribadi yang tidak diperlukan tidak masuk log AI. Nomor WhatsApp dan alamat hanya ada di `umkm_profile`, tidak dikirim ke prompt kecuali benar-benar dibutuhkan untuk konteks, dan pada MVP tidak dikirim.

## 8. Pemetaan ke DDL

| Entitas | Tabel fisik |
|---|---|
| Tenant | tenant |
| User | "user" |
| UMKMProfile | umkm_profile |
| Dimension | dimension |
| Criterion | criterion |
| Assessment | assessment |
| AssessmentAnswer | assessment_answer |
| DimensionScore | dimension_score |
| Segment | segment |
| Roadmap | roadmap |
| Milestone | milestone |
| ProgressLog | progress_log |
| Consultation | consultation |
| AIAnswerLog | ai_answer_log |
| KnowledgeDocument | knowledge_document |
| KnowledgeChunk | knowledge_chunk |
| Plan | plan |
| Subscription | subscription |
| Invoice | invoice |
| MentorSession | mentor_session |
| Report | report |
| Notification | notification |
| AuditLog | audit_log |

DDL: `../08_Source/db/migrations/001_init.sql`. Seed: `../08_Source/db/seed/seed.sql`, penjelasan di `seed-data.md`.
