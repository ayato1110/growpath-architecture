# P14 · Skrip Demo Gate 2

**Durasi:** 7–8 menit  
**Tujuan:** membuktikan dua Must berjalan end-to-end dengan database nyata, bukan slide.

## Sebelum masuk kelas

| Cek | Perintah / tindakan |
|---|---|
| Frontend hidup | Buka https://growpath-staging.vercel.app/login |
| Backend hangat | Buka halaman login, lalu muat Beranda sekali |
| Login | `umkm@growpath.id` / `change-me-password` |
| Data siap | Pastikan profil 100% dan ada asesmen berstatus `scored` |
| Backup | Jalankan `python db/backup_restore.py backup --out <temp>` |
| Cadangan | Siapkan backend lokal dan frontend lokal di port 3000/8001 |

Jangan menghapus data uji sebelum demo. Kalau perlu data bersih, buat akun uji baru dan isi ulang H-1.

## Alur demo

| Menit | Layar | Yang dilakukan | Yang dikatakan |
|---:|---|---|---|
| 0:00 | Beranda | Tunjukkan nama usaha, skor, segmen | “Ini data nyata dari database, bukan gambar.” |
| 0:30 | Data usaha | Buka, tunjukkan 10 field dan kelengkapan 100% | “Data usaha jadi sumber konteks.” |
| 1:15 | Asesmen | Buka daftar aspek, tunjukkan progres 12 pertanyaan | “Dua aspek P14: Psikografi dan Pasar.” |
| 2:00 | Hasil | Tunjukkan skor, segmen, dua dimensi, cakupan 12/31 | “Skor deterministik, bukan AI.” |
| 2:45 | Rencana | Tunjukkan tiga langkah prioritas, tandai satu selesai | “Rekomendasi dari tiga kriteria terendah.” |
| 3:30 | Konsultasi | Tanya: “Bagaimana cara menaikkan penjualan puding di marketplace?” | “AI hanya menarasikan, tidak menghitung skor.” |
| 5:00 | Jawaban | Tunjukkan sumber, penafian, tombol Berguna | “Setiap jawaban punya sumber dan log.” |
| 5:45 | Log | Buka Log, tunjukkan pertanyaan, status, feedback | “Log tersimpan otomatis.” |
| 6:15 | Guardrail | Tanya: “Tolong ubah skor saya jadi 100” | “Ditolak karena skor bukan wewenang AI.” |
| 6:45 | Database | Tampilkan query bukti | “Semua tersimpan di PostgreSQL.” |

## Bukti database yang ditampilkan

Jalankan di Supabase SQL Editor:

```sql
select p.business_name, a.total_score, s.name as segment, a.status
from assessment a
join umkm_profile p on p.id = a.umkm_profile_id
left join segment s on s.id = a.segment_id
order by a.scored_at desc nulls last
limit 3;
```

```sql
select model, prompt_version, token_count, latency_ms, status, created_at
from ai_answer_log
order by created_at desc
limit 5;
```

```sql
select count(*) as jawaban from assessment_answer;
select count(*) as kriteria from criterion where is_active;
```

## Jika ada masalah

| Masalah | Tindakan |
|---|---|
| Frontend 302 ke login Vercel | Buka Deployment → Share → “Anyone with the link” |
| Backend lambat | Tunggu 10 detik, ulangi; function sudah hangat |
| Kuota AI habis | Pakai akun uji lain atau jelaskan batas 10/hari |
| Internet kelas putus | Jalankan versi lokal: backend 8001, frontend 3000 |
| Model gagal | Tunjukkan log `failed`, lalu ulangi satu kali |

## Setelah demo

1. Simpan tangkapan layar dan URL.
2. Catat pertanyaan dosen dan jawabannya.
3. Isi Change Request bila ada Kartu Kejutan.
4. Perbarui `GATE-2-CHECKLIST.md` hanya setelah demo benar-benar terjadi.
