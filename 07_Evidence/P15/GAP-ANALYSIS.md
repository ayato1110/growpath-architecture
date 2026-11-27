# P15 · Gap Analysis per Domain

**Tanggal:** 27 November 2026  
**Posisi:** akhir P14, sebelum PR15 dan P15  
**Sumber acuan:** Vision v1.0, PRD, TRD, ERD 3NF, OpenAPI, ADR-001, dan hasil P14.

## Ringkasan

P14 menyelesaikan dua dari lima Must: **data usaha** dan **rekomendasi**. Skor deterministik, segmen, dan tiga langkah prioritas sudah berjalan di Supabase. Gap terbesar ada di tiga Must yang belum dibangun, staging yang belum deploy, dan bukti UAT yang belum dijalankan.

## 1. Business architecture

| Target | Kondisi 27 November 2026 | Gap | Aksi | Pemilik |
|---|---|---|---|---|
| Lima Must berjalan | Dua Must berjalan: data usaha, rekomendasi | Konsultasi AI, log jawaban, dashboard | Bangun Must 2, 4, 5 sebelum P15 | Bagas, Ripa |
| Tiga KPI Vision terukur | Belum ada pengukuran | Baseline KPI belum diambil | Ukur saat UAT: penyelesaian asesmen, waktu, pemahaman langkah | Ripa |
| Model B2G jelas | BMC ada, harga belum ditetapkan | Harga dan paket masih asumsi | Finalkan di P15/P16 | Ripa |
| Mitra UAT terkonfirmasi | Rumah Setrika, 5 Desember 2026, 10.00 WIB | Pengingat H-1 dan daftar hadir | Kirim pengingat, siapkan berkas UAT | Ripa |
| Change Request dari Kartu Kejutan | Belum ada | CR baru muncul di kelas | Catat dan analisis saat kelas | Ripa |

## 2. Data architecture

| Target | Kondisi | Gap | Aksi | Pemilik |
|---|---|---|---|---|
| 23 entitas, 31 kriteria, 4 segmen | Terpasang di Supabase, terverifikasi | Tidak ada | Jaga migrasi | Wisnu |
| PK, FK, unique, check, index | 126 PK, 68 FK, 73 unique, 97 check, 56 index | Tidak ada | Lampirkan bukti | Wisnu |
| View laporan | `v_assessment_report` aktif | Belum dipakai di UI | Pakai untuk dashboard P15 | Wisnu |
| Backup dan restore terbukti | Drill logical copy 23 tabel, 250 baris, 0 selisih | `pg_dump` belum tersedia; restore penuh belum diuji | Uji `pg_dump`/restore penuh sebelum P15 | Wisnu |
| Transaksi proses kritis | Submit asesmen sudah satu transaksi | Perlu uji kegagalan di tengah | Tambah tes rollback | Bagas |
| Pemisahan data uji dan produksi | Seed P13 dan data uji ada di database staging | Belum ada kebijakan retensi | Bersihkan data uji sebelum demo, catat asal data | Wisnu |
| RLS | Aktif di DDL, backend memakai role owner | RLS belum diuji dari role terbatas | Uji role aplikasi terbatas di P15 | Wisnu, Haikal |

## 3. Application architecture

| Target | Kondisi | Gap | Aksi | Pemilik |
|---|---|---|---|---|
| Kontrak 15 endpoint | 11 endpoint aktif; OpenAPI sudah diselaraskan | Endpoint konsultasi, log, dashboard belum | Tambah endpoint Must 2, 4, 5 | Bagas |
| Must 1 data usaha | Selesai, tervalidasi | Tidak ada | Jaga tes | Bagas |
| Must 3 rekomendasi | Selesai, deterministik | Baru 12 dari 31 kriteria | Lengkapi 31 kriteria | Bagas, Farras |
| Must 2 konsultasi AI | Belum | Butuh DeepSeek, guardrail, kuota, penafian | Bangun `services/ai.py` dan endpoint | Ripa, Bagas |
| Must 4 log jawaban | Belum | Butuh `Consultation`, `AIAnswerLog`, halaman log | Bangun setelah Must 2 | Bagas |
| Must 5 dashboard | Belum | Butuh ringkasan skor, progres, langkah berikutnya | Bangun P15 | Farras |
| Validasi dan error state | Ada di profil dan asesmen | Belum diuji untuk konsultasi | Tambah tes | Bagas |
| Dokumentasi route | OpenAPI dan README diperbarui | Belum ada daftar route per role | Tulis `docs/routes.md` | Bagas |

## 4. Technology architecture

| Target | Kondisi | Gap | Aksi | Pemilik |
|---|---|---|---|---|
| Staging Vercel + Render + Supabase | Supabase aktif; frontend dan backend baru lokal | Staging belum ada | Deploy Render dan Vercel | Haikal |
| ADR tech stack | Accepted 27 November 2026 | Tidak ada | Jaga keputusan | Ripa |
| Topologi dan deployment diagram | Dokumen staging ada; diagram P13 memakai label Singapura | Region database Seoul | Perbarui diagram atau beri catatan | Haikal |
| Keamanan staging | Checklist ada; CORS belum diisi untuk domain Vercel | Deploy belum | Isi env dan uji HTTPS | Haikal |
| Observability | Sentry belum dipasang | Belum ada error tracking | Pasang Sentry saat staging | Haikal |
| TCO 12 bulan | Belum | Belum ada angka | Susun estimasi Render, Vercel, Supabase, DeepSeek | Haikal |
| Kinerja | Belum diukur | LCP, waktu submit, latensi DB belum ada | Ukur saat staging | Haikal |

## 5. People dan process

| Target | Kondisi | Gap | Aksi | Pemilik |
|---|---|---|---|---|
| Setiap anggota berkontribusi | Audit kontribusi lulus | PR P14 belum diunggah per role | Distribusikan paket role dan merge berurutan | Ripa |
| Review pull request | Aturan CODEOWNERS ada | PR P14 belum dibuat | Satu PR per role, review Ripa | Semua |
| UAT dan SUS | Jadwal ada, belum dijalankan | Skenario dan kuesioner belum ada | Pakai `UAT-PLAN.md` dan `SUS-KUESIONER.md` | Farras |
| Notulen dan bukti | Notulen P13 ada | Notulen P15 belum | Catat saat UAT | Haikal |

## Urutan kerja PR15

| Prioritas | Pekerjaan | Alasan |
|---:|---|---|
| P0 | Deploy staging Render + Vercel | Syarat Gate 2 dan P15 |
| P0 | Gap analysis ini disetujui tim | Acuan PR15 |
| P0 | Skenario UAT + SUS siap | UAT 5 Desember |
| P0 | Backup restore drill | Drill logical lulus; uji `pg_dump` menyusul |
| P1 | Must 2 dan 4: konsultasi AI + log | Dua Must tersisa |
| P1 | Transaksi submit asesmen | Mencegah data setengah jadi |
| P1 | TCO 12 bulan | Syarat PR15 |
| P2 | Dashboard Must 5 | P15 |
| P2 | Lengkapi 31 kriteria | P15 |
| P3 | Sentry, domain, polish | P16 |

## Yang tidak boleh dilakukan

- Menambah Must keenam.
- Memakai AI untuk menghitung skor.
- Mengklaim UAT atau SUS sebelum dijalankan.
- Menjalankan `001_init.sql` di database berisi data tanpa backup.
