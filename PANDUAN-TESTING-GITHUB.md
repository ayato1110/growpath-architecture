# Panduan Tes Integrasi GitHub

**Kelompok 6 Growpath**  
**Tes clone, branch, commit, push, pull request, review, dan merge**

Dokumen ini untuk anggota yang **sudah punya akses tulis** ke repositori. Tujuannya agar setiap orang bisa membuktikan bahwa alur GitHub-nya berjalan, bukan hanya clone.

Repositori: <https://github.com/ayato1110/growpath-architecture>

## Prasyarat

- Sudah diundang sebagai collaborator dengan akses `Write`.
- Sudah menerima undangan GitHub.
- Memakai akun GitHub masing-masing, bukan akun Ripa.
- Sudah clone repositori utama, bukan fork.
- Sudah login di GitHub Desktop, VS Code, atau terminal.

Status akses saat ini:

- Farras `farrasdelvioza` sudah punya akses `Write`.
- Wisnu `Wisnucuy` masih menunggu konfirmasi undangan.
- Anggota lain menyusul setelah username dikirim ke Ripa.

## Aturan penting

- Jangan push langsung ke `main` atau `dev`.
- Semua tes dilakukan di branch `test/...`.
- Pull request selalu diarahkan ke `dev`.
- Minimal satu approval. Untuk sementara, reviewer utama adalah Ripa `ayato1110`.
- Jangan memakai file yang sama dengan anggota lain.
- Jangan upload `.env`, token, password, atau data pribadi.
- Setelah tes, simpan tautan pull request sebagai bukti.

## 1. Cek clone dan akun

Masuk ke folder hasil clone, lalu jalankan:

```bash
git remote -v
git config user.name
git config user.email
```

Remote `origin` harus mengarah ke:

```text
https://github.com/ayato1110/growpath-architecture.git
```

Kalau masih mengarah ke fork, clone ulang repositori utama:

```bash
git clone https://github.com/ayato1110/growpath-architecture.git
cd growpath-architecture
```

Atur identitas Git kalau belum:

```bash
git config user.name "Nama Lengkap"
git config user.email "email-github@contoh.com"
```

Gunakan email yang terhubung ke akun GitHub masing-masing.

## 2. Ambil branch dev terbaru

```bash
git checkout dev
git pull origin dev
```

Jangan mulai dari `main` dan jangan push ke `dev`.

## 3. Buat branch tes

Gunakan nama unik. Contoh untuk Farras:

```bash
git checkout -b test/farras-integrasi
```

Contoh untuk anggota lain:

```text
test/wisnu-integrasi
test/bagas-integrasi
test/haikal-integrasi
test/ripa-integrasi
```

## 4. Buat satu file txt

Buat file di folder `07_Evidence` dengan nama unik.

Contoh Farras:

```text
07_Evidence/TEST-INTEGRASI-FARRAS.txt
```

Isi contoh:

```text
Tes integrasi GitHub Kelompok 6.
Nama Mhd Farras Delvioza.
NIM F1E124064.
Tanggal 18 November 2026.
Status Farras berhasil clone, membuat branch, commit, push, dan pull request.
```

Bisa dibuat lewat VS Code, Notepad, atau File Explorer.

## 5. Commit dan push

```bash
git status
git add "07_Evidence/TEST-INTEGRASI-FARRAS.txt"
git commit -m "[Test] Cek integrasi Farras"
git push -u origin test/farras-integrasi
```

Kalau berhasil, terminal akan menampilkan tautan untuk membuat pull request.

## 6. Buat pull request

1. Buka tautan dari terminal atau buka repositori di GitHub.
2. Klik `Compare & pull request`.
3. Pastikan base branch adalah `dev`, bukan `main`.
4. Isi judul, contoh:

```text
[Test][Farras] Cek integrasi GitHub
```

5. Isi deskripsi singkat.
6. Pilih reviewer `ayato1110`.
7. Klik `Create pull request`.
8. Jangan merge sendiri.

## 7. Owner menyetujui dan merge

Ripa sebagai owner:

1. Buka pull request.
2. Cek file, folder, dan commit.
3. Klik `Approve`.
4. Klik `Squash and merge`.
5. Klik `Delete branch`.

Kalau pull request dibuat oleh akun Ripa sendiri, Ripa tidak bisa approve PR sendiri. Minta Farras atau Haikal menjadi approver untuk PR tersebut.

## 8. Tarik hasil merge

Setelah pull request di-merge:

```bash
git checkout dev
git pull origin dev
```

Cek file:

```bash
ls 07_Evidence
```

File `TEST-INTEGRASI-FARRAS.txt` harus muncul.

## 9. Kalau memakai GitHub Desktop

1. Buka repositori di GitHub Desktop.
2. Pilih branch `dev`, lalu `Fetch origin` dan `Pull origin`.
3. Klik `Branch` > `New branch`.
4. Buat branch `test/farras-integrasi`.
5. Klik `Repository` > `Show in Explorer`.
6. Buat file di `07_Evidence`.
7. Buka `Changes`, tulis summary `[Test] Cek integrasi Farras`.
8. Klik `Commit to test/farras-integrasi`.
9. Klik `Push origin`.
10. Klik `Create Pull Request`, pilih base `dev`.
11. Minta Ripa menjadi reviewer.
12. Setelah di-merge, kembali ke `dev` dan `Pull origin`.

## 10. Pembagian file per anggota

| Anggota | Branch | File |
|---|---|---|
| Farras | `test/farras-integrasi` | `07_Evidence/TEST-INTEGRASI-FARRAS.txt` |
| Wisnu | `test/wisnu-integrasi` | `07_Evidence/TEST-INTEGRASI-WISNU.txt` |
| Bagas | `test/bagas-integrasi` | `07_Evidence/TEST-INTEGRASI-BAGAS.txt` |
| Haikal | `test/haikal-integrasi` | `07_Evidence/TEST-INTEGRASI-HAIKAL.txt` |
| Ripa | `test/ripa-integrasi` | `07_Evidence/TEST-INTEGRASI-RIPA.txt` |

Satu orang satu file. Jangan mengubah file anggota lain.

## 11. Cara memastikan semua sudah terintegrasi

Di repo utama:

```bash
git checkout dev
git pull origin dev
ls 07_Evidence
git log --oneline --graph --all --decorate -15
```

Lihat daftar pull request yang sudah merge:

```bash
gh pr list --state merged --limit 20
```

Atau cek lewat GitHub di tab `Pull requests` dengan filter `Closed`.

Indikator berhasil:

- File setiap anggota muncul di `07_Evidence`.
- Commit author sesuai akun masing-masing.
- Pull request tercatat dan di-merge ke `dev`.
- Tidak ada push langsung ke `main` atau `dev`.
- Semua anggota bisa pull dan melihat file yang sama.

## 12. Kalau ada masalah

| Masalah | Solusi |
|---|---|
| `Permission denied` | Pastikan sudah menjadi collaborator dan memakai akun sendiri |
| Tidak bisa push ke `dev` | Memang dilarang. Push ke branch `test/...`, lalu buat PR |
| Pull request tidak bisa merge | Minta approval reviewer. Jangan bypass proteksi |
| File tidak muncul setelah merge | Jalankan `git checkout dev` lalu `git pull origin dev` |
| Konflik | Jangan force push. Pull `dev`, selesaikan konflik, commit, push |
| Salah branch | Pindahkan perubahan ke branch baru sebelum push, lalu minta bantuan |
| Word terkunci | Tutup Word dan hapus file `~$...` |
| Tidak bisa login | Login ulang di GitHub Desktop atau jalankan `gh auth login` |

## 13. Bukti untuk dosen

Simpan:

- Tautan pull request.
- Screenshot halaman `Files changed`.
- Tautan commit.
- Catatan di kartu papan kerja.
- Catatan di notulen.

Jangan hanya mengirim file lewat WhatsApp. Dosen meminta bukti aktivitas di GitHub.

## 14. Setelah tes

File tes boleh tetap disimpan sebagai bukti sampai P13 selesai. Kalau ingin dihapus, hapus lewat pull request baru, jangan langsung ke `main` atau `dev`.

Kalau semua anggota sudah berhasil, berarti alur clone, branch, commit, push, pull request, review, merge, dan pull ulang sudah terintegrasi.
