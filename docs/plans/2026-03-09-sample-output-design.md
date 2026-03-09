# Sample Output Previews Design

## Goal

Add realistic sample output previews to the catalog card grid. Each workflow card becomes a left/right split: card info on the left, styled output mockup on the right. Mobile: swipeable (card default, swipe to see output).

## Layout

### Desktop (>768px)
```
┌─────────────────────────────────────────────────────┐
│  [Card Info]            │  [Slack Message Mockup]    │
│  Category badge         │  ┌──────────────────────┐  │
│  Workflow Name          │  │ 🤖 Aria  12:01 PM    │  │
│  Description...         │  │                      │  │
│  Trigger | Output       │  │ **Acme Corp Update** │  │
│  Nodes | Credentials    │  │ 3 meetings this week │  │
│                         │  │ Deal: Stage 3 → 4    │  │
│                         │  └──────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### Mobile (<768px)
Swipeable card. Default shows card info. Swipe left or tap indicator to reveal sample output. Small dot indicators show which panel is active.

## Mockup Styles

### 1. Slack Message (default)
For: digests, briefs, channel updates, alerts
- Dark left accent bar (Slack-style)
- Bot avatar + name + timestamp
- Formatted message with bold headers, bullet points
- Optional emoji reactions bar at bottom

### 2. Email Message
For: #05 Forecast Coach, any email-primary workflow
- Email header: From, To, Subject
- Clean body with paragraphs
- Light border, white background

### 3. Scorecard
For: #07 Churn Risk, #11 Deal Hygiene, #14 Territory Heat Map, #17 Handoff Scorer
- Structured grid with metrics
- Color-coded indicators (green/yellow/red)
- Score badges or progress bars
- Still delivered via Slack but displayed as rich content

## Workflow → Mockup Style Mapping

| ID | Workflow | Style | Bot Name |
|----|----------|-------|----------|
| 01 | Sales Digest | slack | Aria |
| 02 | Meeting Brief | slack | Aria |
| 03 | Silence & Contract Monitor | slack-alert | Aria |
| 04 | Opportunity Discovery | slack | Aria |
| 05 | Forecast Coach | email | — |
| 06 | Executive Inbox | slack | Aria |
| 07 | Churn Risk Scorecard | scorecard | Aria |
| 08 | Renewal Prep Brief | slack | Aria |
| 09 | Onboarding Pulse | slack | Aria |
| 10 | Activity Gap Detector | slack-alert | Aria |
| 11 | Deal Hygiene Audit | scorecard | Aria |
| 12 | Win/Loss Debrief | slack | Aria |
| 13 | Competitive Displacement Alert | slack-alert | Aria |
| 14 | Territory Heat Map | scorecard | Aria |
| 15 | QBR Auto-Prep | slack | Aria |
| 16 | Executive Sponsor Tracker | slack | Aria |
| 17 | Marketing-Sales Handoff Scorer | scorecard | Aria |
| 18 | Channel Pulse | slack | Aria |

## Data Source

New `## Sample Output` section in each SOURCE.md:

```markdown
## Sample Output

<!--mockup:slack-->
<!--bot:Aria-->

**🏢 Acme Corp — Weekly Pulse**

📊 *3 meetings this week* (2 with VP Eng, 1 with CFO)
📈 Deal moved from Stage 3 → Stage 4
🤝 Renewal conversation initiated by champion
⚠️ No activity from economic buyer in 12 days

*Key contacts: Sarah Chen (champion, active), Mike Torres (EB, quiet)*
```

The `<!--mockup:TYPE-->` HTML comment tells the renderer which style to use. The markdown content is rendered inside the mockup frame.

Build pipeline parses this into `workflows.json` as:
```json
{
  "sample_output": {
    "mockup": "slack",
    "bot_name": "Aria",
    "content": "**🏢 Acme Corp — Weekly Pulse**\n\n..."
  }
}
```

## CSS Components

### Slack Mockup
- White card with subtle shadow
- Left accent bar (4px, colored by category)
- Header: bot avatar (circle, coral bg, "A"), bot name, timestamp
- Body: rendered markdown (bold, italic, bullets, emoji)
- Footer: reaction bar (optional)

### Email Mockup
- White card with top border
- Header row: From/To/Subject in gray
- Body: clean paragraphs
- Lighter, more formal feel

### Scorecard Mockup
- White card
- Header with title
- Grid of metric boxes with colored indicators
- Green/yellow/red status dots or bars

### Slack Alert Variant
- Same as Slack but with orange/red left accent bar
- Urgency indicator in header
- Shorter, punchier content

## Mobile Swipe Implementation

- CSS: `overflow-x: auto; scroll-snap-type: x mandatory;` on the card container
- Two snap children: card-info panel (100% width) and output panel (100% width)
- Dot indicators below (2 dots, active state)
- JS: IntersectionObserver to update active dot
- No heavy swipe library needed — native CSS scroll snap

## Files Changed

- All 18 `*/SOURCE.md` — add `## Sample Output` sections
- `docs/build-catalog.py` — parse sample output section
- `docs/index.html` — CSS for mockup styles + card layout changes + mobile swipe
- `docs/workflows.json` — regenerated with sample_output data
