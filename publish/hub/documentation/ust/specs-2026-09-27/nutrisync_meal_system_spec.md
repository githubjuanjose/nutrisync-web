# NutriSync — Meal Recommendation System Specification
**Feature Addition: Personalized Daily Meal Recommendations**  
**Version:** 1.0 | September 2026  
**For integration into existing NutriSync Developer Specification v1.0**

---

## 1. Feature Overview

Replace the current "top 3 recommended foods" (individual ingredients) on the NutriLog screen with **3 personalized meal recommendations** that update daily. Each meal is:

- **Phase-specific** — aligned with today's hormonal context
- **Personalized** — filtered by diet type, allergies, NutriGoal, health conditions, contraception status
- **Non-repetitive** — smart rotation prevents showing the same meals within 7 days
- **Learnable** — tracks user dismissals and actual logged meals to improve recommendations

Users still log meals via scan or text input (no checklist). The meal recommendations serve as **inspiration and guidance** for what to eat today.

---

## 2. User Flow

### Current State (as of screenshot):
- NutriLog screen shows:
  - Daily Tip card (phase-specific)
  - Body Insights card
  - Mood/Energy/Flow status pills
  - **"Top 3 recommended foods"** — individual ingredients (e.g., Whey Protein Powder, Cauliflower, Rye Bread)
  - "Today's Meals" section (empty until user logs)
  - "+ Log Today's Meal" button

### New State:
- Replace "Top 3 recommended foods" section with **"3 Meal Ideas for Today"**
- Each meal card shows:
  - **Meal name** (e.g., "Salmon & Sweet Potato Bowl")
  - **Nutrient tags** (e.g., "Iron" "Omega-3" "Magnesium")
  - **Phase sync tag** (e.g., "✓ LUTEAL SYNC")
  - **Dismiss icon** (user can hide meals they don't like)
- User taps "+ Log Today's Meal" → scans or writes meal description → meal gets scored

---

## 3. Meal Database Structure

### 3.1 Database Table: `meals`

| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid PK | |
| `meal_name` | text | e.g., "Salmon & Sweet Potato Bowl" |
| `phase` | text | menstrual / follicular / ovulatory / luteal |
| `cycle_day_range` | int[] | e.g., [1,2,3,4,5] for menstrual |
| `nutrient_tags` | text[] | Iron, Omega-3, Magnesium, B6, Protein, Fiber, etc. |
| `diet_compatible` | text[] | vegan, vegetarian, pescatarian, keto, low_carb, balanced |
| `excludes_allergens` | text[] | fish, dairy, eggs, nuts, wheat, soy, shellfish |
| `nutrigoal_fit` | text[] | reduce_pms, emotional_balance, stable_energy, fewer_mood_crashes |
| `health_condition_fit` | text[] | pcos, endometriosis, perimenopause, fibroids |
| `contraception_adjusted` | boolean | Whether meal is adjusted for hormonal contraception users |
| `meal_type` | text | breakfast, lunch, dinner, snack |
| `created_at` | timestamptz | |

### 3.2 Database Table: `user_meal_interactions`

Tracks user behavior to improve recommendations.

| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid PK | |
| `user_id` | uuid FK → users.id | |
| `meal_id` | uuid FK → meals.id | |
| `date` | date | When this interaction happened |
| `interaction_type` | text | dismissed / logged / shown |
| `logged_at` | timestamptz | |

**Interaction types:**
- **shown** — meal was displayed to user
- **dismissed** — user tapped X to hide this meal
- **logged** — user scanned/wrote a meal that matches this one (fuzzy match on name/ingredients)

---

## 4. Meal Recommendation Algorithm

### Step 1: Filter eligible meals
```
SELECT * FROM meals
WHERE phase = [user's current phase]
  AND diet_compatible @> [user's diet_type]
  AND NOT (excludes_allergens && [user's allergies])
  AND nutrigoal_fit @> [user's nutrigoal]
  AND (contraception_adjusted = true IF user on contraception, ELSE true)
  AND (health_condition_fit @> [user's health_conditions] OR health_condition_fit IS NULL)
```

### Step 2: Exclude recently shown meals
Remove meals shown in the last **7 days** to prevent repetition.

```
WHERE meal_id NOT IN (
  SELECT meal_id FROM user_meal_interactions
  WHERE user_id = [current_user]
    AND interaction_type = 'shown'
    AND date >= CURRENT_DATE - INTERVAL '7 days'
)
```

### Step 3: Exclude recently dismissed meals
Remove meals dismissed in the last **14 days** (longer grace period than "shown").

```
WHERE meal_id NOT IN (
  SELECT meal_id FROM user_meal_interactions
  WHERE user_id = [current_user]
    AND interaction_type = 'dismissed'
    AND date >= CURRENT_DATE - INTERVAL '14 days'
)
```

### Step 4: Boost meals user has logged before
If user has previously logged a meal (interaction_type = 'logged'), give it a **2x weight** for future recommendations.

```
ORDER BY 
  (CASE WHEN meal_id IN (
    SELECT meal_id FROM user_meal_interactions 
    WHERE user_id = [current_user] AND interaction_type = 'logged'
  ) THEN 2 ELSE 1 END) DESC,
  RANDOM()
```

### Step 5: Select 3 meals
Return 3 meals, randomized within the weighted set.

### Fallback Logic
If fewer than 3 meals match after all filters:
1. Relax "recently shown" window from 7 days → 3 days
2. If still insufficient, relax "dismissed" window from 14 days → 7 days
3. If still insufficient, remove health condition constraint
4. If still insufficient, show phase-appropriate meals regardless of NutriGoal fit

**Never show meals that violate diet type or allergen constraints.**

---

## 5. Meal Database Content (100+ Meals)

### 5.1 Menstrual Phase Meals (25 meals)

**Nutritional priorities:** Iron replenishment, anti-inflammation, omega-3s, magnesium, vitamin C, warm/comforting foods

| Meal Name | Nutrient Tags | Diet Compatible | Meal Type |
|-----------|---------------|-----------------|-----------|
| **Lentil & Sweet Potato Stew** | Iron, Magnesium, Fiber, Comfort | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Salmon & Spinach Bowl** | Iron, Omega-3, Vitamin C | Pescatarian, Balanced | Lunch/Dinner |
| **Warming Ginger & Turmeric Soup** | Anti-inflammatory, Comfort, Ginger | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Dark Chocolate & Almond Oatmeal** | Magnesium, Iron, Comfort | Vegan, Vegetarian, Balanced | Breakfast |
| **Beef & Kale Stir-Fry** | Iron, Vitamin C, Protein | Balanced, Low Carb | Lunch/Dinner |
| **Chickpea & Red Pepper Curry** | Iron, Vitamin C, Anti-inflammatory | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Chia Seed Pudding with Berries** | Omega-3, Vitamin C, Fiber | Vegan, Vegetarian, Keto | Breakfast/Snack |
| **Pumpkin Seed & Avocado Toast** | Magnesium, Iron, Healthy Fats | Vegan, Vegetarian, Balanced | Breakfast |
| **Bone Broth with Veggies** | Anti-inflammatory, Comfort, Hydration | Balanced, Low Carb, Keto | Lunch/Dinner |
| **Scrambled Eggs with Spinach** | Iron, Protein, B12 | Vegetarian, Balanced, Keto, Low Carb | Breakfast |
| **Red Lentil & Tomato Soup** | Iron, Vitamin C, Comfort | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Walnut & Flaxseed Smoothie** | Omega-3, Magnesium, Fiber | Vegan, Vegetarian, Balanced | Breakfast/Snack |
| **Tofu & Broccoli Stir-Fry** | Iron, Calcium, Protein | Vegan, Vegetarian, Balanced, Low Carb | Lunch/Dinner |
| **Quinoa & Black Bean Bowl** | Iron, Magnesium, Protein | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Sardines on Whole Grain Toast** | Omega-3, Iron, Calcium | Pescatarian, Balanced | Breakfast/Lunch |
| **Miso Soup with Seaweed** | Anti-inflammatory, Iron, Comfort | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Turkey & Veggie Scramble** | Iron, Protein, B Vitamins | Balanced, Low Carb, Keto | Breakfast |
| **Beet & Lentil Salad** | Iron, Fiber, Anti-inflammatory | Vegan, Vegetarian, Balanced | Lunch |
| **Cacao & Banana Smoothie** | Magnesium, Potassium, Comfort | Vegan, Vegetarian, Balanced | Breakfast/Snack |
| **Herbal Tea & Rice Porridge** | Comfort, Easy Digestion, Hydration | Vegan, Vegetarian, Balanced | Breakfast |
| **Kidney Bean & Sweet Potato Chili** | Iron, Fiber, Comfort | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Grilled Chicken & Roasted Veggies** | Iron, Protein, Anti-inflammatory | Balanced, Low Carb, Keto | Lunch/Dinner |
| **Orange & Almond Yogurt Bowl** | Vitamin C, Magnesium, Calcium | Vegetarian, Balanced | Breakfast/Snack |
| **Spinach & Mushroom Omelette** | Iron, Protein, B Vitamins | Vegetarian, Balanced, Keto, Low Carb | Breakfast |
| **Warm Oat & Berry Bowl** | Iron, Fiber, Vitamin C, Comfort | Vegan, Vegetarian, Balanced | Breakfast |

---

### 5.2 Follicular Phase Meals (30 meals)

**Nutritional priorities:** Lean protein, fiber, fermented foods, fresh/light foods, higher carb tolerance

| Meal Name | Nutrient Tags | Diet Compatible | Meal Type |
|-----------|---------------|-----------------|-----------|
| **Greek Yogurt & Berry Bowl** | Protein, Probiotics, Fiber | Vegetarian, Balanced | Breakfast |
| **Kimchi & Edamame Salad** | Probiotics, Protein, Fiber | Vegan, Vegetarian, Balanced | Lunch |
| **Grilled Chicken & Quinoa Bowl** | Protein, Fiber, Complex Carbs | Balanced, Low Carb | Lunch/Dinner |
| **Kefir Smoothie with Flax** | Probiotics, Omega-3, Fiber | Vegetarian, Balanced | Breakfast/Snack |
| **Tempeh & Veggie Stir-Fry** | Protein, Probiotics, Fiber | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Egg White & Veggie Scramble** | Protein, Low Fat, Fresh | Vegetarian, Balanced, Keto, Low Carb | Breakfast |
| **Sauerkraut & Lentil Bowl** | Probiotics, Fiber, Protein | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Cottage Cheese & Cucumber Plate** | Protein, Probiotics, Fresh | Vegetarian, Balanced, Keto, Low Carb | Breakfast/Snack |
| **Fresh Salmon & Greens Salad** | Protein, Omega-3, Fiber | Pescatarian, Balanced, Low Carb | Lunch/Dinner |
| **Kombucha & Chia Breakfast Jar** | Probiotics, Omega-3, Fiber | Vegan, Vegetarian, Balanced | Breakfast |
| **Chickpea & Spinach Curry** | Protein, Fiber, Iron | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Miso-Glazed Tofu Bowl** | Protein, Probiotics, Fresh | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Turkey & Avocado Wrap** | Protein, Healthy Fats, Fiber | Balanced, Low Carb | Lunch |
| **Artichoke & White Bean Salad** | Fiber, Protein, Fresh | Vegan, Vegetarian, Balanced | Lunch |
| **Sprouted Grain Toast with Egg** | Protein, Fiber, Complex Carbs | Vegetarian, Balanced | Breakfast |
| **Fresh Veggie Spring Rolls** | Fiber, Fresh, Light | Vegan, Vegetarian, Balanced | Lunch/Snack |
| **Grilled Fish Tacos** | Protein, Omega-3, Fresh | Pescatarian, Balanced | Lunch/Dinner |
| **Protein-Packed Smoothie Bowl** | Protein, Fiber, Fresh | Vegan, Vegetarian, Balanced | Breakfast |
| **Lentil & Veggie Soup** | Protein, Fiber, Light | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Chicken Breast & Broccoli** | Protein, Fiber, Low Fat | Balanced, Low Carb, Keto | Lunch/Dinner |
| **Fermented Veggie Bowl** | Probiotics, Fiber, Fresh | Vegan, Vegetarian, Balanced | Lunch |
| **Egg & Veggie Frittata** | Protein, Fiber, Fresh | Vegetarian, Balanced, Keto, Low Carb | Breakfast/Lunch |
| **Shrimp & Cucumber Salad** | Protein, Fresh, Light | Pescatarian, Balanced, Keto, Low Carb | Lunch/Dinner |
| **Oatmeal with Berries & Seeds** | Fiber, Protein, Fresh | Vegan, Vegetarian, Balanced | Breakfast |
| **Tuna & Avocado Bowl** | Protein, Omega-3, Healthy Fats | Pescatarian, Balanced, Keto, Low Carb | Lunch/Dinner |
| **Veggie-Packed Omelette** | Protein, Fiber, Fresh | Vegetarian, Balanced, Keto, Low Carb | Breakfast |
| **Fresh Fruit & Nut Yogurt** | Protein, Fiber, Fresh | Vegetarian, Balanced | Breakfast/Snack |
| **Grilled Veggie & Hummus Plate** | Protein, Fiber, Fresh | Vegan, Vegetarian, Balanced | Lunch/Snack |
| **Citrus & Quinoa Salad** | Fiber, Vitamin C, Fresh | Vegan, Vegetarian, Balanced | Lunch |
| **Light Chicken & Veggie Soup** | Protein, Fiber, Light | Balanced, Low Carb | Lunch/Dinner |

---

### 5.3 Ovulatory Phase Meals (20 meals)

**Nutritional priorities:** Antioxidants, cruciferous veg, anti-inflammatory foods, light whole grains, zinc

| Meal Name | Nutrient Tags | Diet Compatible | Meal Type |
|-----------|---------------|-----------------|-----------|
| **Berry & Spinach Smoothie Bowl** | Antioxidants, Fiber, Fresh | Vegan, Vegetarian, Balanced | Breakfast |
| **Broccoli & Quinoa Power Bowl** | Antioxidants, Fiber, Cruciferous | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Grilled Salmon & Kale Salad** | Omega-3, Antioxidants, Cruciferous | Pescatarian, Balanced, Low Carb | Lunch/Dinner |
| **Turmeric Chickpea Stir-Fry** | Anti-inflammatory, Protein, Antioxidants | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Cauliflower Rice & Veggie Bowl** | Cruciferous, Fiber, Antioxidants | Vegan, Vegetarian, Balanced, Keto, Low Carb | Lunch/Dinner |
| **Brussels Sprout & Walnut Salad** | Cruciferous, Omega-3, Antioxidants | Vegan, Vegetarian, Balanced | Lunch |
| **Green Tea & Blueberry Oatmeal** | Antioxidants, Fiber, Comfort | Vegan, Vegetarian, Balanced | Breakfast |
| **Bok Choy & Tofu Stir-Fry** | Cruciferous, Protein, Anti-inflammatory | Vegan, Vegetarian, Balanced, Low Carb | Lunch/Dinner |
| **Rainbow Veggie & Hummus Wrap** | Antioxidants, Fiber, Fresh | Vegan, Vegetarian, Balanced | Lunch |
| **Pumpkin Seed & Kale Pesto Pasta** | Zinc, Cruciferous, Antioxidants | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Grilled Chicken & Pepper Plate** | Protein, Antioxidants, Zinc | Balanced, Low Carb, Keto | Lunch/Dinner |
| **Tomato & Basil Quinoa Bowl** | Antioxidants, Fiber, Anti-inflammatory | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Arugula & Berry Salad** | Antioxidants, Cruciferous, Fresh | Vegan, Vegetarian, Balanced | Lunch |
| **Beet & Carrot Ginger Juice** | Antioxidants, Anti-inflammatory, Fresh | Vegan, Vegetarian, Balanced | Breakfast/Snack |
| **Roasted Veggie & Cashew Bowl** | Antioxidants, Zinc, Healthy Fats | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Green Smoothie with Spirulina** | Antioxidants, Anti-inflammatory, Fresh | Vegan, Vegetarian, Balanced | Breakfast/Snack |
| **Seared Tuna & Veggie Stack** | Protein, Omega-3, Antioxidants | Pescatarian, Balanced, Keto, Low Carb | Lunch/Dinner |
| **Veggie-Packed Brown Rice Bowl** | Fiber, Antioxidants, Fresh | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Kale & Chickpea Salad** | Cruciferous, Protein, Fiber | Vegan, Vegetarian, Balanced | Lunch |
| **Grilled Veggie & Olive Oil Plate** | Antioxidants, Anti-inflammatory, Healthy Fats | Vegan, Vegetarian, Balanced, Keto, Low Carb | Lunch/Dinner |

---

### 5.4 Luteal Phase Meals (30 meals)

**Nutritional priorities:** Magnesium, complex carbs, B6, calcium, protein for satiety, anti-bloat foods

| Meal Name | Nutrient Tags | Diet Compatible | Meal Type |
|-----------|---------------|-----------------|-----------|
| **Sweet Potato & Black Bean Bowl** | Magnesium, B6, Complex Carbs | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Dark Chocolate & Almond Butter Toast** | Magnesium, Comfort, Healthy Fats | Vegan, Vegetarian, Balanced | Breakfast/Snack |
| **Banana & Peanut Butter Smoothie** | B6, Magnesium, Protein | Vegan, Vegetarian, Balanced | Breakfast/Snack |
| **Spinach & White Bean Stew** | Magnesium, Calcium, Protein | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Greek Yogurt & Honey Bowl** | Calcium, Protein, Comfort | Vegetarian, Balanced | Breakfast/Snack |
| **Whole Grain Pasta with Greens** | Complex Carbs, Magnesium, Fiber | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Chicken & Roasted Veggie Bowl** | Protein, B6, Magnesium | Balanced, Low Carb, Keto | Lunch/Dinner |
| **Oatmeal with Banana & Seeds** | Complex Carbs, B6, Magnesium | Vegan, Vegetarian, Balanced | Breakfast |
| **Kale & Tofu Scramble** | Calcium, Protein, Magnesium | Vegan, Vegetarian, Balanced, Keto, Low Carb | Breakfast |
| **Lentil & Sweet Potato Curry** | Complex Carbs, Magnesium, B6 | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Salmon & Brown Rice Bowl** | Omega-3, Complex Carbs, B6 | Pescatarian, Balanced | Lunch/Dinner |
| **Chickpea & Sunflower Seed Salad** | Magnesium, B6, Protein | Vegan, Vegetarian, Balanced | Lunch |
| **Fortified Almond Milk Smoothie** | Calcium, Magnesium, Comfort | Vegan, Vegetarian, Balanced | Breakfast/Snack |
| **Turkey & Veggie Stir-Fry** | Protein, B6, Anti-bloat | Balanced, Low Carb, Keto | Lunch/Dinner |
| **Quinoa & Veggie Buddha Bowl** | Complex Carbs, Magnesium, Fiber | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Egg & Avocado Toast** | Protein, B6, Healthy Fats | Vegetarian, Balanced | Breakfast |
| **Pumpkin Seed Trail Mix** | Magnesium, Protein, Comfort | Vegan, Vegetarian, Balanced, Keto, Low Carb | Snack |
| **Ginger & Fennel Tea with Rice Bowl** | Anti-bloat, Comfort, Complex Carbs | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Tempeh & Sweet Potato Plate** | Protein, Complex Carbs, Magnesium | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Cottage Cheese & Berry Bowl** | Calcium, Protein, Comfort | Vegetarian, Balanced | Breakfast/Snack |
| **Black Bean & Avocado Wrap** | Magnesium, Fiber, Healthy Fats | Vegan, Vegetarian, Balanced | Lunch |
| **Grilled Chicken & Potato Bowl** | Protein, B6, Complex Carbs | Balanced, Low Carb | Lunch/Dinner |
| **Cacao & Chia Pudding** | Magnesium, Omega-3, Comfort | Vegan, Vegetarian, Balanced, Keto | Breakfast/Snack |
| **White Bean & Kale Soup** | Calcium, Magnesium, Comfort | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Whole Grain Wrap with Hummus** | Complex Carbs, Protein, Fiber | Vegan, Vegetarian, Balanced | Lunch |
| **Almond & Date Energy Balls** | Magnesium, Comfort, Healthy Fats | Vegan, Vegetarian, Balanced, Keto | Snack |
| **Turkey & Sweet Potato Hash** | Protein, B6, Complex Carbs | Balanced, Low Carb | Breakfast/Lunch/Dinner |
| **Peppermint Tea & Oat Bowl** | Anti-bloat, Comfort, Complex Carbs | Vegan, Vegetarian, Balanced | Breakfast |
| **Tofu & Veggie Brown Rice Bowl** | Protein, Complex Carbs, Calcium | Vegan, Vegetarian, Balanced | Lunch/Dinner |
| **Dark Leafy Green Smoothie** | Magnesium, Calcium, Anti-bloat | Vegan, Vegetarian, Balanced | Breakfast/Snack |

---

## 6. UI Integration

### 6.1 Where to Display (NutriLog Screen)

**Replace** the current "Top 3 recommended foods" section (individual ingredients) with:

**"Meals to Try Today"**  
3 meal cards displayed vertically, each showing:
- Meal name (bold, larger text)
- Nutrient tag pills (small coral pills, e.g., "Magnesium" "B6" "Comfort")
- Phase sync indicator (small check badge: "✓ LUTEAL SYNC" or current phase)
- Dismiss icon (X in top-right corner of card)

**Visual design delegated to Lucía.**

### 6.2 User Interactions

**Tap on a meal card:**  
Opens a simple modal/overlay with:
- Full meal name
- Brief description (1 sentence): "Warm, magnesium-rich comfort food to ease PMS and cravings."
- Nutrient highlights (expanded list)
- "Got it" button to close

**Tap dismiss (X icon):**  
- Meal card fades out
- Logs `user_meal_interactions` with `interaction_type = 'dismissed'`
- Meal won't reappear for 14 days
- New meal from the eligible pool immediately slides in to replace it

**User logs a meal (via scan or text):**  
- Backend fuzzy-matches the logged meal text against `meal_name` in database
- If match found (>70% similarity), logs `user_meal_interactions` with `interaction_type = 'logged'`
- That meal + similar meals get boosted in future recommendations

### 6.3 Daily Refresh

Recommendations refresh **at midnight** (00:00 local time).  
User opens app on a new day → sees 3 new meal ideas.

If user dismisses all 3 meals → immediately fetch 3 new ones (don't wait until tomorrow).

---

## 7. Developer Implementation Checklist

### Phase 1: Database Setup
- [ ] Create `meals` table in Supabase
- [ ] Create `user_meal_interactions` table in Supabase
- [ ] Enable Row Level Security (RLS) on both tables
- [ ] Populate `meals` table with 105 meals (use CSV import or batch insert script)

### Phase 2: Recommendation Logic
- [ ] Build meal filtering function (diet, allergies, NutriGoal, contraception, health conditions)
- [ ] Implement "recently shown" exclusion (7-day window)
- [ ] Implement "recently dismissed" exclusion (14-day window)
- [ ] Implement boost logic for previously logged meals (2x weight)
- [ ] Implement fallback logic if <3 meals available
- [ ] Build daily refresh trigger (midnight, per user timezone)

### Phase 3: User Interaction Tracking
- [ ] Log `shown` interactions when meals are displayed
- [ ] Log `dismissed` interactions when user taps X
- [ ] Implement fuzzy matching logic to detect when user logs a recommended meal
- [ ] Log `logged` interactions when match detected

### Phase 4: UI Integration
- [ ] Replace "Top 3 recommended foods" section with meal cards
- [ ] Design meal card component (name, nutrient tags, phase badge, dismiss icon)
- [ ] Implement meal detail modal (tap to view)
- [ ] Implement dismiss animation + replacement logic
- [ ] Connect to backend recommendation API

### Phase 5: Testing
- [ ] Test filtering for all diet types (vegan, vegetarian, pescatarian, keto, low carb, balanced)
- [ ] Test allergen exclusion (fish, dairy, nuts, wheat, soy, eggs, shellfish)
- [ ] Test NutriGoal filtering (reduce PMS, emotional balance, stable energy, mood crashes)
- [ ] Test contraception adjustment (meals tagged appropriately)
- [ ] Test rotation (no repeats within 7 days)
- [ ] Test dismiss persistence (14-day grace period)
- [ ] Test boost logic (previously logged meals reappear more often)
- [ ] Test fallback (when <3 meals available after filtering)

### Phase 6: Launch
- [ ] Deploy to production
- [ ] Monitor recommendation quality (are users dismissing too many meals?)
- [ ] Track logging patterns (are users actually logging recommended meals?)
- [ ] Iterate based on user feedback

---

## 8. Future Enhancements (Post-MVP)

- **Meal favoriting:** Users can save meals they love
- **Ingredient swaps:** "Swap salmon for tofu" auto-adjusts tags
- **Portion size guidance:** Based on user's BMR and activity level
- **Recipe links:** Deep-link to external recipe sites or in-app instructions
- **Meal prep mode:** Show meals that can be batch-cooked
- **Shopping list generator:** Compile ingredients for the week's meals
- **Meal rating:** Thumbs up/down to refine recommendations further
- **Seasonal adjustments:** Prioritize in-season ingredients
- **Cultural/regional preferences:** Tag meals by cuisine type (Mediterranean, Asian, Latin, etc.)

---

## 9. Example User Scenarios

### Scenario 1: Vegan user, Luteal Day 24, NutriGoal = Reduce PMS

**Filters applied:**
- Phase = Luteal
- Diet = Vegan
- NutriGoal = Reduce PMS (prioritize magnesium, B6, anti-bloat)
- Exclude: all animal products

**Sample recommendations:**
1. Sweet Potato & Black Bean Bowl (Magnesium, B6, Complex Carbs)
2. Dark Chocolate & Almond Butter Toast (Magnesium, Comfort)
3. Peppermint Tea & Oat Bowl (Anti-bloat, Comfort, Complex Carbs)

User dismisses #2 (doesn't like almond butter).  
→ System immediately replaces with: **Cacao & Chia Pudding** (also magnesium-rich, vegan, luteal-friendly).

---

### Scenario 2: Pescatarian user, Ovulatory Day 15, NutriGoal = Stable Energy, Nut allergy

**Filters applied:**
- Phase = Ovulatory
- Diet = Pescatarian
- NutriGoal = Stable Energy (prioritize antioxidants, complex carbs)
- Exclude: nuts

**Sample recommendations:**
1. Grilled Salmon & Kale Salad (Omega-3, Antioxidants, Cruciferous)
2. Seared Tuna & Veggie Stack (Protein, Omega-3, Antioxidants)
3. Veggie-Packed Brown Rice Bowl (Fiber, Antioxidants)

User logs "salmon and greens for lunch" via text.  
→ System fuzzy-matches to **Grilled Salmon & Kale Salad** → logs `logged` interaction → future recommendations will boost similar fish + greens meals.

---

### Scenario 3: Balanced diet user, Menstrual Day 2, NutriGoal = Emotional Balance, Dairy allergy

**Filters applied:**
- Phase = Menstrual
- Diet = Balanced
- NutriGoal = Emotional Balance (prioritize tryptophan, B vitamins, omega-3)
- Exclude: dairy

**Sample recommendations:**
1. Salmon & Spinach Bowl (Iron, Omega-3, Vitamin C)
2. Turkey & Veggie Scramble (Iron, Protein, B Vitamins)
3. Walnut & Flaxseed Smoothie (Omega-3, Magnesium, Fiber) — **but contains nuts, excluded if nut allergy**

User sees 3 dairy-free, menstrual-phase, emotionally balancing meals.  
User dismisses #2 (doesn't eat turkey).  
→ System replaces with: **Lentil & Sweet Potato Stew** (Iron, Magnesium, Comfort).

---

## 10. Success Metrics

Track these to measure feature performance:

- **Meal log match rate:** % of logged meals that match recommended meals
- **Dismissal rate:** % of recommended meals dismissed (target: <30%)
- **Rotation satisfaction:** Days between seeing the same meal (target: >7 days)
- **Personalization accuracy:** % of users logging meals aligned with their NutriGoal
- **Engagement:** Daily active users viewing meal recommendations vs. logging meals

---

**End of Meal Recommendation System Specification**

NutriSync Collective | Confidential | September 2026