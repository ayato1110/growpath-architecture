# TIM CHARTER GROWPATH P13-P16

**Deliverable:** P13-04
**Pemilik:** Ripa Bagaskara
**Disusun oleh:** Tim Growpath P13, 22 November 2026
**Status:** v1.0, tanda tangan anggota menunggu

## 1. Tujuan tim

Menyelesaikan MVP Growpath lima fitur Must dalam empat pertemuan, dengan arsitektur yang bisa dipertanggungjawabkan dan bukti kontribusi setiap anggota.

Ukuran keberhasilan tim bukan jumlah diagram, tetapi:

1. Lima Must berjalan end-to-end.
2. Setiap keputusan bisa dijelaskan alasannya.
3. Setiap anggota punya artefak, commit, atau kartu yang bisa diperiksa.
4. Gate 1, 2, dan 3 dilewati dengan bukti, bukan klaim.

## 2. Anggota dan peran

| Nama | Peran utama | Domain arsitektur | Deliverable utama P13 |
|---|---|---|---|
| Ripa Bagaskara | CEO / Product Owner, AI Engineer | Business, governance, AI | Vision, MoSCoW, DoD, BMC, arsitektur AI, guardrail, entitas log |
| Wisnu Nugroho | Database Architect | Data | ERD 3NF, kamus data, DDL, normalisasi |
| Mhd Farras Delvioza | System Analyst dan UI/UX | Application (kebutuhan) | BPMN, use case, user story, acceptance criteria, skenario UAT |
| Bagas Adinata | Programmer | Application (implementasi) | Pola aplikasi, struktur folder, repo, login dan role |
| Moch Haikal Ramadhan | Network / DevOps | Technology dan security | Topologi, NFR, dua opsi hosting, deployment, checklist keamanan |

Catatan: pada kelompok enam orang, peran AI Engineer dipegang Ripa. QA dan notulen bergilir: P13 Network, P14 CEO, P15 Database, P16 System Analyst. Untuk kelompok enam, QA dan notulen P16 dipegang AI Engineer.

## 3. Hak keputusan

| Keputusan | Pemutus | Wajib konsultasi |
|---|---|---|
| Visi, lingkup MVP, prioritas Must | CEO | Semua anggota |
| Perubahan di luar lima Must | CEO dengan Change Request | Pemilik domain terdampak |
| Skema data dan normalisasi | Database Architect | Programmer, AI Engineer |
| Kontrak API | Programmer | Analyst, AI Engineer |
| Pilihan teknologi dan hosting | Network bersama Programmer | CEO |
| Guardrail dan kuota AI | AI Engineer | CEO, Network |
| Definition of Done | CEO | Semua anggota |

Jika buntu, CEO memutuskan setelah mendengar semua pihak, dan keputusan dicatat di notulen serta `../design/DECISIONS.md`.

## 4. Irama kerja

| Aktivitas | Waktu | Keluaran |
|---|---|---|
| Stand-up | 10 menit di awal sesi | Tiga hal: selesai, berikutnya, hambatan |
| Role clinic | 15 menit | Pertukaran contoh artefak antar kelompok |
| Sprint kerja | 50 sampai 75 menit | Artefak atau kode yang bisa diperiksa |
| Gate | 30 menit | Presenter acak, demo, umpan balik |
| Evaluasi | 10 menit | Catatan perbaikan dan target berikutnya |

## 5. Komunikasi

- WhatsApp untuk koordinasi harian.
- Discord untuk stand-up dan diskusi sprint.
- Respons maksimal dua jam pada hari kerja.
- Keputusan yang mengubah lingkup tidak boleh hanya lewat pesan pribadi. Harus masuk notulen atau Change Request.

## 6. Norma kerja

1. Hadir tepat waktu dan datang dengan progres.
2. Berbicara dengan data, bukan dugaan.
3. Tidak menyalahkan orang, fokus pada masalah dan dampak.
4. Menutup tugas dengan bukti.
5. Meminta review sebelum menyatakan selesai.
6. Menulis asumsi bila data belum ada, bukan mengarang angka.
7. Menjaga satu sumber kebenaran keputusan di `../design/DECISIONS.md`.

## 7. Konflik

Urutan penyelesaian:

1. Bicara langsung berdua, fokus pada perilaku dan dampak.
2. Mediasi CEO, dicatat di notulen.
3. Mediasi dosen.

CEO tidak boleh mengeluarkan anggota. Konflik yang dicatat dan diselesaikan justru menjadi bukti kedewasaan tim.

## 8. Konsekuensi kontribusi

- Anggota tanpa artefak, commit, atau kartu akan mendapat teguran CEO yang dicatat.
- Bila berlanjut, dibawa ke mediasi dosen.
- Peer assessment rahasia pada P16 memakai lima butir: kontribusi, keandalan, kualitas, komunikasi, dan bantuan ke anggota lain.

## 9. Tanda tangan

| Nama | Peran | Tanda tangan | Tanggal |
|---|---|---|---|
| Ripa Bagaskara | CEO / PO / AI Engineer | | |
| Wisnu Nugroho | Database Architect | | |
| Mhd Farras Delvioza | System Analyst dan UI/UX | | |
| Bagas Adinata | Programmer | | |
| Moch Haikal Ramadhan | Network / DevOps | | |

