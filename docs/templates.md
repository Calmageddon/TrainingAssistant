# Included templates

*Deutsche Fassung: [vorlagen.md](vorlagen.md)*

The integration ships proven training programs as templates
(`custom_components/training_assistant/templates/`). In the card under **Settings → Templates**
you add them with one click. They are not imported automatically. Afterwards you can edit
them like any plan. **The weights are starting values** – adjust them before your first
workout. From then on progression takes over.

The names are our own. Well-known programs are trademarks or books; the templates are
**inspired by** them (set/rep schemes), not copied. If you want to do the original,
read the respective source.

## Strength & hypertrophy

| Template | Days | For whom | Inspired by |
|---|---|---|---|
| Beginner Strength 5×5 | 3×/week, A/B | beginners with a barbell | StrongLifts 5×5 / Starting Strength |
| Tiered Program 4 Days | 4×/week | after the first months | GZCLP (Cody Lefever) |
| Push/Pull/Legs | up to 6×/week | hypertrophy, lots of time | r/Fitness "PPL for beginners" |
| Upper/Lower 4 Days | 4×/week | hypertrophy, intermediates | research (see below) |
| Full Body at Home (Dumbbells) | 3×/week | at home, little equipment | research (see below) |
| Full Body 3 Days (Gym) | 3×/week, A/B/C | gym, beginners, 3 days | frequency/volume research (Schoenfeld et al.) |
| Minimal Strength 2 Days | 2×/week, ~30 min | little time, 1–2 hard sets per exercise | minimal-dose reviews (Androulakis-Korakakis 2020, Nuzzo 2024) |

**Research in short:** For muscle growth, **weekly volume** is what matters. About 10 or more
hard sets per muscle per week bring more than fewer, but even ≤ 4 sets work. **Frequency**
(1–3× per week) hardly matters at equal volume; 2× per week just makes it easier to spread the
volume. Training is usually done in the 6–15 rep range close to failure.

Simplifications: the format knows no percentages and no "last set as many as possible" sets.
That is a hint on the exercise; progression calculates across all sets.

## Bodyweight – no equipment

For home, hotel and travel: no pull-up bar or dip bars needed, at most a chair and a sofa.
Difference to calisthenics: there you need a bar and dip bars and work towards skills.

| Template | Purpose | Basis |
|---|---|---|
| 7-Minute Circuit | conditioning, 12 exercises of 30 s, 2 rounds | Klika & Jordan, ACSM's Health & Fitness Journal 2013 |
| Full-Body Strength, No Equipment | strength/muscle, 3×/week | push-up ≈ bench press at equal effort (Kikuchi & Nakazato 2017) |
| 20-Minute Travel Circuit | as many rounds as possible in 20 min | common circuit format |
| Exercise Snacks | 3 mini workouts of 2–5 min spread over the day | stair snacks (Jenkins et al. 2019, Allison et al. 2017), VILPA (Stamatakis et al. 2022) |
| Balance & Leg Strength | fall prevention, older adults, 3×/week | inspired by the Otago Exercise Programme (Campbell et al. 1997); Cochrane review Sherrington et al. 2019 |
| Core Stability Trio | back-friendly core, ~10 min, daily | inspired by Stuart McGill's "Big 3" |

## Calisthenics

| Template | For whom | Inspired by |
|---|---|---|
| Calisthenics Level 0 (Starter) | no prior experience | common beginner progressions |
| Calisthenics Basics | 3×5 of the basic exercises at an easy level | r/bodyweightfitness Recommended Routine |
| Calisthenics Advanced | 3×8 pull-ups and dips | intermediate progressions |

Calisthenics progresses through **harder variations**. The templates use rep progression
(+1 rep per session). At the upper limit the hint "harder variation" appears. Which variation
comes next is noted as "Levels – …" on the exercise. Then change the name in the plan
(Edit → import again).

## Kettlebell

| Template | For whom | Inspired by |
|---|---|---|
| Kettlebell Swing & Get-up | daily, foundation | Simple & Sinister (Pavel Tsatsouline) |
| Kettlebell Armor Building Complex | strength and mass, two bells | protocol by Dan John |
| Kettlebell Full Body | one bell, 3×/week | press ladders from "Enter the Kettlebell" |
| Kettlebell Swing Intervals | conditioning, short | common swing intervals |

## HIIT & Tabata

Short, hard intervals, timed. Announcements or beeps (blueprint *Signals*) mark the switches.
Every interval is stored as a set, so HIIT counts in the history and weekly view.

| Template | Purpose | Basis |
|---|---|---|
| Tabata Circuit, No Equipment | 4× Tabata (8× 20/10) with bodyweight | Tabata et al. 1996 |
| Tabata Strength (Kettlebell) | 4× Tabata with swings, goblet squats, push-ups | Tabata protocol |
| 10×1 Intervals | 10 × 60 s hard / 60 s easy | Little & Gibala 2010 |
| 4×4 Intervals | 4 × 4 min at 85–95 % HRmax, 3 min easy | Helgerud et al. 2007 |
| 30-20-10 Intervals | 3 blocks of 5 × (30 s easy, 20 s moderate, 10 s sprint) | Gunnarsson & Bangsbo 2012 |
| Sprint Intervals 30/4 | 5 × 30 s all-out, 4 min easy | Burgomaster, Gibala et al. 2005–2008 |

The kettlebell swing intervals stay in the kettlebell group.

## Endurance

Running and steady cardio, timed: the switches between running and walking are marked by a beep (or an announcement).

| Template | Purpose | Basis |
|---|---|---|
| Run Starter 9 Weeks | from walking to 30 min running, 27 runs in order | inspired by the NHS Couch to 5K plan |

## Yoga & mobility

Timed flows: every pose is announced and switches automatically, sides included. Every pose is
stored with its duration. Classic poses (downward dog, warriors, tree, cobra) have no image in the
catalog; their muscle groups are set in the template.

| Template | Purpose | Basis |
|---|---|---|
| Yoga Basics | 2 sessions with the foundation poses, ~20 min | classic hatha poses |
| Sun Salutation Flow | 5 rounds sun salutation, ~15 min | classic sequence |
| Back Care Yoga | gentle, "Gentle" then "Building", ~20 min | inspired by "Back to Health" (Saper et al., Boston Medical Center) |
| Mobility for Lifters | hips & legs or shoulders & spine, ~10 min | yoga-based mobility |
| Yin Yoga | long holds (2–4 min), ~35 min | yin yoga |
| Balance & Strength Yoga | warriors, tree, chair, boat, planks, ~25 min | standing and core poses |

Evidence: the back care study (12 weeks, weekly class) found yoga about as effective as physical
therapy for chronic low back pain; for other sequences there are few controlled studies – they are
common, safe foundation sequences.

## Sources

- Schoenfeld, Grgic, Krieger (2019): *How many times per week should a muscle be trained to maximize muscle hypertrophy?*, [Semantic Scholar](https://www.semanticscholar.org/paper/How-many-times-per-week-should-a-muscle-be-trained-Schoenfeld-Grgic/5f3b9845fdfd15200bdac0f7b9b36da457c48025)
- Summary of volume studies (Schoenfeld 2017 et al.): [Nutrient Metrics](https://nutrient-metrics.com/en/hypertrophy/training-volume-for-hypertrophy/)
- Volume-equated frequency studies (preprint 2026): [medRxiv](https://www.medrxiv.org/content/10.64898/2026.10.07.26365015v3.full)
- StrongLifts vs. Starting Strength: [Outlift](https://outlift.com/starting-strength-vs-stronglifts-5x5/)
- GZCLP: [r/gzcl Wiki](https://reddit.sudovanilla.org/r/gzcl/wiki/GZCLP), [Lift Vault](https://liftvault.com/programs/strength/gzclp-program-spreadsheets/)
- Push/Pull/Legs vs. Upper/Lower: [Speediance](https://www.speediance.com/blogs/strength-programming/upper-lower-vs-ppl-4-day)
- r/bodyweightfitness Recommended Routine: [Antranik](https://antranik.org/rr/), [GitHub mirror](https://github.com/NearHuscarl/recommended-routine)
- Calisthenics levels: [Gravity Fitness](https://gravity.fitness/blogs/training/calisthenics-exercises-every-body-should-master-from-beginner-to-advanced)
- 7-minute workout (Klika & Jordan 2013): [Topend Sports](https://www.topendsports.com/fitness/programs/7min-workout.htm), [original format](https://7minuteworkoutapp.com/blog/original_7_minute_workout_explained.html)
- Push-up vs. bench press (Kikuchi & Nakazato 2017): [ResearchGate](https://www.researchgate.net/publication/318024465_Low-load_bench_press_and_push-up_induce_similar_muscle_hypertrophy_and_strength_gain)
- Simple & Sinister (summary): [kitchi-gami](https://kitchi-gami.com/2023/02/02/kettlebells-simple-and-sinister/)
- Armor Building Complex: [The Workout Mag](https://theworkoutmag.com/training-guide/armor-building-complex-kettlebell-guide)
- Tabata et al. (1996): *Effects of moderate-intensity endurance and high-intensity intermittent training on anaerobic capacity and VO2max*, Med Sci Sports Exerc
- Little, Gibala et al. (2010): *A practical model of low-volume high-intensity interval training*, J Physiol
- Helgerud et al. (2007): *Aerobic high-intensity intervals improve VO2max more than moderate training*, Med Sci Sports Exerc
- Gunnarsson & Bangsbo (2012): *The 10-20-30 training concept improves performance and health profile in moderately trained runners*, J Appl Physiol
- Burgomaster, Gibala et al. (2005, 2008): sprint interval training studies, J Appl Physiol / J Physiol
- Back to Health (Saper et al.): [Teacher manual, Boston Medical Center](https://media.defense.gov/2019/Oct/22/2002198487/-1/-1/0/YOGA%20FOR%20CHRONIC%20LOW%20BACK%20PAIN%20STUDY.PDF), [protocol](https://d-scholarship.pitt.edu/29589/)
- Androulakis-Korakakis et al. (2020): *The minimum effective training dose required to increase 1RM strength in resistance-trained men*, Sports Med
- Nuzzo et al. (2024): *Resistance Exercise Minimal Dose Strategies for Increasing Muscle Strength in the General Population: an Overview*, [Sports Med / PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11127831/)
- Jenkins et al. (2019): stair-climbing exercise snacks, Appl Physiol Nutr Metab; Allison et al. (2017): brief intense stair climbing, PLOS ONE
- Stamatakis et al. (2022): *Association of wearable device-measured vigorous intermittent lifestyle physical activity with mortality*, Nature Medicine
- Otago Exercise Programme (Campbell et al. 1997): [Physiopedia](https://www.physio-pedia.com/Otago_Exercise_Programme); Sherrington et al. (2019): *Exercise for preventing falls in older people living in the community*, Cochrane
- McGill "Big 3": Stuart McGill, *Low Back Disorders* / *Back Mechanic*
- NHS Couch to 5K: [running plan](https://www.nhs.uk/better-health/get-active/get-running-with-couch-to-5k/couch-to-5k-running-plan/)
