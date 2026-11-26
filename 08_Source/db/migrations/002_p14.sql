-- ============================================================================
-- GROWPATH P14
-- View laporan asesmen dan roadmap.
-- Jalankan setelah 001_init.sql. Idempoten.
-- ============================================================================

BEGIN;

CREATE OR REPLACE VIEW v_assessment_report AS
SELECT
  a.id                                                AS assessment_id,
  a.tenant_id,
  a.umkm_profile_id,
  p.business_name,
  p.owner_name,
  p.sector,
  a.status,
  a.scoring_version,
  a.total_score,
  s.code                                              AS segment_code,
  s.name                                              AS segment_name,
  count(ad.criterion_id) FILTER (WHERE ad.score IS NOT NULL)
                                                      AS criteria_answered,
  (SELECT count(*) FROM criterion c WHERE c.is_active)
                                                      AS criteria_total,
  a.started_at,
  a.submitted_at,
  a.scored_at,
  r.id                                                AS roadmap_id,
  r.status                                            AS roadmap_status,
  (SELECT count(*) FROM milestone m WHERE m.roadmap_id = r.id)
                                                      AS milestone_total,
  (SELECT count(*) FROM milestone m
    WHERE m.roadmap_id = r.id AND m.status = 'done')
                                                      AS milestone_done
FROM assessment a
JOIN umkm_profile p ON p.id = a.umkm_profile_id
LEFT JOIN segment s ON s.id = a.segment_id
LEFT JOIN LATERAL (
  SELECT rr.id, rr.status
  FROM roadmap rr
  WHERE rr.assessment_id = a.id AND rr.status = 'active'
  ORDER BY rr.version DESC
  LIMIT 1
) r ON true
LEFT JOIN assessment_answer ad ON ad.assessment_id = a.id
GROUP BY a.id, p.id, s.id, r.id, r.status;

COMMENT ON VIEW v_assessment_report IS
  'Ringkasan laporan per asesmen: profil, segmen, cakupan kriteria, dan progres roadmap.';

COMMIT;
