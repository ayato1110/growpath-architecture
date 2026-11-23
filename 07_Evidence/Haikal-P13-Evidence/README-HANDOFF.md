# Handoff ZIP untuk Haikal

Paket ini untuk diunggah ke GitHub lewat web, atas nama akun `aakaasiaaa-cyber`.

Jangan upload ZIP ini ke repo. Extract dulu.

## Isi

```text
07_Evidence/P13-HAIKAL/
  README.md
  P13-HAIKAL-QA.md
  P13-NFR-Test-Plan.md
  P13-NFR.md
  P13-Hosting-Options.md
  P13-Security-Checklist.md
  P13-Topology-As-Is.png
  P13-Topology-Target.png
  P13-Deployment-Diagram.png
  P13-Topology-Deployment.drawio
```

Semua file berada di folder evidence. File kanonik di `04_Technology/` tidak ditimpa.

## Cara upload lewat GitHub web

1. Buka `https://github.com/ayato1110/growpath-architecture`.
2. Pilih branch `dev`.
3. Klik **Add file** > **Create new file**.
4. Isi nama: `07_Evidence/P13-HAIKAL/README.md`.
5. Copy isi `README.md` dari ZIP.
6. Di bawah, pilih **Create a new branch for this commit and start a pull request**.
7. Nama branch: `docs/p13-haikal-evidence`.
8. Commit.
9. Masih di branch yang sama, klik **Add file** > **Upload files**.
10. Drag folder `P13-HAIKAL` atau semua file ke `07_Evidence/P13-HAIKAL/`.
11. Commit lagi.
12. Buka Pull Request ke `dev`.
13. Judul: `[Tech][Haikal] Bukti QA topologi dan hosting P13`.
14. Reviewer: Ripa atau Bagas.

Kalau GitHub web tidak mau upload folder, buat file satu per satu lewat **Create new file** dengan path yang sama, atau upload file ke folder yang sudah dibuat.

## Jangan

- Jangan upload ZIP ke GitHub.
- Jangan upload ke `04_Technology/`; nanti menimpa file kanonik.
- Jangan upload `.env`, token, atau file sementara.
- Jangan push langsung ke `dev`.

## Catatan

- Vercel Hobby hanya untuk non-komersial.
- Render Free tidur setelah idle.
- Supabase Free pause dan tidak punya backup otomatis.
- Live deployment belum dilakukan; ini bukti QA, bukan aplikasi online.
