-- ============================================================================
-- GROWPATH P14 · Verifikasi skema dan seed
-- Jalankan setelah 001_init.sql, seed.sql, dan 002_p14.sql.
-- Gagal dengan exception bila ada butir yang tidak terpenuhi.
-- ============================================================================

DO $$
DECLARE
  n integer;
  missing text;
BEGIN
  -- Seed katalog
  SELECT count(*) INTO n FROM dimension;
  IF n <> 6 THEN
    RAISE EXCEPTION 'dimension harus 6 baris, ditemukan %', n;
  END IF;

  SELECT count(*) INTO n FROM criterion WHERE is_active;
  IF n <> 31 THEN
    RAISE EXCEPTION 'criterion aktif harus 31 baris, ditemukan %', n;
  END IF;

  SELECT count(*) INTO n
  FROM criterion c JOIN dimension d ON d.id = c.dimension_id
  WHERE d.code = 'PSY';
  IF n <> 3 THEN
    RAISE EXCEPTION 'kriteria Psikografi harus 3, ditemukan %', n;
  END IF;

  SELECT count(*) INTO n
  FROM criterion c JOIN dimension d ON d.id = c.dimension_id
  WHERE d.code = 'PAS';
  IF n <> 9 THEN
    RAISE EXCEPTION 'kriteria Pasar harus 9, ditemukan %', n;
  END IF;

  SELECT count(*) INTO n FROM segment;
  IF n <> 4 THEN
    RAISE EXCEPTION 'segment harus 4 baris, ditemukan %', n;
  END IF;

  SELECT count(*) INTO n FROM "user";
  IF n < 30 THEN
    RAISE EXCEPTION 'seed user minimal 30 baris, ditemukan %', n;
  END IF;

  -- Primary key pada tabel inti
  SELECT string_agg(t.name, ', ') INTO missing
  FROM (VALUES
    ('plan'), ('tenant'), ('user'), ('umkm_profile'), ('dimension'),
    ('criterion'), ('segment'), ('assessment'), ('assessment_answer'),
    ('dimension_score'), ('roadmap'), ('milestone'), ('progress_log')
  ) AS t(name)
  WHERE NOT EXISTS (
    SELECT 1 FROM pg_constraint c
    WHERE c.conrelid = format('public.%I', t.name)::regclass
      AND c.contype = 'p'
  );
  IF missing IS NOT NULL THEN
    RAISE EXCEPTION 'tabel tanpa primary key: %', missing;
  END IF;

  -- Foreign key minimal 20
  SELECT count(*) INTO n FROM pg_constraint WHERE contype = 'f';
  IF n < 20 THEN
    RAISE EXCEPTION 'foreign key minimal 20, ditemukan %', n;
  END IF;

  -- Unique constraint penting
  SELECT string_agg(name, ', ') INTO missing
  FROM (VALUES ('assessment_answer_unique'), ('roadmap_version_unique'),
               ('milestone_order_unique')) AS t(name)
  WHERE NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = t.name AND contype = 'u'
  );
  IF missing IS NOT NULL THEN
    RAISE EXCEPTION 'unique constraint hilang: %', missing;
  END IF;

  -- Check constraint minimal 10
  SELECT count(*) INTO n FROM pg_constraint WHERE contype = 'c';
  IF n < 10 THEN
    RAISE EXCEPTION 'check constraint minimal 10, ditemukan %', n;
  END IF;

  -- Index penting
  SELECT string_agg(name, ', ') INTO missing
  FROM (VALUES ('idx_roadmap_one_active'), ('idx_assessment_profile'),
               ('idx_assessment_answer_assessment'), ('idx_criterion_dimension'))
       AS t(name)
  WHERE NOT EXISTS (
    SELECT 1 FROM pg_class WHERE relname = t.name AND relkind = 'i'
  );
  IF missing IS NOT NULL THEN
    RAISE EXCEPTION 'index hilang: %', missing;
  END IF;

  -- View laporan
  IF NOT EXISTS (
    SELECT 1 FROM pg_views
    WHERE schemaname = 'public' AND viewname = 'v_assessment_report'
  ) THEN
    RAISE EXCEPTION 'view v_assessment_report tidak ada';
  END IF;

  RAISE NOTICE 'OK: skema, seed, constraint, index, dan view P14 terverifikasi.';
END $$;

-- Ringkasan yang bisa dilampirkan sebagai bukti
SELECT 'dimension' AS objek, count(*) AS jumlah FROM dimension
UNION ALL SELECT 'criterion', count(*) FROM criterion
UNION ALL SELECT 'segment', count(*) FROM segment
UNION ALL SELECT 'user', count(*) FROM "user"
UNION ALL SELECT 'assessment', count(*) FROM assessment
UNION ALL SELECT 'roadmap', count(*) FROM roadmap;
