# ASD-STE100 Simplified Technical English (STE) Reference

ASD-STE100 is an international specification for the preparation of technical documentation in a controlled language. Originally created by AECMA in 1979/1986 and maintained by the ASD Simplified Technical English Maintenance Group (STEMG), it eliminates ambiguity, reduces sentence complexity, and enforces strict vocabulary and grammar constraints.

---

## 1. Document Structure & Core Principles

ASD-STE100 consists of two core parts:
- **Part 1: Writing Rules** (Grammar, syntax, style constraints)
- **Part 2: Dictionary** (~900 approved general English words + defined technical names/verbs)

### Fundamental Conventions
1. **One Word = One Meaning + One Part of Speech**: An approved word keeps only its listed meaning and part of speech. For example, `CLOSE` is strictly a verb ("to move together; to stop flow"), never an adjective meaning "near".
2. **Uppercase vs Lowercase**: Approved words appear in `UPPERCASE` in guides/rules. Unapproved words appear in `lowercase`.
3. **Consistency**: Use the same word for the same concept every time. Never use synonyms for variety.
4. **No Missing Articles**: Do not omit articles (`the`, `a`, `this`, `these`).
5. **Vertical Lists**: Use vertical lists for sequential steps or lists of 3+ items.

---

## 2. Hard Quantitative Rule Limits

| Metric | Upper Limit | Notes |
| :--- | :--- | :--- |
| **Procedural sentence** | **Max 20 words** | Action/instruction steps. |
| **Descriptive sentence** | **Max 25 words** | Conceptual, explanatory, or factual text. |
| **Descriptive paragraph** | **Max 6 sentences** | Exactly one topic per paragraph. |
| **Noun cluster** | **Max 3 words** | Maximum 3 nouns strung together (e.g., `hydraulic reservoir cap`). |
| **Instructions per sentence** | **Max 1 instruction** | Unless two actions are strictly simultaneous. |

---

## 3. Approved vs Unapproved Verb Forms

| Verb Form | Example | Status | STE Rule |
| :--- | :--- | :--- | :--- |
| **Command (Imperative)** | *Close the valve.* | **Approved** | Mandatory for procedural steps. |
| **Simple Present** | *The valve closes.* | **Approved** | Standard for system behavior. |
| **Simple Past** | *The valve closed.* | **Approved** | For past events. |
| **Simple Future** | *The valve will close.* | **Approved** | For future conditions. |
| **Infinitive** | *Turn the knob to close it.* | **Approved** | With `to` + root verb. |
| **Past Participle (as adjective)** | *The closed valve.* | **Approved** | Adjectival modifier only. |
| **Progressive (-ing)** | *The valve is closing.* | **NOT Approved** | Never use progressive tenses. Use `-ing` only inside a technical name (e.g. *landing gear*, *operating system*). |
| **Perfect Tenses** | *The valve has closed.* | **NOT Approved** | Ban `has/have/had + past participle`. Use simple past instead. |
| **Passive Voice (in procedures)** | *The valve must be closed.* | **NOT Approved** | Procedural text must be 100% active voice (*Close the valve*). Descriptive text can use passive only when strictly unavoidable. |

---

## 4. Safety Instructions Format

STE standardizes safety notices into strict categories:
- **`WARNING`**: Risk of personal injury or death.
- **`CAUTION`**: Risk of equipment damage or data loss.

**Structure**:
1. First: A clear, simple command.
2. Second: The reason / identified risk.

```text
WARNING: Do not touch the brake unit until it is cool. Hot parts can cause injury.
CAUTION: Do not turn off the power during the flash write. This will damage the device firmware.
```

---

## 5. Common Dictionary Replacements

| Unapproved Word / Phrase | Approved Alternative | Incorrect Example | Approved STE Example |
| :--- | :--- | :--- | :--- |
| `commence` (v) | **START** | *Commence pumping.* | **START the pump.** |
| `ensure` (v) | **MAKE SURE** | *Ensure the switch is off.* | **MAKE SURE that the switch is off.** |
| `prior to` (prep) | **BEFORE** | *Prior to starting the engine.* | **BEFORE you start the engine.** |
| `replenish` (v) | **FILL** | *Replenish the reservoir.* | **FILL the reservoir.** |
| `utilize` (v) | **USE** | *Utilize a torque wrench.* | **USE a torque wrench.** |
| `approximately` (adv) | **ABOUT** | *Wait approximately 10 minutes.* | **Wait for ABOUT 10 minutes.** |
| `in order to` | **TO** | *Remove the panel in order to get access.* | **Remove the panel TO get access.** |
| `terminate` (v) | **STOP** / **END** | *Terminate the process.* | **STOP the process.** |
| `close` (adj) | **NEAR** | *Put the tool close to the panel.* | **Put the tool NEAR the panel.** |
| `modify` (v) | **CHANGE** | *Modify the configuration file.* | **CHANGE the configuration file.** |
| `obtain` (v) | **GET** | *Obtain the authorization token.* | **GET the authorization token.** |
| `subsequent to` | **AFTER** | *Subsequent to the restart.* | **AFTER the restart.** |

---

## 6. The "80% ASD-STE100" Softening

Pure ASD-STE100 is designed for aerospace maintenance where a misunderstanding causes plane crashes. In software engineering, computer science, and LLM comprehension:
- Strict 900-word dictionary rules can cause friction with modern computing terms (e.g. *idempotency*, *asynchronous*, *backpressure*, *sharding*).
- **The "80% ASD-STE100" standard** preserves all high-value structural constraints while allowing natural domain terminology:
  1. **Strict sentence length caps** (procedural ≤ 20 words, descriptive ≤ 25 words).
  2. **Active voice imperative** for all actions and workflows.
  3. **Zero progressive (-ing) and zero perfect tenses** (use simple present/past).
  4. **Max 3-word noun clusters**.
  5. **Max 1 instruction per sentence**.
  6. **Max 6 sentences per paragraph**.
  7. **Zero AI filler words & marketing adjectives** (*delve, leverage, tapestry, revolutionize, seamlessly, comprehensive, robust, blazing-fast*).
  8. **Core plain verb substitutions** (*make sure* instead of *ensure*, *before* instead of *prior to*, *use* instead of *utilize*).

---

## 7. Advanced Structural Heuristics

### A. Total Semicolon Ban (Rule 8.1)
ASD-STE100 permits standard punctuation marks (period, comma, colon, hyphen, parentheses, quotes), but **strictly bans the semicolon (`;`)**. Semicolons hide compound run-on sentences. Split every semicolon into two distinct sentences.

### B. No Nominalizations (Rule 3.7)
Do not freeze an action into a noun. Use the direct verb:
- *Bad*: "Perform an analysis of the logs." $\rightarrow$ *Good*: "Analyze the logs."
- *Bad*: "Provides assistance to the worker." $\rightarrow$ *Good*: "Helps the worker."
- *Bad*: "Carry out the installation." $\rightarrow$ *Good*: "Install the software."

### C. No Soft Phrasal Verbs (Rule 9.3)
Phrasal verbs (verb + preposition) confuse international readers and LLM parsers. Replace with a single unambiguous verb:
- `spin up` $\rightarrow$ **start**
- `reach out` $\rightarrow$ **contact**
- `dive into` $\rightarrow$ **read / inspect**
- `kick off` $\rightarrow$ **begin**
- `circle back` $\rightarrow$ **return**
- `touch base` $\rightarrow$ **communicate**

### D. Modality & Hedge Preservation (Critical Principle)
**Never upgrade a hedge to a false fact.**
If the source states: *"The node may have dropped the connection"*, do NOT simplify to *"The node dropped the connection"*.
Hedges (*may, could, might, is likely to*) convey author confidence and probabilistic reality. Shortening sentences must never sacrifice epistemic accuracy.

### E. No Synonym Rotation
Never use different words for the same component in the same document. If you call it `primary replica`, never alternate with `master node` or `main instance`. Use one term consistently.
