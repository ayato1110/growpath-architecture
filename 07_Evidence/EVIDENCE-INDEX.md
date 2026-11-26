# Indeks Bukti

| Bukti | Status | Catatan |
|---|---|---|
| Wawancara 40 UMKM | Ada di laporan | Sampel awal, bukan nasional |
| Responden SIGINJAI TERRA 24 | Ada di laporan | Sampel awal |
| Konfirmasi mitra Rumah Setrika | Terkonfirmasi: UAT 5 Desember 2026 pukul 10.00 WIB; pengingat H-1 | `07_Evidence/P14-01/PR14-01-Surat-Konfirmasi-Rumah-Setrika.pdf`, `07_Evidence/P14-01/balasan/2026-11-23-2301-WhatsApp-Rumah-Setrika.png` |
| UAT mitra | Belum | Dijadwalkan P15 |
| SUS | Belum | Dijadwalkan P15 |
| Foto dan rekaman | Belum | Dikumpulkan P15 |
| Login dan role lokal (PR14-06, PR14-07) | Ada, sudah merge | `07_Evidence/PR14-06/` dan `07_Evidence/PR14-06-Login-Role.md` |
| Kontribusi P13 Bagas | Ada, sudah merge | PR #26, `07_Evidence/P13-BAGAS/`, `08_Source/backend/tests/test_roles_matrix.py` |
| Use case dan BPMN P13 | Ada, sudah merge | PR #9, `01_Business/` |
| Governance, BMC, dan AI P13 | Ada, sudah merge | PR #11, `00_Vision/`, `01_Business/P13-Business-Model-Canvas.md`, `03_Application/ai/` |
| Tim Charter bertanda tangan | Selesai, 23 November 2026 | `06_Governance/P13-Tim-Charter-Signed.pdf` |
| Notulen stand-up P13 | Ada | `06_Governance/P13-Notulen-Stand-Up.md` |
| Asumsi 31 kriteria | Ada, belum divalidasi KBUMN | `02_Data/P13-31-Kriteria-Asumsi.md` |
| Kepatuhan P13/PR14 ke skenario dosen | Ada | `07_Evidence/P13-DOSEN-COMPLIANCE.md` |
| Pola aplikasi dan struktur folder | Ada, sudah merge | PR #16, `03_Application/P13-App-Structure.md`, `06_Governance/ADR-002-application-structure.md` |
| Wireframe, high-fidelity, dan Tinjau jawaban | Ada di repo | `03_Application/ux/`, termasuk `P13-Tinjau-Fix.md` |
| Rekaman video prototipe (desktop & mobile) | Menunggu unggah | `07_Evidence/rekaman/` |
| Review silang use case, ERD, DDL | Selesai | `07_Evidence/P13-CROSS-REVIEW.md` |
| Kartu papan kerja P13 | Ada | `07_Evidence/P13-WORK-BOARD.md` |
| NFR, topologi as-is/target, hosting, deployment | Ada di repo | `04_Technology/P13-NFR.md`, `P13-Topology-As-Is.png`, `P13-Topology-Target.png`, `P13-Hosting-Options.md`, `P13-Deployment-Diagram.png` |
| QA teknologi P13 | Ada | `07_Evidence/P13-HAIKAL/P13-HAIKAL-QA.md` |
| Data P13, DDL, seed, RLS | Ada, sudah merge | PR #15, `02_Data/`, `08_Source/db/`, bukti di folder ini |
| Eksekusi DDL PostgreSQL (23 tabel) | Selesai | `08_Source/db/migrations/001_init.sql`, bukti di `07_Evidence/DDL.png` |
| Eksekusi Seed Data (31 kriteria, 30 profil) | Selesai | `08_Source/db/seed/seed.sql`, bukti di `07_Evidence/SEED.png` |
| Verifikasi jumlah baris & skor kosong | Selesai | Bukti di `07_Evidence/Verifikasi Jumlah Baris & Skor Kosong.png` (user=30, umkm_profile=30, assessment=30, assessment_answer=31, criterion=31, skor_terisi=0) |
| Uji trigger append-only (`audit_log`) | Selesai | Bukti di `07_Evidence/Uji Trigger.png` (DELETE ditolak trigger `prevent_mutation`) |
| Uji RLS isolasi Tenant 1 | Selesai | Bukti di `07_Evidence/Uji RLS (Row-Level Security) sebagai Tenant 1 .png` (`profil_terlihat_tenant_1 = 30`) |
| Uji RLS isolasi Tenant 2 | Selesai | Bukti di `07_Evidence/Uji RLS (Row-Level Security) sebagai Tenant 2 .png` (`profil_terlihat_tenant_2 = 0`) |
