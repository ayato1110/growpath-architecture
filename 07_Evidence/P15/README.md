# P15 · Status PR15

**Tanggal:** 27 November 2026  
**Arti PR15:** pekerjaan rumah sebelum P15, bukan pull request GitHub.

| Butir PR15 | Status | Bukti atau catatan |
|---|---|---|
| Gap analysis per domain | Ada, draf | `GAP-ANALYSIS.md` |
| Jadwal UAT terkonfirmasi | Ada | Rumah Setrika, 5 Desember 2026, 10.00 WIB |
| Skenario UAT berbasis tugas | Ada | `UAT-PLAN.md`, tujuh tugas |
| Kuesioner SUS 10 butir | Ada | `SUS-KUESIONER.md` |
| Backup dan restore | Sebagian | Drill logical 23 tabel, 250 baris, 0 selisih di `BACKUP-DRILL.txt`; `pg_dump` dan restore penuh belum |
| Transaksi proses kritis | Ada | Submit asesmen memakai satu commit; perlu tes rollback |
| Fitur Must 3 dan 4 | Belum | Konsultasi AI dan log jawaban |
| Dokumentasi route/endpoint | Sebagian | OpenAPI diperbarui; daftar route per role belum |
| TCO 12 bulan | Belum | Menunggu deploy staging |
| MVP hampir lengkap | Belum | 2 dari 5 Must berjalan |

## Urutan berikutnya

1. Deploy staging Render + Vercel.
2. Jalankan UAT 5 Desember dan isi SUS.
3. Uji `pg_dump` dan restore penuh.
4. Bangun Must 3 dan 4.
5. Susun TCO 12 bulan.
6. Lengkapi 31 kriteria dan dashboard di P15.

## Aturan

- Jangan menulis hasil UAT atau skor SUS sebelum sesi 5 Desember.
- Jangan mengklaim backup terbukti penuh; yang sudah diuji baru salinan logis.
- Jangan menambah Must keenam.
