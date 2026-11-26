# BPMN TARGET GROWPATH

**Deliverable:** P13-05
**Pemilik:** Mhd Farras Delvioza
**Disusun oleh:** Tim Growpath P13, 22 November 2026
**Status:** v1.0, dua proses utama

## 1. Standar dan sumber

Diagram memakai BPMN 2.0. Elemen yang dipakai:

- pool dan lane;
- start event dan end event;
- generic task;
- exclusive gateway (XOR);
- sequence flow;
- text annotation.

Sumber notasi: OMG, *BPMN 2.0.2 Specification*; Camunda, *BPMN 2.0 Symbol Reference*, diakses 22 November 2026. P-01 memakai satu pool dengan dua lane. P-02 memakai dua pool, Growpath dan Layanan AI (Gemini), yang dihubungkan message flow. Tidak ada message flow pada P-01. Tidak ada timer, boundary error, atau event subprocess karena penanganan kegagalan pada MVP dijelaskan sebagai alur alternatif di dokumen, bukan sebagai event teknis.

File diagram: `diagrams/bpmn-target.drawio`, dua halaman.

| Halaman | Proses | PNG |
|---|---|---|
| P-01 Asesmen dan Rekomendasi | Dari data usaha sampai rencana aksi | `diagrams/bpmn-p01-asesmen-rekomendasi.png` |
| P-02 Konsultasi AI dan Log | Dari pertanyaan sampai log dan umpan balik | `diagrams/bpmn-p02-konsultasi-log.png` |

## 2. Mengapa dua proses ini

Dua proses dipilih karena bersama-sama mencakup lima fitur Must:

| Must | Proses |
|---|---|
| Data usaha | P-01 |
| Rekomendasi | P-01 |
| Dashboard | P-01, sebagai konsumen hasil |
| Konsultasi AI | P-02 |
| Log jawaban AI | P-02 |

Proses B2G, billing, mentor, dan notifikasi tidak digambar karena di luar MVP.

## 3. P-01 Asesmen dan Rekomendasi

**Tujuan:** UMKM menyelesaikan asesmen, mendapat skor dan segmen, lalu mendapat rencana aksi.
**Pemicu:** UMKM membuka Asesmen.
**Prasyarat:** Sudah masuk dan profil wajib lengkap.
**Hasil:** Asesmen berstatus scored, skor dan segmen tersimpan, roadmap berisi 3 sampai 5 milestone.

| No | Langkah | Lane | Jenis | Masukan | Keluaran | Use case |
|---:|---|---|---|---|---|---|
| 1 | Mulai | UMKM | Start event | Sesi aktif | Token proses | UC-01 |
| 2 | Isi data usaha | UMKM | Task | Data demografi | Profil usaha | UC-02 |
| 3 | Validasi profil | Sistem | Task | Profil usaha | Status kelengkapan | UC-02 |
| 4 | Profil lengkap? | Sistem | XOR gateway | Status kelengkapan | Ya atau tidak | UC-02 |
| 5 | Isi aspek 1-5 | UMKM | Task | 31 pertanyaan | Jawaban per kriteria | UC-03 |
| 6 | Simpan jawaban | Sistem | Task | Jawaban | Draft tersimpan | UC-03 |
| 7 | Tinjau jawaban | UMKM | Task | Draft | Jawaban terverifikasi | UC-04 |
| 8 | Submit asesmen | UMKM | Task | Draft lengkap | Asesmen submitted | UC-04 |
| 9 | Hitung skor dan segmen | Sistem | Task | 31 jawaban | Skor total, skor dimensi, segmen | UC-04, UC-05 |
| 10 | Susun rekomendasi | Sistem | Task | Skor dan gap | 3 sampai 5 milestone | UC-05, UC-06 |
| 11 | Tampilkan hasil dan rencana | UMKM | Task | Skor, segmen, roadmap | Keputusan langkah berikutnya | UC-05, UC-06 |
| 12 | Selesai | UMKM | End event | Hasil tampil | Proses selesai | UC-05 |

Alur alternatif:

- Profil belum lengkap: gateway mengembalikan ke Isi data usaha.
- Jawaban belum lengkap: Submit ditahan, UMKM kembali ke aspek yang kurang.
- Perhitungan gagal: status error, jawaban tetap tersimpan, pengguna bisa mencoba lagi.

Catatan: langkah 9 dan 10 adalah layanan otomatis. Diagram memakai generic task agar terbaca. Pelaksana sebenarnya adalah `Scoring Service` dan `Recommendation Service` di backend. AI tidak terlibat di langkah 9.

## 4. P-02 Konsultasi AI dan Log

**Tujuan:** UMKM bertanya, mendapat jawaban dengan sumber dan penafian, dan setiap jawaban tercatat.
**Pemicu:** UMKM membuka Konsultasi dan mengirim pertanyaan.
**Prasyarat:** Sudah masuk dan sudah punya skor.
**Hasil:** `consultation` dan `ai_answer_log` tersimpan, umpan balik tercatat.

| No | Langkah | Lane atau pool | Jenis | Masukan | Keluaran | Use case |
|---:|---|---|---|---|---|---|
| 1 | Mulai | UMKM | Start event | Sesi aktif | Token proses | UC-07 |
| 2 | Tulis pertanyaan | UMKM | Task | Pertanyaan | Teks pertanyaan | UC-07 |
| 3 | Cek prasyarat dan kuota | Sistem | Task | Sesi, kuota harian | Status boleh lanjut | UC-07 |
| 4 | Boleh lanjut? | Sistem | XOR gateway | Status | Ya atau tidak | UC-07 |
| 5 | Kirim prompt dan konteks | Sistem | Task | Profil, skor, segmen, prioritas, chunk | Permintaan model | UC-07 |
| 6 | Hasilkan jawaban | Pool Layanan AI | Task | Prompt berversimen | Jawaban mentah | UC-07 |
| 7 | Periksa guardrail | Sistem | Task | Jawaban mentah | Status lolos atau ditolak | UC-07 |
| 8 | Lolos? | Sistem | XOR gateway | Status guardrail | Ya atau tidak | UC-07 |
| 9 | Tampilkan jawaban, sumber, penafian | UMKM | Task | Jawaban lolos | Jawaban terbaca | UC-07 |
| 10 | Simpan log | Sistem | Task | Pertanyaan, jawaban, metadata | `ai_answer_log` | UC-07, UC-08 |
| 11 | Umpan balik | UMKM | Task | Penilaian | Status membantu atau tidak | UC-08 |
| 12 | Selesai | UMKM | End event | Log tersimpan | Proses selesai | UC-08 |
| 13 | Tampilkan pesan prasyarat atau kuota | UMKM | Task alternatif | Status tidak boleh lanjut | Pesan dan pertanyaan tersimpan | UC-07 |
| 14 | Tampilkan penolakan dan catat blocked | UMKM | Task alternatif | Guardrail menolak | Pesan sopan dan log blocked | UC-07 |

Langkah 5 ke 6 dan langkah 6 ke 7 adalah message flow, bukan sequence flow, karena melewati batas pool Growpath dan pool Layanan AI. Di diagram, garisnya putus-putus dengan bulatan di sumber.

Alur alternatif:

- Belum punya skor: pesan menjelaskan asesmen harus selesai lebih dulu, tautan ke Asesmen.
- Kuota habis: pertanyaan tetap disimpan, pesan menyebut waktu pemulihan kuota.
- Pertanyaan di luar konteks: guardrail menolak, log mencatat `blocked` dan alasan.
- Model gagal atau timeout: log mencatat `failed`, pengguna bisa mencoba lagi.

## 5. Hubungan ke use case dan tabel

| Proses | Use case | Tabel utama |
|---|---|---|
| P-01 | UC-02 sampai UC-06 | `umkm_profile`, `assessment`, `assessment_answer`, `dimension_score`, `segment`, `roadmap`, `milestone`, `progress_log` |
| P-02 | UC-07, UC-08 | `consultation`, `ai_answer_log`, `knowledge_document`, `knowledge_chunk` |

## 6. Yang belum dimodelkan

- Proses admin mengelola katalog dan dokumen pengetahuan.
- Proses pendamping melihat progres UMKM.
- Proses institusi B2G.
- Alur reset kata sandi secara rinci, mengikuti Supabase Auth.
- Retry teknis dan circuit breaker model. Ini masuk NFR dan arsitektur AI, bukan diagram proses bisnis.

## 7. Aturan revisi

- Perubahan alur harus memperbarui use case dan traceability.
- Jangan menambah lane aktor yang tidak ada di MVP.
- Jangan mengganti generic task dengan ikon yang membuat label tidak terbaca.
- Simpan perubahan di file `.drawio`, bukan hanya PNG.
