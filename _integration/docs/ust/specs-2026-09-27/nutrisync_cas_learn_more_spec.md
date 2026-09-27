# NutriSync — CAS Component Breakdown "Learn More" Screen Specification
**Feature Addition: Detailed CAS Component Education & Improvement Guidance**  
**Version:** 1.0 | September 2026  
**For integration into existing NutriSync Developer Specification v1.0**

---

## 1. Feature Overview

Replace the current tap-on-ring tooltip behavior on the Progress page with a comprehensive **"Learn More"** screen that provides detailed explanations of all 5 CAS components, personalized feedback, and actionable improvement guidance.

### Current State
- Progress page shows 5 mini rings (Phase Confidence / Biomarkers / Nutrition / Recovery / Logging)
- User can tap each ring to see a small tooltip explanation
- No detailed guidance on how to improve each component

### New State
- "Learn More" button appears below the 5 mini rings
- Tapping "Learn More" opens a new full-page screen within the Progress tab
- Screen explains all 5 components in detail with personalized feedback and actionable CTAs
- Remove tap-on-ring tooltip behavior (replaced by this comprehensive screen)
- Back button returns to main Progress view

---

## 2. User Flow

### Entry Point
**Progress Page → "Learn More" button (below the 5 mini component rings)**

User taps "Learn More" → New screen slides in → Shows all 5 components broken down → User can scroll through all → "Back" button returns to Progress

### Navigation
- Header: Back arrow (←) + "How to Improve Your Score" title
- Scrollable content showing all 5 components in sequence
- Optional: jump-to-section navigation if content is long

---

## 3. Screen Structure

Each of the 5 CAS components gets a dedicated section with:

### 3-Tier Explanation Structure

**Tier 1: What It Is (1-2 sentences)**  
Short, clear definition in plain language

**Tier 2: Why It Matters (2-3 sentences)**  
The science behind it + why it affects alignment

**Tier 3: How to Improve (3-5 actionable bullet points)**  
Specific steps the user can take RIGHT NOW

### Personalized Feedback Logic

Content adapts based on user's current score for that component:

- **High score (80%+ of max):** Celebrate + maintain
- **Medium score (50-79%):** Encourage + specific tips
- **Low score (<50%):** Educate + clear action plan

### Actionable CTAs

Each section includes relevant action buttons:
- "Log Your Period" (if Phase Confidence is low)
- "Check Today's NutriLog" (if Nutrition is low)
- "Log Today's Movement" (if Recovery is low)
- "Complete Your Logs" (if Logging Consistency is low)

---

## 4. Component 1: Phase Detection Confidence (max 15 pts)

### What It Is
"Phase Detection Confidence measures how accurately NutriSync can predict which phase of your cycle you're in today."

### Why It Matters
"Your cycle phase determines your hormonal environment — and your hormonal environment determines your body's nutritional and recovery needs. The more accurately we know your phase, the more personalized your recommendations become."

### How to Improve

**Personalized feedback logic:**

#### If score is 10/15 (high):
"You're already doing great! You have a period start date on file and you're logging actively. Keep it up."

**Action items:**
- ✅ Keep logging your period start date each cycle
- ✅ If your cycle changes significantly, update it in Edit Period
- 💡 After 3 logged cycles, we'll use YOUR patterns instead of population averages

#### If score is 5/15 (medium):
"You've logged a period date, but we can be even more accurate. Logging your period consistently every cycle helps us fine-tune your phase predictions."

**Action items:**
- 📅 Log your period start date when it arrives
- 🔄 Update your cycle length in Settings if it changes
- 📊 After 2 more logged cycles, we'll have enough data to personalize your phase boundaries

**CTA Button:** "Log Your Period" (navigates to Edit Period screen)

#### If score is 0/15 (low):
"We don't have a period start date on file yet, so we can't calculate your phase or personalize recommendations. This is the single most important thing you can log."

**Action items:**
- 🚨 Log when your last period started (or when your next one starts)
- 📲 This unlocks all phase-based recommendations
- 🎯 This is worth 15 points toward your daily CAS score

**CTA Button:** "Log Your Period Now" (navigates to Edit Period screen, highlights period start date field)

---

### Special Case: Contraception Users

**If user is on hormonal contraception:**

"You're on hormonal contraception, which suppresses natural ovulation. Your Phase Detection Confidence is capped at 12/15 because your cycle phases work a bit differently — and that's completely normal. You're not being penalized; the app is adjusting to your reality."

**Action items:**
- ✅ Keep logging your withdrawal bleed or period
- 📖 We adapt recommendations to account for synthetic hormones
- 💡 Your patterns still matter — we learn what works for YOUR body

---

## 5. Component 2: Physiological Biomarker Signals (max 25 pts)

### What It Is
"Biomarker Signals track how your energy, mood, sleep, appetite, and physical performance align with what your body physiologically needs in each phase."

### Why It Matters
"This isn't about being 'good' or 'bad' — it's about alignment. Low energy in your menstrual phase is ALIGNED (you get full points). High energy in menstrual when you should be resting is MISALIGNED (you lose points). We're measuring whether you're in sync with your hormones, not judging your health."

### How to Improve

**Personalized feedback logic:**

#### If score is 20-25/25 (high):
"You're incredibly in tune with your cycle. Your logged biomarkers match your hormonal reality almost perfectly."

**What this means:**
- Your energy dips when estrogen/progesterone drop → aligned ✅
- Your mood stabilizes when estrogen rises → aligned ✅
- Your appetite increases in luteal when metabolism revs up → aligned ✅

**Keep doing:**
- ✅ Log your mood and energy every day (morning gate)
- ✅ Use Edit Period to track sleep, cravings, and symptoms
- 💡 After 3 cycles, we'll compare you to YOUR OWN patterns, not population averages

#### If score is 12-19/25 (medium):
"You're somewhat aligned, but there are a few mismatches between what you're logging and what your hormones are doing."

**Common reasons for misalignment:**
- 🔴 High energy in menstrual phase (your body is asking you to rest)
- 🔴 Low energy in follicular/ovulatory (when estrogen peaks)
- 🔴 Very stable mood in late luteal (hormonal crash typically causes variability)

**How to improve:**
- 📊 Check your Daily Tip each day — it explains what's happening hormonally
- 🛌 Prioritize sleep in late luteal and menstrual (this is when your body needs it most)
- 🍫 Honor cravings in luteal (your metabolism is genuinely higher, not "broken")
- 🏃‍♀️ Rest when recommended — rest IS alignment when your hormones are low

**CTA Button:** "See Today's Recommendations" (navigates to NutriLog)

#### If score is 0-11/25 (low):
"Your logged biomarkers suggest you might be pushing through when your body is asking for rest, or resting when your body has energy to burn."

**This often means:**
- You're not logging consistently (missing data = 0 points)
- You're overriding your body's signals (working out hard on Day 2, or skipping workouts in follicular when you feel great)
- Your sleep, mood, or energy patterns don't match your phase

**How to fix it:**
- 📲 Log mood + energy EVERY day (it's just 2 taps in the morning gate)
- 🛌 Log sleep quality in Edit Period
- 📖 Read your Body Insight to understand what's normal for this phase
- 🎯 Trust the science: low energy in menstrual isn't failure, it's biology

**CTA Button:** "Complete Today's Logs" (navigates to Edit Period screen)

---

### The 5 Sub-Metrics Explained

**1. Energy Alignment (5 pts)**
- Menstrual: Low energy = 5/5 ✅
- Follicular: Rising energy = 5/5 ✅
- Ovulatory: Peak energy = 5/5 ✅
- Luteal: Moderate early, lower late = 5/5 ✅

**2. Mood Stability (5 pts)**
- Late luteal mood swings = NORMAL and ALIGNED (5/5) ✅
- We NEVER penalize expected hormonal mood variability

**3. Sleep Quality (5 pts)**
- Logged via Edit Period
- Follicular/ovulatory: good sleep expected
- Late luteal: fragmented sleep is NORMAL (still 5/5) ✅

**4. Appetite (5 pts)**
- Luteal phase: increased appetite/cravings = ALIGNED (5/5) ✅
- Progesterone raises metabolism ~100-300 kcal/day — your body needs more food

**5. Physical Performance (5 pts)**
- Pulled from MovementLog
- Rest in menstrual = aligned ✅
- HIIT in ovulatory = aligned ✅

---

## 6. Component 3: Nutrition Alignment (max 30 pts)

### What It Is
"Nutrition Alignment measures whether the meals you're logging contain the nutrients your body needs TODAY, based on your current cycle phase and NutriGoal."

### Why It Matters
"Your nutritional needs change across your cycle. In menstrual, you need iron and anti-inflammatory foods. In luteal, you need magnesium and B6 to reduce PMS. Eating the right nutrients at the right time reduces symptoms, stabilizes mood and energy, and supports your hormonal health."

### How to Improve

**Personalized feedback logic:**

#### If score is 24-30/30 (high):
"You're nailing it. The meals you're logging are hitting the nutrients your body needs right now."

**Keep it up:**
- ✅ Keep scanning/logging your meals daily
- ✅ Check the 3 recommended meals each day for inspiration
- 💡 Your NutriGoal (**[user's actual NutriGoal]**) is shaping these recommendations

**What you're doing right:**
- [If menstrual] You're prioritizing iron, omega-3s, and anti-inflammatory foods
- [If follicular] You're eating lean protein and fiber to support rising estrogen
- [If ovulatory] You're loading up on antioxidants and cruciferous veg
- [If luteal] You're getting magnesium, B6, and complex carbs to manage PMS

#### If score is 15-23/30 (medium):
"You're logging meals, but they're missing some key nutrients for this phase."

**What's missing:**
- [If menstrual] Not enough iron or omega-3s (your body is bleeding and inflamed)
- [If follicular] Low protein or fiber (needed to support estrogen metabolism)
- [If ovulatory] Missing antioxidants (protect your peak hormone levels)
- [If luteal] Not enough magnesium or B6 (these reduce PMS symptoms)

**How to improve:**
- 🍽️ Check today's 3 recommended meals before you eat
- 📸 Scan your meals so we can track nutrient density
- 🎯 Focus on the nutrients tagged in your recommendations

**CTA Button:** "See Today's Meal Recs" (navigates to NutriLog, scrolls to meal recommendations)

#### If score is 0-14/30 (low):
"You're either not logging meals, or the meals you're logging aren't nutrient-aligned with your phase."

**Why this matters:**
- You're missing out on symptom relief (magnesium reduces cramps, omega-3s reduce inflammation)
- Your energy and mood are harder to stabilize without the right fuel
- PMS symptoms worsen when you don't eat phase-supportively in luteal

**How to fix it:**
- 📲 Log at least ONE meal per day (scan or type)
- 🍽️ Use the 3 recommended meals as a guide
- 📖 Read your Daily Tip to see which nutrients matter today
- 🎯 Prioritize whole foods over processed (higher nutrient density)

**CTA Button:** "Log a Meal Now" (navigates to NutriLog, opens scan/log interface)

---

### Your NutriGoal Matters

**The app shows this section dynamically based on user's selected NutriGoal:**

**If NutriGoal = "Reduce PMS Symptoms":**
"Your meal recommendations prioritize magnesium, B6, calcium, and omega-3s — nutrients proven to reduce cramping, bloating, and mood swings."

**If NutriGoal = "Emotional Balance":**
"Your meal recommendations prioritize tryptophan, omega-3s, and B vitamins — nutrients that support serotonin production and mood stability."

**If NutriGoal = "Stable Energy":**
"Your meal recommendations prioritize complex carbs + protein combos, and flag caffeine/sugar — keeping your blood sugar stable prevents crashes."

**If NutriGoal = "Fewer Mood Crashes":**
"Your meal recommendations prioritize serotonin-supporting foods (tryptophan, B6, magnesium) and blood sugar stabilizers, especially in late luteal."

---

## 7. Component 4: Fitness / Recovery Alignment (max 20 pts)

### What It Is
"Fitness/Recovery Alignment measures whether your movement and rest patterns match your body's physical capacity on this day of your cycle."

### Why It Matters
"Your strength, stamina, and recovery capacity fluctuate with your hormones. Ovulatory phase = peak power. Menstrual phase = lowest recovery capacity. Moving in sync with your cycle prevents burnout, reduces injury risk, and helps you perform better when your body is ready."

### How to Improve

**Personalized feedback logic:**

#### If score is 16-20/20 (high):
"You're moving with your cycle, not against it. Your logged workouts match your body's physical capacity perfectly."

**What this looks like:**
- [If menstrual] You're resting, walking, or doing gentle yoga
- [If follicular] You're ramping up intensity — strength, cardio, moderate-high effort
- [If ovulatory] You're going ALL OUT — HIIT, heavy lifts, personal bests
- [If luteal] You're dialing it back as your period approaches — moderate early, gentle late

**Keep doing:**
- ✅ Log your movement daily (even rest days count!)
- ✅ Listen to your body — rest IS alignment when hormones are low
- 💡 Check MovementLog recommendations before you work out

#### If score is 10-15/20 (medium):
"You're moving, but not quite in sync with your hormonal reality."

**Common misalignments:**
- 🔴 Doing HIIT in menstrual phase (your body can't recover well right now)
- 🔴 Resting in ovulatory phase (you're at PEAK strength and stamina — use it!)
- 🔴 Pushing hard every day in late luteal (progesterone is a sedative; your body needs lower intensity)

**How to improve:**
- 📊 Check your MovementLog recommendations BEFORE you work out
- 🏋️‍♀️ Save your hardest workouts for ovulatory phase (Days 14-16)
- 🛌 Rest guilt-free in menstrual and late luteal — it's not laziness, it's strategy
- 🎯 Match intensity to phase: low → moderate → high → moderate → low

**CTA Button:** "See Today's Movement Rec" (navigates to MovementLog)

#### If score is 0-9/20 (low):
"You're either not logging movement, or you're significantly out of sync with your cycle."

**Why this matters:**
- Overtraining in low-hormone phases increases cortisol and injury risk
- Undertraining in high-hormone phases wastes your body's peak performance window
- Ignoring your cycle leads to burnout, fatigue, and worse results

**How to fix it:**
- 📲 Log your movement EVERY day (even if it's just "rest day" or "10k steps")
- 🏃‍♀️ Follow the MovementLog recommendations — they're science-backed
- 🛌 Rest when recommended (it counts toward your score!)
- 📖 Read your Body Insight to understand why your capacity changes

**CTA Button:** "Log Today's Movement" (navigates to MovementLog)

---

### Special Case: Fitness Opt-Out

**If user opted out of fitness tracking during onboarding:**

"You opted out of fitness tracking, so this component is automatically set to 10/20. If you want to improve this score, you can turn on fitness tracking in Settings."

**CTA Button:** "Turn On Fitness Tracking" (navigates to Settings → Preferences)

---

## 8. Component 5: Logging Consistency (max 10 pts)

### What It Is
"Logging Consistency measures whether you're completing the 4 core daily logs: mood, energy, nutrition, and movement."

### Why It Matters
"NutriSync can't personalize to your patterns if it doesn't have data. The more consistently you log, the smarter the app becomes — and the more accurate your CAS score, phase predictions, and recommendations become."

### How to Improve

**Personalized feedback logic:**

#### If score is 10/10 (perfect):
"You logged all 4 core items today. You're giving NutriSync everything it needs to learn your unique patterns."

**What you logged:**
- ✅ Mood (morning gate)
- ✅ Energy (morning gate)
- ✅ Nutrition (meal logged)
- ✅ Movement (workout or rest day logged)

**Keep it up:**
- After 3 full cycles of consistent logging, we switch from population-level recommendations to YOUR OWN patterns
- Your insights on the Progress page get more accurate
- Your phase predictions get more personalized

#### If score is 7/10 (missing 1 log):
"You're almost there — you logged 3 out of 4 core items today."

**You logged:**
- ✅ Mood
- ✅ Energy
- [Example: Missing] ❌ Nutrition

**Complete your logs:**
- The 4 daily logs take less than 2 minutes total
- Every log improves your score and feeds the learning engine
- Missing data = the app can't personalize as well

**CTA Button:** "Complete Today's Logs" (navigates to whichever screen has the missing log)

#### If score is 0-6/10 (missing 2+ logs):
"You're missing critical data today. Without consistent logging, NutriSync can't learn your patterns or give you personalized insights."

**What happens when you don't log:**
- Your CAS score is incomplete (missing data = 0 points for that component)
- We can't build your personal phase averages
- Recommendations stay generic instead of becoming personalized
- Progress insights stay surface-level

**How to fix it:**
- 📲 Set a daily reminder in Settings (morning for mood/energy, evening for meals/movement)
- 🎯 Aim for 4/4 logs every day
- 💡 Logging takes 2 minutes — but unlocks months of personalized insights

**CTA Button:** "Set Daily Reminder" (navigates to Settings → Notifications)

---

## 9. UI Placement & Navigation

### Entry Point
**Progress Page → Below the 5 mini component rings → "Learn More" button**

- Button style: Coral outlined pill button, centered
- Label: "Learn More" or "How to Improve Your Score"

### New Screen Layout

**Header:**
- Back arrow (←) top-left
- Title: "How to Improve Your Score"
- Optional: User's current total CAS in top-right (e.g., "87/100")

**Body:**
- Scrollable vertical content
- 5 sections (one per component) in order:
  1. Phase Detection Confidence
  2. Biomarker Signals
  3. Nutrition Alignment
  4. Fitness/Recovery Alignment
  5. Logging Consistency

**Section Structure (repeated 5 times):**
- Section header (component name + max points, e.g., "Phase Detection Confidence — up to 15 pts")
- Icon or mini visual (delegated to Lucía)
- "What It Is" paragraph
- "Why It Matters" paragraph
- "How to Improve" section:
  - Personalized intro sentence (based on user's score tier)
  - 3-5 bullet points
  - CTA button (if applicable)

**Footer:**
- "Back to Progress" button (navigates back to main Progress view)

### Design Flexibility (Delegated to Lucía)
- Section dividers (lines, cards, or spacing)
- Icons for each component
- Typography hierarchy
- CTA button styles
- Color accents (use phase colors or stick to coral)
- Optional: jump-to-section navigation at top

---

## 10. Personalization Logic — Developer Implementation

### Data Required for Personalization

For each component, pull:
- User's current score for that component (from `daily_scores` table, today's row)
- User's NutriGoal (from `users` table)
- User's current phase (calculated from `last_period_start_date`)
- User's contraception status (from `users` table)
- User's fitness opt-in status (from `users` table)
- Number of completed cycles (from `users.completed_cycles`)

### Conditional Content Rendering

**Example pseudocode for Component 3 (Nutrition Alignment):**

```javascript
const nutritionScore = user.daily_scores.component_3_nutrition; // 0-30
const nutriGoal = user.nutrigoal; // one of four goals
const currentPhase = user.current_phase; // menstrual/follicular/ovulatory/luteal

let feedbackTier;
if (nutritionScore >= 24) {
  feedbackTier = "high";
} else if (nutritionScore >= 15) {
  feedbackTier = "medium";
} else {
  feedbackTier = "low";
}

// Render personalized content
renderSection({
  title: "Nutrition Alignment — up to 30 pts",
  whatItIs: "Nutrition Alignment measures whether the meals you're logging...",
  whyItMatters: "Your nutritional needs change across your cycle...",
  howToImprove: getNutritionFeedback(feedbackTier, nutriGoal, currentPhase),
  cta: feedbackTier === "low" ? { label: "Log a Meal Now", action: navigateToNutriLog } : null
});
```

### CTA Button Actions

| Button Label | Navigation Target | Notes |
|--------------|-------------------|-------|
| "Log Your Period" | Edit Period screen | Pre-highlight period start date field |
| "See Today's Recommendations" | NutriLog screen | Scroll to meal recommendations |
| "See Today's Meal Recs" | NutriLog screen | Scroll to meal recommendations |
| "Log a Meal Now" | NutriLog screen | Open scan/log interface |
| "See Today's Movement Rec" | MovementLog screen | Scroll to daily tip |
| "Log Today's Movement" | MovementLog screen | Open log interface |
| "Complete Today's Logs" | Edit Period screen | Default view |
| "Set Daily Reminder" | Settings → Notifications | Pre-expand reminder section |
| "Turn On Fitness Tracking" | Settings → Preferences | Pre-expand fitness section |

---

## 11. Tone & Voice — NutriSync Style

All content is written in **NutriSync's "older sister" voice:**
- Warm, knowledgeable, slightly cheeky
- Validates the user's experience
- Science-backed but jargon-free
- Never shaming, always empowering

### Tone Examples (Already Integrated Above)

**Validating:**
- "Low energy in menstrual isn't failure, it's biology."
- "Cravings in luteal are NORMAL — your metabolism is genuinely higher."

**Educational:**
- "Progesterone is a sedative — your body physically can't perform at peak in late luteal."

**Motivational:**
- "You're at PEAK strength and stamina — use it!"
- "After 3 cycles, we'll compare you to YOUR OWN patterns, not population averages."

**Cheeky:**
- "Rest when recommended — it counts toward your score!"
- "The 4 daily logs take less than 2 minutes total."

---

## 12. Removal: Tap-on-Ring Tooltip

### Current Behavior (TO BE REMOVED)
- User taps a mini ring on Progress page
- Small tooltip appears explaining that component

### New Behavior
- Tapping a mini ring does nothing (or optionally: tapping opens the Learn More screen directly, scrolled to that component's section)
- All detailed explanations live on the new Learn More screen

**DEV NOTE:** Remove the tap event listener on the mini component rings, or redirect it to open the Learn More screen.

---

## 13. Developer Checklist

- [ ] Create new "Learn More" screen within Progress tab navigation
- [ ] Add "Learn More" button below the 5 mini rings on main Progress view
- [ ] Remove tap-on-ring tooltip behavior (or redirect to Learn More screen)
- [ ] Pull user's daily component scores from `daily_scores` table
- [ ] Pull user profile data: NutriGoal, phase, contraception status, fitness opt-in, completed cycles
- [ ] Implement 3-tier feedback logic for each component (high/medium/low score)
- [ ] Render personalized content based on user's current state
- [ ] Implement CTA buttons with correct navigation targets
- [ ] Add back button to return to main Progress view
- [ ] Test all 5 components with different score scenarios
- [ ] Test personalization edge cases (contraception users, fitness opt-out, etc.)
- [ ] Pass to Lucía for UI/visual design (icons, layout, spacing, colors)

---

## 14. Future Enhancements (Post-MVP)

- **Progress tracking:** Show user's improvement over time ("You've improved Nutrition Alignment by 12 pts since last cycle")
- **Inline tips:** Small "did you know?" cards between sections
- **Video explainers:** Short animated clips explaining each component
- **Personalized streak badges:** "7-day logging streak — keep it up!"

---

**End of Specification**

**For Questions or Clarifications:** Reach out to Pilar (@nutrisynccollective)