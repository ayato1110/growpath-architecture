# Indeks Bukti

| Bukti | Status | Catatan |
|---|---|---|
| Wawancara 40 UMKM | Ada di laporan | Sampel awal, bukan nasional |
| Responden SIGINJAI TERRA 24 | Ada di laporan | Sampel awal |
| UAT mitra | Belum | Dijadwalkan P15 |
| SUS | Belum | Dijadwalkan P15 |
| Foto dan rekaman | Belum | Dikumpulkan P15 |

| Bukti | Status | Catatan |
|---|---|---|
| Wawancara 40 UMKM | Ada di laporan | Sampel awal, bukan nasional |
| Responden SIGINJAI TERRA 24 | Ada di laporan | Sampel awal |
| UAT mitra | Belum | Dijadwalkan P15 |
| SUS | Belum | Dijadwalkan P15 |
| Foto dan rekaman | Belum | Dikumpulkan P15 |
| Eksekusi DDL PostgreSQL (23 tabel) | Selesai | Bukti di `07_Evidence/DDL.png` |
| Eksekusi Seed Data (31 kriteria, 30 profil) | Selesai | Bukti di `07_Evidence/SEED.png` |
| Verifikasi jumlah baris & skor kosong | Selesai | Bukti di `07_Evidence/Verifikasi Jumlah Baris & Skor Kosong.png` (user=30, umkm_profile=30, assessment=30, assessment_answer=31, criterion=31, skor_terisi=0) |
| Uji trigger append-only (`audit_log`) | Selesai | Bukti di `07_Evidence/Uji Trigger.png` (DELETE ditolak trigger `prevent_mutation`) |
| Uji RLS isolasi Tenant 1 | Selesai | Bukti di `07_Evidence/Uji RLS (Row-Level Security) sebagai Tenant 1 .png` (`profil_terlihat_tenant_1 = 30`) |
| Uji RLS isolasi Tenant 2 | Selesai | Bukti di `07_Evidence/Uji RLS (Row-Level Security) sebagai Tenant 2 .png` (`profil_terlihat_tenant_2 = 0`) |