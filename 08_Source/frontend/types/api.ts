export type Role =
  | "umkm"
  | "pendamping"
  | "mentor"
  | "admin_b2g"
  | "admin_platform";

export type UserStatus = "active" | "invited" | "suspended" | "deleted";

export type User = {
  id: string;
  tenant_id: string;
  email: string;
  full_name: string;
  phone: string | null;
  role: Role;
  status: UserStatus;
  last_login_at: string | null;
};

export type AuthResponse = {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
};

export type Problem = {
  type?: string;
  title: string;
  status: number;
  detail?: string;
  code: string;
  trace_id?: string;
  errors?: { field: string; message: string }[];
};

export type Gender = "male" | "female" | "undisclosed";

export type Sector =
  | "kuliner"
  | "fashion"
  | "kriya"
  | "pertanian"
  | "perdagangan"
  | "jasa"
  | "teknologi"
  | "kesehatan"
  | "pendidikan"
  | "lainnya";

export type ProfileInput = {
  business_name: string;
  owner_name: string;
  gender: Gender | null;
  age: number | null;
  whatsapp: string | null;
  email: string | null;
  address: string | null;
  sector: Sector;
  established_year: number;
  operation_months: number;
  business_description: string | null;
};

export type Profile = ProfileInput & {
  id: string;
  user_id: string;
  tenant_id: string;
  completeness_pct: number;
  created_at: string;
  updated_at: string;
};

export type AssessmentStatus = "draft" | "submitted" | "scored" | "archived";

export type Assessment = {
  id: string;
  tenant_id: string;
  umkm_profile_id: string;
  status: AssessmentStatus;
  scoring_version: string;
  total_score: number | null;
  segment_id: number | null;
  started_at: string;
  submitted_at: string | null;
  scored_at: string | null;
};

export type InputType =
  | "boolean"
  | "scale"
  | "enum"
  | "number"
  | "text"
  | "multi_select";

export type CriterionOption = { code: string; label: string };

export type Criterion = {
  id: number;
  dimension_id: number;
  dimension_code: string;
  dimension_name: string;
  code: string;
  question: string;
  input_type: InputType;
  weight: number;
  order_no: number;
  options: CriterionOption[];
  unit: string | null;
};

export type AssessmentAnswer = {
  criterion_id: number;
  raw_value: Record<string, unknown>;
  numeric_value: number | null;
  score: number | null;
};

export type AssessmentDraft = {
  assessment: Assessment;
  criteria: Criterion[];
  answers: AssessmentAnswer[];
};

export type Segment = { id: number; code: string; name: string };

export type DimensionScore = {
  dimension_id: number;
  dimension_code: string;
  dimension_name: string;
  raw_score: number | null;
  weighted_score: number;
  is_scored: boolean;
};

export type AssessmentDetail = {
  assessment: Assessment;
  criteria: Criterion[];
  answers: AssessmentAnswer[];
  scores: DimensionScore[];
  segment: Segment | null;
};

export type ScoreResult = {
  assessment_id: string;
  total_score: number;
  segment: Segment;
  dimensions: DimensionScore[];
  criteria_answered: number;
  criteria_total: number;
};

export type MilestoneStatus = "pending" | "in_progress" | "done" | "skipped";

export type Milestone = {
  id: string;
  order_no: number;
  title: string;
  description: string | null;
  action_items: string[];
  due_date: string | null;
  status: MilestoneStatus;
  completed_at: string | null;
};

export type Roadmap = {
  id: string;
  assessment_id: string;
  status: string;
  title: string;
  summary: string | null;
  generated_by: string;
  generated_at: string;
  milestones: Milestone[];
};

export type AssessmentList = { items: Assessment[] };


export type ConsultationAnswerStatus = "succeeded" | "blocked" | "failed";
export type ConsultationStatus = "pending" | "processing" | "completed" | "failed";
export type FeedbackValue = "helpful" | "not_helpful";

export type ConsultationSource = {
  source_id?: string;
  label?: string;
  [key: string]: unknown;
};

export type ConsultationAnswer = {
  id: string;
  answer: string;
  sources: ConsultationSource[];
  status: ConsultationAnswerStatus;
  model: string;
  prompt_version: string;
  created_at: string;
};

export type Consultation = {
  id: string;
  assessment_id: string;
  question: string;
  status: ConsultationStatus;
  answer: ConsultationAnswer | null;
  feedback: FeedbackValue | null;
  created_at: string;
};

export type ConsultationList = {
  items: Consultation[];
  page: number;
  limit: number;
  total: number;
};
