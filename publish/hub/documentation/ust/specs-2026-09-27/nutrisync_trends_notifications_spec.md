# NutriSync — Trends & Personalized Notifications Feature Specification
**Feature Addition: Calendar Trends View + Personalized Insights & Notifications**  
**Version:** 1.0 | January 2025  
**For integration into existing NutriSync Developer Specification v1.0**

---

## 1. Feature Overview

Transform the Calendar "Trends" tab from a placeholder into a powerful **pattern recognition and personalization engine** that learns the user's unique cycle over time and surfaces actionable, personalized insights and notifications.

### Core Principles
- **Your body, your patterns** — not population averages masquerading as personal insights
- **Confidence-scored** — users always know how reliable a pattern is
- **Proactive, reactive, and preparatory** — meet users where they are in their day
- **Privacy-first** — sensitive insights stay in-app, never push notifications
- **Progressively smarter** — unlocks deeper insights as more data accumulates

---

## 2. Data Thresholds & Unlock Rules

| Cycles Logged | What Unlocks |
|---------------|-------------|
| **0–1 cycle** | Trends tab shows: "We're learning your rhythm — keep logging to unlock personalized insights" |
| **2 cycles** | Basic trends unlock: cycle length average, period duration, phase energy/mood averages. Disclaimer: "Early insights — we're still learning your patterns." |
| **3 cycles** | Full pattern recognition: recurring symptoms, phase-specific cravings, sleep quality trends, libido patterns, pain timing, skin breakouts. Confidence levels shown. |
| **4+ cycles** | Advanced insights: correlations (e.g., sugar → worse PMS), next period predictions with confidence bands, "Your Unique Cycle" summary unlocked. |

**DEV NOTE:** Display a progress indicator on Trends tab before 2 cycles: "1 of 2 cycles logged — keep going to unlock your insights!"

---

## 3. Trends Page Layout

### 3.1 Header
- **Tab selector:** Month | Year | **Trends** (active = coral pill)
- **Title:** "Your Cycle Trends"
- **Subtitle:** "Patterns we've spotted across [N] logged cycles"

### 3.2 Summary Card — "Your Unique Cycle"
*(Unlocks after 4 cycles)*

Large card at top with key stats:
- **Average cycle length:** "Your cycles run 29 days on average (±2 days)" + population comparison "(2 days longer than average)"
- **Period duration:** "You bleed for 5 days, usually moderate-to-heavy flow"
- **Most challenging phase:** "Late luteal — when PMS symptoms peak for you"
- **Strongest phase:** "Follicular — your energy, mood, and performance are highest here"
- **Next period prediction:** "Expected around [date] (confidence: 85%)" + visual confidence band

**Tone:** Warm, validating, science-backed. Example:  
*"Your cycles are a bit longer than the 28-day textbook, but that's your normal — and knowing it means you can plan around it."*

---

### 3.3 Category Breakdown — Visual + Insights

Each category gets:
- **Mini line chart or bar graph** (last 3–6 cycles)
- **Pattern insight text** in NutriSync voice
- **Confidence level** (e.g., "Appeared in 4 out of 5 cycles")
- **Actionable tip** where relevant

---

## 4. Trend Categories & Logic

### 4.1 Cycle Length & Regularity

**Data source:** `cycles.last_period_start_date` across all logged cycles

**Calculated:**
- Average cycle length
- Standard deviation (regularity)
- Shortest/longest cycle
- Trend direction (getting longer/shorter/stable)

**Chart:** Line graph of cycle length over time

**Insight examples:**
- ✅ **Regular:** *"Your cycles are clockwork — 28 days ±1. You can plan trips, events, and big workouts with confidence."*
- ⚠️ **Variable:** *"Your cycles swing between 25–32 days. Irregular isn't broken — but if it's stressing you out, chat with your doctor."*
- 📊 **Comparison:** *"Your 26-day cycles are 2 days shorter than average, but totally normal for you."*

**Confidence:** "Based on [N] cycles"

---

### 4.2 Flow Heaviness

**Data source:** `daily_logs.flow_level` (1–4) across all menstrual phase days

**Calculated:**
- Average flow level per cycle day (Day 1, Day 2, etc.)
- Heaviest day (mode)
- Total heavy-flow days per cycle

**Chart:** Stacked bar chart showing light/medium/heavy/very heavy days across cycles

**Insight examples:**
- *"Day 2 is always your heaviest — plan for it."*
- *"You typically have 2 heavy days, then taper to light. That's your normal."*
- 🚨 **Flag if very heavy:** *"You're logging 'very heavy' flow often — if you're soaking through products hourly, talk to your doctor."*

**Confidence:** "Consistent across [N] cycles"

---

### 4.3 Recurring Symptoms

**Data source:** `daily_logs.pain_symptoms[]`, `digestion_symptoms[]`, `mood_state[]`, `skin_symptoms[]`, etc.

**Calculated:**
- Which symptoms appear in which phase (frequency %)
- Peak symptom days (e.g., cramps worst on Day 2)
- Symptom clusters (e.g., bloating + headaches + mood swings = late luteal PMS)

**Chart:** Heatmap or bubble chart showing symptom intensity by cycle day

**Insight examples:**
- *"Cramps peak on Day 2–3 for you. Magnesium + heat + rest = your toolkit."*
- *"You get bloated every late luteal phase — it's progesterone-driven water retention, not weight gain."*
- *"Headaches spike around Day 22. Try cutting caffeine 2 days before."*

**Confidence:** "Happened in 4 out of 5 cycles"

---

### 4.4 Libido Patterns

**Data source:** `daily_logs.libido` (1–5 scale)

**Calculated:**
- Average libido by phase
- Peak libido window
- Lowest libido window

**Chart:** Line graph of libido across cycle days

**Insight examples:**
- *"Your libido peaks in ovulatory phase (Days 13–16) — that's biology doing its job."*
- *"You're typically lower-libido in late luteal. Progesterone's a sedative; it's not you."*
- *"Your libido stays pretty stable — not everyone has a dramatic swing, and that's fine."*

**Privacy note:** This insight is **in-app only** — never a push notification.

**Confidence:** "Pattern holds across [N] cycles"

---

### 4.5 Sleep Quality by Phase

**Data source:** `daily_logs.sleep_quality` (Very Poor / Restless / Okay / Restful / Deep → mapped 1–5)

**Calculated:**
- Average sleep quality per phase
- Best sleep phase
- Worst sleep phase
- Sleep disruption patterns (e.g., worse in late luteal)

**Chart:** Bar chart of average sleep quality by phase

**Insight examples:**
- *"You sleep best in follicular phase — estrogen helps. You sleep worst in late luteal — progesterone withdrawal disrupts it."*
- *"Menstrual phase sleep is hit-or-miss for you. Cramps waking you up? Magnesium before bed might help."*
- *"Your sleep stays solid across your cycle — you're lucky, or your sleep hygiene is chef's kiss."*

**Confidence:** "Based on [N] cycles of sleep logs"

---

### 4.6 Energy Levels by Phase

**Data source:** `daily_logs.energy` (1–5 from morning gate)

**Calculated:**
- Average energy per phase
- Highest-energy phase
- Lowest-energy phase
- Energy trajectory (rising/falling within phases)

**Chart:** Line graph of energy across cycle, with phase color-coding

**Insight examples:**
- *"Your energy bottoms out Days 1–3, then climbs through follicular. Schedule light days early, power days mid-cycle."*
- *"You stay pretty energized until Day 24, then crash. That's progesterone dropping — not you failing."*
- *"You're a unicorn — your energy stays stable all cycle. Use it."*

**Confidence:** "Consistent pattern across [N] cycles"

---

### 4.7 Mood Stability by Phase

**Data source:** `daily_logs.mood` (1–5 from morning gate)

**Calculated:**
- Average mood per phase
- Mood stability (low standard deviation = stable)
- Most volatile phase
- Most stable phase

**Chart:** Line graph with confidence bands (shaded area showing mood range)

**Insight examples:**
- *"Your mood is steady through follicular and ovulatory, then gets rocky late luteal. That's the estrogen-progesterone crash — it's chemistry, not character."*
- *"You tend to feel lowest on Days 25–27. Mark it on your calendar. Prep your environment, lower demands, be gentle."*
- *"Your mood stays pretty even — if that changes suddenly, check in with yourself or your doctor."*

**Privacy note:** In-app only for sensitive mood insights.

**Confidence:** "Observed in [N] cycles"

---

### 4.8 Cravings by Phase

**Data source:** `daily_logs.cravings[]` (Carbs, Sweet, Chocolate, etc.)

**Calculated:**
- Which cravings appear in which phase (frequency %)
- Peak craving window
- Craving intensity (Mild vs. Strong)

**Chart:** Stacked bar or bubble chart showing craving types by phase

**Insight examples:**
- *"You crave chocolate Days 20–26 like clockwork. Keep the 70%+ dark stuff stocked — it's magnesium, not weakness."*
- *"Carb cravings spike in late luteal. Your metabolism is higher then — you actually need more fuel."*
- *"You don't report many cravings. Either you're very zen or you're not logging them — both valid."*

**Confidence:** "Appeared in [N] out of [M] cycles"

---

### 4.9 Pain Patterns

**Data source:** `daily_logs.pain_symptoms[]` (Cramps, Headaches, Back pain, etc.)

**Calculated:**
- Which pain types appear when
- Worst pain days
- Pain-free phases

**Chart:** Heatmap of pain intensity by cycle day

**Insight examples:**
- *"Cramps hit hardest Day 1–2, then ease. Front-load your magnesium and heat."*
- *"Headaches cluster around Day 14 (ovulation) and Day 26 (late luteal) — both are estrogen-drop moments."*
- *"Lower back pain shows up menstrual phase — prostaglandins radiating. Stretching + anti-inflammatory foods help."*

**Confidence:** "Happened in [N] cycles"

---

### 4.10 Skin Breakouts

**Data source:** `daily_logs.skin_symptoms[]` (Acne, Oily, Sensitivity, etc.)

**Calculated:**
- When breakouts typically start
- Which phase is worst
- Skin-clear phases

**Chart:** Timeline showing breakout frequency by cycle day

**Insight examples:**
- *"Your skin breaks out Days 18–25 — rising progesterone = more oil. Salicylic acid is your friend."*
- *"You're usually clear follicular and ovulatory, then breakouts hit late luteal. Timing skincare around it helps."*
- *"No strong skin pattern yet — keep logging if it bothers you."*

**Confidence:** "Seen in [N] cycles"

---

### 4.11 Exercise Performance

**Data source:** `movement_checklist` (intensity logged) + `daily_logs.energy`

**Calculated:**
- Phases with most high-intensity workouts
- Phases with most rest days
- Correlation between logged intensity and phase

**Chart:** Bar chart of workout intensity distribution by phase

**Insight examples:**
- *"You crush high-intensity workouts in follicular and ovulatory — that's peak testosterone and estrogen. Use it."*
- *"You naturally rest more in menstrual and late luteal. That's alignment, not laziness."*
- *"You're steady across your cycle — if that feels good, keep it. If you're forcing it, ease up late luteal."*

**Confidence:** "Based on [N] cycles of logged movement"

---

### 4.12 Focus & Productivity

**Data source:** `daily_logs.mood_state[]` (alert, distracted, etc.) + user-reported focus logs (future feature)

**Calculated:**
- Phases with highest "alert" logs
- Phases with most "distracted" logs

**Chart:** Line graph of focus/distraction frequency

**Insight examples:**
- *"You report feeling sharpest in follicular and ovulatory. Book deep work, tough meetings, and learning then."*
- *"Late luteal brain fog is real for you — batch admin work, delegate what you can, forgive the rest."*

**Confidence:** "Based on [N] cycles"

---

### 4.13 Weight & Bloating Fluctuations

**Data source:** `daily_logs.body_changes[]` (Water retention)

**Calculated:**
- When bloating is most common
- Typical bloat window duration

**Chart:** Timeline of water retention frequency

**Insight examples:**
- *"You bloat every late luteal phase, peaking Days 24–27. It's progesterone-driven water retention, not fat. Drink more water (counterintuitive but true)."*
- *"Bloating eases once your period starts. If it doesn't, check your salt and fiber intake."*

**Confidence:** "Consistent in [N] cycles"

---

## 5. Advanced Insights — Correlations

*(Unlocks after 4 cycles)*

**Purpose:** Surface patterns between behaviors and symptoms.

**Examples:**
- *"You logged eating a lot of sugar on Days 20–24. The next day, you rated your mood 2/5. Coincidence? Maybe not."*
- *"When you skip workouts in follicular, your energy dips. Moving helps you feel better."*
- *"Heavy flow days = low iron logs. Load up on spinach, lentils, and red meat (if applicable) during your period."*

**Tone:** Observational, not prescriptive. "We noticed X. You decide if it matters."

**UI:** Collapsible "Possible Connections" section at bottom of Trends page.

---

## 6. Next Period Prediction

**Data source:** Average cycle length + last period start date + regularity (standard deviation)

**Calculated:**
- Predicted start date
- Confidence band (±N days based on regularity)
- Confidence percentage

**Display:**
- On Trends summary card
- On Calendar view (dashed circle on predicted date already exists — add confidence % tooltip)
- On Home page phase ring (small text below cycle day: "Period expected in 12 days")

**Insight examples:**
- ✅ **High confidence (regular cycles):** *"Period expected March 15 (confidence: 92%). You can plan around it."*
- ⚠️ **Medium confidence (somewhat irregular):** *"Period expected March 12–16 (confidence: 68%). Keep an eye out."*
- 🤷 **Low confidence (very irregular):** *"Period expected sometime next week, but your cycles vary a lot. We'll get better at this as you log more."*

---

## 7. Personalized Notifications

### 7.1 Notification Types & Timing

| Type | Timing | Examples |
|------|--------|----------|
| **Proactive** | Morning of predicted pattern day | "Based on your trends, you'll probably crave chocolate today. Dark chocolate (70%+) = magnesium win." |
| **Preparatory** | 1 day before predicted pattern | "Tomorrow's usually a low-energy day for you. Prep easy meals, clear your calendar if you can." |
| **Reactive** | After user logs something | "You logged low energy — totally normal for you on Day 3. Rest is the assignment." |
| **In-gate** | Inside morning mood/energy flow | Inline contextual message based on today's predicted patterns |
| **Banner** | Home page top | Small dismissible banner: "Heads up: Day 22 — when PMS usually starts for you" |
| **Push (optional)** | User setting in Settings > Notifications | Off by default for sensitive topics. User can enable. |

---

### 7.2 Notification Categories & Examples

All written in **NutriSync voice: older sister, warm, witty, cheeky, validating, never condescending.**

#### **Cravings**
- *"Chocolate o'clock. You crave it every late luteal. Stock the good stuff (70%+ dark = magnesium MVP)."*
- *"Carb cravings incoming. Your metabolism's higher right now — you actually need more fuel. Go for sweet potato, oats, or sourdough."*

#### **Energy**
- *"Low-energy window starts today. This is when you usually crash. Clear space, nap if you can, don't fight it."*
- *"Your energy peaks this phase. Book the hard stuff, crush the HIIT, chase the PR. It's your time."*

#### **Mood**
*(In-app only, never push unless user opts in)*
- *"You tend to feel lowest Days 25–27. It's not in your head — it's in your hormones. Be extra gentle with yourself."*
- *"Follicular glow incoming. You usually feel sharper, lighter, more social now. Use it."*

#### **Sleep**
- *"Sleep gets rough for you in late luteal. Magnesium before bed, no screens after 9pm, and lower your expectations."*
- *"You sleep like a rock in follicular. If you've been putting off early mornings, now's the time."*

#### **Pain**
- *"Cramps usually hit tomorrow. Front-load magnesium, heat, and gentle movement today."*
- *"Headache alert: you get them around ovulation. Hydrate hard, skip the wine, keep caffeine steady."*

#### **Skin**
- *"Breakout zone starts Day 18 for you. Salicylic acid, hands off your face, and remember it's temporary."*

#### **Libido**
*(In-app only)*
- *"Your libido usually peaks this week. If you're feeling it, that's biology working as designed."*
- *"You're typically lower-libido late luteal. Totally normal. Progesterone's a sedative."*

#### **Exercise**
- *"You usually crush workouts this phase. Go heavy, go hard, go for it."*
- *"Rest week incoming. You log more rest days here, and that's smart — not lazy."*

#### **Period prediction**
- *"Period expected in 3 days (Day 1 usually = cramps + low energy for you). Prep snacks, clear space, be ready to rest."*
- *"Period's probably starting tomorrow. You've got this. Heating pad, magnesium, and Netflix queued up?"*

#### **Correlations**
- *"Last cycle you ate a ton of sugar Days 22–25, then felt awful. Coincidence? Try swapping for dark chocolate or fruit this time and see."*
- *"You skipped workouts last follicular and your energy tanked. Moving helps you feel better — even a walk counts."*

---

### 7.3 Notification Settings (User Control)

In **Settings > Notifications & Reminders**, add:

**Personalized Insights**
- ☑️ In-app banners (always on)
- ☐ Push notifications for predictions (off by default)
- ☐ Push notifications for sensitive insights (mood, libido) — off by default, explicit opt-in

**Frequency**
- Daily insights (default)
- Every other day
- Weekly summary only

**Topics I want to hear about:**
- Multi-select: Cravings, Energy, Sleep, Pain, Skin, Period predictions, Mood, Libido, Workouts, Correlations
- Default: all checked except Mood and Libido (in-app only unless user enables)

---

## 8. Database Schema Updates

### 8.1 New Table: `user_trends`

| Column | Type | Notes |
|--------|------|-------|
| id | uuid PK | |
| user_id | uuid FK | |
| trend_type | text | cycle_length, flow_heaviness, energy_by_phase, etc. |
| phase | text | null if trend is cycle-wide |
| cycle_day | integer | null if trend spans multiple days |
| pattern_value | jsonb | Flexible: stores averages, frequencies, lists, etc. |
| confidence_score | numeric | 0–100, based on consistency across cycles |
| cycles_observed | integer | How many cycles contributed to this trend |
| first_detected | date | When pattern first appeared |
| last_updated | timestamptz | |

**Example row:**
```json
{
  "trend_type": "cravings_by_phase",
  "phase": "late_luteal",
  "pattern_value": {
    "chocolate": 0.80,  // 80% of late luteal days
    "carbs": 0.65,
    "sweet": 0.55
  },
  "confidence_score": 85,
  "cycles_observed": 5
}
```

---

### 8.2 New Table: `user_notifications`

| Column | Type | Notes |
|--------|------|-------|
| id | uuid PK | |
| user_id | uuid FK | |
| notification_type | text | proactive, preparatory, reactive, correlation |
| category | text | cravings, energy, sleep, pain, etc. |
| message | text | Full notification text in NutriSync voice |
| scheduled_for | date | Which day to show it |
| displayed | boolean | Default false |
| displayed_at | timestamptz | When user saw it |
| dismissed | boolean | |
| created_at | timestamptz | |

---

### 8.3 Update Existing: `users` table

Add:
- `trends_unlocked` boolean (true after 2 cycles)
- `advanced_insights_unlocked` boolean (true after 4 cycles)

---

## 9. Pattern Recognition Logic

### 9.1 When to Calculate Trends

**Trigger:** After user logs a new period start date (cycle completion).

**Process:**
1. Count total completed cycles for user
2. If `completed_cycles >= 2`:
   - Calculate basic trends (cycle length, period duration, phase averages)
   - Set `trends_unlocked = true`
3. If `completed_cycles >= 3`:
   - Calculate symptom patterns, cravings, pain timing, skin, libido
   - Generate confidence scores
4. If `completed_cycles >= 4`:
   - Calculate correlations
   - Unlock "Your Unique Cycle" summary
   - Set `advanced_insights_unlocked = true`

**DEV NOTE:** Run as a background job (Supabase Edge Function or cron) — don't block the UI.

---

### 9.2 Confidence Scoring Formula

**Confidence % = (cycles_where_pattern_appeared / total_cycles) × 100**

**Thresholds:**
- ≥80% = "Strong pattern — this is your normal"
- 60–79% = "Common pattern — happened in X out of Y cycles"
- 40–59% = "Possible pattern — we're still watching"
- <40% = Don't surface (not reliable yet)

**Example:**
- User has 5 logged cycles
- Chocolate cravings appeared in late luteal in 4 of them
- Confidence = (4/5) × 100 = 80%
- Display: *"Strong pattern (4 out of 5 cycles)"*

---

### 9.3 Generating Notifications

**Daily cron job (runs at 6am user local time):**

1. Get user's current cycle day
2. Query `user_trends` for patterns matching today's cycle day or phase
3. Check `user_notifications` preferences (enabled categories, push vs. in-app only)
4. Generate notification text using templates + user-specific data
5. Insert into `user_notifications` table with `scheduled_for = today`
6. If push enabled + category allowed → send push
7. Banner/in-app always show (user can dismiss)

**Reactive notifications (triggered by logging):**
- User logs low energy on Day 3 → check if that's a pattern for them → show: *"Totally normal for you on Day 3"*
- User logs craving chocolate on Day 24 → check pattern → show: *"Called it. You crave this every late luteal."*

---

## 10. UI/UX Considerations for Lucía

### 10.1 Trends Page Layout

**Top:**
- Summary card: "Your Unique Cycle" (large, warm cream background, coral accents)

**Middle (scrollable):**
- Category cards in vertical stack
- Each card:
  - Icon (cycle length 🔁, energy ⚡, mood 💭, sleep 😴, cravings 🍫, etc.)
  - Title
  - Mini chart (line, bar, heatmap, bubble — depends on data type)
  - Insight text (2–3 sentences max, NutriSync voice)
  - Confidence badge (e.g., "85% confident • 4 cycles")
  - Optional "Learn more" expand for deeper details

**Bottom:**
- "Possible Connections" section (correlations, if unlocked)

**Empty state (0–1 cycles):**
- Nutri mascot
- "We're learning your rhythm — keep logging to unlock insights!"
- Progress bar: "1 of 2 cycles logged"

---

### 10.2 Notification Display

**In-app banner (Home page):**
- Small dismissible card below phase ring
- Icon + one-liner
- Tap to expand for full insight
- Dismiss = swipe away or X button

**Inside mood/energy gate:**
- After user logs energy/mood, show inline contextual message if pattern detected
- Example: User logs energy 2/5 → *"Low energy today? That's your normal on Day 3. Rest is alignment."*

**Push notification (if enabled):**
- Short, non-sensitive
- Example: "Period expected in 3 days — prep mode activated 🧡"
- Tap → opens Trends page or Home

---

### 10.3 Chart/Graph Suggestions

| Trend Type | Chart Type |
|------------|-----------|
| Cycle length over time | Line graph with phase color bands |
| Flow heaviness | Stacked bar (light/medium/heavy/very heavy per cycle) |
| Energy by phase | Line graph with shaded phase backgrounds |
| Mood stability | Line with confidence band (shaded range) |
| Cravings | Bubble chart or stacked horizontal bars |
| Pain patterns | Heatmap (cycle day × pain type) |
| Sleep quality | Bar chart (average per phase) |
| Libido | Line graph |
| Skin breakouts | Timeline with breakout markers |
| Exercise intensity | Stacked bar (rest/low/moderate/high per phase) |

**Design note:** Keep charts **simple and scannable** — not overwhelming. Use phase colors for consistency.

---

## 11. Content Writing — Notification Templates

### Template Structure:
1. **Hook** — acknowledge the pattern
2. **Context** — why it happens (science in plain language)
3. **Action** — what to do (if applicable)

### Examples by Category:

**Cravings:**
- *"Chocolate incoming. You crave it Days 22–26 like clockwork. Dark chocolate (70%+) has magnesium — your body's asking for it, not testing your willpower."*
- *"Carb cravings starting. Your metabolism runs 100–300 cal higher in luteal — you actually need more fuel. Sweet potato, oats, sourdough = smart picks."*

**Energy:**
- *"Low-energy zone. This is when you crash every cycle. Your body's doing heavy hormonal lifting behind the scenes. Rest isn't optional — it's the assignment."*
- *"Energy peak unlocked. You're in your power phase — estrogen + testosterone are maxed out. Book the big meetings, crush the HIIT, go for it."*

**Mood:**
- *"Mood dip incoming. Days 25–27 are tough for you — estrogen and progesterone crash together. It's chemistry, not character. Be extra gentle."*
- *"Follicular glow starts now. You usually feel lighter, sharper, more social. If you've been putting off tough convos or creative work, this is your window."*

**Sleep:**
- *"Sleep gets messy for you late luteal. Progesterone withdrawal + cramps + night sweats = rough nights. Magnesium before bed, cooler room, lower expectations."*
- *"You sleep like a rock this phase. If you've been putting off early-morning workouts or sunrise plans, now's the time."*

**Pain:**
- *"Cramps usually hit tomorrow for you (Day 2 = worst day). Front-load magnesium today, heat on standby, gentle movement helps more than you'd think."*
- *"Headache alert: you get them around ovulation when estrogen drops. Stay hydrated, keep caffeine steady (don't spike or crash), and rest if you can."*

**Skin:**
- *"Breakout window opening. Days 18–25 = oily skin + clogged pores for you. Rising progesterone = more sebum. Double cleanse, salicylic acid, hands off your face."*

**Libido:**
- *"Your libido usually peaks this week (ovulation = biology's sales pitch for pregnancy). If you're feeling it, lean in. If not, that's fine too."*
- *"You're typically lower-libido late luteal. Progesterone's a sedative — it's not you, it's hormones. No pressure."*

**Workouts:**
- *"You crush high-intensity stuff this phase. Estrogen + testosterone = strength, stamina, fast recovery. Go heavy, go hard."*
- *"Rest week for you. You log more yoga, walking, and off-days late luteal — and that's smart. Rest is alignment when your body's asking for it."*

**Period Prediction:**
- *"Period expected in 3 days (confidence: 88%). Day 1 usually = low energy + cramps for you. Prep snacks, heat, cozy plans."*
- *"Period's probably starting tomorrow. You've got this. Heating pad charged? Dark chocolate stocked? Let's go."*

**Correlations:**
- *"Last cycle: lots of sugar Days 22–25 → mood tanked. Try swapping for fruit, dark chocolate, or nut butter this time and see if it helps."*
- *"You skipped workouts last follicular, then logged low energy all week. Moving (even just walking) seems to help you feel better. Worth testing again."*

---

## 12. Developer Implementation Checklist

### Phase 1: Data Infrastructure
- [ ] Create `user_trends` table
- [ ] Create `user_notifications` table
- [ ] Update `users` table with `trends_unlocked`, `advanced_insights_unlocked`
- [ ] Build pattern recognition logic (background job after cycle completion)
- [ ] Build confidence scoring formula
- [ ] Build notification generation logic (daily cron + reactive triggers)

### Phase 2: Trends Page UI
- [ ] Build "Your Unique Cycle" summary card (4+ cycles only)
- [ ] Build category cards with charts + insights
- [ ] Implement chart library (Recharts, Chart.js, or similar)
- [ ] Build empty state (0–1 cycles)
- [ ] Build early insights disclaimer (2 cycles)
- [ ] Build "Possible Connections" section (4+ cycles)

### Phase 3: Notifications
- [ ] Build in-app banner component (Home page)
- [ ] Build inline contextual messages (mood/energy gate)
- [ ] Build notification settings screen
- [ ] Implement push notification logic (optional, user-controlled)
- [ ] Write all notification templates in NutriSync voice
- [ ] Test sensitive topic privacy (mood, libido = in-app only by default)

### Phase 4: Testing & Refinement
- [ ] Test with synthetic user data (2, 3, 4, 5+ cycles)
- [ ] Validate pattern accuracy
- [ ] Validate confidence scoring
- [ ] Test notification timing
- [ ] Test notification preferences (opt-in/opt-out)
- [ ] User testing with beta group
- [ ] Iterate based on feedback

---

## 13. Future Enhancements (Post-MVP)

- **Community comparison (anonymized):** "Your cycles are 2 days longer than the community average — totally normal, just your unique rhythm."
- **Export trends as PDF:** For sharing with doctors
- **Voice-based insights:** Audio summaries of trends
- **Integration with wearables:** Sleep tracking from Apple Watch, Oura, etc.
- **AI-powered correlations:** More sophisticated pattern detection (e.g., stress + diet + symptoms)

---

**End of Trends + Personalized Notifications Specification**

NutriSync Collective | Version 1.0 | January 2025
