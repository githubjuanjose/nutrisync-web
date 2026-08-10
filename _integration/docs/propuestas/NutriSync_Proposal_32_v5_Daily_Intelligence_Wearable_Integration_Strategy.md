# NutriSync Proposal 32 v5

## Daily Intelligence, Spain-First Localisation, Trust Architecture & Health/Wearable Integration Strategy

**Meals • Activity • Mood & Energy • Context • Women’s Health News • Segment-of-One Behavioural Learning • Health & Wearable Signals**

**Status:** Draft for founder approval  
**Date:** 10 August 2026  
**Supersedes:** Proposal 32 v4  
**Primary stack:** React Native, Supabase, OpenAI Responses API, USDA FoodData Central  
**Market sequence:** Spain first → continental Europe second → Latin America third → English-language markets fourth

> **Strategic proposition**  
> NutriSync should make daily self-observation almost effortless, then use confirmed longitudinal data to learn what appears to work better for each individual across cycles and life events. The differentiator is the private, trusted closed loop: **observe → ask → confirm → learn → recommend → measure**.

> **v5 strategic amendment**  
> NutriSync should connect to **health data and user-authorised signals, not to brands as a dependency**. Apple HealthKit and Android Health Connect become the preferred operating-system aggregation layer. Direct integrations with Garmin, WHOOP, Fitbit, Oura, Polar, Samsung, Huawei and similar ecosystems are added selectively where they provide unique value and where commercial, technical and AI-use terms permit it. **Strava must not be a dependency for NutriSync’s AI or segment-of-one learning layer under its current API policy.**

---

## Contents

1. Executive recommendation  
2. Strategic differentiation  
3. The NutriSync Trust Covenant  
4. Product principles and boundaries  
5. Progressive onboarding and consent  
6. Axis A — Meal and nutrition intelligence  
7. Axis B — Activity intelligence  
8. Health, fitness & wearable integration strategy **(new in v5)**  
9. Axis C — Mood, energy, behavioural change and life events  
10. Segment-of-one behavioural analysis  
11. Spain-first localisation and market rollout  
12. Women’s Health & Nutrition Now — editorial and news layer  
13. Product experience and visual-design proposal  
14. Unified user journeys  
15. Technical architecture  
16. Data model and event lifecycle  
17. AI model strategy and evaluation  
18. Privacy, security and controlled sharing  
19. Expert and community recommendation layer  
20. Implementation roadmap  
21. KPIs and release gates  
22. Founder decisions  
23. User-facing trust and Spain-Spanish copy  
24. References

---

# 1. Executive recommendation

NutriSync already has the right product foundation: React Native applications, Supabase as the trusted backend, structured cycle and wellbeing data, a content catalogue, and a clear ambition to personalise nutrition and lifestyle guidance. Proposal 32 v5 keeps the v4 product and trust architecture and adds one material strategic amendment: **a formal integration strategy for health, fitness, wearable and sports-platform data**.

The recommended product consists of five connected capabilities:

1. **Meal and nutrition logging from photographs.** A deliberately submitted meal image becomes a structured, editable draft containing likely foods, ingredients, portions, food groups and nutrient ranges.
2. **Activity logging from authorised health data, routines and optional location context.** Workouts are imported or prepared as candidates, then confirmed with one tap or one sentence. Home exercise remains a first-class use case.
3. **A health/wearable signal layer.** Apple HealthKit and Android Health Connect are the primary aggregation routes. Direct vendor integrations are used selectively and never become a single point of product dependency.
4. **Mood and energy check-ins triggered by meaningful behavioural changes.** NutriSync detects that a day differs from the user’s own normal rhythm, but never records or labels a mood until the user answers.
5. **A private segment-of-one behavioural model.** Confirmed meals, movement, sleep, recovery, cycle context, life events and self-reported wellbeing form a personal timeline from which NutriSync can identify repeated associations and select governed recommendations.

The v5 architecture therefore changes the integration question from:

> “Which brands should NutriSync connect to?”

to:

> **“Which user-authorised signals does NutriSync need, what is their provenance, and what lawful/contractually permitted path can supply them?”**

The preferred hierarchy is:

```text
1. Operating-system health aggregation
   Apple HealthKit / Apple Health
   Android Health Connect

2. Direct specialist integrations where uniquely valuable
   WHOOP / Garmin / Fitbit / Oura / Polar / Samsung / Huawei

3. Sports/social platforms only where terms permit the intended processing
   Strava = optional display/import pathway only if permitted;
            not a source for NutriSync AI/ML or cross-domain analytics
```

The existing stack remains sufficient for the pilot. No new application server or graph database is required initially. The new requirement is an **integration abstraction layer** that normalises data, retains provenance and enforces provider-specific policy constraints.

## 1.1 Launch gates added by v5

In addition to the v4 gates:

- Complete a provider-by-provider terms and privacy review before production.
- Treat platform terms as machine-enforceable policy, not documentation.
- Do not ingest Strava data into AI prompts, embeddings, RAG, model evaluation or segment-of-one analytics while current restrictions apply.
- Keep OS-level health data and direct-provider data provenance separate.
- Design all direct integrations to be removable without breaking the NutriSync personal timeline.
- Maintain a current integration register: approval state, scopes, rate limits, licensing, retention, AI restrictions, user deletion obligations and last legal review.

---

# 2. Strategic differentiation

## 2.1 The seven-part moat

| Differentiator | What the user experiences | Why it is difficult to copy well |
|---|---|---|
| **Frictionless multimodal logging** | A photo, imported workout, one tap or one sentence replaces repetitive forms | Requires coordinated vision, device data, data quality, confirmation UX and correction handling |
| **Health-signal abstraction** | The experience works across phones, watches and specialist wearables | Requires data normalisation, provenance, duplication control and provider-policy enforcement |
| **Segment-of-one learning** | Insights compare the user mainly with her own history | Requires longitudinal, confirmed, context-rich data and careful within-person analysis |
| **Governed recommendation loop** | Recommendations come from approved content and are measured after use | Requires structured content, moderation, contraindication controls and outcome capture |
| **Trust architecture** | The user sees which signals are active, why a prompt appeared, who can access data and how to delete it | Requires product, security, data and legal design to work together |
| **Spain-native market fit** | The product sounds written in Spain, recognises local meals and cites Spanish authorities | Requires locale-specific product, evaluation, content and editorial operations |
| **Evidence and news intelligence** | Women’s-health developments are explained calmly and connected to the right app context | Requires source governance, review, localisation, expiry and safe relevance rules |

Feature breadth alone is not the moat. The defensible proposition is the **measured, trusted, within-person action-response loop**, supplied by multiple user-authorised signal sources without becoming hostage to one wearable or sports platform.

## 2.2 Recommended positioning

> **Your pattern, not a platform.**  
> NutriSync privately connects what you eat, how you move, how you recover, how your routine changes and how you say you feel. It learns which practical actions appear to work better for you over time.

Supporting trust line:

> **Your data works for you — not for advertisers.**

---

# 3. The NutriSync Trust Covenant

Trust remains a product capability with contractual, technical and user-experience controls behind it.

| User promise | Product and technical control |
|---|---|
| We do not sell personal data | No data-broker, advertising or audience-resale integration |
| We do not use health, meal, location or mood data for advertising | No advertising SDK access to these domains |
| Other users cannot see private logs | Private-by-default records, RLS, no public storage URLs |
| Experts see only what the user explicitly shares | Scoped, revocable access grant with expiry and audit |
| Mood is never silently inferred and stored | Only explicit user responses become mood/energy facts |
| Precise location is not used to build a general movement history | User-selected Smart Places, device-first processing |
| Connected platforms are optional | Every connector can be disconnected independently |
| Provider-specific restrictions are respected | Policy engine blocks prohibited processing by source |
| The user can see provenance | Each imported signal shows source, device/app and last sync |
| Core logging works without AI, location or wearable permissions | Manual and conversational alternatives remain available |

## 3.1 Processor and platform transparency

NutriSync must distinguish four roles:

1. **Device health store / OS aggregator** — e.g., HealthKit or Health Connect.
2. **Direct data provider** — e.g., Garmin, WHOOP or Fitbit.
3. **NutriSync processor/subprocessor** — e.g., Supabase/OpenAI for specific features.
4. **NutriSync itself as controller of the product experience and personal timeline.**

A user may authorise the same underlying workout through more than one route. Provenance and de-duplication must prevent double counting.

## 3.2 My Data & Learning screen

The screen should show:

- Connected source.
- Data categories granted.
- Last successful sync.
- Whether historical/background access is enabled.
- Whether data may be used in personal analytics.
- Whether the source has provider-specific restrictions.
- Disconnect and deletion controls.
- Which personal patterns rely on each source.

---

# 4. Product principles and boundaries

1. **Progressive profiling, not onboarding interrogation.**
2. **Candidates are not facts.**
3. **AI identifies or explains; deterministic systems calculate and decide.**
4. **Within-person before population comparison.**
5. **No continuous surveillance.**
6. **Governed recommendations only.**
7. **Spain-native before global-generic.**
8. **Environmental context is exploratory.**
9. **Evidence before virality.**
10. **Connect to signals, not brands.**
11. **Provider terms are product constraints.**
12. **A connector must be removable without corrupting the personal timeline.**

---

# 5. Progressive onboarding and consent

## 5.1 Just-in-time health connection

The user should never be asked to connect every possible source during sign-up.

Example:

> **¿Quieres importar tus entrenamientos y sueño?**  
> Conecta Apple Health o Health Connect para evitar registrar dos veces. Tú eliges qué categorías compartir.

Only after that value is understood should the app request specific permissions.

## 5.2 Permission model

| Permission | Ask when | Value shown first |
|---|---|---|
| Camera/photos | User taps meal photo | Turn a photo into an editable meal draft |
| HealthKit/Health Connect | Activity/sleep import | Avoid duplicate logging |
| Direct wearable OAuth | User asks for richer provider-specific data | Add recovery or specialist metrics |
| Notifications | User saves a reminder | Remind only when chosen |
| Smart Places/location | User saves gym/studio | Recognise a possible visit without tracking every journey |
| AI meal analysis | First photo | Analyse only this selected image |
| Personal pattern analysis | After enough confirmed data exists | Learn your own patterns over time |

Revocation must explain what happens to imported records, cached provider data, derived features and learned associations.

---

# 6. Axis A — Meal and nutrition intelligence

The v4 meal architecture remains unchanged:

```text
Photo
→ crop/resize/EXIF removal
→ private upload
→ structured vision draft
→ canonical-food match
→ deterministic nutrient ranges
→ user confirmation/correction
→ personal timeline
```

Key principles remain:

- AI identifies; verified food databases calculate.
- Use ranges, not false precision.
- Separate food groups from nutrients.
- Store AI draft and user-confirmed version separately.
- Original full-resolution images are not uploaded by default.
- Corrections improve product quality only under the relevant consent/governance.

---

# 7. Axis B — Activity intelligence

## 7.1 Product principle

Build **Activity Intelligence**, not a collection of branded connectors.

Evidence hierarchy:

| Evidence | Reliability |
|---|---:|
| User-confirmed activity | Highest |
| HealthKit/Health Connect workout | Very high |
| Direct provider workout with reliable source ID | Very high |
| User-started NutriSync timer | Very high |
| Smart Place dwell | Medium |
| Steps/motion/energy | Supporting |
| Location alone | Insufficient |

## 7.2 Universal activity capture

Activity should work at home, gym/studio, outdoors and in unstructured settings. Direct wearable data enhances these flows but does not replace manual or conversational logging.

## 7.3 Duplicate reconciliation

A single session may arrive from:

- Apple Watch → HealthKit.
- Garmin → Garmin API.
- Garmin → Apple Health.
- Strava → Apple Health.
- Manual NutriSync log.
- Smart Place event.

Use source record IDs, timestamps, duration overlap, activity compatibility and source priority to merge rather than duplicate.

---

# 8. Health, fitness & wearable integration strategy

## 8.1 Strategic principle

> **Connect to the user’s health data, not to the user’s brands.**

NutriSync should not build ten independent data silos. It should define a stable internal signal model and map permitted sources into it.

Preferred architecture:

```text
Wearables / fitness apps
      │
      ├──────────────┐
      ▼              ▼
Apple Health      Health Connect
      │              │
      └──────┬───────┘
             │
      NutriSync Health Gateway
             │
      Normalised Signal Model
             │
   ┌─────────┼─────────┐
   ▼         ▼         ▼
Activity    Sleep    Recovery
   │         │         │
   └─────────┼─────────┘
             ▼
 Nutrition + cycle + context
             ▼
 Segment-of-one analytics
```

Direct provider APIs connect to the **same Health Gateway**, not straight into feature code.

## 8.2 Market-access heatmap

Legend: 🟢 preferred/open-enough for planned use · 🟡 controlled/approval/licensing/extra review · 🔴 materially incompatible with the intended AI/personal-analytics use.

| Ecosystem | Access model | Useful data | Main constraint | NutriSync stance |
|---|---|---|---|---|
| **Apple HealthKit** | Device-local, granular user authorisation | Workouts, steps, energy, heart rate, sleep, body and reproductive-health types where authorised | App Store/privacy requirements; least-privilege permissions | 🟢 **Tier 1 core** |
| **Android Health Connect** | Device platform with declared permissions | Activity, exercise, sleep, vitals and other supported records | Play Console declarations; historical/background permissions are separate | 🟢 **Tier 1 core** |
| **WHOOP** | OAuth 2.0 API + webhooks | Sleep, recovery, workout/strain and related metrics | Vendor terms/scopes; specialist user base | 🟢/🟡 **Tier 2 specialist** |
| **Garmin Connect** | Business developer programme; Health and Activity APIs | Steps, HR, sleep, stress, Body Battery, activities and more | Approval; some commercial metrics/use may require licence or commercial agreement | 🟡 **Tier 2 selective** |
| **Fitbit** | OAuth 2.0 Web API | Activity, body, devices, HR, sleep and subscriptions | Some intraday access for third-party users requires request/approval | 🟡 **Tier 2 selective** |
| **Oura** | OAuth 2.0 API | Ring-derived sleep/readiness/activity data depending scopes | Direct integration maintenance and terms | 🟡 **Tier 2 specialist** |
| **Samsung Health** | Health Data SDK | Samsung Health data with user permission | Public distribution requires Samsung partnership/registration; developer mode otherwise | 🟡 **Tier 2 selective** |
| **Polar** | AccessLink OAuth 2.0 API | Training, daily activity, continuous HR and related data | Partner integration and consent lifecycle | 🟡 **Tier 3** |
| **Huawei Health** | Health Service Kit | Steps, HR and other health/fitness data | Application review/permissions; ecosystem-specific distribution | 🟡 **Tier 3 / market-led** |
| **Strava** | API with access tiers and strict policy | Activities and athlete data | Current policy prohibits AI operation/training/grounding/RAG and cross-data analytics; seven-day cache limit and other restrictions | 🔴 **Do not use as AI/segment-of-one source** |

## 8.3 Why Strava is a special case

Strava still provides a developer API, but its 2026 API Policy materially changes what NutriSync can safely build on top of it.

Current restrictions include prohibitions on using Strava API data in connection with the operation or development of AI applications, including ingestion into an AI context window, grounding, embeddings and retrieval-augmented generation. The policy also restricts analytics, de-identified processing, combining Strava data with other customer data for analytics, persistent indexing and retention beyond a short cache except where expressly permitted.

For NutriSync this means:

```text
Allowed only after legal/terms validation:
- user-authenticated display of permitted Strava data
- narrowly scoped functionality consistent with Strava terms

Not suitable for NutriSync's core:
- feed Strava data to an LLM
- use Strava data in Segment-of-One analytics
- combine Strava activity with nutrition/mood/cycle data for personal analysis
- create embeddings from Strava activity text
- store a long-term Strava-derived corpus
```

**Architectural consequence:** Strava cannot be a foundational source for NutriSync’s AI learning loop while those terms remain in force.

If an activity originally recorded in Strava is separately present in Apple Health or Health Connect under those platforms’ authorised data model, NutriSync must treat the OS health-store record according to the applicable OS/source provenance and legal review; it must not assume that a second path automatically eliminates underlying third-party restrictions. Provenance therefore matters.

## 8.4 Apple HealthKit as the preferred iOS integration layer

HealthKit is strategically important because it is a central health/fitness repository on Apple platforms and uses fine-grained permissions by data type.

NutriSync should:

- Request only needed data types.
- Ask at the moment of value.
- Show source application/device where available.
- Read workouts, sleep, steps, active energy and selected cardio/body signals only when relevant.
- Avoid importing every available health type.
- Keep permissions manageable from the Trust Centre.

Example initial scope:

```text
Workouts
Steps
Active energy
Sleep
Heart rate / resting heart rate
HRV where useful and authorised
Body weight where user chooses
```

Reproductive/cycle data should remain a separate, explicit permission family because of sensitivity.

## 8.5 Android Health Connect as the preferred Android layer

Health Connect should be the Android equivalent of the core iOS strategy.

NutriSync must:

- Declare the exact health permissions used.
- Match app-store declarations to actual data use.
- Request additional historical/background permissions only when justified.
- Provide an obvious route for the user to manage access.
- Handle missing permissions without degrading the core app.

## 8.6 Garmin

Garmin’s Connect Developer Program provides Health and Activity APIs with rich all-day and workout data. It is attractive for high-engagement fitness users and can provide metrics such as sleep, stress and Body Battery.

NutriSync should not assume every metric is commercially free. The integration register must track:

- Programme approval status.
- Contract/licensing status.
- Exact permitted metrics.
- Refresh and webhook/push model.
- User deletion obligations.
- Whether data can be combined into NutriSync personal analytics.
- Attribution requirements.

Recommendation: **pilot after OS aggregation**, unless user research shows a material Garmin-heavy cohort whose unique metrics justify direct access.

## 8.7 WHOOP

WHOOP’s OAuth API exposes specialist recovery, sleep and workout data. For NutriSync, this can be more strategically relevant than a purely social sports feed because recovery signals connect directly to sleep, energy, exercise load and nutrition context.

Recommendation:

- Consider WHOOP as the first specialist direct connector after HealthKit/Health Connect.
- Preserve WHOOP’s own metric names and source provenance.
- Do not reinterpret proprietary scores as clinical facts.
- Use raw/derived values only within contractual permission.

## 8.8 Fitbit

Fitbit continues to expose a Web API using OAuth. It provides activity, body, device, heart-rate, sleep and related data. Some granular intraday data for third-party users requires a request/approval.

Recommendation:

- Prefer Health Connect on Android where it provides sufficient user-authorised data.
- Use direct Fitbit API only for gaps that materially improve the product.
- Treat intraday access as controlled rather than automatically available.

## 8.9 Samsung Health

Samsung Health Data SDK can expose Samsung Health data to partner apps, but distribution requires a partnership request/registration; otherwise the SDK operates only in developer mode.

Recommendation:

- Do not promise Samsung direct integration in the MVP until partnership approval is secured.
- Prefer Health Connect for common Android signals.
- Add Samsung direct access when unique Samsung data justifies it.

## 8.10 Oura, Polar and Huawei

These are useful direct connectors for specific cohorts:

- **Oura:** strong sleep/readiness-oriented use case.
- **Polar:** training and daily-activity access via AccessLink.
- **Huawei:** potentially important for European and international Android cohorts, subject to Health Service Kit approval and market/distribution requirements.

They belong behind the same abstraction layer and are activated based on cohort demand, not brand completeness.

## 8.11 Normalised NutriSync signal model

The AI and analytics layer should not know that “Garmin says X” or “WHOOP says Y” unless provenance is needed for explanation. It should consume normalized, policy-cleared records.

```text
activity.steps
activity.distance
activity.active_minutes
activity.workout_type
activity.workout_duration
activity.active_energy

sleep.duration
sleep.efficiency
sleep.stages
sleep.interruptions

cardio.heart_rate
cardio.resting_hr
cardio.hrv

recovery.provider_score
stress.provider_score

body.weight
body.composition
```

Every record includes:

```text
source_platform
source_application
source_device
source_record_id
observed_at
imported_at
permission_scope
provider_policy_class
confirmation_status
quality/confidence
original_or_derived
allowed_uses
retention_deadline
```

## 8.12 Provider policy classes

Introduce an enforceable policy classification:

```text
P0 = normal NutriSync processing permitted
P1 = personal analytics permitted, AI restricted
P2 = display/import only
P3 = short-cache only
P4 = prohibited for target use
```

Example:

```text
Strava API data:
AI use = prohibited
cross-domain analytics = prohibited
persistent index = prohibited
retention = restricted
=> block before analytics/LLM pipeline
```

This is safer than relying on engineers to remember legal text.

## 8.13 Integration service design

New backend components:

```text
health-connection-registry
health-sync-jobs
source-policy-registry
health-normaliser
activity-deduplicator
signal-provenance-store
provider-token-vault
provider-deletion-worker
provider-audit-log
```

No access token enters the mobile bundle if server-side OAuth exchange is appropriate. Refresh tokens are encrypted and scoped.

## 8.14 Direct integration decision test

Before building a connector, answer:

1. Does OS aggregation already provide the required signal?
2. Is the direct provider data materially better or unique?
3. Is production access guaranteed or approval-based?
4. Is there a fee/licence/minimum commitment?
5. Can the data be stored long enough for the intended feature?
6. Can it be combined with NutriSync data?
7. Can it be used by AI?
8. Can NutriSync derive long-term features from it?
9. What must happen on disconnect/deletion?
10. Can the connector be removed without breaking the user’s timeline?

Build only when the answer justifies the operational burden.

---

# 9. Axis C — Mood, energy, behavioural change and life events

The v4 principle remains unchanged: **do not build a hidden mood detector**.

Signals may create a check-in candidate, not a mood fact. Wearable signals such as sleep, resting heart rate, HRV, activity load or proprietary recovery scores are supporting context only.

Safe sequence:

```text
sleep/recovery/activity change
+ another independent change
→ optional check-in
→ user reports mood/energy
→ confirmed record
```

Unsafe:

```text
low recovery score
→ "you are stressed"
```

Provider-defined scores must be labelled as provider metrics, not transformed into clinical labels.

---

# 10. Segment-of-one behavioural analysis

## 10.1 Definition

A segment of one is a user-owned, continuously updated model of confirmed routines, contexts, actions and reported responses.

The v5 addition is that **every analytical feature is filtered by provider policy before it enters the model**.

Pipeline:

```text
Imported signal
→ provenance
→ provider-policy check
→ normalisation
→ de-duplication
→ confirmation/reliability
→ comparable personal baseline
→ association analysis
→ governed recommendation
```

A source that is classified as display-only never enters the analytical layer.

## 10.2 Recommendation-response loop

Record:

```text
recommendation shown
→ viewed
→ accepted / rejected
→ action completed / not completed
→ subsequent response recorded
→ relevance updated
```

This remains the proposed long-term data advantage.

---

# 11. Spain-first localisation and market rollout

Spain remains the source market.

The wearable strategy must also be market-local:

- iOS versus Android device mix.
- Popular wearable brands by pilot cohort.
- Availability of provider programmes in Europe.
- Spanish-language OAuth/consent copy.
- EU/Spain privacy review for direct provider integrations.
- Market-specific deletion and support procedures.

Do not build a Garmin, WHOOP or Samsung connector only because it is globally recognizable. Build from observed Spain pilot demand and unique signal value.

---

# 12. Women’s Health & Nutrition Now — editorial and news layer

The v4 editorial strategy remains:

- Regulator-first.
- General information clearly separate from personal recommendations.
- Human review for health/medication topics.
- Spain-first sources such as AEMPS/AESAN/EMA.
- No inference of medication use, diagnosis or body goal from browsing.
- No use of health-platform data to target medicine news.

Wearable data may support general wellbeing context, but it must never be used to imply that a user needs a medicine or diagnosis.

---

# 13. Product experience and visual-design proposal

## 13.1 Today screen

```text
Hoy
├── Cycle / life-stage chip
├── Daily Context strip
├── Quick actions
│   ├── Comida
│   ├── Movimiento
│   └── Ánimo y energía
├── Connected-signals status
├── Confirmed daily timeline
├── One personal insight
└── One clearly separate editorial card
```

## 13.2 Connected signals component

Example:

> **Tus conexiones**  
> Apple Health · conectado hace 12 min  
> Workouts · Sueño · Pasos  
> **Gestionar**

For a restricted connector:

> **Strava**  
> Conectado para funciones permitidas. Sus datos no se utilizan en el motor de IA ni en el análisis personal de NutriSync.

Only show this if the actual implemented use is contractually permitted.

---

# 14. Unified user journeys

## J1 — Apple Health import

A user grants workouts and sleep. NutriSync imports only those categories, shows Apple Health as the source and uses the records in the personal timeline.

## J2 — Garmin direct + Apple Health duplicate

A strength workout arrives from Garmin’s direct API and also appears through HealthKit. The de-duplication engine matches source/time/duration and stores one activity with multiple provenance references.

## J3 — WHOOP recovery context

A user connects WHOOP. NutriSync may show the WHOOP recovery value as provider-sourced context and compare it with the user’s own confirmed energy reports, only where terms permit. It does not call a low score a diagnosis.

## J4 — Strava restriction

The user connects Strava for an allowed feature. The policy registry prevents the record from being passed to OpenAI, embeddings, personal cross-domain analytics or long-term indexing.

## J5 — Connector revocation

The user disconnects Fitbit. NutriSync revokes tokens, stops sync, follows provider deletion obligations, and explains which historical NutriSync records remain or are removed under the applicable policy/consent.

---

# 15. Technical architecture

## 15.1 Target architecture

```text
React Native
│
├── Camera / voice / manual capture
├── HealthKit
├── Health Connect
├── Local permissions
└── Optional provider OAuth launch
        │
        ▼
Supabase API Boundary
│
├── Auth / RLS / Storage
├── Health Connection Registry
├── Provider Token Vault
├── Source Policy Registry
├── Health Sync Workers
├── Signal Normaliser
├── Activity De-duplicator
├── Queues / Realtime
└── Personal Timeline
        │
        ├── OpenAI Responses API
        │     └── only policy-cleared payloads
        │
        ├── Canonical nutrition sources
        ├── Weather/context services
        └── Editorial pipeline
```

## 15.2 New domain-specific functions

```text
connect-health-source
exchange-provider-token
refresh-provider-token
sync-provider-data
normalise-health-signal
enforce-source-policy
reconcile-duplicate-activity
disconnect-health-source
delete-provider-derived-data
audit-source-usage
```

## 15.3 Hard architectural rule

No raw provider payload is sent directly from a sync worker to an LLM.

Required path:

```text
provider payload
→ source policy
→ normalisation/minimisation
→ allowed-use decision
→ feature-specific payload
→ AI only if permitted
```

---

# 16. Data model and event lifecycle

## 16.1 New core entities

| Domain | Suggested entities |
|---|---|
| Health connections | `health_connections`, `provider_tokens`, `health_sync_state`, `provider_scopes` |
| Source governance | `source_policy_registry`, `source_policy_versions`, `allowed_processing_rules` |
| Normalised signals | `health_signals`, `health_signal_provenance`, `health_signal_derivations` |
| Activity | `activity_logs`, `activity_components`, `activity_source_links`, `activity_candidates` |
| Audit | `source_usage_audit`, `provider_deletion_jobs`, `provider_revocations` |

## 16.2 Representative connection record

```sql
create table public.health_connections (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  provider text not null,
  connection_type text not null,
  status text not null,
  scopes text[] not null,
  policy_version text not null,
  connected_at timestamptz not null default now(),
  last_sync_at timestamptz,
  disconnected_at timestamptz
);
```

## 16.3 Representative signal provenance

```sql
create table public.health_signal_provenance (
  id uuid primary key default gen_random_uuid(),
  signal_id uuid not null,
  source_platform text not null,
  source_application text,
  source_device text,
  source_record_id text,
  provider_policy_class text not null,
  ai_allowed boolean not null default false,
  analytics_allowed boolean not null default false,
  retention_deadline timestamptz,
  imported_at timestamptz not null default now()
);
```

## 16.4 Deletion lifecycle

```text
disconnect requested
→ provider token revoked where supported
→ future sync stopped
→ provider-specific deletion obligations evaluated
→ derived-data dependency graph evaluated
→ delete/recompute affected derived records
→ user-visible completion
→ auditable confirmation
```

---

# 17. AI model strategy and evaluation

The v4 model strategy remains, with one new mandatory evaluation dimension: **source-policy compliance**.

For every AI job, log:

```text
input source classes
policy decision
data minimisation result
model
prompt/schema version
output
retention class
```

Release metric:

> **Provider-restricted data reaching prohibited AI route: 0.**

The same applies to embeddings, vector stores, RAG, model evaluation and prompt context.

---

# 18. Privacy, security and controlled sharing

## 18.1 Direct-provider data adds new risks

- OAuth token theft.
- Over-broad scopes.
- Provider terms changing after launch.
- Data retained after user revocation.
- Double collection through OS and direct provider.
- Secondary use not permitted by source contract.
- Proprietary health/recovery scores being misrepresented.
- Cross-border processing differences.

Controls:

- Encrypted server-side token vault.
- Shortest necessary scopes.
- Automated policy-version review reminders.
- Connector kill switch.
- Provider-specific deletion worker.
- Source labels on every derived record.
- No general “health data” permission abstraction that hides source differences.

## 18.2 Provider terms change management

Create a quarterly and event-driven review:

```text
policy/terms changed
→ legal/product review
→ source_policy_registry updated
→ affected features identified
→ processing blocked if necessary
→ user communication if material
→ deletion/re-consent workflow where required
```

Strava demonstrates why this is necessary: a technically functioning API can become strategically unsuitable for a planned analytics/AI use without the endpoint disappearing.

---

# 19. Expert and community recommendation layer

No change to the core v4 rule:

```text
private profile
+ approved card metadata
→ private ranking
→ card shown
```

Direct wearable providers, experts and community contributors do not receive the user’s private NutriSync profile unless a separate, explicit sharing grant authorises a defined scope.

Provider data should never be disclosed to a professional merely because the professional is connected to the user’s NutriSync account.

---

# 20. Implementation roadmap

## Phase A — Spain-first language, trust and policy foundation

Add:

- Health-provider inventory for Spain pilot.
- Source-policy registry.
- Provider terms/legal review template.
- Consent copy for OS health stores and direct connectors.

## Phase 0 — Trust and data foundation

Add:

- Provenance schema.
- Provider-policy classes.
- Connector audit/deletion framework.

## Phase 1 — Meal intelligence pilot

No material v5 change.

## Phase 2 — Core health integration

Deliver:

- Apple HealthKit.
- Android Health Connect.
- Workouts, steps and sleep first.
- De-duplication.
- Trust Centre connection management.

Gate:

- Permission and revocation flows pass store/privacy review.
- Duplicate rate within target.
- 100% source provenance.

## Phase 3 — Specialist direct connector pilot

Recommended order:

1. WHOOP, if Spain/user demand supports it.
2. Garmin.
3. Fitbit/Oura.
4. Samsung direct, after partnership approval.
5. Polar/Huawei based on cohort demand.

Gate:

- Commercial terms approved.
- Policy registry complete.
- Connector can be disabled independently.
- Deletion tested.

## Phase 4 — Smart Places and life context

Proceed after core health import so location remains supporting evidence.

## Phase 5 — Contextual Wellbeing and Personal Rhythm

Only policy-cleared wearable signals enter personal analytics.

## Phase 6 — Governed recommendation loop

Measure whether adding sleep/recovery/activity context improves recommendation relevance versus nutrition/cycle data alone.

## Phase 7 — Women’s Health & Nutrition Now

Continue in parallel with regulator-first governance.

## Strava workstream

Do **not** make Strava a Phase 2 dependency. Keep a legal/product watch item. If its terms change, re-evaluate through the same connector decision test.

---

# 21. KPIs and release gates

Add the following v5 metrics:

| KPI | Target use |
|---|---|
| Connected-health activation | Demand for integrations |
| Permission completion by data type | Consent UX quality |
| Sync success/failure rate | Operational quality |
| Duplicate workout rate | Data trust |
| Source provenance completeness | Governance |
| Direct connector cost per active user | Commercial viability |
| Provider-restricted data sent to AI | **0** |
| Provider-restricted data used in prohibited analytics | **0** |
| Revocation/deletion SLA compliance | Trust |
| Connector-specific support incidents | Maintainability |
| OS aggregation coverage vs direct connector gap | Build-vs-buy decision |

---

# 22. Founder decisions

| ID | Decision | Recommended choice |
|---|---|---|
| **D12–D27** | v4 decisions | Retain unless explicitly superseded |
| **D28** | Health integration architecture | HealthKit + Health Connect first |
| **D29** | Direct connector principle | Build only for unique value/gaps |
| **D30** | Strava dependency | No core dependency |
| **D31** | Strava AI/analytics | Prohibit while current policy applies |
| **D32** | Provider provenance | Mandatory on every imported/derived signal |
| **D33** | Provider policy enforcement | Machine-enforced source policy registry |
| **D34** | First specialist connector | WHOOP or Garmin, selected from Spain pilot demand |
| **D35** | Samsung | Do not commit to production until partnership approval |
| **D36** | Fitbit | Health Connect first; direct API only for justified gaps |
| **D37** | Connector removal | Every connector independently removable |
| **D38** | Terms monitoring | Quarterly + event-driven review |

Recommended approval shorthand:

> **Approve Proposal 32 v5 as the v4 product/trust architecture plus a source-aware health integration layer. Make HealthKit and Health Connect the core, keep direct wearable connectors selective, and explicitly exclude Strava API data from NutriSync AI/segment-of-one processing while current terms prohibit that use.**

---

# 23. User-facing trust and Spain-Spanish copy

## 23.1 Connected health

> **Tus datos de salud, bajo tu control.**  
> Tú eliges qué fuentes conectar y qué categorías compartir. Puedes desconectar una fuente cuando quieras. NutriSync conserva el origen de cada dato y aplica las condiciones específicas de cada plataforma.

## 23.2 Direct wearable

> **Conectar WHOOP / Garmin / Fitbit / Oura**  
> Esta conexión es opcional. Antes de activarla te mostraremos qué datos se importan, para qué se usan y cómo puedes retirar el permiso.

## 23.3 Restricted source

> **Algunas plataformas limitan cómo pueden utilizarse sus datos.**  
> NutriSync respeta esas condiciones técnicamente: si una fuente no permite análisis con IA o combinación con otros datos, esa información no entra en esas funciones.

## 23.4 Trust FAQ addition

**¿NutriSync necesita conectarse directamente con todas mis apps deportivas?**  
No. En iPhone priorizamos Apple Health y en Android Health Connect cuando ofrecen las señales necesarias. Las conexiones directas se añaden solo cuando aportan datos relevantes que no están disponibles por esa vía.

**¿Por qué algunas conexiones no pueden utilizarse para todos los análisis?**  
Porque cada proveedor establece condiciones distintas. NutriSync aplica esas restricciones por fuente en lugar de asumir que todo dato autorizado puede utilizarse para cualquier finalidad.

---

# 24. References

## Internal NutriSync baseline

**[I1] NutriSync Proposal 32 v4 — Daily Intelligence, Spain-First Localisation and Trust Architecture.** 9 August 2026. Baseline product, trust, AI, localisation, activity, wellbeing, editorial, architecture and roadmap proposal.

## Core health platforms

**[R40] Apple — Authorizing access to health data.** Fine-grained HealthKit permissions by data type.  
https://developer.apple.com/documentation/healthkit/authorizing-access-to-health-data

**[R41] Apple — HealthKit.** Central health and fitness framework and privacy model.  
https://developer.apple.com/documentation/healthkit

**[R42] Android — Get started with Health Connect.** SDK, declarations, permissions and read/write health data.  
https://developer.android.com/health-and-fitness/health-connect/get-started

**[R43] Android — Health Connect data types and permissions.** Historical/background access requirements and supported records.  
https://developer.android.com/health-and-fitness/health-connect/data-types

## Direct wearable / fitness providers

**[R44] Garmin — Garmin Connect Developer Program FAQ.** Business access and commercial/licensing considerations for some metrics/use cases.  
https://developer.garmin.com/gc-developer-program/program-faq/

**[R45] Garmin — Health API.** All-day health metrics including steps, heart rate, sleep and stress.  
https://developer.garmin.com/gc-developer-program/health-api/

**[R46] Garmin — Activity API.** Detailed fitness activity data.  
https://developer.garmin.com/gc-developer-program/activity-api/

**[R47] WHOOP — Developer API.** OAuth-based access to sleep, recovery and workout data.  
https://developer.whoop.com/api/

**[R48] WHOOP — OAuth 2.0.** User authorisation flow.  
https://developer.whoop.com/docs/developing/oauth/

**[R49] Fitbit — Web API explorer.** OAuth-accessible activity, body, device, heart-rate, sleep and related resources.  
https://dev.fitbit.com/build/reference/web-api/explore/

**[R50] Fitbit — Activity intraday API.** Third-party intraday access may require a request.  
https://dev.fitbit.com/build/reference/web-api/intraday/get-activity-intraday-by-date-range/

**[R51] Oura — API documentation.** OAuth2-based API and rate-limit/error handling.  
https://cloud.ouraring.com/docs/

**[R52] Samsung — Health Data SDK app creation process.** Distribution requires partnership/registration; developer mode otherwise.  
https://developer.samsung.com/health/data/process.html

**[R53] Polar — AccessLink API v3.** OAuth2 access to training and daily activity data.  
https://www.polar.com/accesslink-api/

**[R54] Huawei — Health Service Kit.** User-authorised health/fitness data access and application review.  
https://developer.huawei.com/consumer/en/hms/huaweihealth/

## Strava policy — strategic restriction

**[R55] Strava — API Policy (effective 1 June 2026).** Access tiers, endpoint controls, AI/ML restrictions, analytics restrictions, retention and deletion obligations.  
https://www.strava.com/legal/api_policy

**[R56] Strava — Getting Started / rate limits.** Application access mode and API limits.  
https://developers.strava.com/docs/getting-started/

---

> **Final recommendation**  
> Approve Proposal 32 v5. Preserve the v4 trust, Spain-first, multimodal and segment-of-one architecture, but add a provider-aware Health Gateway. Use Apple HealthKit and Android Health Connect as the default integration plane; add direct wearable connectors only for demonstrable signal value; and treat provider terms as enforceable product policy. This avoids strategic dependence on brands, reduces integration cost, strengthens user control and protects the segment-of-one learning model from source-specific contractual restrictions.
