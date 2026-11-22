-- =============================================================================
-- GROWPATH — DDL POSTGRESQL 15+ (SUPABASE COMPATIBLE)
-- =============================================================================
-- Proyek      : Growpath — Platform Advisory UMKM Berbasis AI (Kelompok 6, R-001)
-- Fase        : P13 · Pembekuan Arsitektur & Desain Sistem (PR sebelum P14)
-- Disusun oleh: Wisnu Nugroho (F1E124032) — Database Architect
-- Direview oleh: Bagas Adinata (Programmer), Ripa Bagaskara (CEO / AI Engineer)
-- Tanggal     : 22 November 2026
-- Cakupan     : 24 Entitas (21 Entitas Progress 12 + 3 Entitas AI P13–P14)
--               [Tenant, User, UMKMProfile, Assessment, AssessmentAnswer,
--                Dimension, Criterion, DimensionScore, Segment, Roadmap,
--                Milestone, ProgressLog, MentorSession, Plan, Subscription,
--                Invoice, KnowledgeDocument, KnowledgeChunk, Report,
--                Notification, AuditLog, AIConsultation, AIResponseLog,
--                AIUsageQuota]
-- =============================================================================

BEGIN;

-- -----------------------------------------------------------------------------
-- 1. EKSTENSI POSTGRESQL
-- -----------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS vector;

-- -----------------------------------------------------------------------------
-- 2. TIPE ENUM
-- -----------------------------------------------------------------------------
CREATE TYPE tenant_type_enum AS ENUM ('platform', 'institution', 'partner');
CREATE TYPE tenant_status_enum AS ENUM ('active', 'suspended', 'inactive');

CREATE TYPE user_role_enum AS ENUM ('umkm', 'pendamping', 'mentor', 'admin_b2g', 'admin_platform');
CREATE TYPE user_status_enum AS ENUM ('active', 'invited', 'suspended', 'deleted');

CREATE TYPE umkm_sector_enum AS ENUM ('kuliner', 'fashion', 'lainnya');
CREATE TYPE revenue_band_enum AS ENUM ('<1jt', '1-5jt', '5-25jt', '>25jt');

CREATE TYPE assessment_status_enum AS ENUM ('draft', 'submitted', 'scored', 'archived');
CREATE TYPE criterion_input_type_enum AS ENUM ('boolean', 'scale', 'enum', 'number', 'text');

CREATE TYPE roadmap_status_enum AS ENUM ('draft', 'active', 'completed', 'superseded');
CREATE TYPE roadmap_generated_by_enum AS ENUM ('rule', 'llm', 'hybrid', 'manual');
CREATE TYPE milestone_status_enum AS ENUM ('pending', 'in_progress', 'done', 'skipped');

CREATE TYPE mentor_session_status_enum AS ENUM ('requested', 'confirmed', 'completed', 'cancelled', 'no_show');

CREATE TYPE plan_audience_enum AS ENUM ('umkm', 'institution');
CREATE TYPE subscription_status_enum AS ENUM ('trialing', 'active', 'past_due', 'cancelled', 'expired');
CREATE TYPE invoice_status_enum AS ENUM ('draft', 'issued', 'paid', 'void', 'overdue');

CREATE TYPE knowledge_doc_type_enum AS ENUM ('regulation', 'guideline', 'faq', 'template', 'other');
CREATE TYPE knowledge_doc_status_enum AS ENUM ('draft', 'review', 'published', 'archived');

CREATE TYPE report_type_enum AS ENUM ('monthly', 'quarterly', 'impact', 'custom');
CREATE TYPE report_status_enum AS ENUM ('queued', 'generating', 'ready', 'failed');

CREATE TYPE notification_channel_enum AS ENUM ('in_app', 'email', 'whatsapp');
CREATE TYPE notification_status_enum AS ENUM ('queued', 'sent', 'failed', 'read');

-- Enum khusus 3 entitas AI (P13–P14 Kelompok 6)
CREATE TYPE ai_consultation_category_enum AS ENUM (
    'operasional', 'pemasaran', 'keuangan', 'legalitas', 'strategi', 'lainnya'
);
CREATE TYPE ai_consultation_status_enum AS ENUM ('active', 'closed', 'escalated', 'archived');
CREATE TYPE ai_guardrail_status_enum AS ENUM ('passed', 'flagged', 'blocked', 'escalated_to_mentor');

-- -----------------------------------------------------------------------------
-- 3. FUNGSI TRIGGER UPDATED_AT
-- -----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- -----------------------------------------------------------------------------
-- 4. TABEL REFERENSI (MASTER DATA)
-- -----------------------------------------------------------------------------

-- 4.1 Plan
CREATE TABLE plans (
    id              SMALLINT PRIMARY KEY,
    code            VARCHAR(32) NOT NULL UNIQUE,
    name            VARCHAR(80) NOT NULL,
    audience        plan_audience_enum NOT NULL,
    price_monthly   NUMERIC(12, 2) NOT NULL CHECK (price_monthly >= 0),
    price_yearly    NUMERIC(12, 2) NULL CHECK (price_yearly IS NULL OR price_yearly >= 0),
    quota_umkm      INTEGER NULL,
    features        JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_plans_institution_quota CHECK (
        audience <> 'institution' OR (quota_umkm IS NOT NULL AND quota_umkm > 0)
    )
);

-- 4.2 Dimension (6 Dimensi Framework)
CREATE TABLE dimensions (
    id              SMALLINT PRIMARY KEY,
    code            VARCHAR(32) NOT NULL UNIQUE,
    name            VARCHAR(80) NOT NULL,
    weight          NUMERIC(5, 2) NOT NULL CHECK (weight >= 0 AND weight <= 100),
    is_scored       BOOLEAN NOT NULL DEFAULT TRUE,
    order_no        SMALLINT NOT NULL UNIQUE CHECK (order_no > 0),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 4.3 Criterion (31 Kriteria Scoring)
CREATE TABLE criteria (
    id              SMALLINT PRIMARY KEY,
    dimension_id    SMALLINT NOT NULL REFERENCES dimensions(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    code            VARCHAR(16) NOT NULL UNIQUE,
    question        TEXT NOT NULL,
    input_type      criterion_input_type_enum NOT NULL,
    weight          NUMERIC(5, 2) NOT NULL CHECK (weight >= 0 AND weight <= 100),
    scoring_rule    JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    version         VARCHAR(16) NOT NULL DEFAULT '1.0',
    order_no        SMALLINT NOT NULL CHECK (order_no > 0),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 4.4 Segment (4 Segmen Kematangan Usaha)
CREATE TABLE segments (
    id              SMALLINT PRIMARY KEY,
    code            VARCHAR(32) NOT NULL UNIQUE,
    name            VARCHAR(80) NOT NULL,
    min_score       NUMERIC(5, 2) NOT NULL CHECK (min_score >= 0 AND min_score <= 100),
    max_score       NUMERIC(5, 2) NOT NULL CHECK (max_score >= 0 AND max_score <= 100),
    curriculum      TEXT NULL,
    order_no        SMALLINT NOT NULL UNIQUE CHECK (order_no > 0),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_segments_score_range CHECK (min_score < max_score)
);

-- -----------------------------------------------------------------------------
-- 5. KELOMPOK IDENTITAS & DATA USAHA (FITUR MUST #1)
-- -----------------------------------------------------------------------------

-- 5.1 Tenant
CREATE TABLE tenants (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(160) NOT NULL,
    slug            VARCHAR(80) NOT NULL UNIQUE,
    type            tenant_type_enum NOT NULL,
    status          tenant_status_enum NOT NULL DEFAULT 'active',
    contact_email   CITEXT NULL,
    plan_id         SMALLINT NULL REFERENCES plans(id) ON UPDATE CASCADE ON DELETE SET NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 5.2 User
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL REFERENCES tenants(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    email           CITEXT NOT NULL UNIQUE,
    full_name       VARCHAR(120) NOT NULL,
    phone           VARCHAR(20) NULL,
    role            user_role_enum NOT NULL DEFAULT 'umkm',
    status          user_status_enum NOT NULL DEFAULT 'active',
    last_login_at   TIMESTAMPTZ NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 5.3 UMKMProfile
CREATE TABLE umkm_profiles (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id              UUID NOT NULL UNIQUE REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
    tenant_id            UUID NOT NULL REFERENCES tenants(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    business_name        VARCHAR(160) NOT NULL,
    owner_name           VARCHAR(120) NOT NULL,
    sector               umkm_sector_enum NOT NULL,
    city                 VARCHAR(80) NOT NULL,
    province             VARCHAR(80) NOT NULL,
    established_year     SMALLINT NOT NULL CHECK (established_year BETWEEN 1900 AND 2100),
    operation_months     SMALLINT NOT NULL CHECK (operation_months >= 0),
    monthly_revenue_band revenue_band_enum NULL,
    employees_count      SMALLINT NULL CHECK (employees_count IS NULL OR employees_count >= 0),
    business_description TEXT NULL,
    completeness_pct     NUMERIC(5, 2) NOT NULL DEFAULT 0 CHECK (completeness_pct >= 0 AND completeness_pct <= 100),
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- -----------------------------------------------------------------------------
-- 6. KELOMPOK ASESMEN 31 KRITERIA & SCORING DETERMINISTIK
-- -----------------------------------------------------------------------------

-- 6.1 Assessment
CREATE TABLE assessments (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL REFERENCES tenants(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    umkm_profile_id UUID NOT NULL REFERENCES umkm_profiles(id) ON UPDATE CASCADE ON DELETE CASCADE,
    status          assessment_status_enum NOT NULL DEFAULT 'draft',
    scoring_version VARCHAR(16) NOT NULL DEFAULT '1.0',
    total_score     NUMERIC(5, 2) NULL CHECK (total_score IS NULL OR (total_score >= 0 AND total_score <= 100)),
    segment_id      SMALLINT NULL REFERENCES segments(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    submitted_at    TIMESTAMPTZ NULL,
    scored_at       TIMESTAMPTZ NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_assessments_scored_segment CHECK (
        status <> 'scored' OR (segment_id IS NOT NULL AND total_score IS NOT NULL)
    )
);

-- 6.2 AssessmentAnswer
CREATE TABLE assessment_answers (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    assessment_id   UUID NOT NULL REFERENCES assessments(id) ON UPDATE CASCADE ON DELETE CASCADE,
    criterion_id    SMALLINT NOT NULL REFERENCES criteria(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    raw_value       JSONB NOT NULL,
    numeric_value   NUMERIC(8, 2) NULL,
    score           NUMERIC(5, 2) NULL CHECK (score IS NULL OR (score >= 0 AND score <= 100)),
    answered_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_assessment_answers_pair UNIQUE (assessment_id, criterion_id)
);

-- 6.3 DimensionScore
CREATE TABLE dimension_scores (
    assessment_id   UUID NOT NULL REFERENCES assessments(id) ON UPDATE CASCADE ON DELETE CASCADE,
    dimension_id    SMALLINT NOT NULL REFERENCES dimensions(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    raw_score       NUMERIC(5, 2) NULL CHECK (raw_score IS NULL OR (raw_score >= 0 AND raw_score <= 100)),
    weighted_score  NUMERIC(5, 2) NOT NULL CHECK (weighted_score >= 0 AND weighted_score <= 100),
    is_scored       BOOLEAN NOT NULL,
    computed_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (assessment_id, dimension_id)
);

-- -----------------------------------------------------------------------------
-- 7. KELOMPOK REKOMENDASI, ROADMAP & PROGRES (FITUR MUST #3 & #5)
-- -----------------------------------------------------------------------------

-- 7.1 Roadmap
CREATE TABLE roadmaps (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL REFERENCES tenants(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    assessment_id   UUID NOT NULL REFERENCES assessments(id) ON UPDATE CASCADE ON DELETE CASCADE,
    version         SMALLINT NOT NULL DEFAULT 1 CHECK (version > 0),
    status          roadmap_status_enum NOT NULL DEFAULT 'draft',
    title           VARCHAR(160) NOT NULL,
    summary         TEXT NULL,
    generated_by    roadmap_generated_by_enum NOT NULL DEFAULT 'hybrid',
    model_name      VARCHAR(80) NULL,
    prompt_version  VARCHAR(32) NULL,
    generated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_roadmaps_assessment_version UNIQUE (assessment_id, version)
);

-- Satu roadmap active per assessment
CREATE UNIQUE INDEX uq_roadmaps_one_active_per_assessment
    ON roadmaps (assessment_id)
    WHERE status = 'active';

-- 7.2 Milestone
CREATE TABLE milestones (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    roadmap_id      UUID NOT NULL REFERENCES roadmaps(id) ON UPDATE CASCADE ON DELETE CASCADE,
    order_no        SMALLINT NOT NULL CHECK (order_no > 0),
    title           VARCHAR(160) NOT NULL,
    description     TEXT NULL,
    action_items    JSONB NULL,
    due_date        DATE NULL,
    estimated_cost  NUMERIC(12, 2) NULL CHECK (estimated_cost IS NULL OR estimated_cost >= 0),
    status          milestone_status_enum NOT NULL DEFAULT 'pending',
    completed_at    TIMESTAMPTZ NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_milestones_roadmap_order UNIQUE (roadmap_id, order_no)
);

-- 7.3 ProgressLog (append-only)
CREATE TABLE progress_logs (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tenant_id       UUID NOT NULL REFERENCES tenants(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    milestone_id    UUID NOT NULL REFERENCES milestones(id) ON UPDATE CASCADE ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    progress_pct    SMALLINT NOT NULL CHECK (progress_pct BETWEEN 0 AND 100),
    note            TEXT NULL,
    evidence_url    TEXT NULL,
    logged_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- -----------------------------------------------------------------------------
-- 8. KELOMPOK KONSULTASI AI, LOG JAWABAN AI & KUOTA (FITUR MUST #2 & #4)
-- -----------------------------------------------------------------------------

-- 8.1 AIConsultation
CREATE TABLE ai_consultations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL REFERENCES tenants(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    umkm_profile_id UUID NOT NULL REFERENCES umkm_profiles(id) ON UPDATE CASCADE ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    assessment_id   UUID NULL REFERENCES assessments(id) ON UPDATE CASCADE ON DELETE SET NULL,
    topic           VARCHAR(160) NOT NULL,
    category        ai_consultation_category_enum NOT NULL DEFAULT 'strategi',
    status          ai_consultation_status_enum NOT NULL DEFAULT 'active',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 8.2 AIResponseLog (append-only, wajib penafian & sitasi)
CREATE TABLE ai_response_logs (
    id                BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tenant_id         UUID NOT NULL REFERENCES tenants(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    consultation_id   UUID NOT NULL REFERENCES ai_consultations(id) ON UPDATE CASCADE ON DELETE CASCADE,
    user_id           UUID NOT NULL REFERENCES users(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    user_prompt       TEXT NOT NULL,
    ai_response       TEXT NOT NULL,
    disclaimer_text   TEXT NOT NULL,
    disclaimer_shown  BOOLEAN NOT NULL DEFAULT TRUE CHECK (disclaimer_shown = TRUE),
    citations         JSONB NOT NULL DEFAULT '[]'::jsonb,
    guardrail_status  ai_guardrail_status_enum NOT NULL DEFAULT 'passed',
    guardrail_reason  VARCHAR(200) NULL,
    model_name        VARCHAR(80) NOT NULL,
    prompt_version    VARCHAR(32) NOT NULL,
    tokens_input      INTEGER NOT NULL DEFAULT 0 CHECK (tokens_input >= 0),
    tokens_output     INTEGER NOT NULL DEFAULT 0 CHECK (tokens_output >= 0),
    latency_ms        INTEGER NULL CHECK (latency_ms IS NULL OR latency_ms >= 0),
    user_rating       SMALLINT NULL CHECK (user_rating IS NULL OR user_rating BETWEEN 1 AND 5),
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 8.3 AIUsageQuota (kontrol kuota per pengguna per periode)
CREATE TABLE ai_usage_quotas (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL REFERENCES tenants(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    user_id         UUID NOT NULL REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
    period_start    DATE NOT NULL,
    period_end      DATE NOT NULL,
    quota_limit     INTEGER NOT NULL CHECK (quota_limit > 0),
    used_count      INTEGER NOT NULL DEFAULT 0 CHECK (used_count >= 0),
    token_limit     INTEGER NULL CHECK (token_limit IS NULL OR token_limit > 0),
    tokens_used     INTEGER NOT NULL DEFAULT 0 CHECK (tokens_used >= 0),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_ai_quota_period CHECK (period_start <= period_end),
    CONSTRAINT chk_ai_quota_usage CHECK (used_count <= quota_limit),
    CONSTRAINT uq_ai_quota_user_period UNIQUE (user_id, period_start, period_end)
);

-- -----------------------------------------------------------------------------
-- 9. KELOMPOK KNOWLEDGE / RAG
-- -----------------------------------------------------------------------------

-- 9.1 KnowledgeDocument
CREATE TABLE knowledge_documents (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NULL REFERENCES tenants(id) ON UPDATE CASCADE ON DELETE CASCADE,
    title           VARCHAR(200) NOT NULL,
    source_name     VARCHAR(160) NOT NULL,
    source_url      TEXT NULL,
    document_type   knowledge_doc_type_enum NOT NULL,
    version         VARCHAR(32) NOT NULL,
    effective_date  DATE NULL,
    expiry_date     DATE NULL,
    status          knowledge_doc_status_enum NOT NULL DEFAULT 'draft',
    file_url        TEXT NULL,
    checksum        CHAR(64) NULL CHECK (checksum IS NULL OR char_length(checksum) = 64),
    reviewer_id     UUID NULL REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL,
    published_at    TIMESTAMPTZ NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_knowledge_doc_dates CHECK (
        effective_date IS NULL OR expiry_date IS NULL OR expiry_date > effective_date
    )
);

-- 9.2 KnowledgeChunk
CREATE TABLE knowledge_chunks (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    document_id     UUID NOT NULL REFERENCES knowledge_documents(id) ON UPDATE CASCADE ON DELETE CASCADE,
    chunk_index     SMALLINT NOT NULL CHECK (chunk_index >= 0),
    section_label   VARCHAR(160) NULL,
    content         TEXT NOT NULL,
    token_count     SMALLINT NOT NULL CHECK (token_count > 0),
    embedding       VECTOR(768) NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_knowledge_chunks_doc_idx UNIQUE (document_id, chunk_index)
);

-- -----------------------------------------------------------------------------
-- 10. KELOMPOK OPERASIONAL, BILLING, MENTOR, PELAPORAN & TATA KELOLA
-- -----------------------------------------------------------------------------

-- 10.1 MentorSession (Fase 2)
CREATE TABLE mentor_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL REFERENCES tenants(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    umkm_profile_id UUID NOT NULL REFERENCES umkm_profiles(id) ON UPDATE CASCADE ON DELETE CASCADE,
    mentor_id       UUID NOT NULL REFERENCES users(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    scheduled_at    TIMESTAMPTZ NOT NULL,
    duration_min    SMALLINT NOT NULL CHECK (duration_min BETWEEN 15 AND 180),
    status          mentor_session_status_enum NOT NULL DEFAULT 'requested',
    topic           VARCHAR(160) NULL,
    notes           TEXT NULL,
    fee_amount      NUMERIC(12, 2) NULL CHECK (fee_amount IS NULL OR fee_amount >= 0),
    platform_fee    NUMERIC(12, 2) NULL CHECK (platform_fee IS NULL OR platform_fee >= 0),
    mentor_fee      NUMERIC(12, 2) NULL CHECK (mentor_fee IS NULL OR mentor_fee >= 0),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 10.2 Subscription (Fase 2 — owner polimorfik tenant atau user)
CREATE TABLE subscriptions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NULL REFERENCES tenants(id) ON UPDATE CASCADE ON DELETE CASCADE,
    user_id         UUID NULL REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
    plan_id         SMALLINT NOT NULL REFERENCES plans(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    status          subscription_status_enum NOT NULL DEFAULT 'trialing',
    period_start    DATE NOT NULL,
    period_end      DATE NOT NULL,
    price           NUMERIC(12, 2) NOT NULL CHECK (price >= 0),
    auto_renew      BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_subscriptions_single_owner CHECK (
        (tenant_id IS NOT NULL AND user_id IS NULL) OR
        (tenant_id IS NULL AND user_id IS NOT NULL)
    ),
    CONSTRAINT chk_subscriptions_period CHECK (period_start < period_end)
);

-- 10.3 Invoice (Fase 2)
CREATE TABLE invoices (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subscription_id UUID NOT NULL REFERENCES subscriptions(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    number          VARCHAR(40) NOT NULL UNIQUE,
    amount          NUMERIC(12, 2) NOT NULL CHECK (amount >= 0),
    tax_amount      NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (tax_amount >= 0),
    status          invoice_status_enum NOT NULL DEFAULT 'draft',
    issued_at       DATE NOT NULL,
    due_at          DATE NOT NULL,
    paid_at         TIMESTAMPTZ NULL,
    payment_ref     VARCHAR(120) NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_invoices_due_date CHECK (due_at >= issued_at)
);

-- 10.4 Report (Pelaporan Agregat B2G)
CREATE TABLE reports (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL REFERENCES tenants(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    type            report_type_enum NOT NULL,
    period_start    DATE NOT NULL,
    period_end      DATE NOT NULL,
    status          report_status_enum NOT NULL DEFAULT 'queued',
    file_url        TEXT NULL,
    parameters      JSONB NOT NULL DEFAULT '{}'::jsonb,
    generated_by    UUID NULL REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL,
    generated_at    TIMESTAMPTZ NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_reports_period CHECK (period_start <= period_end)
);

-- 10.5 Notification
CREATE TABLE notifications (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL REFERENCES tenants(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    user_id         UUID NOT NULL REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
    type            VARCHAR(40) NOT NULL,
    channel         notification_channel_enum NOT NULL DEFAULT 'in_app',
    title           VARCHAR(160) NOT NULL,
    body            TEXT NOT NULL,
    status          notification_status_enum NOT NULL DEFAULT 'queued',
    sent_at         TIMESTAMPTZ NULL,
    read_at         TIMESTAMPTZ NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 10.6 AuditLog (append-only)
CREATE TABLE audit_logs (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tenant_id       UUID NULL REFERENCES tenants(id) ON UPDATE CASCADE ON DELETE SET NULL,
    actor_user_id   UUID NULL REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL,
    action          VARCHAR(80) NOT NULL,
    entity_type     VARCHAR(60) NOT NULL,
    entity_id       VARCHAR(64) NULL,
    before_data     JSONB NULL,
    after_data      JSONB NULL,
    ip_address      INET NULL,
    user_agent      TEXT NULL,
    trace_id        UUID NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- -----------------------------------------------------------------------------
-- 11. INDEKS KINERJA & PENCARIAN
-- -----------------------------------------------------------------------------
CREATE INDEX idx_users_tenant_role            ON users (tenant_id, role);
CREATE INDEX idx_umkm_profiles_tenant_sector  ON umkm_profiles (tenant_id, sector);
CREATE INDEX idx_assessments_tenant_profile   ON assessments (tenant_id, umkm_profile_id, created_at DESC);
CREATE INDEX idx_assessments_segment          ON assessments (segment_id);
CREATE INDEX idx_assessment_answers_assess    ON assessment_answers (assessment_id);
CREATE INDEX idx_criteria_dimension_active    ON criteria (dimension_id, is_active);
CREATE INDEX idx_roadmaps_tenant_assessment   ON roadmaps (tenant_id, assessment_id);
CREATE INDEX idx_milestones_roadmap_status    ON milestones (roadmap_id, status);
CREATE INDEX idx_progress_logs_milestone_time ON progress_logs (milestone_id, logged_at DESC);

CREATE INDEX idx_ai_consultations_profile     ON ai_consultations (tenant_id, umkm_profile_id, created_at DESC);
CREATE INDEX idx_ai_response_logs_consult     ON ai_response_logs (consultation_id, created_at DESC);
CREATE INDEX idx_ai_response_logs_user_time   ON ai_response_logs (user_id, created_at DESC);
CREATE INDEX idx_ai_response_logs_guardrail   ON ai_response_logs (guardrail_status);
CREATE INDEX idx_ai_usage_quotas_user_period  ON ai_usage_quotas (user_id, period_start, period_end);

CREATE INDEX idx_knowledge_docs_tenant_status ON knowledge_documents (tenant_id, status);
CREATE INDEX idx_knowledge_chunks_doc         ON knowledge_chunks (document_id);
CREATE INDEX idx_reports_tenant_period        ON reports (tenant_id, period_start, period_end);
CREATE INDEX idx_notifications_user_status    ON notifications (user_id, status, created_at DESC);
CREATE INDEX idx_audit_logs_tenant_time       ON audit_logs (tenant_id, created_at DESC);
CREATE INDEX idx_audit_logs_entity            ON audit_logs (entity_type, entity_id);

-- Indeks HNSW pgvector untuk pencarian kemiripan RAG (aktifkan saat data embedding tersedia)
CREATE INDEX idx_knowledge_chunks_embedding_hnsw
    ON knowledge_chunks USING hnsw (embedding vector_cosine_ops);

-- -----------------------------------------------------------------------------
-- 12. TRIGGER UPDATED_AT PADA TABEL MUTABLE
-- -----------------------------------------------------------------------------
CREATE TRIGGER trg_plans_updated_at              BEFORE UPDATE ON plans              FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_dimensions_updated_at         BEFORE UPDATE ON dimensions         FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_criteria_updated_at           BEFORE UPDATE ON criteria           FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_segments_updated_at           BEFORE UPDATE ON segments           FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_tenants_updated_at            BEFORE UPDATE ON tenants            FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_users_updated_at              BEFORE UPDATE ON users              FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_umkm_profiles_updated_at      BEFORE UPDATE ON umkm_profiles      FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_assessments_updated_at        BEFORE UPDATE ON assessments        FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_roadmaps_updated_at           BEFORE UPDATE ON roadmaps           FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_milestones_updated_at         BEFORE UPDATE ON milestones         FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_ai_consultations_updated_at   BEFORE UPDATE ON ai_consultations   FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_ai_usage_quotas_updated_at    BEFORE UPDATE ON ai_usage_quotas    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_knowledge_docs_updated_at     BEFORE UPDATE ON knowledge_documents FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_mentor_sessions_updated_at    BEFORE UPDATE ON mentor_sessions    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_subscriptions_updated_at      BEFORE UPDATE ON subscriptions      FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_invoices_updated_at           BEFORE UPDATE ON invoices           FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_reports_updated_at            BEFORE UPDATE ON reports            FOR EACH ROW EXECUTE FUNCTION set_updated_at();

COMMIT;