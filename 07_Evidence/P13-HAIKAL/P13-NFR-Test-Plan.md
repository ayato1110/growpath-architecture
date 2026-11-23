# Rencana Uji NFR P13

**Pemilik:** Moch Haikal Ramadhan
**Sumber:** `04_Technology/P13-NFR.md`
**Status:** Rencana, belum dijalankan.

| NFR | Target | Cara uji | Fase |
|---|---|---|---|
| NFR-01 | p95 baca di bawah 500 ms | Load test endpoint baca | P14 |
| NFR-03 | LCP di bawah 2,5 detik pada 4G 390px | Lighthouse | P14 |
| NFR-04 | INP di bawah 200 ms, CLS di bawah 0,1 | Lighthouse dan uji browser | P14 |
| NFR-05 | Jawaban AI di bawah 15 detik, timeout 20 detik | Uji 20 pertanyaan, catat `latency_ms` | P14 |
| NFR-06 | Submit asesmen di bawah 2 detik | Unit test 31 jawaban | P14 |
| NFR-09 | RPO maksimal 24 jam | Uji backup dan restore | P15 |
| NFR-10 | RTO maksimal 4 jam | Simulasi restore | P15 |
| NFR-11 | Skor deterministik 100% | Unit test tiga profil | P14 |
| NFR-12 | Submit asesmen atomik | Uji rollback saat gagal | P14 |
| NFR-13 | `progress_log` dan `audit_log` append-only | Uji trigger update/delete | P14 |
| NFR-17 | Isolasi tenant | Uji RLS dua tenant | P14 |
| NFR-18 | Tidak ada service role key di browser | Grep bundle dan uji jaringan | P14 |
| NFR-19 | 60 request per menit, 10 konsultasi per hari | Uji 429 | P14 |

## Catatan

- Uji beban, Lighthouse, dan restore membutuhkan staging.
- Hasil uji dicatat di `07_Evidence/`.
- Jangan mengklaim lulus sebelum ada bukti.
