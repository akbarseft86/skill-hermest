# skill-hermest

Kumpulan skill Hermes untuk dibagikan ke bot/profile lain.

## Isi

- `github/github-repo-management/` — skill untuk cepat baca/kelola repo GitHub.

## Cara pasang ke bot Hermes lain

```bash
mkdir -p ~/.hermes/skills/github
cp -r github/github-repo-management ~/.hermes/skills/github/
```

Lalu di chat bot:

```text
/reload-skills
```

Prompt penggunaan:

```text
Kalau user minta cek repo GitHub atau kirim screenshot repo, load skill github-repo-management dulu. Ekstrak owner/repo, baca GitHub API metadata, README raw, docs penting seperti install.md, lalu jawab ringkas: fungsi, stats, risiko, rekomendasi.
```
