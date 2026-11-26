# KEBUTUHAN NON-FUNGSIONAL GROWPATH

**Deliverable:** P13-15
**Pemilik:** Moch Haikal Ramadhan
**Disusun oleh:** Tim Growpath P13, 22 November 2026
**Status:** v1.0, target desain. Belum ada pengukuran pada aplikasi.

## 1. Cara membaca

Setiap NFR punya target terukur, cara verifikasi, dan status. Status "target" berarti angka belum diukur. Jangan mengutip angka di dokumen ini sebagai hasil uji.

## 2. Performa

| ID | Kebutuhan | Target | Verifikasi | Status |
|---|---|---|---|---|
| NFR-01 | Respons API baca | p95 di bawah 500 ms pada 50 pengguna bersamaan | Load test staging dengan k6 atau Locust | Target |
| NFR-02 | Respons API tulis | p95 di bawah 800 ms, tidak termasuk panggilan AI | Load test staging | Target |
| NFR-03 | Waktu muat halaman | LCP di bawah 2,5 detik pada 4G, viewport 390px | Lighthouse dan WebPageTest | Target |
| NFR-04 | Interaksi halaman | INP di bawah 200 ms, CLS di bawah 0,1 | Lighthouse dan data lapangan | Target |
| NFR-05 | Waktu jawaban AI | Jawaban lengkap di bawah 15 detik, timeout 20 detik | Uji 20 pertanyaan, catat `latency_ms` | Target |
| NFR-06 | Submit asesmen | Skor selesai di bawah 2 detik untuk 31 jawaban | Uji beban dan unit test | Target |

## 3. Keandalan dan data

| ID | Kebutuhan | Target | Verifikasi | Status |
|---|---|---|---|---|
| NFR-07 | Ketersediaan MVP | 99,5% per bulan, satu region | Monitoring uptime | Target |
| NFR-08 | Backup database | Harian otomatis, retensi 7 hari | Cek jadwal Supabase | Target |
| NFR-09 | RPO | Maksimal 24 jam | Uji restore | Target |
| NFR-10 | RTO | Maksimal 4 jam | Simulasi P15 | Target |
| NFR-11 | Determinisme skor | Input dan versi sama menghasilkan skor identik, 100% | Unit test 3 profil contoh | Target |
| NFR-12 | Integritas transaksi | Submit asesmen atomik: jawaban, skor, segmen, roadmap | Uji rollback saat gagal | Target |
| NFR-13 | Append-only | `progress_log` dan `audit_log` menolak update dan delete | Uji trigger | Target |

## 4. Keamanan dan privasi

| ID | Kebutuhan | Target | Verifikasi | Status |
|---|---|---|---|---|
| NFR-14 | Transport | TLS 1.2 atau lebih baru, HSTS | Uji SSL Labs | Target |
| NFR-15 | Sesi | Access token 1 jam, refresh 7 hari, rotasi refresh | Uji Supabase Auth | Target |
| NFR-16 | Otorisasi | Setiap endpoint memeriksa peran dan kepemilikan | Uji 15 endpoint dengan dua akun | Target |
| NFR-17 | Isolasi tenant | Tidak ada data tenant lain yang terbaca | Uji RLS dan uji API | Target |
| NFR-18 | Rahasia | Tidak ada service role key atau API key di bundle browser | Pemeriksaan build dan grep | Target |
| NFR-19 | Rate limit | 60 per menit per pengguna, 10 konsultasi per hari | Uji 429 | Target |
| NFR-20 | Validasi input | Semua body divalidasi Pydantic dan tipe frontend | Unit test schema | Target |
| NFR-21 | Privasi log AI | Tidak ada nama, WhatsApp, email, atau alamat di prompt dan log | Uji redaksi | Target |
| NFR-22 | Retensi | Audit 24 bulan, asesmen 5 tahun, konsultasi 24 bulan | Jadwal pembersihan | Target |

## 5. Aksesibilitas dan kompatibilitas

| ID | Kebutuhan | Target | Verifikasi | Status |
|---|---|---|---|---|
| NFR-23 | Kontras | Teks normal minimal 4.5:1, teks besar 3:1 | Pemeriksaan token dan audit | Target |
| NFR-24 | Target sentuh | Minimal 44x44 px pada mobile | Inspeksi dan uji perangkat | Target |
| NFR-25 | Keyboard | Seluruh alur utama bisa dipakai tanpa mouse, fokus terlihat | Uji manual | Target |
| NFR-26 | Zoom | Teks dapat diperbesar sampai 200% tanpa kehilangan konten | Uji browser | Target |
| NFR-27 | Pembaca layar | Label, error, dan status diumumkan | Uji NVDA atau VoiceOver | Target |
| NFR-28 | Reflow | Tidak ada horizontal scroll pada 390px dan 320px | Uji viewport | Target |
| NFR-29 | Browser | Chrome, Edge, Firefox, Safari dua versi terakhir | Uji matrix | Target |
| NFR-30 | Perangkat | Android 10+ dan iOS 15+ | Uji perangkat atau emulator | Target |

## 6. Kapasitas dan operasi

| ID | Kebutuhan | Target | Verifikasi | Status |
|---|---|---|---|---|
| NFR-31 | Pengguna terdaftar | 1.000 akun pada MVP | Desain dan load test | Asumsi desain |
| NFR-32 | Pengguna bersamaan | 50 pengguna | Load test | Asumsi desain |
| NFR-33 | Asesmen per tahun | 10.000 asesmen | Perkiraan kapasitas | Asumsi desain |
| NFR-34 | Ukuran database | Di bawah 5 GB pada tahun pertama | Monitoring | Asumsi desain |
| NFR-35 | Observability | Error frontend dan backend masuk Sentry, log punya `trace_id` | Uji error buatan | Target |
| NFR-36 | Waktu deploy | Di bawah 10 menit dari merge ke staging | Catat waktu deploy | Target |

## 7. AI

| ID | Kebutuhan | Target | Verifikasi | Status |
|---|---|---|---|---|
| NFR-37 | Log jawaban | 100% jawaban punya `ai_answer_log` | Uji 20 pertanyaan | Target |
| NFR-38 | Penafian | 100% jawaban menampilkan penafian | Uji UI dan snapshot | Target |
| NFR-39 | Skor oleh AI | 0 perhitungan skor dilakukan model | Pemeriksaan prompt dan kode | Target |
| NFR-40 | Sumber | 0 sitasi yang tidak ada di database | Uji guardrail G-06 | Target |
| NFR-41 | Kuota | 10 konsultasi per pengguna per hari, reset 00.00 Asia/Jakarta | Uji 11 pertanyaan | Target |
| NFR-42 | Penolakan | 100% pertanyaan di luar konteks ditolak dengan kode yang benar | Uji 5 pertanyaan probe | Target |
| NFR-43 | Biaya | Biaya AI tercatat per konsultasi dari `token_count` | Rekap bulanan | Target |

## 8. Pemeliharaan

| ID | Kebutuhan | Target | Verifikasi | Status |
|---|---|---|---|---|
| NFR-44 | Cakupan tes skor | Minimal 90% baris untuk `scoring.py` | Coverage report | Target |
| NFR-45 | CI | Lint, build, dan tes berjalan pada setiap pull request | Status check GitHub | Target |
| NFR-46 | Kontrak API | Tipe frontend dihasilkan dari OpenAPI | Pemeriksaan build | Target |
| NFR-47 | Migrasi | Setiap perubahan skema punya migrasi naik dan turun | Review DDL | Target |
| NFR-48 | Dokumentasi | README lokal bisa diikuti orang baru dalam 30 menit | Uji coba satu anggota | Target |

## 9. Keterbatasan yang diakui

- Tidak ada SLA kepada pengguna pada MVP.
- Satu region, belum multi-region.
- RLS baru target dan belum diuji penuh.
- Belum ada uji penetrasi.
- Angka kapasitas adalah asumsi desain, bukan hasil pengukuran.
- Belum ada uji beban nyata.
- Belum ada pengukuran Core Web Vitals di perangkat pengguna.

## 10. Cara verifikasi di P14 dan P15

1. P14: uji endpoint, uji RLS dengan dua tenant, uji rate limit, ukur p95 dengan data seed.
2. P14: Lighthouse pada Beranda dan Asesmen di 390px dan 1440px.
3. P15: uji restore backup, hitung SUS, uji keyboard dan pembaca layar.
4. P15: rekap biaya AI dari `token_count` dan harga yang berlaku.
5. Semua hasil ditulis di laporan UAT atau bukti QA, bukan di dokumen ini.
