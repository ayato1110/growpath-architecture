# Panduan Kontribusi Growpath

Panduan ini untuk semua anggota Kelompok 6. Tujuannya agar setiap update dari masing-masing peran masuk melalui GitHub dan bisa dilacak lewat commit, pull request, review, dan kartu papan kerja.

Repositori: <https://github.com/ayato1110/growpath-architecture>

## Aturan utama

- Jangan push langsung ke `main` atau `dev`.
- `main` adalah versi stabil untuk gate, demo, dan submission.
- `dev` adalah tempat integrasi hasil kerja harian.
- Setiap update dibuat di branch `feature/...`, lalu masuk ke `dev` lewat pull request.
- Minimal satu anggota lain menjadi reviewer.
- Satu pull request untuk satu topik. Jangan campur data, aplikasi, dan desain dalam satu PR.
- Jangan pernah upload `.env`, token, password, API key, atau data pribadi mentah.
- Setiap PR harus menyebut peran, folder, perubahan, dan bukti berupa kartu atau tautan.

## 1. Akses awal

### Untuk pemilik repo

1. Buka `Settings` > `Collaborators` > `Add people`.
2. Masukkan username GitHub masing-masing anggota.
3. Pilih role `Write`.
4. Kirim undangan.

Kalau anggota belum menjadi collaborator, mereka tetap bisa memakai cara fork. Namun untuk kerja tim, collaborator lebih mudah karena bisa langsung membuat branch di repo utama.

### Untuk anggota

1. Pakai akun GitHub masing-masing. Jangan memakai akun pemilik repo.
2. Terima undangan collaborator lewat email atau notifikasi GitHub.
3. Install GitHub Desktop atau VS Code.
4. Install Git bila memakai terminal.
5. Atur nama dan email Git:

```bash
git config --global user.name "Nama Lengkap"
git config --global user.email "email@contoh.com"
```

## 2. Clone repo

### Jalur GitHub Desktop, paling mudah

1. Buka GitHub Desktop.
2. Pilih `File` > `Clone repository`.
3. Pilih tab `URL`.
4. Masukkan `https://github.com/ayato1110/growpath-architecture.git`.
5. Tentukan folder lokal, misalnya `D:\Growpath-Architecture`.
6. Klik `Clone`.

### Jalur terminal

```bash
git clone https://github.com/ayato1110/growpath-architecture.git
cd growpath-architecture
git checkout dev
git pull origin dev
```

## 3. Alur wajib setiap update

Alur ini dipakai untuk semua peran.

1. Pastikan branch `dev` sudah paling baru.
2. Buat branch baru dari `dev`.
3. Tambah atau ubah file di folder peran.
4. Commit dengan pesan yang jelas.
5. Push branch ke GitHub.
6. Buat pull request ke `dev`.
7. Minta reviewer.
8. Setelah disetujui, merge.
9. Hapus branch fitur.
10. Kembali ke `dev` dan pull lagi.

### GitHub Desktop, langkah demi langkah

1. Buka repo Growpath di GitHub Desktop.
2. Klik `Current branch` lalu pilih `dev`.
3. Klik `Fetch origin`, lalu `Pull origin` bila ada update.
4. Klik `Branch` > `New branch`.
5. Beri nama branch, contoh `feature/data-wisnu-p13`.
6. Klik `Create branch`.
7. Buka folder repo lewat `Repository` > `Show in Explorer`.
8. Tambah atau ubah file di folder yang sesuai.
9. Kembali ke GitHub Desktop, buka tab `Changes`.
10. Periksa file yang berubah. Pastikan tidak ada file sementara seperti `~$nama.docx`.
11. Tulis summary, contoh `[Data] Tambah ERD logis P13`.
12. Klik `Commit to feature/data-wisnu-p13`.
13. Klik `Push origin`.
14. Klik `Create Pull Request`.
15. Pastikan base branch adalah `dev`, bukan `main`.
16. Isi judul dan deskripsi, lalu klik `Create pull request`.
17. Minta reviewer lewat WhatsApp atau Discord.
18. Setelah disetujui, klik `Squash and merge` atau `Merge pull request`.
19. Klik `Delete branch`.
20. Kembali ke `dev`, klik `Pull origin`, lalu buat branch baru untuk tugas berikutnya.

### GitHub web, untuk file Markdown atau upload file

1. Buka repo di browser.
2. Ganti branch ke `dev`.
3. Klik branch dropdown, ketik nama branch baru, lalu `Create branch`.
4. Untuk Markdown, klik file, klik ikon pensil, edit, lalu commit ke branch baru.
5. Untuk DOCX, PNG, atau file lain, klik `Add file` > `Upload files`, lalu commit ke branch baru.
6. Setelah commit, klik `Compare & pull request`.
7. Base branch harus `dev`.
8. Isi deskripsi dan buat PR.

Jangan mengedit DOCX langsung di browser. Upload file hasil Word yang sudah ditutup.

### Terminal, alternatif

```bash
git checkout dev
git pull origin dev
git checkout -b feature/data-wisnu-p13

# tambah atau ubah file di folder yang benar
git status
git add "02_Data/Nama-File.png"
git commit -m "[Data] Tambah ERD logis P13"
git push -u origin feature/data-wisnu-p13
```

Setelah push, buka tautan yang muncul di terminal untuk membuat pull request. Kalau memakai GitHub CLI:

```bash
gh pr create --base dev --head feature/data-wisnu-p13 \
  --title "[Data][Wisnu] ERD logis P13" \
  --body "Menambahkan ERD logis dan catatan relasi."
```

## 4. Folder untuk masing-masing peran

| Peran | Folder utama | Contoh update | Reviewer disarankan |
|---|---|---|---|
| Ripa, CEO/Product Owner dan AI Engineer | `00_Vision`, `03_Application`, `05_Opportunities`, `06_Governance`, `09_Pitch` | Visi v1.0, arsitektur AI, ADR, pitch | Farras atau Haikal |
| Farras, System Analyst dan UI/UX | `01_Business`, `03_Application`, `07_Evidence` | BPMN, use case, user story, wireframe, rencana UAT | Ripa |
| Wisnu, Database Architect | `02_Data`, `03_Application`, `06_Governance` | ERD, kamus data, DDL, catatan backend | Bagas atau Ripa |
| Bagas, Programmer | `08_Source`, `03_Application`, `06_Governance` | Kode, endpoint, README, changelog | Wisnu atau Ripa |
| Haikal, Network/DevOps | `04_Technology`, `07_Evidence`, `06_Governance` | Topologi, deployment, keamanan, bukti UAT | Bagas atau Ripa |

Boleh menyentuh folder lain bila memang terkait. Jelaskan alasannya di PR dan pilih reviewer yang relevan.

## 5. Penamaan file

- Untuk memperbarui file yang sudah ada, pakai nama file yang sama agar tautan tidak putus.
- Untuk file baru, gunakan pola `P13-Topik-Peran-v01.ext`.
- Contoh `P13-ERD-Logis-Wisnu-v01.png`.
- Contoh `P13-Skenario-UAT-Haikal-v01.md`.
- Contoh `P14-Endpoint-Login-Bagas-v01.md`.
- Untuk diagram, simpan file sumber `.drawio` dan hasil `.png` sekaligus.
- Jangan memakai nama `final-final`, `baru`, atau `fixbanget`.

## 6. Format commit

Gunakan awalan folder atau peran agar mudah dicari.

```text
[Vision] Perbarui ringkasan visi P13
[Business] Perbarui BPMN to-be
[Data] Tambah ERD logis P13
[App] Perbaiki kontrak endpoint login
[Tech] Perbarui topologi deployment
[Governance] Catat permintaan perubahan
[Evidence] Tambah rencana UAT
[Source] Tambah modul login
[Pitch] Perbarui slide masalah
```

Hindari pesan seperti `update`, `fix`, atau `baru` tanpa penjelasan.

## 7. Aturan pull request

- Base branch selalu `dev`.
- Judul memakai pola `[Folder][Nama] Topik`, contoh `[Data][Wisnu] ERD logis P13`.
- Isi template PR yang sudah disediakan.
- Sertakan tautan kartu papan kerja atau issue.
- Sertakan bukti berupa screenshot, file, atau tautan.
- Minta minimal satu reviewer.
- Jangan merge PR sendiri tanpa review.
- Setelah merge, hapus branch fitur.

### Pembagian review

- Perubahan visi, governance, dan pitch direview Ripa, lalu Farras atau Haikal.
- Perubahan bisnis dan UX direview Farras, lalu Ripa.
- Perubahan data dan backend direview Wisnu, lalu Bagas atau Ripa.
- Perubahan aplikasi dan source code direview Bagas, lalu Wisnu atau Ripa.
- Perubahan teknologi dan keamanan direview Haikal, lalu Bagas atau Ripa.
- Perubahan bukti UAT direview Haikal atau Farras, lalu Ripa.

## 8. Sinkronisasi dan konflik

Sebelum mulai kerja:

```bash
git checkout dev
git pull origin dev
git checkout -b feature/nama-peran-topik
```

Kalau branch sudah lama dan PR tertinggal:

1. Buka PR di GitHub.
2. Klik `Update branch` bila tombol tersedia.
3. Atau di terminal:

```bash
git checkout feature/nama-peran-topik
git pull origin dev
```

Kalau ada konflik:

1. Jangan force push.
2. Buka file yang konflik.
3. Pilih isi yang benar, lalu simpan.
4. Jalankan `git add`, `git commit`, dan `git push`.
5. Kalau ragu, minta Ripa atau reviewer membantu.

## 9. Aturan file dan keamanan

- Jangan upload `.env`, password, token, API key, atau sertifikat.
- Gunakan `.env.example` untuk contoh konfigurasi.
- Jangan upload data pribadi mentah. Anonimkan nama, nomor telepon, alamat, dan email.
- Repositori ini public, jadi semua file bisa dibaca orang lain.
- Kompres gambar sebelum upload. File besar memperlambat clone.
- Jangan upload file sementara Word seperti `~$notulensi.docx`.
- Jangan mengganti nama file utama tanpa catatan di PR.
- Jangan menghapus file orang lain tanpa persetujuan pemilik file.

## 10. Kalau ada masalah

| Masalah | Solusi |
|---|---|
| Tidak bisa push | Pastikan sudah menjadi collaborator dan memakai akun sendiri |
| `Permission denied` | Terima undangan collaborator atau minta akses `Write` |
| `Protected branch` | Jangan push ke `main` atau `dev`. Buat branch dan PR |
| PR tertinggal | Klik `Update branch` atau pull `dev` ke branch fitur |
| Konflik | Selesaikan manual, commit, push. Jangan force push |
| File terlalu besar | Kompres gambar atau pecah file |
| File Word terkunci | Tutup Word, hapus file `~$...`, lalu commit ulang |
| Salah branch | Pindahkan perubahan ke branch baru sebelum push, lalu minta bantuan owner |

## 11. Checklist sebelum minta review

- [ ] Branch dibuat dari `dev` terbaru.
- [ ] File berada di folder yang benar.
- [ ] Tidak ada `.env`, token, password, atau data pribadi.
- [ ] Tidak ada file sementara `~$...`.
- [ ] Commit memakai awalan folder atau peran.
- [ ] PR mengarah ke `dev`, bukan `main`.
- [ ] Deskripsi PR menjelaskan perubahan.
- [ ] Tautan kartu papan kerja atau issue sudah dicantumkan.
- [ ] Reviewer sudah diminta.
- [ ] Bukti berupa screenshot atau file sudah dilampirkan.

## 12. Bukti untuk dosen

Setiap update sebaiknya meninggalkan jejak berikut.

- Commit di branch fitur.
- Pull request ke `dev`.
- Review dan komentar dari anggota lain.
- File atau artefak yang berubah.
- Tautan kartu papan kerja.
- Catatan di notulen.

Simpan tautan PR di kartu papan kerja dan notulen. Jangan hanya mengirim file lewat WhatsApp karena dosen meminta bukti aktivitas di GitHub.

## 13. Pengaturan branch protection untuk pemilik repo

Agar aturan benar-benar berjalan:

1. Buka `Settings` > `Branches`.
2. Klik `Add branch protection rule`.
3. Isi branch name pattern `main`.
4. Aktifkan `Require a pull request before merging`.
5. Aktifkan `Require approvals` minimal 1.
6. Aktifkan `Do not allow force pushes`.
7. Simpan.
8. Ulangi untuk branch `dev`.

Dengan pengaturan ini, anggota tidak bisa push langsung ke `main` atau `dev`.

## 14. Ringkasan cepat

```text
Pull dev
Buat branch feature/...
Tambah file di folder peran
Commit dengan awalan [Peran]
Push
Buat PR ke dev
Minta reviewer
Merge
Hapus branch
Pull dev lagi
```

Kalau bingung, tanyakan di Discord tim sebelum memaksa push. Jangan gunakan `git push --force` ke `main` atau `dev`.
