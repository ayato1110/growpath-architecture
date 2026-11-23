# ERD 3NF GROWPATH

**Deliverable:** P13-09, P13-11
**Pemilik:** Wisnu Nugroho
**Disusun oleh:** Tim Growpath P13, 22 November 2026
**Status:** v1.0, 23 entitas

## 1. Notasi dan sumber

Diagram memakai notasi crow's foot (IE notation): persegi untuk entitas, garis untuk relasi, simbol satu dan banyak di ujung relasi, serta lingkaran untuk relasi opsional. Sumber notasi: Redgate Data Modeler, *Crow's Foot Notation*, diakses 22 November 2026; Gordon Everest (1976) sebagai asal notasi.

File: `diagrams/erd-3nf.drawio`, empat halaman.

| Halaman | Isi | PNG |
|---|---|---|
| Inti | Tenant, User, UMKMProfile, Assessment, Segment, DimensionScore | `diagrams/erd-inti.png` |
| Katalog dan Jawaban | Assessment, AssessmentAnswer, Criterion, Dimension | `diagrams/erd-katalog-jawaban.png` |
| Advisory dan AI | Assessment, Roadmap, Milestone, ProgressLog, Consultation, AIAnswerLog, KnowledgeDocument, KnowledgeChunk | `diagrams/erd-advisory-ai.png` |
| Pendukung Fase 2 | Tenant, User, Subscription, Plan, Invoice, MentorSession, Report, Notification, AuditLog | `diagrams/erd-pendukung-fase2.png` |

Entitas yang muncul di dua halaman adalah rujukan agar relasi tetap terbaca. Entitas fisiknya hanya satu.

## 2. Daftar entitas

| No | Entitas | Fungsi | PK | FK utama | Keterangan |
|---:|---|---|---|---|---|
| 1 | Tenant | Institusi B2G atau tenant platform | id | plan_id | Tetap ada pada MVP satu tenant |
| 2 | User | Akun pengguna dan peran | id | tenant_id | Satu pengguna satu tenant |
| 3 | UMKMProfile | Profil usaha dan data demografi | id | user_id, tenant_id | user_id unik |
| 4 | Dimension | Enam aspek framework | id | - | Demografi is_scored false |
| 5 | Criterion | 31 kriteria scoring | id | dimension_id | Katalog berversi |
| 6 | Assessment | Satu sesi asesmen | id | tenant_id, umkm_profile_id, segment_id | Menyimpan skor total |
| 7 | AssessmentAnswer | Jawaban per kriteria | id | assessment_id, criterion_id | Unik per asesmen dan kriteria |
| 8 | DimensionScore | Skor per dimensi | assessment_id, dimension_id | assessment_id, dimension_id | Enam baris per asesmen |
| 9 | Segment | Empat segmen kematangan | id | - | Ambang 0, 30, 55, 80 |
| 10 | Roadmap | Rencana aksi per asesmen | id | tenant_id, assessment_id | Berversi |
| 11 | Milestone | Langkah rencana aksi | id | roadmap_id | 3 sampai 5 per roadmap |
| 12 | ProgressLog | Riwayat progres milestone | id | tenant_id, milestone_id, user_id | Append-only |
| 13 | Consultation | Sesi pertanyaan pengguna | id | tenant_id, user_id, assessment_id | Satu pertanyaan per baris |
| 14 | AIAnswerLog | Jawaban, metadata, dan umpan balik | id | consultation_id | Satu atau lebih per consultation |
| 15 | KnowledgeDocument | Dokumen rujukan | id | tenant_id, reviewer_id | tenant_id null berarti global |
| 16 | KnowledgeChunk | Potongan dokumen dan embedding | id | document_id | vector 768 |
| 17 | Plan | Paket langganan | id | - | Fase 2 untuk billing |
| 18 | Subscription | Langganan tenant atau user | id | tenant_id, user_id, plan_id | Owner polimorfik |
| 19 | Invoice | Tagihan langganan | id | subscription_id | Retensi 7 tahun |
| 20 | MentorSession | Sesi dengan mentor | id | tenant_id, umkm_profile_id, mentor_id | Fase 2 |
| 21 | Report | Laporan agregat B2G | id | tenant_id, generated_by | Fase 2 |
| 22 | Notification | Notifikasi pengguna | id | tenant_id, user_id | Kanal whatsapp fase 2 |
| 23 | AuditLog | Peristiwa keamanan | id | tenant_id, actor_user_id | Append-only |

Perubahan dari kamus data lama:

- `Consultation` dan `AIAnswerLog` adalah entitas baru.
- `AIAnswerLog` menyimpan `feedback` dan `feedback_at` agar umpan balik tidak butuh entitas keempat.
- `Criterion.input_type` menambah nilai `multi_select`.
- `Dimension` menyimpan `is_scored`, `Criterion` tidak perlu karena semua kriteria di bawah dimensi yang dinilai adalah scoring.
- `UMKMProfile` tetap memuat sepuluh field demografi. Demografi tidak dibuat sebagai `Criterion` karena bukan pertanyaan berskor.

## 3. Relasi dan kardinalitas

| Sumber | Tujuan | Kardinalitas | Arti |
|---|---|---|---|
| Tenant | User | 1 ke 0..* | Tenant memiliki pengguna |
| User | UMKMProfile | 1 ke 0..1 | Satu akun satu profil usaha |
| UMKMProfile | Assessment | 1 ke 0..* | Profil dapat punya banyak asesmen |
| Segment | Assessment | 1 ke 0..* | Segmen ditentukan setelah skor |
| Assessment | AssessmentAnswer | 1 ke 0..* | Satu jawaban per kriteria |
| Criterion | AssessmentAnswer | 1 ke 0..* | Satu kriteria dijawab di banyak asesmen |
| Dimension | Criterion | 1 ke 0..* | Dimensi berisi kriteria |
| Assessment | DimensionScore | 1 ke 0..6 | Enam aspek, satu baris per aspek |
| Dimension | DimensionScore | 1 ke 0..* | Skor per dimensi |
| Assessment | Roadmap | 1 ke 0..* | Roadmap berversi |
| Roadmap | Milestone | 1 ke 0..* | Tiga sampai lima langkah |
| Milestone | ProgressLog | 1 ke 0..* | Riwayat progres |
| User | ProgressLog | 1 ke 0..* | Pencatat progres |
| Assessment | Consultation | 1 ke 0..* | Konsultasi memakai konteks asesmen |
| User | Consultation | 1 ke 0..* | Pemilik pertanyaan |
| Consultation | AIAnswerLog | 1 ke 0..* | Satu pertanyaan dapat punya percobaan jawaban |
| KnowledgeDocument | KnowledgeChunk | 1 ke 0..* | Dokumen dipecah menjadi chunk |
| Plan | Subscription | 1 ke 0..* | Paket langganan |
| Subscription | Invoice | 1 ke 0..* | Tagihan |
| Tenant | MentorSession | 1 ke 0..* | Fase 2 |
| Tenant | Report | 1 ke 0..* | Fase 2 |
| User | Notification | 1 ke 0..* | Penerima notifikasi |
| Tenant | AuditLog | 1 ke 0..* | Jejak audit |

## 4. Bukti 3NF

### 4.1 First Normal Form

Setiap kolom menyimpan satu nilai atomik. Pengecualian yang disengaja adalah kolom JSONB:

- `Criterion.scoring_rule`: daftar opsi dan poin untuk satu kriteria.
- `AssessmentAnswer.raw_value`: jawaban mentah yang tipenya berbeda per kriteria.
- `Milestone.action_items`: daftar tindakan kecil dalam satu milestone.
- `AIAnswerLog.sources`: daftar sumber yang dipakai satu jawaban.
- `AIAnswerLog.guardrail_result`: hasil pemeriksaan guardrail.
- `Report.parameters`: parameter laporan.

JSONB dipakai karena bentuk payload berubah mengikuti konfigurasi, bukan karena malas menormalisasi. Tidak ada query lintas opsi yang dibutuhkan pada MVP. Jika nanti perlu filter per opsi, `CriterionOption` dapat ditambahkan lewat Change Request.

### 4.2 Second Normal Form

Semua tabel memakai primary key tunggal berupa UUID atau bigint, kecuali `DimensionScore` yang memakai composite key `(assessment_id, dimension_id)`. Pada `DimensionScore`, tidak ada atribut non-kunci yang bergantung pada sebagian key: `raw_score`, `weighted_score`, dan `is_scored` bergantung pada pasangan asesmen dan dimensi.

Pada tabel lain, tidak ada dependensi parsial karena key-nya tunggal.

### 4.3 Third Normal Form

Tidak ada dependensi transitif antar atribut non-kunci:

- Nama dimensi dan kode ada di `Dimension`, bukan diulang di `Criterion`.
- Nama segmen dan ambang ada di `Segment`, bukan diulang di `Assessment`.
- Poin opsi ada di `Criterion.scoring_rule`, bukan di `AssessmentAnswer`.
- Data profil usaha ada di `UMKMProfile`, bukan diulang di `Assessment`.
- `Roadmap` dan `Milestone` dipisah karena satu roadmap punya banyak langkah.

Kolom turunan yang disimpan untuk audit:

| Kolom | Asal | Alasan disimpan |
|---|---|---|
| `Assessment.total_score` | Perhitungan dari `AssessmentAnswer` dan `Criterion.weight` | Membekukan hasil saat asesmen dikunci |
| `Assessment.segment_id` | Pemetaan skor ke `Segment` | Membekukan segmen saat asesmen dikunci |
| `DimensionScore.raw_score` dan `weighted_score` | Perhitungan per dimensi | Mempercepat tampilan dan audit |
| `UMKMProfile.completeness_pct` | Kelengkapan field profil | Mempercepat pemeriksaan prasyarat |
| `Milestone.status` | Proyeksi dari `ProgressLog` terbaru | Mempercepat tampilan daftar langkah |

Kolom turunan tidak diedit manual. Nilainya dihitung ulang oleh layanan terkait.

### 4.4 Denormalisasi yang disengaja

`tenant_id` diulang pada tabel yang terikat tenant untuk row-level security dan query agregat. Konsistensi dijaga oleh layanan aplikasi dan dapat ditambah trigger di P14. Ini bukan pelanggaran 3NF karena `tenant_id` adalah foreign key, bukan atribut deskriptif yang bergantung pada non-kunci.

## 5. Keputusan desain penting

1. Demografi tidak masuk skor berbobot. `UMKMProfile.completeness_pct` hanya mengukur kelengkapan.
2. `DimensionScore` selalu enam baris, termasuk Demografi dengan `is_scored = false`.
3. Satu `Consultation` dapat punya beberapa `AIAnswerLog` untuk percobaan ulang. Yang ditampilkan adalah log dengan `created_at` terbaru berstatus `succeeded` atau `blocked`.
4. Umpan balik disimpan di `AIAnswerLog`, bukan tabel terpisah, karena umpan balik melekat pada satu jawaban.
5. Sumber jawaban disimpan sebagai JSONB berisi rujukan chunk, bukan foreign key, karena satu jawaban dapat memakai beberapa chunk.
6. `Criterion` memakai `version` dan `Assessment` memakai `scoring_version` agar skor lama dapat direproduksi.

## 6. Yang belum final

- Bobot resmi per kriteria belum ditemukan. Default 1/31.
- Batas segmen 30, 55, dan 80 masih mengikuti materi, belum diverifikasi ke dokumen resmi.
- Tipe input dan poin per opsi masih draft yang perlu divalidasi fasilitator.
- RLS baru target. Implementasi penuh diuji P14.
- View laporan B2G belum dibuat karena dashboard B2G di luar MVP.

## 7. Aturan perubahan

- Perubahan entitas harus memperbarui `kamus-data-p13.md`, `../08_Source/db/migrations/001_init.sql`, dan traceability.
- Jangan menambah entitas baru tanpa Change Request dan alasan yang bisa diuji.
- Jangan memindahkan data turunan menjadi sumber kebenaran.
