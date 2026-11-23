# Kartu Papan Kerja P13

**Tanggal:** 23 November 2026
**Bentuk:** work board Markdown di repo. Jika GitHub Projects tersedia, kartu ini dapat dipindahkan tanpa mengubah isi.

## 1. Kartu anggota

| ID | Kartu | Pemilik | Lingkup | Bukti atau PR | Status |
|---|---|---|---|---|---|
| WB-01 | Governance, visi, BMC, AI | Ripa Bagaskara | Vision, MoSCoW, DoD, BMC, AI architecture, guardrail, traceability, Gate 1 | PR #11, `00_Vision/`, `01_Business/P13-Business-Model-Canvas.md`, `03_Application/ai/`, `06_Governance/P13-Tim-Charter-Signed.pdf` | Selesai |
| WB-02 | Analisis bisnis dan UX | Mhd Farras Delvioza | Use case, BPMN, user stories, wireframe, high-fidelity | PR #9, `01_Business/`, `03_Application/ux/` | Selesai, desain masuk repo |
| WB-03 | Data dan database | Wisnu Nugroho | ERD, kamus data, DDL, seed, backup, bukti database | PR #15, `02_Data/`, `08_Source/db/`, `07_Evidence/` | Selesai |
| WB-04 | Aplikasi dan repo | Bagas Adinata | Pola aplikasi, struktur folder, branch, login, role, README | PR #14, PR #16, `03_Application/P13-App-Structure.md`, `08_Source/` | Selesai |
| WB-05 | Teknologi dan QA | Moch Haikal Ramadhan | NFR, topologi as-is/target, hosting, deployment, QA | `04_Technology/P13-NFR.md`, `P13-Hosting-Options.md`, `P13-Topology-As-Is.png`, `P13-Topology-Target.png`, `P13-Deployment-Diagram.png` | Selesai, topologi as-is generik |

## 2. Kartu Gate 1

| ID | Kartu | Pemilik | Bukti | Status |
|---|---|---|---|---|
| G1-A | Tanda tangan Tim Charter | Ripa | `06_Governance/P13-Tim-Charter-Signed.pdf` | Terpenuhi 23 November 2026 |
| G1-B | Work board anggota | Ripa | Dokumen ini | Terpenuhi |
| G1-C | Konfirmasi mitra | Ripa | `07_Evidence/P13-Partner-Confirmation.md` | Draf, PR14-01 sebelum P14 |
| G1-D | Review silang use case, ERD, DDL | Ripa, Farras, Wisnu | `07_Evidence/P13-CROSS-REVIEW.md` | Terpenuhi |
| G1-E | Perbaikan Tinjau jawaban | Farras | `03_Application/ux/P13-Tinjau-Fix.md` | Terpenuhi |

## 3. Catatan

- Setiap kartu menautkan artefak atau PR di repo.
- GitHub Projects belum dipakai. Work board ini menjadi bukti yang bisa diperiksa.
- Gate 1 **Hijau**; konfirmasi mitra adalah PR14-01 dan tetap wajib sebelum P14.
- Paket kontribusi P13 Bagas (role-matrix test dan dokumen kontribusi) masih berupa ZIP di workspace dan belum diunggah. PR #14 dan #16 adalah artefak aplikasi yang sudah ada di repo.
