# Bukti Normalisasi 3NF & Pemetaan Skema MVP Growpath (P13)

- **Proyek:** Growpath — Platform Advisory UMKM Berbasis AI (Kelompok 6, Kelas R-001)
- **Fase:** P13 · Pembekuan Arsitektur dan Desain Sistem (Gate 1 · Design Review)
- **Disusun oleh:** Wisnu Nugroho (F1E124032) — Database Architect
- **Direview oleh:** Bagas Adinata (Programmer), Ripa Bagaskara (CEO / AI Engineer)
- **Tanggal:** 22 November 2026

## 1. Ringkasan Cakupan Skema

Skema basis data Growpath terdiri dari **24 entitas**:
- **21 entitas arsitektur lengkap (Progress 12):** `tenants`, `users`, `umkm_profiles`, `assessments`, `assessment_answers`, `dimensions`, `criteria`, `dimension_scores`, `segments`, `roadmaps`, `milestones`, `progress_logs`, `mentor_sessions`, `plans`, `subscriptions`, `invoices`, `knowledge_documents`, `knowledge_chunks`, `reports`, `notifications`, dan `audit_logs`.
- **3 entitas khusus AI untuk P13–P14 Kelompok 6:** `ai_consultations`, `ai_response_logs`, dan `ai_usage_quotas`.

## 2. Pembuktian Normalisasi (UNF → 1NF → 2NF → 3NF)

### A. Kondisi Awal (Unnormalized Form / UNF) — Proses Pembinaan Manual (As-Is)
Pada proses manual berbasis Google Form dan Excel, seluruh data UMKM, 31 jawaban kriteria, skor 6 dimensi, segmen, saran fasilitator, dan riwayat konsultasi dicatat dalam satu lembar kerja (*flat sheet*) dengan atribut berulang (`kriteria_1..kriteria_31`, `milestone_1..milestone_5`, `catatan_sesi_1..N`). Hal ini memicu anomali *insert*, *update*, dan *delete*.

### B. First Normal Form (1NF) — Atomisitas Nilai & Penghapusan Kelompok Berulang
- Setiap sel menyimpan nilai atomik dan setiap tabel memiliki *primary key* unik (`UUID` untuk tabel transaksional, `SMALLINT` untuk tabel referensi, `BIGINT IDENTITY` untuk log).
- Kelompok berulang 31 jawaban asesmen dipisahkan ke baris individual di `assessment_answers` dengan kunci unik `(assessment_id, criterion_id)`.
- Kelompok berulang langkah rekomendasi dipisahkan ke baris individual di `milestones` dengan kunci unik `(roadmap_id, order_no)`.
- Kelompok berulang percakapan konsultasi AI dipisahkan menjadi sesi (`ai_consultations`) dan log tiap giliran tanya-jawab (`ai_response_logs`).
- Potongan dokumen RAG dipisahkan ke `knowledge_chunks` dengan kunci unik `(document_id, chunk_index)`.

### C. Second Normal Form (2NF) — Menghilangkan Ketergantungan Parsial
- Seluruh tabel ber-PK tunggal otomatis memenuhi 2NF karena setiap atribut non-kunci bergantung penuh pada PK.
- Pada tabel ber-PK komposit `dimension_scores (assessment_id, dimension_id)`, seluruh atribut non-kunci (`raw_score`, `weighted_score`, `is_scored`, `computed_at`) bergantung penuh pada kombinasi **kedua** kunci (`assessment_id` dan `dimension_id`), bukan hanya pada salah satunya.
- Atribut master dimensi (`name`, `weight`) tidak disimpan ulang di `dimension_scores`, melainkan tetap di tabel `dimensions`.

### D. Third Normal Form (3NF) — Menghilangkan Ketergantungan Transitif
Setiap atribut non-kunci hanya bergantung pada *primary key*, tidak melalui atribut non-kunci lain:
- `umkm_profiles` memisahkan data usaha dari akun pengguna (`users`) dan institusi (`tenants`), sehingga pembaruan nama institusi cukup dilakukan sekali di `tenants`.
- `criteria` hanya menyimpan `dimension_id` (FK), tidak mengulang nama atau bobot dimensi.
- `assessments` menyimpan `segment_id` (FK ke `segments`), bukan mengulang nama segmen, rentang skor, atau kurikulum di setiap baris asesmen.
- `subscriptions` mereferensikan `plan_id` (FK ke `plans`), tidak mengulang nama paket atau kuota UMKM.
- `ai_response_logs` mereferensikan `consultation_id` (FK ke `ai_consultations`), tidak mengulang topik atau kategori sesi konsultasi di setiap baris log.
- `ai_usage_quotas` memisahkan pelacakan kuota periode (`period_start`, `period_end`, `quota_limit`, `used_count`) dari tabel `users` agar histori kuota per periode tidak menimpa data pengguna.

## 3. Catatan Denormalisasi Terkendali & Kolom Turunan

Beberapa kolom sengaja disimpan secara terkendali dengan alasan kinerja, audit, dan keamanan multi-tenant:

| Pola | Tabel Terdampak | Alasan Teknis | Kontrol Konsistensi |
|---|---|---|---|
| **Pengulangan `tenant_id`** | `umkm_profiles`, `assessments`, `roadmaps`, `progress_logs`, `ai_consultations`, `ai_response_logs`, `ai_usage_quotas`, `mentor_sessions`, `reports`, `notifications`, `audit_logs` | Mempercepat *Row-Level Security* (RLS) PostgreSQL dan kueri agregat dasbor B2G tanpa *join* bertingkat. | Wajib sama dengan `users.tenant_id`; dijaga oleh *application service* dan *trigger* di P14. |
| **Kolom turunan (snapshot audit)** | `assessments.total_score`, `assessments.segment_id`, `dimension_scores.weighted_score`, `umkm_profiles.completeness_pct`, `milestones.status` | Menjaga hasil diagnosis historis tetap dapat diaudit meskipun versi bobot kriteria berubah di kemudian hari. | Hanya dihitung oleh *scoring/progress service*, tidak boleh diedit manual. |
| **Kolom `JSONB` terbatas** | `criteria.scoring_rule`, `assessment_answers.raw_value`, `milestones.action_items`, `ai_response_logs.citations`, `reports.parameters`, `audit_logs.before_data/after_data` | Menampung struktur semi-terstruktur yang bentuknya bervariasi (misalnya aturan skor tiap tipe input atau daftar sitasi RAG). | Validasi skema dilakukan di Pydantic (FastAPI) sebelum disimpan. |
| **Tabel *append-only*** | `progress_logs`, `ai_response_logs`, `audit_logs` | Menjamin jejak audit dan bukti penafian (*disclaimer*) AI tidak dapat diubah diam-diam. | Tidak memiliki `updated_at`; hak `UPDATE`/`DELETE` dibatasi di level peran DB. |

## 4. Pemetaan 5 Fitur Must MVP ke Tabel (Untuk Matriks Ketelusuran Farras)

| Fitur Must MVP | Tabel Utama yang Digunakan | Aturan Integritas Kritis di DB |
|---|---|---|
| **1. Data Usaha** | `tenants`, `users`, `umkm_profiles` | `users.email` unik; `umkm_profiles.user_id` unik (1:1); `completeness_pct` 0–100; `established_year` 1900–2100. |
| **2. Konsultasi AI** | `ai_consultations`, `ai_usage_quotas`, `knowledge_documents`, `knowledge_chunks` | `used_count <= quota_limit`; satu kuota unik per `(user_id, period_start, period_end)`; konteks usaha terikat `umkm_profile_id`. |
| **3. Rekomendasi (Mesin 31 Kriteria)** | `dimensions`, `criteria`, `segments`, `assessments`, `assessment_answers`, `dimension_scores`, `roadmaps`, `milestones` | Unik `(assessment_id, criterion_id)`; status `scored` wajib punya `segment_id` & `total_score`; maks. 1 roadmap `active` per asesmen. |
| **4. Log Jawaban AI** | `ai_response_logs`, `audit_logs` | *Append-only*; `CHECK (disclaimer_shown = TRUE)` menjamin penafian selalu tampil; `guardrail_status` mencatat batasan saran; `user_rating` 1–5 untuk UAT P15. |
| **5. Dasbor** | `umkm_profiles`, `assessments`, `dimension_scores`, `roadmaps`, `milestones`, `progress_logs`, `ai_response_logs`, `ai_usage_quotas` | Indeks komposit pada `(tenant_id, umkm_profile_id, created_at DESC)` dan *view* agregasi dasbor (dibangun di P14). |
