# PR14-06 Login dan Role Lokal

**Deliverable:** PR14-06 Aplikasi lokal login dan role, PR14-07 README cara menjalankan
**Pemilik:** Bagas
**Disusun oleh:** Sesi implementasi P14, 23 November 2026
**Status:** Ada, menunggu review
**Pull request:** https://github.com/ayato1110/growpath-architecture/pull/14

## Lingkup

Bukti ini hanya mencakup dua hal: aplikasi lokal dengan login, role `umkm`, route `/app` terlindungi, dan README cara menjalankan. Semua uji dijalankan pada mode `AUTH_MODE=local` karena tidak ada kredensial Supabase di mesin ini. Jalur Supabase ada di kode tetapi belum dijalankan.

## Perintah dan hasil

| Perintah | Hasil |
|---|---|
| `.venv\Scripts\python -m pytest -q` di `08_Source/backend` | 23 passed |
| `.venv\Scripts\python -m ruff check .` di `08_Source/backend` | All checks passed |
| `npm run lint` di `08_Source/frontend` | 0 error, 0 warning |
| `npm run build` di `08_Source/frontend` | Build sukses, rute `/`, `/app`, `/login`, `/api/login`, `/api/logout` |
| `curl -I http://localhost:3000/app` | CSP, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, dan `Referrer-Policy` ada, `X-Powered-By` tidak ada |
| `curl http://127.0.0.1:8000/health` | `{"status":"ok","version":"0.1.0","dependencies":{"auth":"local"}}` |
| `curl -i http://127.0.0.1:8000/auth/me` tanpa token | 401, `content-type: application/problem+json`, `code: AUTH_TOKEN_MISSING` |
| `POST /auth/login` dengan akun uji | 200, `token_type: Bearer`, `expires_in: 3600`, `user.role: umkm` |
| `POST /auth/login` untuk lima akun lokal | 200 semua, `user.role` sesuai akun: `umkm`, `pendamping`, `mentor`, `admin_b2g`, `admin_platform` |
| `POST /auth/login` dengan kata sandi salah | 401 `AUTH_INVALID_CREDENTIALS` |
| `GET /auth/me` dengan Bearer token | 200, `email`, `tenant_id`, dan `role` akun uji |

## Alur yang diuji di browser

1. Buka `/app` tanpa sesi. Dialihkan ke `/login`.
2. Masuk dengan email dan kata sandi akun uji. Sampai di `/app`, tampil email, peran UMKM, dan tenant.
3. Tekan Keluar. Kembali ke `/login`.
4. Buka `/app` lagi. Dialihkan ke `/login`, jadi route benar-benar terlindungi.
5. `document.cookie` kosong setelah login, karena token disimpan di cookie `httpOnly`.
6. Pada lebar 390, `scrollWidth` sama dengan `clientWidth`, jadi tidak ada geser horizontal.
7. Backend dimatikan, `/app` menampilkan "Sesi tidak dapat diperiksa" tanpa menghapus cookie. Setelah backend menyala, tautan Coba lagi mengembalikan akun.
8. Konfigurasi yang salah menolak start. `AUTH_MODE=supabase` tanpa `SUPABASE_URL`, tenant bukan UUID, dan peran di luar daftar semuanya gagal dengan pesan yang menyebut variabelnya.
9. Login `mentor@growpath.id` sampai di `/app` dengan label peran Mentor, dan `/auth/me` mengembalikan role `mentor`. Kelima akun lokal diuji dengan cara yang sama.

## Screenshot

| File | Isi | Yang dibuktikan |
|---|---|---|
| `07_Evidence/PR14-06/login-1440.png` | Halaman Masuk, desktop 1440 | Form tampil dengan token DESIGN.md, hasil redirect dari `/app` tanpa sesi |
| `07_Evidence/PR14-06/app-1440.png` | Halaman `/app`, desktop 1440 | Sesi aktif, email dan peran UMKM tampil, tombol Keluar tersedia |
| `07_Evidence/PR14-06/login-390.png` | Halaman Masuk, mobile 390 | Layout mobile sendiri, input dan tombol penuh selebar kartu |
| `07_Evidence/PR14-06/app-390.png` | Halaman `/app`, mobile 390 | Data akun terbaca di 390 tanpa geser horizontal |

Screenshot diambil dari `npm run start` dengan hasil `npm run build`, bukan dari dev server, supaya penanda dev Next.js tidak ikut tampil.

## Batas dan hal yang belum diklaim

- Mode local belum diuji dengan Supabase. Jalur `AUTH_MODE=supabase` belum dijalankan sama sekali.
- Logout hanya menghapus cookie. Pencabutan refresh token Supabase belum ada.
- Belum ada tes frontend otomatis. TRD menyebut Vitest dan Playwright, keduanya masuk bersama alur asesmen.
- Belum ada UAT mitra, belum ada SUS, dan belum ada pengukuran waktu atau tingkat keberhasilan tugas.
- Tidak ada dashboard, data usaha, asesmen, skor, konsultasi, AI, atau log di bukti ini.
