# DATA DICTIONARY GROWPATH

- **Fase:** P13 · Pembekuan Arsitektur & Desain Sistem (Pembaruan 24 Entitas)
- **Disusun oleh:** Wisnu Nugroho (F1E124032) — Database Architect
- **Direview oleh:** Bagas Adinata (Programmer), Ripa Bagaskara (CEO / AI Engineer)
- **Tanggal:** 22 November 2026

Dokumen ini memuat definisi entitas, atribut, kunci, constraint, dan catatan normalisasi untuk model data Growpath. Jumlah entitas 24: 14 entitas inti Progress 12, 7 entitas pendukung Progress 12, dan 3 entitas AI (P13–P14 Kelompok 6: `AIConsultation`, `AIResponseLog`, `AIUsageQuota`). Tipe data mengikuti PostgreSQL 15+ dengan `uuid`, `citext`, `jsonb`, `timestamptz`, dan `vector(768)` dari pgvector.

## Ringkasan entitas

| Entitas | Definisi | PK | FK utama | Retensi |
|---|---|---|---|---|
| Tenant | Institusi B2G atau tenant platform yang memiliki pengguna, langganan, laporan, dan batas data. | id | plan_id -> Plan.id | Selama kontrak dan 24 bulan setelah berakhir. |
| User | Akun pengguna dengan peran dan tenant aktif. Satu pengguna hanya terikat pada satu tenant. | id | tenant_id -> Tenant.id | Selama akun aktif dan 24 bulan setelah penghapusan. |
| UMKMProfile | Profil usaha satu pengguna UMKM, termasuk data demografi dan kelengkapan profil. | id | user_id -> User.id; tenant_id -> Tenant.id | Selama akun aktif; anonimisasi 90 hari setelah permintaan. |
| Assessment | Satu sesi asesmen 31 kriteria untuk satu profil UMKM, menyimpan skor total dan segmen. | id | tenant_id -> Tenant.id; umkm_profile_id -> UMKMProfile.id; segment_id -> Segment.id | 5 tahun. |
| AssessmentAnswer | Jawaban satu kriteria dalam satu asesmen. | id | assessment_id -> Assessment.id; criterion_id -> Criterion.id | 5 tahun. |
| Dimension | Enam dimensi framework: Demografi, Psikografi, Proses Internal, Pasar, Lingkungan, Keuangan. | id | Tidak ada. | Referensi permanen. |
| Criterion | 31 kriteria scoring beserta bobot, tipe input, dan aturan skor. | id | dimension_id -> Dimension.id | Referensi permanen; versi lama disimpan. |
| DimensionScore | Skor satu dimensi untuk satu asesmen; enam baris per asesmen. | assessment_id, dimension_id | assessment_id -> Assessment.id; dimension_id -> Dimension.id | 5 tahun. |
| Segment | Empat segmen kematangan usaha dan rentang skornya. | id | Tidak ada. | Referensi permanen. |
| Roadmap | Roadmap personal untuk satu asesmen, berisi versi dan status. | id | tenant_id -> Tenant.id; assessment_id -> Assessment.id | 5 tahun. |
| Milestone | Langkah roadmap dengan status, tenggat, dan action items. | id | roadmap_id -> Roadmap.id | 5 tahun. |
| ProgressLog | Catatan progres append-only untuk satu milestone. | id | tenant_id -> Tenant.id; milestone_id -> Milestone.id; user_id -> User.id | 5 tahun. |
| MentorSession | Sesi konsultasi UMKM dengan mentor, termasuk jadwal, catatan, dan bagi hasil. | id | tenant_id -> Tenant.id; umkm_profile_id -> UMKMProfile.id; mentor_id -> User.id | 5 tahun. |
| Plan | Paket langganan Free, Premium, dan B2G beserta kuota dan harga. | id | Tidak ada. | Referensi permanen; paket nonaktif disimpan. |
| Subscription | Langganan tenant B2G atau pengguna Premium. | id | tenant_id -> Tenant.id; user_id -> User.id; plan_id -> Plan.id | 7 tahun untuk catatan keuangan. |
| Invoice | Tagihan untuk satu langganan. | id | subscription_id -> Subscription.id | 7 tahun. |
| KnowledgeDocument | Dokumen pengetahuan resmi untuk RAG, dengan versi, masa berlaku, dan status review. | id | tenant_id -> Tenant.id; reviewer_id -> User.id | Sampai kedaluwarsa ditambah 2 tahun. |
| KnowledgeChunk | Potongan dokumen dan embedding untuk pencarian RAG. | id | document_id -> KnowledgeDocument.id | Mengikuti dokumen induk. |
| Report | Laporan agregat B2G untuk periode tertentu. | id | tenant_id -> Tenant.id; generated_by -> User.id | 5 tahun. |
| Notification | Notifikasi email atau in-app untuk pengguna. | id | tenant_id -> Tenant.id; user_id -> User.id | 12 bulan. |
| AuditLog | Catatan peristiwa keamanan dan perubahan data yang append-only. | id | tenant_id -> Tenant.id; actor_user_id -> User.id | 24 bulan. |
| AIConsultation | Sesi konsultasi AI berbasis konteks profil usaha dan asesmen UMKM. | id | tenant_id -> Tenant.id; umkm_profile_id -> UMKMProfile.id; user_id -> User.id; assessment_id -> Assessment.id | 5 tahun. |
| AIResponseLog | Log append-only tanya-jawab AI beserta penafian wajib, sitasi, status guardrail, dan rating UAT. | id | tenant_id -> Tenant.id; consultation_id -> AIConsultation.id; user_id -> User.id | 24 bulan. |
| AIUsageQuota | Pelacakan batas kuota konsultasi dan token AI per pengguna per periode. | id | tenant_id -> Tenant.id; user_id -> User.id | 24 bulan. |

## Relasi dan kardinalitas

| Entitas sumber | Entitas tujuan | Kardinalitas | Nama relasi | Foreign key |
|---|---|---|---|---|
| Tenant | User | 1..* | memiliki | User.tenant_id |
| Tenant | UMKMProfile | 1..* | menaungi | UMKMProfile.tenant_id |
| User | UMKMProfile | 1..0..1 | memiliki profil | UMKMProfile.user_id (unik) |
| UMKMProfile | Assessment | 1..* | mengisi | Assessment.umkm_profile_id |
| Assessment | AssessmentAnswer | 1..* | menjawab | AssessmentAnswer.assessment_id |
| Criterion | AssessmentAnswer | 1..* | dijawab | AssessmentAnswer.criterion_id |
| Dimension | Criterion | 1..* | berisi | Criterion.dimension_id |
| Assessment | DimensionScore | 1..6 | menghitung | DimensionScore.assessment_id |
| Dimension | DimensionScore | 1..* | dihitung | DimensionScore.dimension_id |
| Segment | Assessment | 1..* | menentukan | Assessment.segment_id |
| Assessment | Roadmap | 1..* | menyusun versi | Roadmap.assessment_id |
| Roadmap | Milestone | 1..* | memiliki | Milestone.roadmap_id |
| Milestone | ProgressLog | 1..* | mencatat | ProgressLog.milestone_id |
| User | ProgressLog | 1..* | memperbarui | ProgressLog.user_id |
| Tenant | MentorSession | 1..* | mengelola | MentorSession.tenant_id |
| UMKMProfile | MentorSession | 1..* | mengikuti | MentorSession.umkm_profile_id |
| User | MentorSession | 1..* | menjadi mentor | MentorSession.mentor_id |
| Plan | Subscription | 1..* | dipilih | Subscription.plan_id |
| Tenant | Subscription | 1..* | berlangganan | Subscription.tenant_id |
| User | Subscription | 1..* | berlangganan | Subscription.user_id |
| Subscription | Invoice | 1..* | menagih | Invoice.subscription_id |
| KnowledgeDocument | KnowledgeChunk | 1..* | dipecah | KnowledgeChunk.document_id |
| User | KnowledgeDocument | 1..* | mereview | KnowledgeDocument.reviewer_id |
| Tenant | KnowledgeDocument | 1..* | memiliki | KnowledgeDocument.tenant_id (opsional) |
| Tenant | Report | 1..* | menyusun | Report.tenant_id |
| Tenant | Notification | 1..* | mengirim | Notification.tenant_id |
| User | Notification | 1..* | menerima | Notification.user_id |
| Tenant | AuditLog | 1..* | mencatat | AuditLog.tenant_id |
| User | AuditLog | 1..* | menjadi aktor | AuditLog.actor_user_id |
| Tenant | AIConsultation | 1..* | menaungi sesi AI | AIConsultation.tenant_id |
| UMKMProfile | AIConsultation | 1..* | berkonsultasi | AIConsultation.umkm_profile_id |
| User | AIConsultation | 1..* | memulai sesi | AIConsultation.user_id |
| Assessment | AIConsultation | 1..0..* | menjadi konteks | AIConsultation.assessment_id |
| AIConsultation | AIResponseLog | 1..* | merekam jawaban | AIResponseLog.consultation_id |
| User | AIResponseLog | 1..* | mengirim prompt | AIResponseLog.user_id |
| Tenant | AIUsageQuota | 1..* | membatasi kuota | AIUsageQuota.tenant_id |
| User | AIUsageQuota | 1..* | memiliki kuota | AIUsageQuota.user_id |

## Atribut per entitas

### Tenant

Institusi B2G atau tenant platform yang memiliki pengguna, langganan, laporan, dan batas data.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | NOT NULL | default gen_random_uuid() |
| name | varchar(160) | - | NOT NULL | - |
| slug | varchar(80) | UQ | NOT NULL | unik |
| type | enum | - | NOT NULL | platform, institution, partner |
| status | enum | - | NOT NULL | active, suspended, inactive |
| contact_email | citext | - | NULL | - |
| plan_id | smallint | FK | NULL | Plan.id |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** plan_id -> Plan.id. **Constraint:** slug unik; type dan status dibatasi enum.. **Normalisasi:** Plan dipisah ke tabel referensi. tenant_id tidak diulang di Tenant..

### User

Akun pengguna dengan peran dan tenant aktif. Satu pengguna hanya terikat pada satu tenant.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | NOT NULL | Supabase auth.users.id |
| tenant_id | uuid | FK | NOT NULL | Tenant.id |
| email | citext | UQ | NOT NULL | unik |
| full_name | varchar(120) | - | NOT NULL | - |
| phone | varchar(20) | - | NULL | - |
| role | enum | - | NOT NULL | umkm, pendamping, mentor, admin_b2g, admin_platform |
| status | enum | - | NOT NULL | active, invited, suspended, deleted |
| last_login_at | timestamptz | - | NULL | - |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** tenant_id -> Tenant.id. **Constraint:** email unik; role dan status dibatasi enum.. **Normalisasi:** tenant_id langsung, bukan tabel keanggotaan, karena satu UMKM satu tenant..

### UMKMProfile

Profil usaha satu pengguna UMKM, termasuk data demografi dan kelengkapan profil.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | NOT NULL | - |
| user_id | uuid | FK | NOT NULL | User.id, unik |
| tenant_id | uuid | FK | NOT NULL | Tenant.id |
| business_name | varchar(160) | - | NOT NULL | - |
| owner_name | varchar(120) | - | NOT NULL | - |
| sector | enum | - | NOT NULL | kuliner, fashion, lainnya |
| city | varchar(80) | - | NOT NULL | - |
| province | varchar(80) | - | NOT NULL | - |
| established_year | smallint | - | NOT NULL | 1900-2100 |
| operation_months | smallint | - | NOT NULL | >= 0 |
| monthly_revenue_band | enum | - | NULL | <1jt, 1-5jt, 5-25jt, >25jt |
| employees_count | smallint | - | NULL | >= 0 |
| business_description | text | - | NULL | - |
| completeness_pct | numeric(5,2) | - | NOT NULL | 0-100, default 0 |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** user_id -> User.id; tenant_id -> Tenant.id. **Constraint:** user_id unik; completeness_pct 0-100; established_year 1900-2100.. **Normalisasi:** tenant_id diulang untuk RLS; completeness_pct adalah nilai turunan..

### Assessment

Satu sesi asesmen 31 kriteria untuk satu profil UMKM, menyimpan skor total dan segmen.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | NOT NULL | - |
| tenant_id | uuid | FK | NOT NULL | Tenant.id |
| umkm_profile_id | uuid | FK | NOT NULL | UMKMProfile.id |
| status | enum | - | NOT NULL | draft, submitted, scored, archived |
| scoring_version | varchar(16) | - | NOT NULL | - |
| total_score | numeric(5,2) | - | NULL | 0-100 |
| segment_id | smallint | FK | NULL | Segment.id |
| submitted_at | timestamptz | - | NULL | - |
| scored_at | timestamptz | - | NULL | - |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** tenant_id -> Tenant.id; umkm_profile_id -> UMKMProfile.id; segment_id -> Segment.id. **Constraint:** total_score 0-100; status scored wajib punya segment_id.. **Normalisasi:** total_score dan segment_id adalah nilai turunan yang disimpan untuk audit..

### AssessmentAnswer

Jawaban satu kriteria dalam satu asesmen.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | bigint | PK | NOT NULL | - |
| assessment_id | uuid | FK | NOT NULL | Assessment.id |
| criterion_id | smallint | FK | NOT NULL | Criterion.id |
| raw_value | jsonb | - | NOT NULL | - |
| numeric_value | numeric(8,2) | - | NULL | - |
| score | numeric(5,2) | - | NULL | 0-100 |
| answered_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** assessment_id -> Assessment.id; criterion_id -> Criterion.id. **Constraint:** unik (assessment_id, criterion_id); score 0-100.. **Normalisasi:** Satu baris per kriteria; raw_value JSONB untuk input bertipe campuran..

### Dimension

Enam dimensi framework: Demografi, Psikografi, Proses Internal, Pasar, Lingkungan, Keuangan.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | smallint | PK | NOT NULL | - |
| code | varchar(32) | UQ | NOT NULL | unik |
| name | varchar(80) | - | NOT NULL | - |
| weight | numeric(5,2) | - | NOT NULL | 0-100 |
| is_scored | boolean | - | NOT NULL | default true |
| order_no | smallint | - | NOT NULL | - |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** Tidak ada.. **Constraint:** code unik; weight 0-100.. **Normalisasi:** Tabel referensi; Demografi is_scored false..

### Criterion

31 kriteria scoring beserta bobot, tipe input, dan aturan skor.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | smallint | PK | NOT NULL | - |
| dimension_id | smallint | FK | NOT NULL | Dimension.id |
| code | varchar(16) | UQ | NOT NULL | unik |
| question | text | - | NOT NULL | - |
| input_type | enum | - | NOT NULL | boolean, scale, enum, number, text |
| weight | numeric(5,2) | - | NOT NULL | 0-100 |
| scoring_rule | jsonb | - | NOT NULL | - |
| is_active | boolean | - | NOT NULL | default true |
| version | varchar(16) | - | NOT NULL | default 1.0 |
| order_no | smallint | - | NOT NULL | - |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** dimension_id -> Dimension.id. **Constraint:** code unik; weight 0-100.. **Normalisasi:** Tabel referensi; aturan skor fleksibel di JSONB dan versi disimpan..

### DimensionScore

Skor satu dimensi untuk satu asesmen; enam baris per asesmen.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| assessment_id | uuid | PK/FK | NOT NULL | Assessment.id |
| dimension_id | smallint | PK/FK | NOT NULL | Dimension.id |
| raw_score | numeric(5,2) | - | NULL | 0-100 |
| weighted_score | numeric(5,2) | - | NOT NULL | 0-100 |
| is_scored | boolean | - | NOT NULL | - |
| computed_at | timestamptz | - | NOT NULL | default now() |

**PK:** assessment_id, dimension_id. **FK:** assessment_id -> Assessment.id; dimension_id -> Dimension.id. **Constraint:** composite primary key; raw_score dan weighted_score 0-100.. **Normalisasi:** Turunan dari AssessmentAnswer; Demografi is_scored false..

### Segment

Empat segmen kematangan usaha dan rentang skornya.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | smallint | PK | NOT NULL | - |
| code | varchar(32) | UQ | NOT NULL | unik |
| name | varchar(80) | - | NOT NULL | - |
| min_score | numeric(5,2) | - | NOT NULL | 0-100 |
| max_score | numeric(5,2) | - | NOT NULL | 0-100 |
| curriculum | text | - | NULL | - |
| order_no | smallint | - | NOT NULL | - |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** Tidak ada.. **Constraint:** code unik; min_score < max_score; rentang 0-100.. **Normalisasi:** Tabel referensi; batas segmen memakai desimal untuk menghindari tumpang tindih..

### Roadmap

Roadmap personal untuk satu asesmen, berisi versi dan status.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | NOT NULL | - |
| tenant_id | uuid | FK | NOT NULL | Tenant.id |
| assessment_id | uuid | FK | NOT NULL | Assessment.id |
| version | smallint | - | NOT NULL | default 1 |
| status | enum | - | NOT NULL | draft, active, completed, superseded |
| title | varchar(160) | - | NOT NULL | - |
| summary | text | - | NULL | - |
| generated_by | enum | - | NOT NULL | rule, llm, hybrid, manual |
| model_name | varchar(80) | - | NULL | - |
| prompt_version | varchar(32) | - | NULL | - |
| generated_at | timestamptz | - | NOT NULL | default now() |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** tenant_id -> Tenant.id; assessment_id -> Assessment.id. **Constraint:** unik (assessment_id, version); satu roadmap active per assessment.. **Normalisasi:** Versi lama berstatus superseded; generated_by menyimpan provenance..

### Milestone

Langkah roadmap dengan status, tenggat, dan action items.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | NOT NULL | - |
| roadmap_id | uuid | FK | NOT NULL | Roadmap.id |
| order_no | smallint | - | NOT NULL | - |
| title | varchar(160) | - | NOT NULL | - |
| description | text | - | NULL | - |
| action_items | jsonb | - | NULL | - |
| due_date | date | - | NULL | - |
| estimated_cost | numeric(12,2) | - | NULL | >= 0 |
| status | enum | - | NOT NULL | pending, in_progress, done, skipped |
| completed_at | timestamptz | - | NULL | - |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** roadmap_id -> Roadmap.id. **Constraint:** unik (roadmap_id, order_no); estimated_cost >= 0.. **Normalisasi:** status adalah proyeksi dari ProgressLog; action_items JSONB..

### ProgressLog

Catatan progres append-only untuk satu milestone.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | bigint | PK | NOT NULL | - |
| tenant_id | uuid | FK | NOT NULL | Tenant.id |
| milestone_id | uuid | FK | NOT NULL | Milestone.id |
| user_id | uuid | FK | NOT NULL | User.id |
| progress_pct | smallint | - | NOT NULL | 0-100 |
| note | text | - | NULL | - |
| evidence_url | text | - | NULL | - |
| logged_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** tenant_id -> Tenant.id; milestone_id -> Milestone.id; user_id -> User.id. **Constraint:** progress_pct 0-100; append-only.. **Normalisasi:** Log terbaru menentukan progres; tidak ada updated_at..

### MentorSession

Sesi konsultasi UMKM dengan mentor, termasuk jadwal, catatan, dan bagi hasil.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | NOT NULL | - |
| tenant_id | uuid | FK | NOT NULL | Tenant.id |
| umkm_profile_id | uuid | FK | NOT NULL | UMKMProfile.id |
| mentor_id | uuid | FK | NOT NULL | User.id |
| scheduled_at | timestamptz | - | NOT NULL | - |
| duration_min | smallint | - | NOT NULL | 15-180 |
| status | enum | - | NOT NULL | requested, confirmed, completed, cancelled, no_show |
| topic | varchar(160) | - | NULL | - |
| notes | text | - | NULL | - |
| fee_amount | numeric(12,2) | - | NULL | >= 0 |
| platform_fee | numeric(12,2) | - | NULL | >= 0 |
| mentor_fee | numeric(12,2) | - | NULL | >= 0 |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** tenant_id -> Tenant.id; umkm_profile_id -> UMKMProfile.id; mentor_id -> User.id. **Constraint:** duration_min 15-180; fee >= 0.. **Normalisasi:** Bagi hasil disimpan untuk audit; catatan sesi berupa teks..

### Plan

Paket langganan Free, Premium, dan B2G beserta kuota dan harga.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | smallint | PK | NOT NULL | - |
| code | varchar(32) | UQ | NOT NULL | unik |
| name | varchar(80) | - | NOT NULL | - |
| audience | enum | - | NOT NULL | umkm, institution |
| price_monthly | numeric(12,2) | - | NOT NULL | >= 0 |
| price_yearly | numeric(12,2) | - | NULL | >= 0 |
| quota_umkm | integer | - | NULL | > 0 untuk institusi |
| features | jsonb | - | NOT NULL | - |
| is_active | boolean | - | NOT NULL | default true |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** Tidak ada.. **Constraint:** code unik; harga >= 0; kuota institusi > 0.. **Normalisasi:** Tabel referensi; features JSONB untuk entitlements..

### Subscription

Langganan tenant B2G atau pengguna Premium.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | NOT NULL | - |
| tenant_id | uuid | FK | NULL | Tenant.id |
| user_id | uuid | FK | NULL | User.id |
| plan_id | smallint | FK | NOT NULL | Plan.id |
| status | enum | - | NOT NULL | trialing, active, past_due, cancelled, expired |
| period_start | date | - | NOT NULL | - |
| period_end | date | - | NOT NULL | - |
| price | numeric(12,2) | - | NOT NULL | >= 0 |
| auto_renew | boolean | - | NOT NULL | default false |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** tenant_id -> Tenant.id; user_id -> User.id; plan_id -> Plan.id. **Constraint:** tepat satu owner (tenant_id atau user_id); period_start < period_end.. **Normalisasi:** Owner polimorfik dengan check constraint; dapat dipecah bila billing tumbuh..

### Invoice

Tagihan untuk satu langganan.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | NOT NULL | - |
| subscription_id | uuid | FK | NOT NULL | Subscription.id |
| number | varchar(40) | UQ | NOT NULL | unik |
| amount | numeric(12,2) | - | NOT NULL | >= 0 |
| tax_amount | numeric(12,2) | - | NOT NULL | >= 0 |
| status | enum | - | NOT NULL | draft, issued, paid, void, overdue |
| issued_at | date | - | NOT NULL | - |
| due_at | date | - | NOT NULL | - |
| paid_at | timestamptz | - | NULL | - |
| payment_ref | varchar(120) | - | NULL | - |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** subscription_id -> Subscription.id. **Constraint:** number unik; amount >= 0; due_at >= issued_at.. **Normalisasi:** Line item belum dimodelkan di MVP; satu amount per invoice..

### KnowledgeDocument

Dokumen pengetahuan resmi untuk RAG, dengan versi, masa berlaku, dan status review.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | NOT NULL | - |
| tenant_id | uuid | FK | NULL | Tenant.id; NULL berarti global |
| title | varchar(200) | - | NOT NULL | - |
| source_name | varchar(160) | - | NOT NULL | - |
| source_url | text | - | NULL | - |
| document_type | enum | - | NOT NULL | regulation, guideline, faq, template, other |
| version | varchar(32) | - | NOT NULL | - |
| effective_date | date | - | NULL | - |
| expiry_date | date | - | NULL | - |
| status | enum | - | NOT NULL | draft, review, published, archived |
| file_url | text | - | NULL | - |
| checksum | char(64) | - | NULL | - |
| reviewer_id | uuid | FK | NULL | User.id |
| published_at | timestamptz | - | NULL | - |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** tenant_id -> Tenant.id; reviewer_id -> User.id. **Constraint:** expiry_date > effective_date bila keduanya ada; checksum 64 karakter.. **Normalisasi:** tenant_id NULL berarti global; chunk dipisah ke KnowledgeChunk..

### KnowledgeChunk

Potongan dokumen dan embedding untuk pencarian RAG.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | bigint | PK | NOT NULL | - |
| document_id | uuid | FK | NOT NULL | KnowledgeDocument.id |
| chunk_index | smallint | - | NOT NULL | - |
| section_label | varchar(160) | - | NULL | - |
| content | text | - | NOT NULL | - |
| token_count | smallint | - | NOT NULL | > 0 |
| embedding | vector(768) | - | NULL | pgvector |
| created_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** document_id -> KnowledgeDocument.id. **Constraint:** unik (document_id, chunk_index); token_count > 0.. **Normalisasi:** Chunk memisahkan unit retrieval; embedding 768 dimensi..

### Report

Laporan agregat B2G untuk periode tertentu.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | NOT NULL | - |
| tenant_id | uuid | FK | NOT NULL | Tenant.id |
| type | enum | - | NOT NULL | monthly, quarterly, impact, custom |
| period_start | date | - | NOT NULL | - |
| period_end | date | - | NOT NULL | - |
| status | enum | - | NOT NULL | queued, generating, ready, failed |
| file_url | text | - | NULL | - |
| parameters | jsonb | - | NOT NULL | default {} |
| generated_by | uuid | FK | NULL | User.id |
| generated_at | timestamptz | - | NULL | - |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** tenant_id -> Tenant.id; generated_by -> User.id. **Constraint:** period_start <= period_end.. **Normalisasi:** Menyimpan parameter dan file agregat; tidak menyimpan PII mentah..

### Notification

Notifikasi email atau in-app untuk pengguna.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | NOT NULL | - |
| tenant_id | uuid | FK | NOT NULL | Tenant.id |
| user_id | uuid | FK | NOT NULL | User.id |
| type | varchar(40) | - | NOT NULL | - |
| channel | enum | - | NOT NULL | in_app, email, whatsapp |
| title | varchar(160) | - | NOT NULL | - |
| body | text | - | NOT NULL | - |
| status | enum | - | NOT NULL | queued, sent, failed, read |
| sent_at | timestamptz | - | NULL | - |
| read_at | timestamptz | - | NULL | - |
| created_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** tenant_id -> Tenant.id; user_id -> User.id. **Constraint:** channel dan status dibatasi enum.. **Normalisasi:** Queue dengan status; WhatsApp fase 2..

### AuditLog

Catatan peristiwa keamanan dan perubahan data yang append-only.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | bigint | PK | NOT NULL | - |
| tenant_id | uuid | FK | NULL | Tenant.id |
| actor_user_id | uuid | FK | NULL | User.id |
| action | varchar(80) | - | NOT NULL | - |
| entity_type | varchar(60) | - | NOT NULL | - |
| entity_id | varchar(64) | - | NULL | - |
| before_data | jsonb | - | NULL | - |
| after_data | jsonb | - | NULL | - |
| ip_address | inet | - | NULL | - |
| user_agent | text | - | NULL | - |
| trace_id | uuid | - | NULL | - |
| created_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** tenant_id -> Tenant.id; actor_user_id -> User.id. **Constraint:** append-only; tidak ada grant update atau delete.. **Normalisasi:** Partisi bulanan saat skala besar; entity_id polimorfik tanpa FK..


### AIConsultation

Sesi konsultasi AI berbasis data usaha dan konteks asesmen UMKM (Fitur Must #2).

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | NOT NULL | default gen_random_uuid() |
| tenant_id | uuid | FK | NOT NULL | Tenant.id |
| umkm_profile_id | uuid | FK | NOT NULL | UMKMProfile.id |
| user_id | uuid | FK | NOT NULL | User.id |
| assessment_id | uuid | FK | NULL | Assessment.id |
| topic | varchar(160) | - | NOT NULL | - |
| category | enum | - | NOT NULL | operasional, pemasaran, keuangan, legalitas, strategi, lainnya |
| status | enum | - | NOT NULL | active, closed, escalated, archived |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** tenant_id -> Tenant.id; umkm_profile_id -> UMKMProfile.id; user_id -> User.id; assessment_id -> Assessment.id. **Constraint:** category dan status dibatasi enum. **Normalisasi:** Memisahkan metadata sesi konsultasi dari riwayat giliran percakapan di `AIResponseLog` (3NF).

### AIResponseLog

Catatan append-only setiap prompt pengguna dan jawaban AI, lengkap dengan penafian wajib, sitasi RAG, status guardrail, dan rating UAT (Fitur Must #4).

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | bigint | PK | NOT NULL | GENERATED ALWAYS AS IDENTITY |
| tenant_id | uuid | FK | NOT NULL | Tenant.id |
| consultation_id | uuid | FK | NOT NULL | AIConsultation.id |
| user_id | uuid | FK | NOT NULL | User.id |
| user_prompt | text | - | NOT NULL | - |
| ai_response | text | - | NOT NULL | - |
| disclaimer_text | text | - | NOT NULL | - |
| disclaimer_shown | boolean | - | NOT NULL | default true; CHECK (disclaimer_shown = true) |
| citations | jsonb | - | NOT NULL | default '[]' |
| guardrail_status | enum | - | NOT NULL | passed, flagged, blocked, escalated_to_mentor |
| guardrail_reason | varchar(200) | - | NULL | - |
| model_name | varchar(80) | - | NOT NULL | - |
| prompt_version | varchar(32) | - | NOT NULL | - |
| tokens_input | integer | - | NOT NULL | >= 0, default 0 |
| tokens_output | integer | - | NOT NULL | >= 0, default 0 |
| latency_ms | integer | - | NULL | >= 0 |
| user_rating | smallint | - | NULL | 1-5 (mendukung evaluasi UAT P15) |
| created_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** tenant_id -> Tenant.id; consultation_id -> AIConsultation.id; user_id -> User.id. **Constraint:** append-only; `disclaimer_shown = true`; `user_rating` 1-5. **Normalisasi:** Tidak ada `updated_at`; daftar sitasi dokumen resmi disimpan di JSONB `citations`.

### AIUsageQuota

Kontrol kuota konsultasi dan pemakaian token AI per pengguna per periode untuk pengendalian biaya Gemini API.

| Atribut | Tipe | Kunci | Null | Constraint |
|---|---|---|---|---|
| id | uuid | PK | NOT NULL | default gen_random_uuid() |
| tenant_id | uuid | FK | NOT NULL | Tenant.id |
| user_id | uuid | FK | NOT NULL | User.id |
| period_start | date | - | NOT NULL | - |
| period_end | date | - | NOT NULL | period_start <= period_end |
| quota_limit | integer | - | NOT NULL | > 0 |
| used_count | integer | - | NOT NULL | 0 <= used_count <= quota_limit |
| token_limit | integer | - | NULL | > 0 |
| tokens_used | integer | - | NOT NULL | >= 0 |
| created_at | timestamptz | - | NOT NULL | default now() |
| updated_at | timestamptz | - | NOT NULL | default now() |

**PK:** id. **FK:** tenant_id -> Tenant.id; user_id -> User.id. **Constraint:** unik (user_id, period_start, period_end); `used_count <= quota_limit`; `period_start <= period_end`. **Normalisasi:** Memisahkan histori kuota per periode dari tabel `User` agar sesuai 3NF.

## Catatan normalisasi umum

1. Tabel transaksional mengikuti 3NF. Tabel referensi Dimension, Criterion, Segment, dan Plan memisahkan nilai berulang.
2. Kolom turunan yang disimpan adalah `Assessment.total_score`, `Assessment.segment_id`, `DimensionScore.weighted_score`, `UMKMProfile.completeness_pct`, dan `Milestone.status`. Nilai ini dihitung ulang oleh layanan terkait dan tidak diedit manual.
3. `tenant_id` diulang pada tabel yang terikat tenant untuk row-level security dan query agregat. Konsistensi dijaga oleh trigger atau layanan aplikasi.
4. JSONB hanya dipakai untuk payload yang bentuknya berubah: `Criterion.scoring_rule`, `Milestone.action_items`, `Report.parameters`, `AuditLog.before_data`, `AuditLog.after_data`, dan `AssessmentAnswer.raw_value`.
5. `ProgressLog`, `AIResponseLog`, dan `AuditLog` append-only. `AIResponseLog` mewajibkan `disclaimer_shown = true`. `ProgressLog` tidak memiliki `updated_at`. `AuditLog` tidak memiliki grant update atau delete.
6. `Subscription` memakai owner polimorfik dengan check constraint tepat satu dari `tenant_id` atau `user_id`.
7. `KnowledgeDocument.tenant_id` NULL berarti dokumen global. RLS mengizinkan dokumen global dan dokumen milik tenant.

## Asumsi desain

- PostgreSQL 15+ dengan ekstensi `pgcrypto`, `citext`, dan `pgvector`.
- UUID memakai `gen_random_uuid()`. Semua waktu disimpan dalam UTC.
- Bobot kriteria dan dimensi bersifat konfigurasi. Nilai awal belum diverifikasi ke dokumen resmi framework 31 kriteria.
- Batas segmen memakai 0-29,99; 30-54,99; 55-79,99; 80-100 untuk menghindari tumpang tindih pada batas 30, 55, dan 80.
- Skor Demografi dihitung dari kelengkapan profil, bukan dari bobot kriteria.
- Embedding memakai Gemini `text-embedding-004` dengan 768 dimensi.
- Retensi audit 24 bulan, progres 5 tahun, laporan 5 tahun, dan invoice 7 tahun. Angka ini asumsi desain.
- RLS menjadi target arsitektur. MVP menerapkan scoping tenant di application layer dan RLS pada tabel berisiko tinggi.