-- ============================================================================
-- GROWPATH P13 DDL
-- PostgreSQL 15+ (Supabase)
-- 23 entitas, 31 kriteria sebagai seed terpisah
-- Jalankan di database kosong atau database uji. Skrip ini menghapus tabel
-- Growpath yang sudah ada.
-- ============================================================================

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS vector;

-- ---------------------------------------------------------------------------
-- Bersihkan objek Growpath (urutan terbalik dari dependensi)
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS audit_log CASCADE;
DROP TABLE IF EXISTS notification CASCADE;
DROP TABLE IF EXISTS report CASCADE;
DROP TABLE IF EXISTS invoice CASCADE;
DROP TABLE IF EXISTS subscription CASCADE;
DROP TABLE IF EXISTS mentor_session CASCADE;
DROP TABLE IF EXISTS knowledge_chunk CASCADE;
DROP TABLE IF EXISTS knowledge_document CASCADE;
DROP TABLE IF EXISTS ai_answer_log CASCADE;
DROP TABLE IF EXISTS consultation CASCADE;
DROP TABLE IF EXISTS progress_log CASCADE;
DROP TABLE IF EXISTS milestone CASCADE;
DROP TABLE IF EXISTS roadmap CASCADE;
DROP TABLE IF EXISTS dimension_score CASCADE;
DROP TABLE IF EXISTS assessment_answer CASCADE;
DROP TABLE IF EXISTS assessment CASCADE;
DROP TABLE IF EXISTS segment CASCADE;
DROP TABLE IF EXISTS criterion CASCADE;
DROP TABLE IF EXISTS dimension CASCADE;
DROP TABLE IF EXISTS umkm_profile CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS tenant CASCADE;
DROP TABLE IF EXISTS plan CASCADE;

DROP TYPE IF EXISTS notification_status CASCADE;
DROP TYPE IF EXISTS notification_channel CASCADE;
DROP TYPE IF EXISTS report_status CASCADE;
DROP TYPE IF EXISTS report_type CASCADE;
DROP TYPE IF EXISTS mentor_session_status CASCADE;
DROP TYPE IF EXISTS invoice_status CASCADE;
DROP TYPE IF EXISTS subscription_status CASCADE;
DROP TYPE IF EXISTS plan_audience CASCADE;
DROP TYPE IF EXISTS document_status CASCADE;
DROP TYPE IF EXISTS document_type CASCADE;
DROP TYPE IF EXISTS feedback_value CASCADE;
DROP TYPE IF EXISTS ai_log_status CASCADE;
DROP TYPE IF EXISTS consultation_status CASCADE;
DROP TYPE IF EXISTS milestone_status CASCADE;
DROP TYPE IF EXISTS roadmap_generated_by CASCADE;
DROP TYPE IF EXISTS roadmap_status CASCADE;
DROP TYPE IF EXISTS input_type CASCADE;
DROP TYPE IF EXISTS assessment_status CASCADE;
DROP TYPE IF EXISTS profile_sector CASCADE;
DROP TYPE IF EXISTS gender_value CASCADE;
DROP TYPE IF EXISTS user_status CASCADE;
DROP TYPE IF EXISTS user_role CASCADE;
DROP TYPE IF EXISTS tenant_status CASCADE;
DROP TYPE IF EXISTS tenant_type CASCADE;

-- ---------------------------------------------------------------------------
-- Enum
-- ---------------------------------------------------------------------------
CREATE TYPE tenant_type AS ENUM ('platform', 'institution', 'partner');
CREATE TYPE tenant_status AS ENUM ('active', 'suspended', 'inactive');
CREATE TYPE user_role AS ENUM ('umkm', 'pendamping', 'mentor', 'admin_b2g', 'admin_platform');
CREATE TYPE user_status AS ENUM ('active', 'invited', 'suspended', 'deleted');
CREATE TYPE gender_value AS ENUM ('male', 'female', 'undisclosed');
CREATE TYPE profile_sector AS ENUM ('kuliner', 'fashion', 'kriya', 'pertanian', 'perdagangan', 'jasa', 'teknologi', 'kesehatan', 'pendidikan', 'lainnya');
CREATE TYPE assessment_status AS ENUM ('draft', 'submitted', 'scored', 'archived');
CREATE TYPE input_type AS ENUM ('boolean', 'scale', 'enum', 'number', 'text', 'multi_select');
CREATE TYPE roadmap_status AS ENUM ('draft', 'active', 'completed', 'superseded');
CREATE TYPE roadmap_generated_by AS ENUM ('rule', 'llm', 'hybrid', 'manual');
CREATE TYPE milestone_status AS ENUM ('pending', 'in_progress', 'done', 'skipped');
CREATE TYPE consultation_status AS ENUM ('pending', 'processing', 'completed', 'failed');
CREATE TYPE ai_log_status AS ENUM ('succeeded', 'blocked', 'failed');
CREATE TYPE feedback_value AS ENUM ('helpful', 'not_helpful');
CREATE TYPE document_type AS ENUM ('regulation', 'guideline', 'faq', 'template', 'other');
CREATE TYPE document_status AS ENUM ('draft', 'review', 'published', 'archived');
CREATE TYPE plan_audience AS ENUM ('umkm', 'institution');
CREATE TYPE subscription_status AS ENUM ('trialing', 'active', 'past_due', 'cancelled', 'expired');
CREATE TYPE invoice_status AS ENUM ('draft', 'issued', 'paid', 'void', 'overdue');
CREATE TYPE mentor_session_status AS ENUM ('requested', 'confirmed', 'completed', 'cancelled', 'no_show');
CREATE TYPE report_type AS ENUM ('monthly', 'quarterly', 'impact', 'custom');
CREATE TYPE report_status AS ENUM ('queued', 'generating', 'ready', 'failed');
CREATE TYPE notification_channel AS ENUM ('in_app', 'email', 'whatsapp');
CREATE TYPE notification_status AS ENUM ('queued', 'sent', 'failed', 'read');

-- ---------------------------------------------------------------------------
-- Helper
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION set_updated_at() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION prevent_mutation() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
  RAISE EXCEPTION 'Tabel % bersifat append-only', TG_TABLE_NAME;
END;
$$;

CREATE OR REPLACE FUNCTION current_tenant_id() RETURNS uuid
LANGUAGE sql STABLE AS $$
  SELECT nullif(current_setting('app.tenant_id', true), '')::uuid
$$;

-- ---------------------------------------------------------------------------
-- Plan
-- ---------------------------------------------------------------------------
CREATE TABLE plan (
  id              smallint PRIMARY KEY,
  code            varchar(32) NOT NULL UNIQUE,
  name            varchar(80) NOT NULL,
  audience        plan_audience NOT NULL,
  price_monthly   numeric(12,2) NOT NULL DEFAULT 0 CHECK (price_monthly >= 0),
  price_yearly    numeric(12,2) CHECK (price_yearly >= 0),
  quota_umkm      integer CHECK (quota_umkm > 0),
  features        jsonb NOT NULL DEFAULT '{}'::jsonb,
  is_active       boolean NOT NULL DEFAULT true,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- Tenant
-- ---------------------------------------------------------------------------
CREATE TABLE tenant (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name            varchar(160) NOT NULL,
  slug            varchar(80) NOT NULL UNIQUE,
  type            tenant_type NOT NULL,
  status          tenant_status NOT NULL DEFAULT 'active',
  contact_email   citext,
  plan_id         smallint REFERENCES plan(id) ON DELETE SET NULL,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- User
-- ---------------------------------------------------------------------------
CREATE TABLE "user" (
  id              uuid PRIMARY KEY,
  tenant_id       uuid NOT NULL REFERENCES tenant(id) ON DELETE CASCADE,
  email           citext NOT NULL UNIQUE,
  full_name       varchar(120) NOT NULL,
  phone           varchar(20),
  role            user_role NOT NULL DEFAULT 'umkm',
  status          user_status NOT NULL DEFAULT 'active',
  last_login_at   timestamptz,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_user_tenant ON "user" (tenant_id);

-- ---------------------------------------------------------------------------
-- UMKMProfile
-- ---------------------------------------------------------------------------
CREATE TABLE umkm_profile (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id             uuid NOT NULL UNIQUE REFERENCES "user"(id) ON DELETE CASCADE,
  tenant_id           uuid NOT NULL REFERENCES tenant(id) ON DELETE CASCADE,
  business_name       varchar(160) NOT NULL,
  owner_name          varchar(120) NOT NULL,
  gender              gender_value,
  age                 smallint CHECK (age BETWEEN 15 AND 100),
  whatsapp            varchar(20),
  email               citext,
  address             text,
  sector              profile_sector NOT NULL,
  established_year    smallint NOT NULL CHECK (established_year BETWEEN 1900 AND 2100),
  operation_months    smallint NOT NULL CHECK (operation_months >= 0),
  business_description text,
  completeness_pct    numeric(5,2) NOT NULL DEFAULT 0 CHECK (completeness_pct BETWEEN 0 AND 100),
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_umkm_profile_tenant ON umkm_profile (tenant_id);

-- ---------------------------------------------------------------------------
-- Dimension dan Criterion
-- ---------------------------------------------------------------------------
CREATE TABLE dimension (
  id              smallint PRIMARY KEY,
  code            varchar(32) NOT NULL UNIQUE,
  name            varchar(80) NOT NULL,
  weight          numeric(5,2) NOT NULL DEFAULT 0 CHECK (weight BETWEEN 0 AND 100),
  is_scored       boolean NOT NULL DEFAULT true,
  order_no        smallint NOT NULL,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE criterion (
  id              smallint PRIMARY KEY,
  dimension_id    smallint NOT NULL REFERENCES dimension(id) ON DELETE RESTRICT,
  code            varchar(16) NOT NULL UNIQUE,
  question        text NOT NULL,
  input_type      input_type NOT NULL,
  weight          numeric(5,2) NOT NULL DEFAULT 1 CHECK (weight >= 0),
  scoring_rule    jsonb NOT NULL,
  is_active       boolean NOT NULL DEFAULT true,
  version         varchar(16) NOT NULL DEFAULT '1.0',
  order_no        smallint NOT NULL,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_criterion_dimension ON criterion (dimension_id, order_no);

-- ---------------------------------------------------------------------------
-- Segment
-- ---------------------------------------------------------------------------
CREATE TABLE segment (
  id              smallint PRIMARY KEY,
  code            varchar(32) NOT NULL UNIQUE,
  name            varchar(80) NOT NULL,
  min_score       numeric(5,2) NOT NULL CHECK (min_score BETWEEN 0 AND 100),
  max_score       numeric(5,2) NOT NULL CHECK (max_score BETWEEN 0 AND 100),
  curriculum      text,
  order_no        smallint NOT NULL,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT segment_range CHECK (min_score < max_score)
);

-- ---------------------------------------------------------------------------
-- Assessment
-- ---------------------------------------------------------------------------
CREATE TABLE assessment (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES tenant(id) ON DELETE CASCADE,
  umkm_profile_id     uuid NOT NULL REFERENCES umkm_profile(id) ON DELETE CASCADE,
  status              assessment_status NOT NULL DEFAULT 'draft',
  scoring_version     varchar(16) NOT NULL DEFAULT '2026.11-v1',
  total_score         numeric(5,2) CHECK (total_score BETWEEN 0 AND 100),
  segment_id          smallint REFERENCES segment(id) ON DELETE RESTRICT,
  started_at          timestamptz NOT NULL DEFAULT now(),
  submitted_at        timestamptz,
  scored_at           timestamptz,
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT assessment_scored_fields CHECK (
    status <> 'scored' OR (segment_id IS NOT NULL AND total_score IS NOT NULL)
  )
);

CREATE INDEX idx_assessment_profile ON assessment (umkm_profile_id, created_at DESC);
CREATE INDEX idx_assessment_tenant_status ON assessment (tenant_id, status);

-- ---------------------------------------------------------------------------
-- AssessmentAnswer
-- ---------------------------------------------------------------------------
CREATE TABLE assessment_answer (
  id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  assessment_id   uuid NOT NULL REFERENCES assessment(id) ON DELETE CASCADE,
  criterion_id    smallint NOT NULL REFERENCES criterion(id) ON DELETE RESTRICT,
  raw_value       jsonb NOT NULL,
  numeric_value   numeric(8,2),
  score           numeric(5,2) CHECK (score BETWEEN 0 AND 100),
  answered_at     timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT assessment_answer_unique UNIQUE (assessment_id, criterion_id)
);

CREATE INDEX idx_assessment_answer_assessment ON assessment_answer (assessment_id);
CREATE INDEX idx_assessment_answer_criterion ON assessment_answer (criterion_id);

-- ---------------------------------------------------------------------------
-- DimensionScore
-- ---------------------------------------------------------------------------
CREATE TABLE dimension_score (
  assessment_id   uuid NOT NULL REFERENCES assessment(id) ON DELETE CASCADE,
  dimension_id    smallint NOT NULL REFERENCES dimension(id) ON DELETE RESTRICT,
  raw_score       numeric(5,2) CHECK (raw_score BETWEEN 0 AND 100),
  weighted_score  numeric(5,2) CHECK (weighted_score BETWEEN 0 AND 100),
  is_scored       boolean NOT NULL,
  computed_at     timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (assessment_id, dimension_id)
);

-- ---------------------------------------------------------------------------
-- Roadmap, Milestone, ProgressLog
-- ---------------------------------------------------------------------------
CREATE TABLE roadmap (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES tenant(id) ON DELETE CASCADE,
  assessment_id   uuid NOT NULL REFERENCES assessment(id) ON DELETE CASCADE,
  version         smallint NOT NULL DEFAULT 1,
  status          roadmap_status NOT NULL DEFAULT 'draft',
  title           varchar(160) NOT NULL,
  summary         text,
  generated_by    roadmap_generated_by NOT NULL DEFAULT 'rule',
  model_name      varchar(80),
  prompt_version  varchar(32),
  generated_at    timestamptz NOT NULL DEFAULT now(),
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT roadmap_version_unique UNIQUE (assessment_id, version)
);

CREATE UNIQUE INDEX idx_roadmap_one_active ON roadmap (assessment_id) WHERE status = 'active';
CREATE INDEX idx_roadmap_tenant ON roadmap (tenant_id);

CREATE TABLE milestone (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  roadmap_id      uuid NOT NULL REFERENCES roadmap(id) ON DELETE CASCADE,
  order_no        smallint NOT NULL,
  title           varchar(160) NOT NULL,
  description     text,
  action_items    jsonb,
  due_date        date,
  estimated_cost  numeric(12,2) CHECK (estimated_cost >= 0),
  status          milestone_status NOT NULL DEFAULT 'pending',
  completed_at    timestamptz,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT milestone_order_unique UNIQUE (roadmap_id, order_no)
);

CREATE INDEX idx_milestone_roadmap ON milestone (roadmap_id, order_no);

CREATE TABLE progress_log (
  id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id       uuid NOT NULL REFERENCES tenant(id) ON DELETE CASCADE,
  milestone_id    uuid NOT NULL REFERENCES milestone(id) ON DELETE CASCADE,
  user_id         uuid NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
  progress_pct    smallint NOT NULL CHECK (progress_pct BETWEEN 0 AND 100),
  note            text,
  evidence_url    text,
  logged_at       timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_progress_log_milestone ON progress_log (milestone_id, logged_at DESC);
CREATE INDEX idx_progress_log_tenant ON progress_log (tenant_id);

-- ---------------------------------------------------------------------------
-- Consultation dan AIAnswerLog
-- ---------------------------------------------------------------------------
CREATE TABLE consultation (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES tenant(id) ON DELETE CASCADE,
  user_id         uuid NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  assessment_id   uuid NOT NULL REFERENCES assessment(id) ON DELETE RESTRICT,
  question        text NOT NULL CHECK (char_length(question) BETWEEN 3 AND 1000),
  status          consultation_status NOT NULL DEFAULT 'pending',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_consultation_user ON consultation (user_id, created_at DESC);
CREATE INDEX idx_consultation_tenant ON consultation (tenant_id, created_at DESC);
CREATE INDEX idx_consultation_assessment ON consultation (assessment_id);

CREATE TABLE ai_answer_log (
  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  consultation_id   uuid NOT NULL REFERENCES consultation(id) ON DELETE CASCADE,
  model             varchar(80) NOT NULL,
  prompt_version    varchar(32) NOT NULL,
  answer            text,
  sources           jsonb NOT NULL DEFAULT '[]'::jsonb,
  guardrail_result  jsonb NOT NULL DEFAULT '{}'::jsonb,
  token_count       integer CHECK (token_count >= 0),
  latency_ms        integer CHECK (latency_ms >= 0),
  status            ai_log_status NOT NULL,
  feedback          feedback_value,
  feedback_at       timestamptz,
  created_at        timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT ai_answer_log_answer CHECK (
    (status = 'failed' AND answer IS NULL)
    OR (status <> 'failed' AND answer IS NOT NULL)
  ),
  CONSTRAINT ai_answer_log_feedback CHECK (feedback_at IS NULL OR feedback IS NOT NULL)
);

CREATE INDEX idx_ai_answer_log_consultation ON ai_answer_log (consultation_id, created_at DESC);
CREATE INDEX idx_ai_answer_log_status ON ai_answer_log (status);

-- ---------------------------------------------------------------------------
-- Knowledge
-- ---------------------------------------------------------------------------
CREATE TABLE knowledge_document (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid REFERENCES tenant(id) ON DELETE SET NULL,
  title           varchar(200) NOT NULL,
  source_name     varchar(160) NOT NULL,
  source_url      text,
  document_type   document_type NOT NULL,
  version         varchar(32) NOT NULL,
  effective_date  date,
  expiry_date     date,
  status          document_status NOT NULL DEFAULT 'draft',
  file_url        text,
  checksum        char(64),
  reviewer_id     uuid REFERENCES "user"(id) ON DELETE SET NULL,
  published_at    timestamptz,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT knowledge_document_dates CHECK (
    effective_date IS NULL OR expiry_date IS NULL OR expiry_date > effective_date
  )
);

CREATE TABLE knowledge_chunk (
  id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  document_id     uuid NOT NULL REFERENCES knowledge_document(id) ON DELETE CASCADE,
  chunk_index     smallint NOT NULL,
  section_label   varchar(160),
  content         text NOT NULL,
  token_count     smallint NOT NULL CHECK (token_count > 0),
  embedding       vector(768),
  created_at      timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT knowledge_chunk_unique UNIQUE (document_id, chunk_index)
);

CREATE INDEX idx_knowledge_chunk_document ON knowledge_chunk (document_id, chunk_index);

-- ---------------------------------------------------------------------------
-- MentorSession, Subscription, Invoice
-- ---------------------------------------------------------------------------
CREATE TABLE mentor_session (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES tenant(id) ON DELETE CASCADE,
  umkm_profile_id uuid NOT NULL REFERENCES umkm_profile(id) ON DELETE CASCADE,
  mentor_id       uuid NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
  scheduled_at    timestamptz NOT NULL,
  duration_min    smallint NOT NULL CHECK (duration_min BETWEEN 15 AND 180),
  status          mentor_session_status NOT NULL DEFAULT 'requested',
  topic           varchar(160),
  notes           text,
  fee_amount      numeric(12,2) CHECK (fee_amount >= 0),
  platform_fee    numeric(12,2) CHECK (platform_fee >= 0),
  mentor_fee      numeric(12,2) CHECK (mentor_fee >= 0),
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE subscription (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid REFERENCES tenant(id) ON DELETE CASCADE,
  user_id         uuid REFERENCES "user"(id) ON DELETE CASCADE,
  plan_id         smallint NOT NULL REFERENCES plan(id) ON DELETE RESTRICT,
  status          subscription_status NOT NULL DEFAULT 'trialing',
  period_start    date NOT NULL,
  period_end      date NOT NULL,
  price           numeric(12,2) NOT NULL DEFAULT 0 CHECK (price >= 0),
  auto_renew      boolean NOT NULL DEFAULT false,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT subscription_one_owner CHECK (
    ((tenant_id IS NOT NULL)::int + (user_id IS NOT NULL)::int) = 1
  ),
  CONSTRAINT subscription_period CHECK (period_start < period_end)
);

CREATE TABLE invoice (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  subscription_id uuid NOT NULL REFERENCES subscription(id) ON DELETE CASCADE,
  number          varchar(40) NOT NULL UNIQUE,
  amount          numeric(12,2) NOT NULL CHECK (amount >= 0),
  tax_amount      numeric(12,2) NOT NULL DEFAULT 0 CHECK (tax_amount >= 0),
  status          invoice_status NOT NULL DEFAULT 'draft',
  issued_at       date NOT NULL,
  due_at          date NOT NULL,
  paid_at         timestamptz,
  payment_ref     varchar(120),
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT invoice_due CHECK (due_at >= issued_at)
);

-- ---------------------------------------------------------------------------
-- Report, Notification, AuditLog
-- ---------------------------------------------------------------------------
CREATE TABLE report (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES tenant(id) ON DELETE CASCADE,
  type            report_type NOT NULL,
  period_start    date NOT NULL,
  period_end      date NOT NULL,
  status          report_status NOT NULL DEFAULT 'queued',
  file_url        text,
  parameters      jsonb NOT NULL DEFAULT '{}'::jsonb,
  generated_by    uuid REFERENCES "user"(id) ON DELETE SET NULL,
  generated_at    timestamptz,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT report_period CHECK (period_start <= period_end)
);

CREATE TABLE notification (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES tenant(id) ON DELETE CASCADE,
  user_id         uuid NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  type            varchar(40) NOT NULL,
  channel         notification_channel NOT NULL,
  title           varchar(160) NOT NULL,
  body            text NOT NULL,
  status          notification_status NOT NULL DEFAULT 'queued',
  sent_at         timestamptz,
  read_at         timestamptz,
  created_at      timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_notification_user ON notification (user_id, created_at DESC);

CREATE TABLE audit_log (
  id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id       uuid REFERENCES tenant(id) ON DELETE SET NULL,
  actor_user_id   uuid REFERENCES "user"(id) ON DELETE SET NULL,
  action          varchar(80) NOT NULL,
  entity_type     varchar(60) NOT NULL,
  entity_id       varchar(64),
  before_data     jsonb,
  after_data      jsonb,
  ip_address      inet,
  user_agent      text,
  trace_id        uuid,
  created_at      timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_audit_log_tenant ON audit_log (tenant_id, created_at DESC);
CREATE INDEX idx_audit_log_entity ON audit_log (entity_type, entity_id);

-- ---------------------------------------------------------------------------
-- Trigger updated_at
-- ---------------------------------------------------------------------------
CREATE TRIGGER trg_plan_updated BEFORE UPDATE ON plan FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_tenant_updated BEFORE UPDATE ON tenant FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_user_updated BEFORE UPDATE ON "user" FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_umkm_profile_updated BEFORE UPDATE ON umkm_profile FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_dimension_updated BEFORE UPDATE ON dimension FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_criterion_updated BEFORE UPDATE ON criterion FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_segment_updated BEFORE UPDATE ON segment FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_assessment_updated BEFORE UPDATE ON assessment FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_roadmap_updated BEFORE UPDATE ON roadmap FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_milestone_updated BEFORE UPDATE ON milestone FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_consultation_updated BEFORE UPDATE ON consultation FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_knowledge_document_updated BEFORE UPDATE ON knowledge_document FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_subscription_updated BEFORE UPDATE ON subscription FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_invoice_updated BEFORE UPDATE ON invoice FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_report_updated BEFORE UPDATE ON report FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Append-only
CREATE TRIGGER trg_progress_log_append_only BEFORE UPDATE OR DELETE ON progress_log
FOR EACH ROW EXECUTE FUNCTION prevent_mutation();
CREATE TRIGGER trg_audit_log_append_only BEFORE UPDATE OR DELETE ON audit_log
FOR EACH ROW EXECUTE FUNCTION prevent_mutation();

-- ---------------------------------------------------------------------------
-- Row level security
-- Backend wajib menjalankan SET LOCAL app.tenant_id = '<uuid>' pada transaksi
-- pengguna. Service role Supabase melewati RLS, sehingga scoping aplikasi tetap
-- wajib.
-- ---------------------------------------------------------------------------
ALTER TABLE umkm_profile ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessment ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessment_answer ENABLE ROW LEVEL SECURITY;
ALTER TABLE dimension_score ENABLE ROW LEVEL SECURITY;
ALTER TABLE roadmap ENABLE ROW LEVEL SECURITY;
ALTER TABLE milestone ENABLE ROW LEVEL SECURITY;
ALTER TABLE progress_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultation ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_answer_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON umkm_profile
  USING (tenant_id = current_tenant_id())
  WITH CHECK (tenant_id = current_tenant_id());

CREATE POLICY tenant_isolation ON assessment
  USING (tenant_id = current_tenant_id())
  WITH CHECK (tenant_id = current_tenant_id());

CREATE POLICY tenant_isolation ON assessment_answer
  USING (EXISTS (
    SELECT 1 FROM assessment a
    WHERE a.id = assessment_answer.assessment_id
      AND a.tenant_id = current_tenant_id()
  ))
  WITH CHECK (EXISTS (
    SELECT 1 FROM assessment a
    WHERE a.id = assessment_answer.assessment_id
      AND a.tenant_id = current_tenant_id()
  ));

CREATE POLICY tenant_isolation ON dimension_score
  USING (EXISTS (
    SELECT 1 FROM assessment a
    WHERE a.id = dimension_score.assessment_id
      AND a.tenant_id = current_tenant_id()
  ))
  WITH CHECK (EXISTS (
    SELECT 1 FROM assessment a
    WHERE a.id = dimension_score.assessment_id
      AND a.tenant_id = current_tenant_id()
  ));

CREATE POLICY tenant_isolation ON roadmap
  USING (tenant_id = current_tenant_id())
  WITH CHECK (tenant_id = current_tenant_id());

CREATE POLICY tenant_isolation ON milestone
  USING (EXISTS (
    SELECT 1 FROM roadmap r
    WHERE r.id = milestone.roadmap_id
      AND r.tenant_id = current_tenant_id()
  ))
  WITH CHECK (EXISTS (
    SELECT 1 FROM roadmap r
    WHERE r.id = milestone.roadmap_id
      AND r.tenant_id = current_tenant_id()
  ));

CREATE POLICY tenant_isolation ON progress_log
  USING (tenant_id = current_tenant_id())
  WITH CHECK (tenant_id = current_tenant_id());

CREATE POLICY tenant_isolation ON consultation
  USING (tenant_id = current_tenant_id())
  WITH CHECK (tenant_id = current_tenant_id());

CREATE POLICY tenant_isolation ON ai_answer_log
  USING (EXISTS (
    SELECT 1 FROM consultation c
    WHERE c.id = ai_answer_log.consultation_id
      AND c.tenant_id = current_tenant_id()
  ))
  WITH CHECK (EXISTS (
    SELECT 1 FROM consultation c
    WHERE c.id = ai_answer_log.consultation_id
      AND c.tenant_id = current_tenant_id()
  ));

CREATE POLICY tenant_isolation ON audit_log
  USING (tenant_id = current_tenant_id())
  WITH CHECK (tenant_id = current_tenant_id());

COMMIT;

-- ============================================================================
-- Catatan operasional
-- 1. Jalankan seed.sql setelah DDL.
-- 2. Untuk uji RLS: SET LOCAL app.tenant_id = '<uuid>'.
-- 3. Jangan memakai service role dari browser.
-- 4. Tabel "user" memakai tanda kutip karena user adalah kata kunci PostgreSQL.
-- ============================================================================
