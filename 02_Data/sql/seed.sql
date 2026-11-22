-- ============================================================================
-- GROWPATH P13 SEED
-- Data uji, bukan data produksi.
-- Nama pengguna dan usaha di bawah sintetis. Tidak ada mitra nyata.
-- Skor tidak dihitung di seed. Skor dihitung oleh Scoring Service.
-- Jalankan setelah ddl.sql.
-- ============================================================================

BEGIN;

-- ---------------------------------------------------------------------------
-- Referensi: 6 dimensi
-- ---------------------------------------------------------------------------
INSERT INTO dimension (id, code, name, weight, is_scored, order_no) VALUES
  (1, 'DEM', 'Demografi', 0, false, 1),
  (2, 'PSY', 'Psikografi', 20, true, 2),
  (3, 'INT', 'Proses Internal', 20, true, 3),
  (4, 'PAS', 'Pasar', 20, true, 4),
  (5, 'LIN', 'Lingkungan', 20, true, 5),
  (6, 'KEU', 'Keuangan', 20, true, 6);

-- ---------------------------------------------------------------------------
-- Referensi: 4 segmen
-- Batas bawah inklusif. Batas atas eksklusif, kecuali 100 masuk segmen 4.
-- ---------------------------------------------------------------------------
INSERT INTO segment (id, code, name, min_score, max_score, curriculum, order_no) VALUES
  (1, 'S1', 'Foundation Builders', 0, 30, 'Fondasi usaha, legalitas dasar, pencatatan sederhana', 1),
  (2, 'S2', 'Branding Enthusiasts', 30, 55, 'Branding, kanal penjualan, digitalisasi dasar', 2),
  (3, 'S3', 'Commerce Optimizers', 55, 80, 'Optimasi pasar, keuangan, dan proses internal', 3),
  (4, 'S4', 'Sustainability Advocates', 80, 100, 'Keberlanjutan, sertifikasi, dan ekspansi', 4);

-- ---------------------------------------------------------------------------
-- Referensi: paket. Harga 0 berarti belum ditetapkan, bukan gratis.
-- ---------------------------------------------------------------------------
INSERT INTO plan (id, code, name, audience, price_monthly, price_yearly, quota_umkm, features, is_active) VALUES
  (1, 'free', 'Free UMKM', 'umkm', 0, 0, NULL, '{"tier":"free","note":"layanan inti tanpa biaya"}'::jsonb, true),
  (2, 'premium', 'Premium UMKM', 'umkm', 0, 0, NULL, '{"price_status":"not_set","phase":2}'::jsonb, false),
  (3, 'b2g', 'B2G Institution', 'institution', 0, 0, NULL, '{"price_status":"not_set","billing":"annual","phase":2}'::jsonb, false);

-- ---------------------------------------------------------------------------
-- Referensi: 31 kriteria scoring
-- Bobot 1 per kriteria, dinormalisasi oleh Scoring Service.
-- ---------------------------------------------------------------------------
INSERT INTO criterion (id, dimension_id, code, question, input_type, weight, scoring_rule, order_no) VALUES
-- Psikografi
(1, 2, 'PSY-01', 'Apa motif utama Anda menjalankan usaha?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"survival","label":"Kebutuhan bertahan hidup","points":20},{"code":"extra_income","label":"Penghasilan tambahan","points":40},{"code":"market","label":"Peluang pasar","points":70},{"code":"skill","label":"Keahlian atau minat","points":80},{"code":"sustainable","label":"Membangun usaha berkelanjutan","points":100}]}'::jsonb, 1),
(2, 2, 'PSY-02', 'Mengapa Anda memilih bidang usaha ini?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"trend","label":"Ikut tren atau kebetulan","points":20},{"code":"family","label":"Warisan keluarga","points":40},{"code":"experience","label":"Pengalaman kerja","points":60},{"code":"skill","label":"Keahlian atau minat","points":80},{"code":"research","label":"Riset pasar dan peluang","points":100}]}'::jsonb, 2),
(3, 2, 'PSY-03', 'Bagaimana sikap Anda terhadap risiko usaha?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"avoid","label":"Menghindari risiko","points":20},{"code":"careful","label":"Sangat hati-hati","points":40},{"code":"balanced","label":"Seimbang","points":70},{"code":"calculated","label":"Berani dengan perhitungan","points":100},{"code":"aggressive","label":"Agresif tanpa perhitungan","points":30}]}'::jsonb, 3),
-- Proses Internal
(4, 3, 'INT-01', 'Berapa jumlah SDM bergaji tetap saat ini?', 'number', 1,
 '{"type":"numeric","unit":"orang","buckets":[{"min":0,"max":1,"points":0},{"min":1,"max":3,"points":25},{"min":3,"max":6,"points":50},{"min":6,"max":11,"points":75},{"min":11,"points":100}]}'::jsonb, 1),
(5, 3, 'INT-02', 'Dari mana sumber bahan baku utama Anda?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"unstable","label":"Tidak tetap","points":20},{"code":"local_market","label":"Pasar lokal","points":40},{"code":"fixed_supplier","label":"Supplier tetap","points":60},{"code":"long_contract","label":"Kontrak jangka panjang","points":80},{"code":"own_production","label":"Produksi sendiri dan cadangan","points":100}]}'::jsonb, 2),
(6, 3, 'INT-03', 'Bagaimana metode produksi yang Anda pakai?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"manual","label":"Manual","points":20},{"code":"semi","label":"Semi-otomatis","points":50},{"code":"auto","label":"Otomatis","points":80},{"code":"auto_qc","label":"Otomatis dengan kendali mutu","points":100}]}'::jsonb, 3),
(7, 3, 'INT-04', 'Pelatihan apa yang pernah Anda ikuti?', 'multi_select', 1,
 '{"type":"multi_select","cap":100,"options":[{"code":"marketing","label":"Pemasaran","points":20},{"code":"finance","label":"Keuangan","points":20},{"code":"production","label":"Produksi","points":20},{"code":"digital","label":"Digital","points":20},{"code":"management","label":"Manajemen","points":20}]}'::jsonb, 4),
-- Pasar
(8, 4, 'PAS-01', 'Unsur branding apa yang sudah Anda miliki?', 'multi_select', 1,
 '{"type":"multi_select","cap":100,"options":[{"code":"logo","label":"Logo","points":25},{"code":"packaging","label":"Kemasan","points":25},{"code":"social","label":"Media sosial","points":25},{"code":"website","label":"Website","points":25}]}'::jsonb, 1),
(9, 4, 'PAS-02', 'Di mana saja Anda menjual produk?', 'multi_select', 1,
 '{"type":"multi_select","cap":100,"options":[{"code":"store","label":"Toko fisik","points":25},{"code":"marketplace","label":"Marketplace","points":25},{"code":"reseller","label":"Reseller","points":20},{"code":"distributor","label":"Distributor","points":20},{"code":"own_outlet","label":"Gerai sendiri","points":10}]}'::jsonb, 2),
(10, 4, 'PAS-03', 'Sejauh mana cakupan pasar Anda?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"local","label":"Lokal","points":20},{"code":"city","label":"Kecamatan atau kota","points":40},{"code":"province","label":"Provinsi","points":60},{"code":"national","label":"Nasional","points":80},{"code":"export","label":"Ekspor","points":100}]}'::jsonb, 3),
(11, 4, 'PAS-04', 'Bentuk digitalisasi apa yang sudah Anda pakai?', 'multi_select', 1,
 '{"type":"multi_select","cap":100,"options":[{"code":"social","label":"Media sosial","points":20},{"code":"marketplace","label":"Marketplace","points":20},{"code":"website","label":"Website","points":20},{"code":"ads","label":"Iklan digital","points":20},{"code":"payment","label":"Pembayaran digital","points":20}]}'::jsonb, 4),
(12, 4, 'PAS-05', 'Pernahkah Anda menerima order sub-kontrak masuk?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"never","label":"Tidak pernah","points":0},{"code":"once","label":"Pernah sekali","points":40},{"code":"several","label":"Beberapa kali","points":70},{"code":"routine","label":"Rutin atau kontrak","points":100}]}'::jsonb, 5),
(13, 4, 'PAS-06', 'Pernahkah Anda mengambil order sub-kontrak keluar?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"never","label":"Tidak pernah","points":0},{"code":"once","label":"Pernah","points":40},{"code":"routine","label":"Rutin","points":70},{"code":"contract","label":"Kontrak","points":100}]}'::jsonb, 6),
(14, 4, 'PAS-07', 'Sejauh mana Anda memahami pesaing?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"none","label":"Tidak tahu","points":0},{"code":"name","label":"Tahu nama","points":25},{"code":"price","label":"Tahu harga dan produk","points":50},{"code":"periodic","label":"Riset berkala","points":75},{"code":"strategy","label":"Analisis strategi","points":100}]}'::jsonb, 7),
(15, 4, 'PAS-08', 'Apa pengalaman pameran Anda?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"none","label":"Belum","points":0},{"code":"local","label":"Lokal","points":25},{"code":"regional","label":"Regional","points":50},{"code":"national","label":"Nasional","points":75},{"code":"international","label":"Internasional","points":100}]}'::jsonb, 8),
(16, 4, 'PAS-09', 'Apa pengalaman penjualan luar negeri Anda?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"none","label":"Belum","points":0},{"code":"tried","label":"Pernah coba","points":40},{"code":"routine","label":"Rutin ekspor","points":100}]}'::jsonb, 9),
-- Lingkungan
(17, 5, 'LIN-01', 'Dokumen legalitas apa yang sudah Anda miliki?', 'multi_select', 1,
 '{"type":"multi_select","cap":100,"options":[{"code":"nib","label":"NIB","points":40},{"code":"npwp","label":"NPWP","points":30},{"code":"sector_permit","label":"Izin usaha sektoral","points":30}]}'::jsonb, 1),
(18, 5, 'LIN-02', 'Sertifikasi usaha apa yang sudah Anda miliki?', 'multi_select', 1,
 '{"type":"multi_select","cap":100,"options":[{"code":"halal","label":"Halal","points":30},{"code":"bpom","label":"BPOM","points":30},{"code":"iso_sni","label":"ISO atau SNI","points":20},{"code":"haccp","label":"HACCP","points":20}]}'::jsonb, 2),
(19, 5, 'LIN-03', 'Dokumen perpajakan apa yang sudah Anda miliki?', 'multi_select', 1,
 '{"type":"multi_select","cap":100,"options":[{"code":"npwp","label":"NPWP","points":40},{"code":"pkp","label":"Status PKP","points":20},{"code":"spt","label":"SPT rutin","points":20},{"code":"tax_invoice","label":"Faktur pajak","points":20}]}'::jsonb, 3),
(20, 5, 'LIN-04', 'Apa pengalaman organisasi usaha Anda?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"never","label":"Tidak pernah","points":0},{"code":"once","label":"Pernah","points":30},{"code":"active","label":"Aktif","points":60},{"code":"board","label":"Pengurus","points":100}]}'::jsonb, 4),
(21, 5, 'LIN-05', 'Bagaimana pengelolaan sampah dan limbah Anda?', 'multi_select', 1,
 '{"type":"multi_select","cap":100,"options":[{"code":"sorting","label":"Pemilahan","points":25},{"code":"recycle","label":"Bank sampah atau daur ulang","points":25},{"code":"treatment","label":"Pengolahan limbah","points":25},{"code":"certified","label":"Limbah tersertifikasi","points":25}]}'::jsonb, 5),
(22, 5, 'LIN-06', 'Upaya efisiensi energi apa yang sudah dilakukan?', 'multi_select', 1,
 '{"type":"multi_select","cap":100,"options":[{"code":"led","label":"Lampu LED","points":20},{"code":"efficient","label":"Alat hemat energi","points":20},{"code":"renewable","label":"Energi terbarukan","points":30},{"code":"audit","label":"Audit energi","points":30}]}'::jsonb, 6),
-- Keuangan
(23, 6, 'KEU-01', 'Apa bentuk kepemilikan usaha Anda?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"sole","label":"Perseorangan","points":30},{"code":"cv","label":"CV","points":50},{"code":"coop","label":"Koperasi","points":80},{"code":"pt","label":"PT","points":100}]}'::jsonb, 1),
(24, 6, 'KEU-02', 'Dari mana pendanaan usaha Anda berasal?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"informal","label":"Pinjaman informal","points":20},{"code":"family","label":"Keluarga","points":30},{"code":"own","label":"Modal sendiri","points":40},{"code":"bank","label":"Bank atau koperasi","points":80},{"code":"investor","label":"Investor","points":100}]}'::jsonb, 2),
(25, 6, 'KEU-03', 'Apakah usaha punya rekening bank terpisah?', 'boolean', 1,
 '{"type":"boolean","true_points":100,"false_points":0}'::jsonb, 3),
(26, 6, 'KEU-04', 'Bagaimana pencatatan transaksi keuangan Anda?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"none","label":"Tidak ada","points":0},{"code":"simple","label":"Manual sederhana","points":30},{"code":"book","label":"Buku atau spreadsheet","points":60},{"code":"app","label":"Aplikasi","points":100}]}'::jsonb, 4),
(27, 6, 'KEU-05', 'Laporan keuangan apa yang Anda miliki?', 'enum', 1,
 '{"type":"single_choice","options":[{"code":"none","label":"Tidak ada","points":0},{"code":"pl","label":"Laba rugi","points":40},{"code":"pl_bs","label":"Laba rugi dan neraca","points":70},{"code":"full","label":"Laporan lengkap","points":100}]}'::jsonb, 5),
(28, 6, 'KEU-06', 'Bentuk digitalisasi transaksi apa yang sudah dipakai?', 'multi_select', 1,
 '{"type":"multi_select","cap":100,"options":[{"code":"qris","label":"QRIS","points":20},{"code":"transfer","label":"Transfer bank","points":20},{"code":"marketplace","label":"Marketplace","points":20},{"code":"pos","label":"POS","points":20},{"code":"digital_book","label":"Pembukuan digital","points":20}]}'::jsonb, 6),
(29, 6, 'KEU-07', 'Berapa omzet usaha per tahun?', 'number', 1,
 '{"type":"numeric","unit":"rupiah_per_year","buckets":[{"min":0,"max":50000000,"points":20},{"min":50000000,"max":300000000,"points":40},{"min":300000000,"max":2500000000,"points":60},{"min":2500000000,"max":10000000000,"points":80},{"min":10000000000,"points":100}]}'::jsonb, 7),
(30, 6, 'KEU-08', 'Berapa nilai aset usaha saat ini?', 'number', 1,
 '{"type":"numeric","unit":"rupiah","buckets":[{"min":0,"max":50000000,"points":20},{"min":50000000,"max":500000000,"points":40},{"min":500000000,"max":2000000000,"points":60},{"min":2000000000,"max":10000000000,"points":80},{"min":10000000000,"points":100}]}'::jsonb, 8),
(31, 6, 'KEU-09', 'Berapa laba bersih usaha per tahun?', 'number', 1,
 '{"type":"numeric","unit":"rupiah_per_year","buckets":[{"max":0,"points":0},{"min":0,"max":50000000,"points":30},{"min":50000000,"max":250000000,"points":60},{"min":250000000,"max":1000000000,"points":80},{"min":1000000000,"points":100}]}'::jsonb, 9);

-- ---------------------------------------------------------------------------
-- Tenant uji
-- ---------------------------------------------------------------------------
INSERT INTO tenant (id, name, slug, type, status, plan_id) VALUES
  ('00000000-0000-0000-0000-000000000001', 'Growpath Platform', 'growpath-platform', 'platform', 'active', 1),
  ('00000000-0000-0000-0000-000000000002', 'Tenant Uji Institusi', 'tenant-uji-institusi', 'institution', 'active', 3);

-- ---------------------------------------------------------------------------
-- 30 pengguna uji pada tenant platform
-- Email memakai domain .invalid yang tidak dapat dikirimi surat.
-- ---------------------------------------------------------------------------
INSERT INTO "user" (id, tenant_id, email, full_name, role, status)
SELECT
  gen_random_uuid(),
  '00000000-0000-0000-0000-000000000001'::uuid,
  'uji' || lpad(i::text, 2, '0') || '@contoh.invalid',
  'Pengguna Uji ' || lpad(i::text, 2, '0'),
  'umkm',
  'active'
FROM generate_series(1, 30) AS i;

-- ---------------------------------------------------------------------------
-- 30 profil usaha uji
-- ---------------------------------------------------------------------------
WITH numbered AS (
  SELECT
    id,
    tenant_id,
    email,
    row_number() OVER (ORDER BY email) AS n
  FROM "user"
  WHERE email LIKE 'uji%@contoh.invalid'
)
INSERT INTO umkm_profile (
  user_id, tenant_id, business_name, owner_name, gender, age, whatsapp, email,
  address, sector, established_year, operation_months, business_description, completeness_pct
)
SELECT
  id,
  tenant_id,
  'Usaha Uji ' || lpad(n::text, 2, '0'),
  'Pemilik Uji ' || lpad(n::text, 2, '0'),
  'undisclosed',
  (25 + (n % 30))::smallint,
  NULL,
  email,
  'Alamat uji nomor ' || n || ', Kota Uji',
  CASE (n % 5)
    WHEN 0 THEN 'kuliner'::profile_sector
    WHEN 1 THEN 'fashion'::profile_sector
    WHEN 2 THEN 'kriya'::profile_sector
    WHEN 3 THEN 'perdagangan'::profile_sector
    ELSE 'jasa'::profile_sector
  END,
  (2010 + (n % 12))::smallint,
  (12 + (n * 3) % 60)::smallint,
  'Profil uji untuk pengujian teknis, bukan usaha nyata.',
  100
FROM numbered;

-- ---------------------------------------------------------------------------
-- 30 asesmen draft, satu per profil
-- ---------------------------------------------------------------------------
INSERT INTO assessment (tenant_id, umkm_profile_id, status, scoring_version)
SELECT tenant_id, id, 'draft', '2026.11-v1'
FROM umkm_profile;

-- Jadikan asesmen pertama berstatus submitted agar Scoring Service dapat diuji.
UPDATE assessment
SET status = 'submitted', submitted_at = now()
WHERE id = (
  SELECT id FROM assessment ORDER BY created_at ASC, id ASC LIMIT 1
);

-- ---------------------------------------------------------------------------
-- 31 jawaban untuk asesmen submitted pertama
-- Skor dibiarkan null. Scoring Service yang menghitung.
-- ---------------------------------------------------------------------------
WITH target AS (
  SELECT id FROM assessment
  WHERE status = 'submitted'
  ORDER BY submitted_at ASC, id ASC
  LIMIT 1
),
answers (code, raw_value) AS (
  VALUES
    ('PSY-01', '{"option":"skill"}'::jsonb),
    ('PSY-02', '{"option":"skill"}'::jsonb),
    ('PSY-03', '{"option":"balanced"}'::jsonb),
    ('INT-01', '{"value":2}'::jsonb),
    ('INT-02', '{"option":"fixed_supplier"}'::jsonb),
    ('INT-03', '{"option":"manual"}'::jsonb),
    ('INT-04', '{"options":["marketing","finance"]}'::jsonb),
    ('PAS-01', '{"options":["logo","packaging"]}'::jsonb),
    ('PAS-02', '{"options":["store"]}'::jsonb),
    ('PAS-03', '{"option":"city"}'::jsonb),
    ('PAS-04', '{"options":["social","payment"]}'::jsonb),
    ('PAS-05', '{"option":"never"}'::jsonb),
    ('PAS-06', '{"option":"never"}'::jsonb),
    ('PAS-07', '{"option":"name"}'::jsonb),
    ('PAS-08', '{"option":"local"}'::jsonb),
    ('PAS-09', '{"option":"none"}'::jsonb),
    ('LIN-01', '{"options":["nib","npwp"]}'::jsonb),
    ('LIN-02', '{"options":[]}'::jsonb),
    ('LIN-03', '{"options":["npwp"]}'::jsonb),
    ('LIN-04', '{"option":"once"}'::jsonb),
    ('LIN-05', '{"options":["sorting"]}'::jsonb),
    ('LIN-06', '{"options":["led"]}'::jsonb),
    ('KEU-01', '{"option":"sole"}'::jsonb),
    ('KEU-02', '{"option":"own"}'::jsonb),
    ('KEU-03', '{"value":false}'::jsonb),
    ('KEU-04', '{"option":"simple"}'::jsonb),
    ('KEU-05', '{"option":"pl"}'::jsonb),
    ('KEU-06', '{"options":["qris","transfer"]}'::jsonb),
    ('KEU-07', '{"value":180000000}'::jsonb),
    ('KEU-08', '{"value":30000000}'::jsonb),
    ('KEU-09', '{"value":20000000}'::jsonb)
)
INSERT INTO assessment_answer (assessment_id, criterion_id, raw_value)
SELECT t.id, c.id, a.raw_value
FROM target t
CROSS JOIN answers a
JOIN criterion c ON c.code = a.code;

-- ---------------------------------------------------------------------------
-- Satu dokumen pengetahuan draft. Bukan klaim kurasi selesai.
-- ---------------------------------------------------------------------------
INSERT INTO knowledge_document (
  tenant_id, title, source_name, document_type, version, status
) VALUES (
  NULL,
  'Kurikulum UMKM Naik Kelas',
  'Kementerian BUMN',
  'guideline',
  '2025-04-25',
  'draft'
);

INSERT INTO knowledge_chunk (document_id, chunk_index, section_label, content, token_count)
SELECT id, 1, 'Profiling Matrix',
       'Katalog 31 kriteria dan 10 field demografi. Status draft, belum dikurasi untuk produksi.',
       14
FROM knowledge_document
WHERE title = 'Kurikulum UMKM Naik Kelas';

COMMIT;

-- ============================================================================
-- Setelah seed:
-- 1. Jalankan Scoring Service untuk asesmen submitted pertama.
-- 2. Periksa hasil dengan query di seed-data.md.
-- 3. Jangan memakai data ini sebagai bukti UAT atau data mitra.
-- ============================================================================
