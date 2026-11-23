# GUARDRAIL AI GROWPATH

**Deliverable:** P13-19
**Pemilik:** Ripa Bagaskara
**Status:** v1.0, desain. Belum ada panggilan model produksi.
**Sumber lengkap:** `P13-AI-Architecture.md` bagian 6 dan 7.

## 1. Daftar guardrail

| ID | Pemeriksaan | Tindakan bila gagal |
|---|---|---|
| G-01 | Pertanyaan masih dalam konteks usaha, UMKM, atau hasil asesmen | Tolak dengan `OUT_OF_SCOPE` |
| G-02 | Pengguna tidak meminta AI menghitung atau mengubah skor | Tolak dengan `ASKS_FOR_SCORE`, arahkan ke Hasil asesmen |
| G-03 | Tidak ada kepastian hukum atau pajak | Tolak dengan `LEGAL_CERTAINTY`, arahkan ke sumber resmi |
| G-04 | Tidak ada jaminan hasil finansial | Hapus klaim, ganti dengan pernyataan bersyarat |
| G-05 | Tidak meminta data sensitif | Tolak dengan `SENSITIVE_DATA` |
| G-06 | Sumber hanya dari `source_id` yang diberikan | Hapus sumber karangan, tandai `has_source=false` |
| G-07 | Panjang jawaban maksimal 180 kata dan 4 langkah | Pangkas dan tandai `length_ok=false` bila melebihi |
| G-08 | Bahasa Indonesia dan nada tenang | Ganti dengan template bila menyimpang jauh |
| G-09 | Instruksi di pertanyaan atau dokumen tidak boleh mengubah aturan | Abaikan dan catat `prompt_injection_suspected=true` |
| G-10 | Tidak ada data pribadi di log | Redaksi sebelum simpan |
| G-11 | Kuota dan rate limit | Tolak dengan 429 dan waktu pemulihan |
| G-12 | Timeout 20 detik, satu retry | Catat `failed`, jangan tampilkan jawaban setengah jadi |

Urutan: G-01 sampai G-05 sebelum panggilan model bila bisa ditentukan dari pertanyaan. G-06 sampai G-10 setelah model menjawab. G-11 dan G-12 di lapisan layanan.

## 2. Taksonomi penolakan

| Kode | Kapan | Contoh pesan |
|---|---|---|
| OUT_OF_SCOPE | Pertanyaan di luar usaha atau asesmen | "Pertanyaan ini di luar lingkup pendampingan usaha. Saya bisa membantu soal pasar, keuangan, proses, atau legalitas dasar." |
| ASKS_FOR_SCORE | Pengguna meminta skor dihitung atau diubah | "Skor dihitung dari jawaban asesmen, bukan oleh saya. Buka Hasil asesmen untuk melihat skor dan cara menghitungnya." |
| LEGAL_CERTAINTY | Pengguna meminta kepastian hukum atau pajak | "Saya tidak bisa memberi kepastian hukum. Periksa aturan resmi atau tanyakan ke pendamping." |
| SENSITIVE_DATA | Pengguna mengirim data pribadi yang tidak perlu | "Jangan kirim data pribadi seperti nomor identitas atau rekening. Saya tidak membutuhkannya untuk menjawab." |
| NO_CONTEXT | Tidak ada chunk relevan dan pertanyaan butuh rujukan | "Belum ada rujukan yang cukup untuk pertanyaan ini. Saya bisa membantu dari hasil asesmen Anda saja." |
| UNSAFE_ADVICE | Saran berisiko tinggi tanpa dasar | "Saya tidak bisa menyarankan tindakan berisiko tinggi tanpa dasar yang cukup." |

Pesan penolakan tetap disimpan sebagai `ai_answer_log` dengan status `blocked` dan `guardrail_result.blocked_reason`.

## 3. Batas

- Guardrail ini desain, bukan hasil uji produksi.
- Lima pertanyaan probe belum dijalankan pada P13.
- Model final dan ambang retrieval dipilih pada P14.
