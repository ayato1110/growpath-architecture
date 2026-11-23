# TRACEABILITY MATRIX GROWPATH

**Deliverables:** P13-20 dan P13-11 (bagian aplikasi)
**Pemilik:** Mhd Farras Delvioza dan Ripa Bagaskara
**Disusun oleh:** Tim Growpath P13, 22 November 2026
**Status:** v1.0, 15 baris

## 1. Aturan

Setiap baris menghubungkan kebutuhan nyata ke use case, user story, tabel, layar, dan endpoint. Baris tanpa tabel atau endpoint berarti kebutuhan non-fungsional yang diverifikasi lewat uji, bukan lewat satu endpoint.

Kolom bukti menunjuk file yang bisa diperiksa. Tidak ada baris yang hanya berisi niat.

## 2. Matriks

| ID | Kebutuhan | Use case | User story | Tabel utama | Layar | Endpoint | Bukti |
|---|---|---|---|---|---|---|---|
| TR-01 | UMKM perlu menyimpan profil usahanya sekali dan memakainya sebagai konteks | UC-02 | US-01 | `tenant`, `user`, `umkm_profile` | Data usaha, Profil | `GET /me/profile`, `PUT /me/profile`, `PATCH /me/profile` | `use-cases.md`, `../08_Source/db/migrations/001_init.sql` |
| TR-02 | Asesmen 31 kriteria harus bisa diselesaikan bertahap tanpa kehilangan jawaban | UC-03 | US-02 | `assessment`, `assessment_answer`, `criterion`, `dimension` | Asesmen | `POST /assessments`, `GET /assessments/{id}`, `PUT /assessments/{id}/answers` | `kamus-data-p13.md`, `bpmn-target.md` |
| TR-03 | Pengguna harus memeriksa jawaban sebelum skor dihitung | UC-04 | US-03 | `assessment`, `assessment_answer` | Tinjau jawaban | `POST /assessments/{id}/submit` | `user-stories.md` US-03 |
| TR-04 | Skor harus deterministik dan bisa direproduksi | UC-04, UC-05 | US-04 | `dimension_score`, `segment`, `assessment.scoring_version` | Hasil asesmen | `GET /assessments/{id}/scores` | `../02_Data/P13-31-Kriteria.md`, `nfr.md` NFR-05 |
| TR-05 | Rekomendasi harus berupa langkah yang bisa dikerjakan dan dilacak | UC-06 | US-05 | `roadmap`, `milestone`, `progress_log` | Rencana aksi | `GET /assessments/{id}/roadmap`, `PATCH /milestones/{id}` | `moscow-backlog.md` B-03 |
| TR-06 | Konsultasi AI harus memakai konteks asesmen, bukan jawaban generik | UC-07 | US-06 | `consultation`, `ai_answer_log`, `knowledge_document`, `knowledge_chunk` | Konsultasi | `POST /consultations` | `ai-architecture.md` |
| TR-07 | Setiap jawaban AI wajib punya log yang bisa dibuka lagi | UC-07, UC-08 | US-06, US-07 | `ai_answer_log` | Konsultasi, Log jawaban | `GET /consultations`, `GET /consultations/{id}` | `ai-architecture.md` bagian log schema |
| TR-08 | Pengguna harus bisa menilai kegunaan jawaban | UC-08 | US-07 | `ai_answer_log.feedback`, `feedback_at` | Log jawaban, detail | `POST /consultations/{id}/feedback` | `katalog` feedback di `ai-architecture.md` |
| TR-09 | Dashboard harus menjawab satu pertanyaan: apa langkah berikutnya | UC-09 | US-08 | `assessment`, `dimension_score`, `milestone` | Beranda | `GET /me/dashboard` | `moscow-backlog.md` B-05 |
| TR-10 | Kuota AI harus mencegah biaya tak terkendali dan dijelaskan ke pengguna | UC-07 | US-06 | `ai_answer_log`, konfigurasi kuota | Konsultasi, pesan kuota | `POST /consultations` dengan respons 429 | `ai-architecture.md` bagian kuota |
| TR-11 | Data satu pengguna tidak boleh terlihat pengguna lain | UC-01 sampai UC-09 | Semua | Semua tabel ber-`tenant_id` dan `user_id` | Semua | Semua endpoint dengan JWT | `security-checklist.md` SEC-03 |
| TR-12 | Katalog kriteria harus berversi agar skor lama tidak berubah | UC-03, UC-04 | US-02, US-04 | `criterion.version`, `assessment.scoring_version` | Asesmen, Hasil | `POST /assessments`, `GET /assessments/{id}/scores` | `kamus-data-p13.md` bagian versi |
| TR-13 | Alur utama harus selesai di bawah 12 menit pada ponsel 390px | UC-03, UC-04 | US-02, US-03 | Tidak ada tabel baru | Asesmen, Tinjau | Tidak ada endpoint khusus | `nfr.md` NFR-01, `vision-v1.md` KPI-2 |
| TR-14 | Halaman harus bisa dipakai dengan keyboard dan pembaca layar | UC-01 sampai UC-09 | Semua | Tidak ada tabel baru | Semua | Tidak ada endpoint khusus | `nfr.md` NFR-07, `security-checklist.md` |
| TR-15 | Jawaban AI harus bisa diaudit sampai prompt dan model yang dipakai | UC-07, UC-08 | US-06, US-07 | `ai_answer_log.model`, `prompt_version`, `guardrail_result` | Log detail | `GET /consultations/{id}` | `ai-architecture.md` bagian log schema |

## 3. Cakupan per Must

| Must | Baris traceability | Status |
|---|---|---|
| M-01 Data usaha | TR-01, TR-11 | Tertutup |
| M-02 Konsultasi AI | TR-06, TR-10, TR-15 | Tertutup |
| M-03 Rekomendasi | TR-02, TR-03, TR-04, TR-05, TR-12 | Tertutup |
| M-04 Log jawaban AI | TR-07, TR-08, TR-15 | Tertutup |
| M-05 Dashboard | TR-09 | Tertutup |

## 4. Yang belum ditelusuri

- Harga dan lisensi B2G belum punya kebutuhan fungsional karena dashboard B2G belum dibangun.
- Admin CMS dan pengelolaan katalog belum punya layar MVP.
- Notifikasi email belum masuk MVP.
- Migrasi data dari spreadsheet belum masuk MVP, hanya rencana P15.

## 5. Aturan pemutakhiran

1. Setiap user story baru wajib menambah minimal satu baris.
2. Setiap tabel baru wajib muncul di minimal satu baris.
3. Setiap endpoint baru wajib muncul di minimal satu baris.
4. Baris yang tidak bisa menunjuk file bukti dianggap belum selesai.
