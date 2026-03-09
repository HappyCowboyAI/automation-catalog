# Sample Output Preview Implementation Plan (Channel Pulse #18 Only)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a Slack message mockup sample output to the Channel Pulse card in the catalog grid, using a left/right split layout with mobile swipe support.

**Architecture:** Sample output content lives in SOURCE.md as a `## Sample Output` section. Build pipeline parses it into workflows.json. Card renderer creates a left/right split with the card info and a Slack-styled mockup. Mobile uses CSS scroll-snap for swipe.

**Tech Stack:** HTML/CSS/JS (single-file SPA), Python build pipeline, CSS scroll-snap

---

### Task 1: Add Sample Output to SOURCE.md and build pipeline

**Files:**
- Modify: `18-channel-pulse/SOURCE.md`
- Modify: `docs/build-catalog.py`

**Step 1: Add Sample Output section to SOURCE.md**

Append to end of `18-channel-pulse/SOURCE.md`:

```markdown
## Sample Output

<!--mockup:slack-->
<!--bot:Aria-->

**Acme Corp — Weekly Pulse**

*3 meetings this week* — 2 with VP Engineering (Sarah Chen), 1 with CFO (Mike Torres). Deal advanced from Stage 3 to Stage 4 after technical validation completed. Champion initiated renewal conversation — positive signals.

No activity from economic buyer in 12 days — consider a check-in before QBR.

**Key Contacts**
- Sarah Chen (Champion) — Active, 3 touchpoints this week
- Mike Torres (Economic Buyer) — Quiet, last activity 12 days ago
- James Park (Technical Eval) — Active, completed POC review
```

**Step 2: Update build pipeline to parse sample output**

In `docs/build-catalog.py`, in the `parse_source_md` function (around line 142), add parsing for the new section. After the `quick_start_vs_full` parsing block:

```python
    # --- Sample Output ---
    sample_raw = sections.get("sample output", "").strip()
    if sample_raw:
        mockup_type = "slack"
        bot_name = "Aria"
        m_type = re.search(r'<!--mockup:(\w+)-->', sample_raw)
        if m_type:
            mockup_type = m_type.group(1)
        m_bot = re.search(r'<!--bot:(\w+)-->', sample_raw)
        if m_bot:
            bot_name = m_bot.group(1)
        # Strip HTML comments from content
        content = re.sub(r'<!--.*?-->\n?', '', sample_raw).strip()
        meta["sample_output"] = {
            "mockup": mockup_type,
            "bot_name": bot_name,
            "content": content,
        }
    else:
        meta["sample_output"] = None
```

In the `build_workflow_entry` function (around line 309), add the field to the entry dict:

```python
        "sample_output": meta.get("sample_output"),
```

**Step 3: Rebuild catalog and verify**

Run: `python3 docs/build-catalog.py`
Expected: "Generated docs/workflows.json with 18 workflow(s)"

Then verify: `python3 -c "import json; d=json.load(open('docs/workflows.json')); cp=[w for w in d['workflows'] if w['id']=='18-channel-pulse'][0]; print(json.dumps(cp.get('sample_output'), indent=2))"`
Expected: JSON with mockup="slack", bot_name="Aria", and the markdown content.

**Step 4: Commit**

```bash
git add 18-channel-pulse/SOURCE.md docs/build-catalog.py docs/workflows.json
git commit -m "feat: add sample output to Channel Pulse SOURCE.md and build pipeline"
```

---

### Task 2: Add Slack mockup CSS and card layout

**Files:**
- Modify: `docs/index.html` (CSS section)

**Step 1: Add Slack mockup CSS styles**

Insert before the `/* Details Tab */` comment (around line 642) in the `<style>` block:

```css
  /* Sample Output Mockups */
  .slack-mockup {
    background: var(--ac-white);
    border: 1px solid var(--ac-light-gray);
    border-radius: 8px;
    font-size: 13px;
    overflow: hidden;
  }
  .slack-mockup-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 12px 0;
  }
  .slack-mockup-avatar {
    width: 28px;
    height: 28px;
    border-radius: 4px;
    background: var(--ac-coral);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
    flex-shrink: 0;
  }
  .slack-mockup-botname {
    font-weight: 700;
    font-size: 13px;
    color: var(--ac-dark);
  }
  .slack-mockup-time {
    font-size: 11px;
    color: var(--ac-med-gray);
  }
  .slack-mockup-body {
    padding: 6px 12px 12px 48px;
    color: var(--ac-dark);
    line-height: 1.5;
    font-size: 12.5px;
    max-height: 180px;
    overflow: hidden;
    mask-image: linear-gradient(to bottom, black 70%, transparent 100%);
    -webkit-mask-image: linear-gradient(to bottom, black 70%, transparent 100%);
  }
  .slack-mockup-body p { margin: 0 0 6px; }
  .slack-mockup-body strong { font-weight: 700; }
  .slack-mockup-body em { font-style: italic; color: var(--ac-dark-secondary); }
  .slack-mockup-body ul { margin: 4px 0; padding-left: 16px; }
  .slack-mockup-body li { margin: 2px 0; }
```

**Step 2: Update card layout CSS for left/right split**

Replace the existing `.card-grid` and `.card` CSS (lines ~196-240):

Change `.card-grid` from:
```css
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 16px;
  }
```
To:
```css
  .card-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
  }
```

Change `.card` from just a padded box to a flex container:
```css
  .card {
    background: var(--ac-white);
    border-radius: var(--radius);
    border: 1px solid var(--ac-light-gray);
    cursor: pointer;
    transition: all 0.25s;
    position: relative;
    border-left: 4px solid transparent;
    display: flex;
    overflow: hidden;
  }
```

Add new card inner layout classes:
```css
  .card-info {
    flex: 1;
    padding: 20px;
    min-width: 0;
  }
  .card-preview {
    flex: 0 0 340px;
    padding: 16px;
    background: #F8F9FA;
    border-left: 1px solid var(--ac-light-gray);
    display: flex;
    align-items: center;
  }
  .card-preview .slack-mockup {
    width: 100%;
  }
```

**Step 3: Add mobile swipe CSS**

In the `@media (max-width: 768px)` block, add:
```css
    .card {
      flex-direction: row;
      overflow-x: auto;
      scroll-snap-type: x mandatory;
      scrollbar-width: none;
    }
    .card::-webkit-scrollbar { display: none; }
    .card-info {
      flex: 0 0 100%;
      scroll-snap-align: start;
    }
    .card-preview {
      flex: 0 0 100%;
      scroll-snap-align: start;
      border-left: none;
      border-top: none;
    }
    .card-dots {
      display: flex;
      justify-content: center;
      gap: 6px;
      padding: 8px 0 4px;
    }
    .card-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--ac-light-gray);
    }
    .card-dot.active {
      background: var(--ac-coral);
    }
```

Also add desktop hide for dots:
```css
  .card-dots { display: none; }
```

(Place this after the `.card-preview` block in the main CSS, not in the media query.)

**Step 4: Commit**

```bash
git add docs/index.html
git commit -m "feat: add Slack mockup CSS and card split layout with mobile swipe"
```

---

### Task 3: Update card rendering JS

**Files:**
- Modify: `docs/index.html` (JS section, `renderCards` function)

**Step 1: Add markdown-to-HTML helper**

Before the `renderCards` function (~line 918), add:

```javascript
function mdToHtml(md) {
  return md
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
    .split('\n\n').map(p => {
      if (p.startsWith('<ul>') || p.startsWith('<li>')) return p;
      return `<p>${p.replace(/\n/g, '<br>')}</p>`;
    }).join('');
}

function renderSlackMockup(sample) {
  const initial = sample.bot_name ? sample.bot_name[0] : 'A';
  return `
    <div class="slack-mockup">
      <div class="slack-mockup-header">
        <div class="slack-mockup-avatar">${initial}</div>
        <span class="slack-mockup-botname">${sample.bot_name || 'Bot'}</span>
        <span class="slack-mockup-time">9:01 AM</span>
      </div>
      <div class="slack-mockup-body">${mdToHtml(sample.content)}</div>
    </div>`;
}
```

**Step 2: Update renderCards to include preview panel**

Replace the card template in `renderCards` (lines ~940-950) from:
```javascript
    return `
      <div class="card" onclick="navigate('#/workflow/${w.id}')">
        <div class="card-number">${w.id} &middot; ${cat ? cat.name : ''}</div>
        <div class="card-name">${w.name}</div>
        <div class="card-desc">${w.description}</div>
        <div class="card-meta">
          <span class="badge badge-trigger">${triggerShort}</span>
          ${w.output ? `<span class="badge badge-output">${w.output}</span>` : ''}
          <span class="badge badge-category">${cat ? cat.name : ''}</span>
        </div>
      </div>`;
```
To:
```javascript
    const preview = w.sample_output
      ? renderSlackMockup(w.sample_output)
      : '';
    return `
      <div class="card" onclick="navigate('#/workflow/${w.id}')">
        <div class="card-info">
          <div class="card-number">${w.id} &middot; ${cat ? cat.name : ''}</div>
          <div class="card-name">${w.name}</div>
          <div class="card-desc">${w.description}</div>
          <div class="card-meta">
            <span class="badge badge-trigger">${triggerShort}</span>
            ${w.output ? `<span class="badge badge-output">${w.output}</span>` : ''}
            <span class="badge badge-category">${cat ? cat.name : ''}</span>
          </div>
        </div>
        ${preview ? `<div class="card-preview">${preview}</div>` : ''}
        ${preview ? `<div class="card-dots"><span class="card-dot active"></span><span class="card-dot"></span></div>` : ''}
      </div>`;
```

**Step 3: Add mobile swipe dot tracking**

After the `renderCards` function, add:

```javascript
function initCardSwipe() {
  if (window.innerWidth > 768) return;
  document.querySelectorAll('.card').forEach(card => {
    const dots = card.querySelectorAll('.card-dot');
    if (dots.length < 2) return;
    card.addEventListener('scroll', () => {
      const scrolled = card.scrollLeft > card.offsetWidth * 0.4;
      dots[0].classList.toggle('active', !scrolled);
      dots[1].classList.toggle('active', scrolled);
    });
  });
}
```

Then call `initCardSwipe()` at the end of `renderCards`:

```javascript
  // At end of renderCards, after the innerHTML assignment
  initCardSwipe();
```

**Step 4: Verify locally**

Open `docs/index.html` in a browser. Channel Pulse (#18) should show the Slack mockup on the right. Other cards should look the same as before (no preview panel). Resize to mobile width — the card should be swipeable.

**Step 5: Commit**

```bash
git add docs/index.html
git commit -m "feat: render Slack mockup preview on Channel Pulse card"
```

---

### Task 4: Rebuild, push, verify

**Step 1: Rebuild catalog**

Run: `python3 docs/build-catalog.py`

**Step 2: Commit and push**

```bash
git add docs/workflows.json
git commit -m "docs: rebuild catalog with sample output data"
git push origin main
```

**Step 3: Verify on GitHub Pages**

Check https://happycowboyai.github.io/automation-catalog/ — Channel Pulse card should show the Slack mockup preview on the right side.
