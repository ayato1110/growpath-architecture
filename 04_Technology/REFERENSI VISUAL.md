# REFERENSI VISUAL DAN TEKNIS GROWPATH

Dokumen ini mencatat sumber yang dipakai sebelum menggambar dan menulis desain data, aplikasi, serta API Growpath. Semua tautan dicek pada 10 November 2026.

## Standar arsitektur

| Keperluan | Sumber | Tautan |
|---|---|---|
| TOGAF 10 | The Open Group. (2022). *TOGAF Standard, 10th Edition* | https://publications.opengroup.org/standards/c220 |
| Pengantar TOGAF 10 | The Open Group. *An Introduction to the TOGAF Standard, 10th Edition* | https://pubs.opengroup.org/architecture/w212/ |
| Artefak Phase C | TOGAF 10 Architecture Content, Conceptual Data Diagram, Logical Data Diagram, Data Entity/Business Function Matrix, Application Communication Diagram | https://pubs.opengroup.org/architecture/w212/ |
| ArchiMate 3.2 | The Open Group. (2022). *ArchiMate 3.2 Specification* | https://publications.opengroup.org/archimate-library/c226 |
| BPMN 2.0 | Object Management Group. (2011). *Business Process Model and Notation 2.0* | https://www.omg.org/spec/BPMN/2.0/ |
| Crow's Foot | draw.io. *Crow's foot notation for ER diagrams* | https://www.drawio.com/docs/tutorials/crows-foot-notation/ |
| Crow's Foot, sejarah dan simbol | Redgate. *Crow's Foot Notation* | https://www.red-gate.com/blog/crow-s-foot-notation/ |
| Crow's Foot, cardinality | Aalto University. *Entity-Relationship Diagrams* | https://csfoundations.cs.aalto.fi/en/courses/databases/part-5/7-entity-relationship-diagrams |

## Standar API

| Keperluan | Sumber | Tautan |
|---|---|---|
| OpenAPI 3.1 | OpenAPI Initiative. *OpenAPI Specification 3.1.0* | https://spec.openapis.org/oas/v3.1.0 |
| JSON Schema 2020-12 | JSON Schema. *JSON Schema Specification Draft 2020-12* | https://json-schema.org/draft/2020-12 |
| Format error | RFC 9457. *Problem Details for HTTP APIs* | https://www.rfc-editor.org/rfc/rfc9457 |
| Semantik HTTP | RFC 9110. *HTTP Semantics* | https://www.rfc-editor.org/rfc/rfc9110 |
| OWASP API Security Top 10 2023 | OWASP. *API Security Top 10 2023* | https://owasp.org/API-Security/editions/2023/en/0x00-header/ |
| Rate limit | IETF. *RateLimit header fields for HTTP* | https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/ |

## Implementasi data dan keamanan

| Keperluan | Sumber | Tautan |
|---|---|---|
| Row-level security | PostgreSQL. *Row Security Policies* | https://www.postgresql.org/docs/current/ddl-rowsecurity.html |
| Vektor RAG | pgvector. *Open-source vector similarity search for PostgreSQL* | https://github.com/pgvector/pgvector |
| Autentikasi | Supabase. *Auth* | https://supabase.com/docs/guides/auth |
| RLS Supabase | Supabase. *Row Level Security* | https://supabase.com/docs/guides/database/postgres/row-level-security |
| Embedding | Google. *Gemini API embeddings* | https://ai.google.dev/gemini-api/docs/embeddings |

## Phase D: SSO, API Gateway, dan deployment

| Keperluan | Sumber | Tautan |
|---|---|---|
| TOGAF 10 Phase D | The Open Group. (2022). *TOGAF Standard, 10th Edition*, Phase D Technology Architecture dan Architecture Content | https://publications.opengroup.org/standards/c220 |
| Security dan risiko | The Open Group. (2022). *TOGAF Series Guide: Integrating Risk and Security within a TOGAF Enterprise Architecture* (G152) | https://publications.opengroup.org/guides/togaf/g152 |
| Microservices dan API Gateway | The Open Group. (2022). *TOGAF Series Guide: Microservices Architecture (MSA)* (G21I) | https://publications.opengroup.org/guides/togaf/g21i |
| Federasi identitas dan SSO | NIST. (2025). *SP 800-63C-4: Digital Identity Guidelines: Federation and Assertions* | https://csrc.nist.gov/pubs/sp/800/63/c/4/final |
| OpenID Connect | OpenID Foundation. (2023). *OpenID Connect Core 1.0 incorporating errata set 2* | https://openid.net/specs/openid-connect-core-1_0.html |
| Keamanan microservices | NIST. (2019). *SP 800-204: Security Strategies for Microservices-based Application Systems* | https://csrc.nist.gov/pubs/sp/800/204/final |
| Notasi deployment | Object Management Group. (2017). *OMG Unified Modeling Language (UML) 2.5.1* | https://www.omg.org/spec/UML/2.5.1/ |
| SSO Supabase | Supabase. (2026). *Enterprise Single Sign-On* | https://supabase.com/docs/guides/auth/enterprise-sso |
| Edge security | Cloudflare. (2026). *API Shield* | https://developers.cloudflare.com/api-shield/ |
| Rate limit Cloudflare | Cloudflare. (2026). *Rate limiting rules* | https://developers.cloudflare.com/waf/rate-limiting-rules/ |
| Private networking | Railway. (2026). *Private Networking* | https://docs.railway.com/networking/private-networking |

## Catatan pemakaian

- ERD konseptual dan logical memakai Crow's Foot. Primary key dan foreign key ditulis di dalam entitas. Cardinality ditulis di kedua ujung relasi. Nama relasi memakai kata kerja.
- Diagram modul memakai ArchiMate 3.2 application layer. Setiap komponen menunjukkan tanggung jawab dan dependensi.
- Diagram API memakai ArchiMate 3.2 application layer dan satu sequence diagram untuk alur inti.
- BPMN as-is dan to-be memakai BPMN 2.0. Functional decomposition memakai hierarki fungsi.
- Board Phase D memakai tiga panel: sequence SSO, topologi API Gateway, dan deployment ArchiMate 3.2 Technology Layer.
- Spesifikasi API memakai OpenAPI 3.1.0 dan JSON Schema 2020-12.
- Error API memakai RFC 9457 dengan media type `application/problem+json`.
- Risiko API dipetakan ke OWASP API Security Top 10 2023.
- Semua diagram memakai font minimal 10 pt, judul, legenda, dan ekspor SVG atau PNG 300 dpi.
