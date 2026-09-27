# NutriSync — Wellness State Feature Specification
**Feature Addition: Daily Wellness State Logging**  
**Version:** 1.1 | January 2025  
**For integration into existing NutriSync Developer Specification v1.0**

---

## 1. Feature Overview

Add a **daily wellness state logging option** to the morning mood/energy gate that allows users to flag when they are not feeling well. When logged, the app adapts that day's NutriLog and MovementLog recommendations to science-backed recovery guidance and adjusts CAS scoring to avoid penalizing rest and reduced activity when the user is genuinely unwell.

### Core Principles
- Rest and recovery are alignment when sick — not failure
- Recommendations prioritize evidence-based recovery support
- CAS scoring reflects physiological reality: being unwell is not the same as being out of sync
- The wellness state resets daily — users must re-log each day

---

## 2. User Flow Integration

### 2.1 Placement: Morning Mood & Energy Gate

**Current flow:**
1. User opens app
2. "Before we Sync..." gate appears
3. Mood slider (1-5)
4. Energy slider (1-5)
5. Home page

**New flow:**
1. User opens app
2. "Before we Sync..." gate appears
3. Mood slider (1-5)
4. Energy slider (1-5)
5. **NEW:** "Not feeling well today?" toggle or button
   - If YES → wellness category selector appears
   - If NO → proceed to home page
6. Home page

**UI Placement:**
- After energy slider, before "next" CTA
- Presented as a soft opt-in: "Not feeling well today?" with a toggle or pill button
- Tapping YES expands to show 6 category options (see below)
- **Design decision delegated to Lucía** — can be toggle, expandable card, or modal

### 2.2 Wellness State Categories

Users select ONE category per day:

| Category | Icon Suggestion | Short Description |
|----------|----------------|-------------------|
| **Sick** | 🤒 | Cold, flu, fever, illness |
| **Hungover** | 🥴 | Alcohol recovery |
| **Exhausted** | 😴 | Extreme fatigue, burnout |
| **Digestive Issues** | 🤢 | Nausea, stomach pain, IBS flare |
| **Headache/Migraine** | 🤕 | Head pain, migraine |
| **Injured** | 🩹 | Physical injury, pain, recovery |

**Visual treatment:**
- Icons or text tags in a scrollable horizontal pill selector
- Selected category highlighted in coral
- "Confirm" CTA updates wellness_state for the day

**Daily reset:**
- Wellness state is date-scoped
- Every calendar day, the flag is cleared
- User must re-select if still unwell the next day

---

## 3. Modified Recommendations Logic

When a wellness state is logged, **both NutriLog and MovementLog swap to recovery-specific content** for that day, overriding the standard phase-based recommendations.

### 3.1 NutriLog Recovery Recommendations

#### **SICK (Cold/Flu/Fever)**

**Nutritional priorities:** Immune support, hydration, easy-to-digest foods, anti-inflammatory nutrients

**Recommended foods:**
- **Hydration:** Water, coconut water, herbal teas (ginger, chamomile, peppermint), bone broth
- **Vitamin C:** Citrus fruits, bell peppers, strawberries, kiwi, orange juice
- **Zinc:** Pumpkin seeds, chickpeas, lentils, chicken (if applicable)
- **Anti-inflammatory:** Turmeric, ginger, garlic, honey
- **Easy protein:** Chicken soup, eggs (if applicable), Greek yogurt (if applicable), tofu
- **Warm & comforting:** Soups, stews, oatmeal, mashed sweet potato

**Daily Tip (example):**  
"Your immune system is working overtime. Hydrate constantly, load up on vitamin C and zinc, and stick to warm, easy-to-digest foods. Rest is medicine."

**Body Insight (example):**  
"When you're fighting an infection, your body diverts energy to immune function. Cytokines trigger fatigue to force you to rest — it's not laziness, it's biology doing its job."

---

#### **HUNGOVER**

**Nutritional priorities:** Rehydration, electrolyte replenishment, blood sugar stabilization, liver support, anti-nausea

**Recommended foods:**
- **Hydration + electrolytes:** Coconut water, water with lemon, electrolyte drinks (low-sugar), herbal teas
- **Blood sugar stabilization:** Bananas, oats, toast with nut butter, sweet potato
- **B vitamins (alcohol depletes):** Eggs, avocado, spinach, whole grains
- **Anti-nausea:** Ginger tea, crackers, plain rice
- **Liver support:** Beets, leafy greens, lemon water
- **Protein (gentle):** Eggs, Greek yogurt (if applicable), chicken, tofu

**Avoid:** Caffeine (dehydrates further), greasy fried foods, refined sugar

**Daily Tip (example):**  
"Rehydrate first, then stabilize blood sugar. Coconut water, eggs, bananas, and ginger tea are your best friends today. Skip the greasy takeout — it'll make you feel worse."

**Body Insight (example):**  
"Alcohol is a diuretic and a toxin. Your liver is working hard to clear acetaldehyde while you're dehydrated and depleted of B vitamins and electrolytes. Food is damage control."

---

#### **EXHAUSTED**

**Nutritional priorities:** Sustained energy (no crashes), adrenal support, magnesium, B vitamins, blood sugar stability

**Recommended foods:**
- **Complex carbs + protein:** Oats with nut butter, quinoa bowls, whole grain toast with eggs
- **Magnesium (adrenal support):** Dark chocolate (≥70%), almonds, spinach, pumpkin seeds, avocado
- **B vitamins (energy production):** Eggs, bananas, chickpeas, sunflower seeds, leafy greens
- **Healthy fats:** Avocado, nuts, seeds, olive oil, salmon (if applicable)
- **Iron (if depleted):** Lentils, spinach, red meat (if applicable), pumpkin seeds
- **Hydration:** Water, herbal teas, coconut water

**Avoid:** Refined sugar (causes crashes), excessive caffeine (adrenal strain)

**Daily Tip (example):**  
"You're running on empty. Prioritize slow-release carbs, magnesium, and B vitamins. Skip the sugar and caffeine — they'll crash you harder. Sleep is non-negotiable."

**Body Insight (example):**  
"Chronic fatigue often signals depleted cortisol and blood sugar dysregulation. Your adrenals need magnesium and rest, not another coffee. Eating for stable energy today protects tomorrow."

---

#### **DIGESTIVE ISSUES**

**Nutritional priorities:** Easy-to-digest foods, anti-inflammatory, gut-soothing, avoid triggers

**Recommended foods:**
- **Bland & gentle:** White rice, plain oats, bananas, applesauce, toast
- **Anti-inflammatory:** Ginger tea, peppermint tea, turmeric, fennel
- **Low-FODMAP (if sensitive):** Rice, eggs, carrots, zucchini, lactose-free yogurt
- **Probiotics (if tolerated):** Plain kefir, sauerkraut (small amounts), miso
- **Hydration:** Water, herbal teas (ginger, chamomile, fennel)
- **Protein (gentle):** Eggs, chicken, tofu, white fish (if applicable)

**Avoid:** Dairy (if sensitive), high-fiber raw veg, caffeine, alcohol, spicy foods, fried foods

**Daily Tip (example):**  
"Your gut is inflamed or irritated. Stick to bland, easy-to-digest foods like rice, bananas, ginger tea, and cooked veg. Avoid dairy, caffeine, and anything fried or spicy."

**Body Insight (example):**  
"Digestive distress can be triggered by stress, food sensitivities, or gut dysbiosis. Reducing gut workload with simple foods gives your digestive system time to heal."

---

#### **HEADACHE/MIGRAINE**

**Nutritional priorities:** Hydration, magnesium, anti-inflammatory, avoid triggers (caffeine, sugar, histamines)

**Recommended foods:**
- **Hydration:** Water, coconut water, herbal teas (ginger, peppermint)
- **Magnesium:** Dark chocolate (≥70%), almonds, spinach, pumpkin seeds, avocado
- **Anti-inflammatory:** Ginger, turmeric, fatty fish (if applicable), olive oil
- **B vitamins (especially B2/riboflavin):** Eggs, spinach, almonds, mushrooms
- **Complex carbs:** Oats, quinoa, sweet potato, brown rice
- **Protein (steady blood sugar):** Eggs, chicken, tofu, lentils

**Avoid:** Aged cheese, processed meats, alcohol, caffeine (unless withdrawal headache), refined sugar, artificial sweeteners

**Daily Tip (example):**  
"Hydrate constantly and load up on magnesium. Avoid sugar, caffeine, and processed foods — they can trigger or worsen headaches. Rest in a dark, quiet space if possible."

**Body Insight (example):**  
"Migraines are linked to magnesium deficiency, dehydration, blood sugar crashes, and inflammatory triggers. Food can't cure a migraine, but it can reduce severity and frequency."

---

#### **INJURED**

**Nutritional priorities:** Protein (tissue repair), anti-inflammatory, vitamin C (collagen synthesis), zinc, omega-3s

**Recommended foods:**
- **Protein (tissue repair):** Chicken, eggs, Greek yogurt, tofu, lentils, salmon (if applicable)
- **Vitamin C (collagen synthesis):** Citrus, bell peppers, strawberries, kiwi, broccoli
- **Zinc (wound healing):** Pumpkin seeds, chickpeas, beef (if applicable), cashews
- **Omega-3 (anti-inflammatory):** Salmon, walnuts, flaxseed, chia seeds
- **Antioxidants:** Berries, dark leafy greens, turmeric, ginger
- **Calcium (if bone injury):** Dairy (if applicable), fortified plant milks, kale, white beans

**Avoid:** Alcohol (impairs healing), excessive sugar (inflammation), processed foods

**Daily Tip (example):**  
"Your body is rebuilding tissue. Load up on protein, vitamin C, and omega-3s. Anti-inflammatory foods speed recovery. Rest is as important as nutrition right now."

**Body Insight (example):**  
"Tissue repair requires amino acids (protein), collagen (vitamin C), and reduced inflammation (omega-3s). Your body prioritizes healing — give it the raw materials it needs."

---

### 3.2 MovementLog Recovery Recommendations

When a wellness state is logged, the **MovementLog checklist is replaced** with a recovery-specific activity list.

#### Movement Recommendations by Wellness State

| Wellness State | Recommended Activities | Intensity | Avoid |
|----------------|------------------------|-----------|-------|
| **Sick** | Complete rest, light stretching (if able), gentle walking (if fever-free) | Minimal | All cardio, strength, HIIT |
| **Hungover** | Rest, gentle walking, light stretching, hydration focus | Low | HIIT, heavy strength, running |
| **Exhausted** | Rest day, restorative yoga, light walking, stretching | Minimal | All high-intensity, strength training |
| **Digestive Issues** | Rest, gentle walking, light yoga (avoid inversions), stretching | Low | HIIT, core-heavy exercises, running |
| **Headache/Migraine** | Complete rest, dark quiet space, light stretching (if tolerated) | Minimal | All exercise (can worsen migraines) |
| **Injured** | Rest affected area, physical therapy exercises (if prescribed), gentle mobility for unaffected areas | Depends on injury | Activities that stress injury site |

**Daily Tip (Movement) — Examples:**

- **Sick:** "Your immune system needs all your energy. Rest is not optional — it's the assignment. Gentle stretching is fine if you feel up to it, but don't push."
- **Hungover:** "Light movement can help (gentle walk, stretching), but this is not a workout day. Rehydrate, rest, and forgive yourself."
- **Exhausted:** "You are in energy debt. Rest is the only way to pay it back. A gentle walk or restorative yoga is fine, but no intensity today."
- **Digestive Issues:** "Movement can sometimes help digestion, but keep it light — gentle walking or stretching. Avoid core-heavy or high-intensity work."
- **Headache/Migraine:** "Rest in a dark, quiet space. Movement can worsen migraines for many people. Listen to your body — if it says stop, stop."
- **Injured:** "Protect the injury. Follow any physical therapy guidance you've been given. Gentle mobility for unaffected areas is fine, but don't push through pain."

---

## 4. CAS Scoring Adjustments

When a wellness state is logged, the **daily CAS calculation is modified** to reflect that rest and recovery are alignment, not failure.

### 4.1 Modified Component Scoring

| Component | Normal Max | Adjustment When Unwell | Rationale |
|-----------|-----------|------------------------|-----------|
| **Phase Detection** | 15 pts | No change | Wellness state does not affect cycle tracking |
| **Biomarker Signals** | 25 pts | Mismatch penalties reduced by 50% | Low energy/mood when unwell is expected, not misalignment |
| **Nutrition Alignment** | 30 pts | Scored against recovery checklist, full points possible | Following recovery foods = full alignment |
| **Fitness/Recovery** | 20 pts | Capped at 15/20 if rest or gentle movement logged | Rest IS alignment when unwell |
| **Logging Consistency** | 10 pts | Full credit (10 pts) | Logging wellness state counts as logging |

**Example CAS when unwell:**
- User logs "Sick"
- Follows recovery nutrition checklist: 30/30
- Rests or does light stretching: 15/20
- Logs mood/energy (both low, but expected): ~20/25 (penalties halved)
- Period tracking active: 10/15
- All required logs complete: 10/10
- **Total CAS: 85-90/100** — reflects that they are aligned with their body's needs, even while unwell

### 4.2 Implementation Notes

**Biomarker penalty reduction:**
- For energy, mood, sleep, appetite, and perceived performance sub-metrics, when a mismatch occurs (e.g., low energy in a high-energy phase), reduce the penalty by 50%
- Example: Normally low energy in Ovulatory phase = 1/5. When sick, low energy in Ovulatory = 3/5 (halved penalty)

**Fitness/Recovery cap:**
- If the user logs rest, light walking, stretching, or gentle yoga while in a wellness state, award 15/20 instead of scoring it as a mismatch
- If they log high-intensity activity while sick (against recommendations), score normally (likely a mismatch = low score)

**Nutrition scoring:**
- Use the recovery-specific food checklist for Component 3 calculation
- If they check off recovery foods, they get full points just like normal phase alignment

---

## 5. Database Schema Changes

### 5.1 New Column in `daily_logs`

Add to existing **`daily_logs`** table:

```sql
ALTER TABLE daily_logs 
ADD COLUMN wellness_state text NULL;
```

**Allowed values:**
- `sick`
- `hungover`
- `exhausted`
- `digestive_issues`
- `headache_migraine`
- `injured`
- `NULL` (default — user is not unwell)

**Date-scoped reset:**
- Wellness state is tied to `date` field in `daily_logs`
- Each new calendar day, wellness_state defaults to NULL
- User must re-log if still unwell

### 5.2 Updated CAS Calculation Function

The real-time CAS calculation function (Edge Function or client-side) must:

1. Check if `wellness_state IS NOT NULL` for today
2. If YES:
   - Load recovery-specific food checklist for `wellness_state` category
   - Load recovery-specific movement recommendations
   - Apply modified scoring rules (biomarker penalty reduction, fitness cap, etc.)
3. If NO:
   - Proceed with standard phase-based logic

---

## 6. Content Index: Recovery Food & Movement Checklists

### 6.1 Recovery NutriLog Checklists

For each wellness state, create a **nutrition_checklist** entry set with `wellness_state` tag instead of `phase` tag.

**Example structure (sick):**

| item_name | nutrient_tag | wellness_state |
|-----------|--------------|----------------|
| Water | Hydration | sick |
| Ginger tea | Anti-inflammatory | sick |
| Citrus fruits | Vitamin C | sick |
| Chicken soup | Protein | sick |
| Honey | Immune support | sick |
| Oatmeal | Comfort | sick |
| Bell peppers | Vitamin C | sick |
| Pumpkin seeds | Zinc | sick |
| Turmeric | Anti-inflammatory | sick |
| Bone broth | Hydration + protein | sick |

Repeat for all 6 wellness states.

### 6.2 Recovery MovementLog Checklists

For each wellness state, create a **movement_checklist** entry set with `wellness_state` tag.

**Example structure (exhausted):**

| item_name | category_tag | intensity_level | wellness_state |
|-----------|--------------|-----------------|----------------|
| Complete rest | Recovery | Minimal | exhausted |
| Restorative yoga | Mobility | Low | exhausted |
| Light stretching | Mobility | Low | exhausted |
| Gentle walk (10 min) | Walking | Low | exhausted |

Repeat for all 6 wellness states.

---

## 7. UI/UX Specifications

### 7.1 Morning Gate Wellness State Selector

**Visual design (delegated to Lucía):**
- Option 1: Toggle + expandable card
- Option 2: "Not feeling well?" button → modal with 6 icons
- Option 3: Inline pill selector that appears on tap

**User flow:**
1. User completes mood slider
2. User completes energy slider
3. **NEW:** "Not feeling well today?" appears
   - Default state: NO (collapsed or untoggled)
   - User taps YES → wellness category selector appears
4. User selects one category (or skips)
5. Taps "next" or "continue"
6. Wellness state saved to `daily_logs.wellness_state` for today
7. Home page loads

**Confirmation:**
- No separate confirmation screen needed
- Selection is saved when user proceeds past the gate

### 7.2 NutriLog & MovementLog Visual Indicators

When a wellness state is active for the day:

**NutriLog:**
- Top banner or pill tag: "Recovery Mode: [Category]" (e.g., "Recovery Mode: Sick 🤒")
- Daily Tip and Body Insight reflect recovery content
- Checklist shows recovery foods instead of phase foods
- "see all" still works, but shows recovery list

**MovementLog:**
- Top banner or pill tag: "Recovery Mode: [Category]"
- Daily Tip reflects rest guidance
- Checklist shows recovery activities (rest, gentle movement)

**Home Page:**
- Optional: small banner or icon indicator that user is in recovery mode today
- Phase ring still shows current phase (wellness state doesn't change cycle tracking)

---

## 8. Daily Reset Logic

**Wellness state is date-scoped and resets automatically.**

- Every calendar day at 00:00 (user's local timezone), `wellness_state` defaults to NULL for the new day's `daily_logs` row
- User must re-select wellness state when they open the app the next day (via the morning gate)
- If a user is sick for 3 days, they log it 3 separate times — this is intentional (allows them to exit recovery mode as soon as they feel better without manual reset)

**Edge case:**
- If user skips the morning gate (closes app before completing), wellness state is NULL until they complete the gate
- NutriLog and MovementLog show standard phase recommendations until wellness state is set

---

## 9. Developer Checklist

**Backend / Database:**
- [ ] Add `wellness_state` column to `daily_logs` table
- [ ] Create 6 recovery-specific `nutrition_checklist` content sets (one per wellness state)
- [ ] Create 6 recovery-specific `movement_checklist` content sets (one per wellness state)
- [ ] Update CAS calculation function to detect `wellness_state` and apply modified scoring
- [ ] Implement daily reset logic (wellness_state = NULL for new calendar day)

**Frontend / UI:**
- [ ] Add wellness state selector to morning mood/energy gate (design by Lucía)
- [ ] Design 6 category icons or text labels (Sick, Hungover, Exhausted, Digestive Issues, Headache/Migraine, Injured)
- [ ] Implement "Recovery Mode" banner on NutriLog and MovementLog when wellness_state is active
- [ ] Swap NutriLog checklist content when wellness_state is set
- [ ] Swap MovementLog checklist content when wellness_state is set
- [ ] Update Daily Tip and Body Insight content to pull from recovery content set

**Content:**
- [ ] Write Daily Tips for each of 6 wellness states (nutrition)
- [ ] Write Body Insights for each of 6 wellness states (nutrition)
- [ ] Write Daily Tips for each of 6 wellness states (movement)
- [ ] Populate food recommendation lists for each wellness state
- [ ] Populate movement recommendation lists for each wellness state

**Testing:**
- [ ] Test CAS scoring with and without wellness state logged
- [ ] Verify daily reset clears wellness state at midnight
- [ ] Test UI flow: gate → wellness state → recovery content → correct CAS
- [ ] Verify recovery checklists load correctly for all 6 categories
- [ ] Test edge case: user skips gate, then logs wellness state later in the day

---

## 10. Non-Negotiable Rules

**From original NutriSync spec, still apply:**
- All data strictly user-scoped (RLS enforced)
- Real-time CAS updates on every log action
- Phase detection remains independent of wellness state
- Wellness state affects recommendations and scoring, NOT cycle tracking

**New rules:**
- Wellness state is optional — users can skip it and proceed with standard phase logic
- Wellness state resets daily — no persistent "sick mode" without re-logging
- Rest and gentle movement when unwell scores as alignment, not failure
- Recovery recommendations are science-backed, not generic wellness advice

---

**End of Wellness State Feature Specification**

NutriSync Collective | January 2025 | Confidential