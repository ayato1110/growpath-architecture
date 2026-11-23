# SECURITY CHECKLIST GROWPATH

**Deliverable:** checklist keamanan P13
**Pemilik:** Moch Haikal Ramadhan
**Disusun oleh:** Tim Growpath P13, 22 November 2026
**Status:** Desain. Belum ada uji keamanan pada aplikasi.

## 1. Dasar

Checklist ini memakai:

- OWASP API Security Top 10 2023.
- OWASP ASVS Level 1 sebagai subset, bukan sertifikasi.
- Prinsip least privilege, defense in depth, dan gagal tertutup.

Status:

- **Dirancang**: kontrol sudah ditetapkan, belum ada kode.
- **P14**: wajib diterapkan sebelum Gate 2.
- **P15**: wajib diuji sebelum UAT.
- **Target**: praktik baik yang diakui, belum dijadwalkan.

Tidak ada butir yang boleh ditandai lulus tanpa bukti uji.

## 2. Autentikasi dan sesi

| ID | Kontrol | Rencana | Verifikasi | Status |
|---|---|---|---|---|
| SEC-01 | Login melalui Supabase Auth, bukan implementasi sendiri | Email dan kata sandi, reset melalui email | Uji daftar, masuk, keluar, reset | P14 |
| SEC-02 | Access token berumur pendek | 1 jam, refresh 7 hari, rotasi refresh | Inspeksi konfigurasi Supabase | P14 |
| SEC-03 | JWT diverifikasi di backend | Signature, issuer, audience, expiry | Uji token palsu dan kedaluwarsa | P14 |
| SEC-04 | Sesi dihapus dari browser saat keluar | Hapus token dan cookie | Uji keluar lalu buka halaman terproteksi | P14 |
| SEC-05 | Rate limit autentikasi | 5 percobaan per menit per IP | Uji 429 | P14 |
| SEC-06 | Pesan error login tidak membocorkan akun | Pesan umum untuk email atau kata sandi salah | Uji kasus akun tidak ada | P14 |
| SEC-07 | MFA admin | Fase 2, bukan MVP | - | Target |

## 3. Otorisasi dan isolasi tenant

| ID | Kontrol | Rencana | Verifikasi | Status |
|---|---|---|---|---|
| SEC-08 | Setiap endpoint memeriksa peran | Middleware FastAPI | Uji 15 endpoint dengan peran berbeda | P14 |
| SEC-09 | Setiap endpoint memeriksa kepemilikan sumber daya | Query selalu menyertakan `user_id` dan `tenant_id` | Uji dua akun, akses silang harus 403 atau 404 | P14 |
| SEC-10 | `tenant_id` dari JWT | Body yang memuat `tenant_id` diabaikan | Uji body berisi tenant lain | P14 |
| SEC-11 | RLS pada tabel berisiko tinggi | 10 tabel di `../08_Source/db/migrations/001_init.sql` | Uji dengan `SET LOCAL app.tenant_id` | P14 |
| SEC-12 | Service role tidak pernah ke browser | Hanya di backend | Grep bundle dan environment | P14 |
| SEC-13 | Admin platform tidak tampil di UI MVP | Endpoint admin tidak diaktifkan | Inspeksi route | P14 |
| SEC-14 | Prinsip least privilege database | Role aplikasi tanpa DDL | Inspeksi grant | P15 |

## 4. Data dan privasi

| ID | Kontrol | Rencana | Verifikasi | Status |
|---|---|---|---|---|
| SEC-15 | Tidak ada data pribadi di prompt AI | Nama, WhatsApp, email, alamat tidak dikirim | Uji log dan payload | P14 |
| SEC-16 | Redaksi sebelum simpan log | Nomor telepon, email, NIK, rekening | Uji dengan pertanyaan berisi data pribadi | P14 |
| SEC-17 | Retensi data | Audit 24 bulan, konsultasi 24 bulan, asesmen 5 tahun | Cek jadwal pembersihan | P15 |
| SEC-18 | Hak hapus dan anonimisasi | Anonimisasi 90 hari setelah permintaan | Uji prosedur manual | Target |
| SEC-19 | Backup terenkripsi | Sesuai penyedia, TLS dan at-rest | Konfirmasi dokumentasi vendor | P15 |
| SEC-20 | Data seed bukan data nyata | Domain `.invalid`, nama sintetis | Review `../08_Source/db/seed/seed.sql` | Selesai |
| SEC-21 | Log tidak menyimpan prompt penuh | Simpan versi prompt dan ringkasan konteks | Inspeksi schema | P14 |

## 5. API dan validasi

| ID | Kontrol | Rencana | Verifikasi | Status |
|---|---|---|---|---|
| SEC-22 | Validasi input di server | Pydantic v2 untuk semua body dan query | Uji nilai ekstrem dan tipe salah | P14 |
| SEC-23 | Validasi input di klien | Tipe, panjang, dan format | Uji form | P14 |
| SEC-24 | Query parameterized | ORM atau driver, tanpa string SQL | Code review | P14 |
| SEC-25 | Cegah XSS | React escaping, tanpa `dangerouslySetInnerHTML` pada input pengguna | Code review dan uji payload | P14 |
| SEC-26 | CORS terbatas | Hanya domain aplikasi | Uji origin lain | P14 |
| SEC-27 | Security headers | CSP, HSTS, X-Content-Type-Options, Referrer-Policy, frame-ancestors | Uji header respons | P14 |
| SEC-28 | Error tidak membocorkan stack | Problem details tanpa stack trace | Uji error produksi | P14 |
| SEC-29 | Rate limit umum | 60 per menit per pengguna | Uji 429 | P14 |
| SEC-30 | Batas ukuran body | Maksimal 1 MB, pertanyaan 1000 karakter | Uji body besar | P14 |
| SEC-31 | Tidak ada unggah file pada MVP | Storage belum dipakai | Inspeksi route | P14 |
| SEC-32 | Idempotency untuk mutasi rawan ganda | Kunci opsional pada submit dan konsultasi | Uji klik ganda | P15 |

## 6. AI

| ID | Kontrol | Rencana | Verifikasi | Status |
|---|---|---|---|---|
| SEC-33 | Model AI hanya dari backend | Kunci di server | Grep dan uji jaringan | P14 |
| SEC-34 | Prompt injection diabaikan | Instruksi pengguna tidak mengubah aturan | Uji T-05 | P14 |
| SEC-35 | Sumber tidak boleh dikarang | Validasi `used_source_ids` terhadap konteks | Uji guardrail G-06 | P14 |
| SEC-36 | Penafian wajib | Tampil di setiap jawaban | Snapshot UI | P14 |
| SEC-37 | Kuota harian | 10 per pengguna | Uji 11 pertanyaan | P14 |
| SEC-38 | Timeout dan retry terbatas | 20 detik, satu retry | Uji model lambat | P14 |
| SEC-39 | Log setiap panggilan | `ai_answer_log` | Uji 20 pertanyaan | P14 |
| SEC-40 | Konten tidak dipakai pelatihan | Paket API berbayar | Konfirmasi terms | P15 |

## 7. Infrastruktur dan operasi

| ID | Kontrol | Rencana | Verifikasi | Status |
|---|---|---|---|---|
| SEC-41 | TLS dan HSTS | Cloudflare dan Railway | SSL Labs | P15 |
| SEC-42 | Rahasia di secret manager | Railway dan Supabase, bukan repo | Scan repo | P14 |
| SEC-43 | `.env` tidak di-commit | `.gitignore` dan pemeriksaan PR | Scan riwayat | P14 |
| SEC-44 | Dependency scanning | Dependabot atau `npm audit` dan `pip-audit` | Jadwal mingguan | P15 |
| SEC-45 | Debug mode mati di produksi | `APP_ENV=production` | Uji error | P14 |
| SEC-46 | Backup dan restore | Harian, uji restore P15 | Simulasi | P15 |
| SEC-47 | Monitoring error | Sentry frontend dan backend | Uji error buatan | P14 |
| SEC-48 | Audit log append-only | Trigger database | Uji update dan delete | P14 |
| SEC-49 | Akses staging dibatasi | Basic auth atau allowlist | Uji akses luar | P15 |

## 8. SDLC dan bukti

| ID | Kontrol | Rencana | Verifikasi | Status |
|---|---|---|---|---|
| SEC-50 | Branch protection | PR, review, code owner | Inspeksi GitHub | Selesai |
| SEC-51 | Review keamanan pada PR yang menyentuh auth, data, AI | Checklist PR | Sampel 3 PR | P14 |
| SEC-52 | Tidak ada kredensial di artefak laporan | Screenshot dan dokumen | Review bukti | P15 |
| SEC-53 | Uji akses silang dua akun | Dua tenant dan dua pengguna | Hasil uji | P14 |
| SEC-54 | Uji OWASP API Top 10 | Fokus BOLA, broken auth, rate limit, mass assignment | Laporan uji | P15 |

## 9. Risiko yang belum tertutup

- Belum ada uji penetrasi.
- Belum ada WAF berbayar.
- Belum ada MFA untuk admin.
- Belum ada enkripsi kolom tambahan di luar enkripsi penyedia.
- Belum ada pelatihan keamanan tim.
- RLS belum diuji pada semua kombinasi query.
- Belum ada rencana insiden dan kontak darurat.
- Kepatuhan UU PDP belum dinilai secara formal.

## 10. Bukti yang harus dikumpulkan

1. Screenshot pengaturan branch protection.
2. Hasil uji dua akun pada 15 endpoint.
3. Hasil uji 429 untuk kuota dan rate limit.
4. Hasil uji token palsu dan kedaluwarsa.
5. Hasil scan rahasia pada repo.
6. Hasil uji restore backup.
7. Hasil uji prompt injection dan pertanyaan di luar konteks.
8. Header keamanan dari respons produksi.

Tanpa bukti di atas, checklist ini tetap berstatus desain.
