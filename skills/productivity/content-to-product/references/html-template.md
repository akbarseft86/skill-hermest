# HTML Product Presentation Template

Base template for presenting digital product concepts derived from content analysis.

## Structure

```html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>5 Produk Digital dari [Nama Konten]</title>
  <style>
    /* DARK THEME base */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #0f0f0f; color: #e0e0e0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; }
    .container { max-width: 900px; margin: 0 auto; padding: 20px; }
    
    /* ACCENT: use #ff8c00 (orange) or #6366f1 (indigo) or #10b981 (emerald) */
    .accent { color: #ff8c00; }
    .accent-bg { background: #ff8c00; }
    .accent-border { border: 2px solid #ff8c00; }
    
    /* HERO */
    .hero { text-align: center; padding: 60px 20px 40px; }
    .hero h1 { font-size: 2.2em; font-weight: 800; margin-bottom: 15px; }
    .hero p { color: #888; font-size: 1.1em; max-width: 600px; margin: 0 auto; }
    
    /* PRODUCT CARDS */
    .product-card { 
      background: #1a1a1a; border-radius: 16px; padding: 30px; margin: 20px 0;
      transition: transform 0.2s;
    }
    .product-card:hover { transform: translateY(-2px); }
    .product-number { 
      font-size: 0.85em; color: #ff8c00; font-weight: 700; 
      text-transform: uppercase; letter-spacing: 2px;
    }
    .product-title { 
      font-size: 1.8em; font-weight: 800; margin: 10px 0 15px;
      line-height: 1.3;
    }
    .product-hook { color: #aaa; font-size: 1.1em; margin-bottom: 20px; }
    
    /* BENEFITS CHECKLIST */
    .benefits { list-style: none; padding: 0; }
    .benefits li { 
      padding: 8px 0 8px 28px; position: relative;
      background: url("data:image/svg+xml,...") left center no-repeat;
    }
    .benefits li::before { content: "✅"; position: absolute; left: 0; }
    
    /* TARGET AUDIENCE TAGS */
    .target-tags { display: flex; flex-wrap: wrap; gap: 8px; margin: 15px 0; }
    .target-tag {
      background: #2a2a2a; padding: 5px 14px; border-radius: 20px;
      font-size: 0.85em; color: #ccc;
    }
    
    /* THEME SECTION */
    .theme-section { background: #161616; border-radius: 16px; padding: 30px; margin: 20px 0; }
    .theme-bar { 
      height: 24px; border-radius: 12px; margin: 8px 0;
      background: linear-gradient(90deg, #ff8c00, #ff6b00);
      display: flex; align-items: center; padding-left: 12px;
      font-size: 0.8em; font-weight: 600; color: #fff; 
    }
    .theme-label { display: flex; justify-content: space-between; margin-top: 15px; color: #aaa; }
    .theme-label span { font-size: 0.9em; }
    
    /* SOURCE CONTENT */
    .source-link { 
      background: #222; padding: 10px 16px; border-radius: 10px; margin: 5px 0;
      font-size: 0.9em; color: #aaa; text-decoration: none; display: inline-block;
    }
    .source-link:hover { background: #333; }
    
    /* FOOTER */
    .footer { text-align: center; padding: 40px 0; color: #555; font-size: 0.85em; }
    
    /* COPY BUTTON */
    .copy-btn {
      background: transparent; border: 1px solid #444; color: #ccc;
      padding: 8px 16px; border-radius: 8px; cursor: pointer;
      font-size: 0.85em; transition: all 0.2s;
    }
    .copy-btn:hover { background: #333; border-color: #ff8c00; color: #fff; }
    
    /* RESPONSIVE */
    @media (max-width: 600px) {
      .hero h1 { font-size: 1.6em; }
      .product-title { font-size: 1.3em; }
      .container { padding: 15px; }
    }
  </style>
</head>
<body>
  <div class="container">
    
    <!-- HERO -->
    <div class="hero">
      <h1>🔥 5 Produk Digital <span class="accent">Dari [Nama Konten]</span></h1>
      <p>[Deskripsi singkat]</p>
    </div>

    <!-- THEME ANALYSIS (optional but recommended) -->
    <div class="theme-section">
      <h2 style="margin-bottom: 20px;">📊 Analisa Tema dari [N] Konten</h2>
      <!-- Theme bars: width as percentage -->
      <div class="theme-label">
        <span>Tema A</span><span>X dari N video</span>
      </div>
      <div class="theme-bar" style="width: 85%">Tema A</div>
      <!-- ...repeat for each theme... -->
    </div>

    <!-- PRODUCT CARDS -->
    <!-- Repeat 5x with different content -->
    <div class="product-card">
      <div class="product-number">Produk #1</div>
      <h2 class="product-title">RAHASIA KALIMAT SET-UP:<br><span class="accent">Kunci 1 Menit Instant Healing</span></h2>
      <p class="product-hook">Satu kalimat yang mengubah segalanya — tanpa ini, SEFT Anda hanya gerakan kosong.</p>
      
      <h3 style="margin: 20px 0 10px;">✨ Apa yang Kamu Dapatkan:</h3>
      <ul class="benefits">
        <li>Benefit 1 — spesifik dan terukur</li>
        <li>Benefit 2 — spesifik dan terukur</li>
        <li>Benefit 3 — spesifik dan terukur</li>
      </ul>
      
      <div>
        <h3 style="margin: 20px 0 10px;">🎯 Untuk Kamu yang:</h3>
        <div class="target-tags">
          <span class="target-tag">Persona 1</span>
          <span class="target-tag">Persona 2</span>
          <span class="target-tag">Persona 3</span>
        </div>
      </div>
      
      <button class="copy-btn" onclick="copyProduct(this, 1)">📋 Salin Deskripsi Produk</button>
    </div>

    <!-- ...repeat 4 more times... -->

    <!-- FOOTER -->
    <div class="footer">
      Dibuat dari analisis [N] konten [nama seri] • [Tanggal]
    </div>

  </div>

  <script>
    function copyProduct(btn, num) {
      const cards = document.querySelectorAll('.product-card');
      const card = cards[num - 1];
      // Build text from card content
      const title = card.querySelector('.product-title').innerText;
      const hook = card.querySelector('.product-hook').innerText;
      const benefits = [...card.querySelectorAll('.benefits li')].map(l => l.innerText).join('\n');
      const tags = [...card.querySelectorAll('.target-tag')].map(t => t.innerText).join(', ');
      const text = `PRODUK #${num}\n${title}\n\n${hook}\n\nApa yang Kamu Dapatkan:\n${benefits}\n\nUntuk: ${tags}`;
      
      navigator.clipboard.writeText(text).then(() => {
        btn.innerText = '✅ Tersalin!';
        setTimeout(() => btn.innerText = '📋 Salin Deskripsi Produk', 2000);
      }).catch(() => {
        // Fallback for non-HTTPS
        const ta = document.createElement('textarea');
        ta.value = text; document.body.appendChild(ta);
        ta.select(); document.execCommand('copy');
        document.body.removeChild(ta);
        btn.innerText = '✅ Tersalin!';
        setTimeout(() => btn.innerText = '📋 Salin Deskripsi Produk', 2000);
      });
    }

    function copyAll() {
      let all = '';
      document.querySelectorAll('.product-card').forEach(card => {
        const num = all.split('PRODUK').length;
        const title = card.querySelector('.product-title').innerText;
        const hook = card.querySelector('.product-hook').innerText;
        const benefits = [...card.querySelectorAll('.benefits li')].map(l => l.innerText).join('\n');
        all += `PRODUK #${num}\n${title}\n${hook}\n\n${benefits}\n\n---\n\n`;
      });
      navigator.clipboard.writeText(all).then(() => {
        alert('Semua produk tersalin!');
      });
    }
  </script>
</body>
</html>
```

## Key Design Decisions

- **Dark theme**: `#0f0f0f` background, `#1a1a1a` card bg, `#ff8c00` accent (or customize per brand)
- **One product per card**: Each product gets its own distinct card with visual hierarchy
- **Copy per product**: Each card has a copy button for individual product descriptions
- **Theme visualization**: Bar chart-style theme frequency shows buyers why these products exist
- **Mobile-first**: Cards stack, fonts resize, no horizontal scroll
- **No frameworks**: Pure HTML/CSS/JS — works on any server, no dependencies
