/*
 * TrainingAssistant – Dashboard-Karte
 * Wird von der Integration automatisch geladen (keine Ressource nötig).
 * Karte im Dashboard: type: custom:training-assistant-card
 */
const CARD_VERSION = "0.5.0";
const DOMAIN = "training_assistant";

/* ------------------------------------------------------------------ Sprachen
 * Die Karte folgt der Sprache von Home Assistant (Profil des Nutzers), sonst Englisch.
 * Neue Sprache: Eintrag mit denselben Schlüsseln wie "en" ergänzen – fehlende fallen auf Englisch zurück.
 */
const I18N = {
  en: {
    tab_training: "Training", tab_history: "History", tab_plans: "Settings", loading: "Loading …",
    conn_failed: "Could not connect to the integration: {err}. Is TrainingAssistant set up?",
    st_planned: "planned", st_pending: "asking …", st_confirmed: "confirmed", st_corrected: "corrected",
    st_edited: "edited", st_unconfirmed: "unconfirmed", st_skipped: "skipped",
    ph_ready: "Ready", ph_active: "Training", ph_interval: "HIIT", ph_finished: "Done", ph_paused: "Paused",
    ty_warmup: "Warm-up", ty_circuit: "Circuit", ty_sets: "Sets", ty_interval: "HIIT", ty_flow: "Flow", ty_cooldown: "Cool-down",
    u_reps: "reps", u_sec: "sec", per_side: "per side", per_side_short: "/side",
    hold_max_short: "hold max", amrap_short: "max reps", reps_n: "{n} reps", tile_hold: "sec hold", goal_range: "goal {lo}–{hi}",
    pos_round_of: "Round {r}/{n}", pos_round: "Round {r}", pos_set_of: "Set {s}/{n}", pos_set: "Set {s}",
    no_plan: "No training plan yet.", import_plan: "Import plan", start: "▶ Start workout", program: "Program",
    workout: "Workout", wo_pos: "Workout {p} of {n}", wo_after: " · then {name}",
    wo_auto: " · after finishing, the program moves on automatically.", voice_via: "Announcements via {sat}",
    no_sat: "No default satellite: the workout runs silently on this card (choose a satellite in the integration options or when starting by voice).",
    pv_rounds: "{n} rounds", pv_cap: "{m} min alternating", pv_between_ex: "{d} between exercises",
    pv_between_rounds: "{d} between rounds", pv_sets: "{n} sets", pv_sets_until: "Sets until {n} reps", pv_rest: "{d} rest",
    pv_interval: "{w} s work / {r} s rest", pv_block_rest: "⏸ {d} rest", pv_flow: "{n} steps · about {m} min",
    flow_switch: "Switch", b_end_flow: "End flow",
    tempo: "Tempo {t}", iv_work: "WORK", iv_rest: "REST", t_rest: "Rest", t_left: "Time left",
    t_up: "Time's up – finish the exercise", t_question: "Voice question … (Next = as planned)",
    b_resume: "▶ Resume", b_go: "▶ Go", b_end_hiit: "End HIIT", b_set_done: "✓ Set done",
    b_set_done_changed: "✓ Set done (changed)", b_next: "Next", step: "Step {i}/{n}", b_back: "↶ Back",
    b_pause: "❚❚ Pause", b_continue: "▶ Continue", b_skip: "⤼ Skip", b_finish: "⚑ Finish", c_finish: "Really finish?",
    b_discard: "✕ Discard", c_discard: "Really discard?", coming_up: "Coming up", logged: "Logged (tap to correct)",
    un_done: "Workout complete", un_label: "Up next",
    a_seconds: "Seconds", a_reps: "Reps", a_reps_side: "Reps/side", a_weight: "Weight", a_less: "{l} less", a_more: "{l} more",
    e_save: "Save", e_skipped: "Skipped", e_cancel: "Cancel",
    h_loading: "Loading history …", h_empty: "No workouts saved yet.", h_ex_meta: "{n}× · last {d}", h_sets: "{n} sets",
    h_unconfirmed: "{n} unconfirmed", h_aborted: "aborted", c_delete: "Really delete?", h_delete: "Delete workout",
    h_th_ex: "Exercise", h_th_hist: "History", h_last8: "(last 8)", h_th_last: "Last", h_th_next: "Next time",
    h_tab_ex: "Exercises", h_tab_sess: "Workouts",
    tpl_loading: "Loading templates …", n_workout: "{n} workout", n_workouts: "{n} workouts",
    tpl_reload_c: "Reload? Your own changes will be lost.", tpl_installed: "✓ Added · reload", tpl_take: "Add",
    p_active: "active program", p_noimg: "No image: {list}", p_edit: "Edit", p_delete: "Delete", p_next_badge: "up next",
    p_set_next: "Up next", p_start: "Start",
    p_tpl_intro: "Proven programs ready to add – afterwards they're ready to start under “My plans”. Weights are starting values; progression adjusts them.",
    p_import_intro: "Below is a commented example plan – adjust it and import. A plan with the same name is replaced, your history is kept. The guide explains everything and includes a ready-made prompt that lets ChatGPT or Claude write a plan for you.",
    p_dl_guide: "⤓ Guide (.txt)", p_dl_example: "⤓ Example plan (.yaml)", p_insert: "Insert example", p_clear: "Clear",
    p_placeholder: "schema_version: 1\nname: My plan\n…", p_import: "Import", p_none: "No plans yet.",
    p_pick_tpl: "Choose a template", p_own: "Create your own plan",
    p_tab_mine: "My plans", p_tab_tpl: "Templates", p_tab_own: "Own plan",
    m_imported: "“{name}” imported ({n} workouts). Images: {m} of {t} exercises", m_missing: " – no image: {list}",
    m_tpl: "Template “{name}” added ({n} workouts). Weights are starting values – please adjust.",
    m_example: "Example plan inserted – adjust it and import.",
    m_loaded: "Plan loaded – change it and import again (the same name replaces it).",
    c_first: "First workout with this exercise", c_last: "last {v} {u}", c_last_best: "last {v} · best {b} {u}",
    c_n: "{n} workouts", c_1: "1 workout", c_aria: "History {l}",
    guide_file: "guide-custom-plans.txt", example_file: "example-plan.yaml",
    guide_dl: "TrainingAssistant-Guide-Custom-Plans.txt", example_dl: "TrainingAssistant-Example-Plan.yaml",
    "sug.no_progression_timed": "No progression (time or max.)", "sug.plan_values": "Plan values (no history yet)",
    "sug.harder_variant": "All sets with {reps} reps done – harder variation or added weight",
    "sug.all_reps_add_weight": "All sets with {reps} reps done → +{kg} kg",
    "sug.hold_weight_target": "Keep the weight, aim for {target} reps (up to {max})",
    "sug.target_reps": "Aim for {target} reps (up to {max})",
    "sug.cap_reached": "Limit of {cap} reps reached – harder variation or added weight",
    "sug.all_reps_add_reps": "All sets with {reps} reps done → +{add} reps",
    "sug.repeat_target": "Target of {target} reps not yet reached in every set – repeat",
    "sug.all_done": "All sets done", "sug.all_done_add_weight": "All sets done → +{kg} kg",
    "sug.not_all_hold": "Not all sets done → keep the weight", "sug.fixed": "Fixed value from the plan (no progression)",
    "tg.kraft": "Strength & hypertrophy",
    "tg.kraft.about": "Barbell, dumbbells, machines – muscle and maximal strength in the gym or home gym.",
    "tg.bodyweight": "Bodyweight – no equipment",
    "tg.bodyweight.about": "At home, in a hotel, on the road – circuits and strength with a chair and sofa.",
    "tg.calisthenics": "Calisthenics",
    "tg.calisthenics.about": "Pull-up bar and dip bars – progress through ever harder variations up to skills.",
    "tg.kettlebell": "Kettlebell",
    "tg.kettlebell.about": "One or two bells – strength, muscular endurance and conditioning in little time.",
    "tg.hiit": "HIIT & Tabata",
    "tg.hiit.about": "Short, hard intervals – timed, with beeps or announcements. Bodyweight, kettlebell, bike, rower or running.",
    "tg.yoga": "Yoga & mobility",
    "tg.yoga.about": "Flows, stretching and balance – runs on its own, every pose is announced. A mat is enough.",
    "tg.other": "More",
    wk_title: "This week", wk_goal: "Goal (number of workouts)", wk_aria: "{d} of {n} workouts this week", wk_streak: "🔥 {n} weeks in a row",
    wk_streak1: "🔥 1 week", wk_bars: "Sets per day", wk_left: "{n} to go", wk_reached: "Weekly goal reached",
    wk_total: "{n} workouts logged in total", wk_goal_less: "Lower weekly goal", wk_goal_more: "Raise weekly goal",
    "mg.chest": "Chest", "mg.back": "Back", "mg.shoulders": "Shoulders", "mg.biceps": "Biceps", "mg.triceps": "Triceps",
    "mg.core": "Abs", "mg.quads": "Quads", "mg.hamstrings": "Hamstrings", "mg.glutes": "Glutes", "mg.calves": "Calves",
    h_tab_over: "Overview", tile_week: "This week", tile_streak: "Streak", tile_weeks: "{n} weeks", tile_week1: "1 week",
    tile_total: "Workouts in total", tile_since: "since {d}", tile_time: "Time this week", tile_time_avg: "Ø {m} min/week",
    rec_title: "Recent records", rec_none: "No records yet – they appear from your second workout with an exercise.",
    rec_weight: "{v} kg", rec_e1rm: "est. max {v} kg", rec_reps: "{v} reps", rec_duration: "{v} s", rec_prev: "before {v}",
    vol_title: "Sets per muscle group this week", vol_hint: "Guide: about 10 hard sets per muscle and week (line).",
    vol_last: "last week {n}", vol_none: "No sets this week yet.",
    vol_unassigned: "Without muscle group: {n} sets ({list}) – add muscles: […] to the exercise in the plan.",
    rc_title: "Recovery", rc_fresh: "Just trained", rc_recovering: "Recovering", rc_ready: "Ready", rc_soon: "Train soon", rc_overdue: "Overdue",
    rc_none: "Not trained yet", rc_h: "last {n} h ago", rc_d: "last {n} days ago", rc_since_h: "for {n} h",
    rc_since_d: "for {n} days",
    mt_primary: "Main muscle", mt_secondary: "Also worked",
    ef_last: "How did it feel?", ef_easy: "Easy", ef_normal: "Normal", ef_hard: "Hard",
    st_wait: "Waiting for Go", st_go: "Go!", el_title: "Workout time", el_last: "last time {d}",
    t_record: "🏆 New record: {name}", rest_less: "−15 s", rest_more: "+15 s",
    who: "Who's training?", p_tab_people: "People",
    pp_intro: "Every person has their own history, suggestions, weekly goal and program position. Plans are shared.",
    pp_active: "selected", pp_select: "Select", pp_rename: "Rename", pp_delete: "Delete", pp_c_delete: "Delete incl. history?",
    pp_add: "+ Add person", pp_name: "Name", pp_save: "Save", pp_busy: "You can select someone else after the workout.",
    pp_goal: "Weekly goal: {n} workouts",
    pp_user: "Home Assistant user", pp_user_none: "– not linked –",
    pp_user_hint: "A linked person is selected automatically when that user opens the card (e.g. on their own phone).",
    pp_linked: "🔗 {name}", pp_linked_anon: "🔗 linked",
    "sug.hard_hold": "Felt hard last time → same again", "sug.easy_target": "Felt easy → aim for {target} reps (up to {max})",
    "sug.easy_add_reps": "All sets felt easy → +{add} reps", "sug.easy_add_weight": "All sets felt easy → +{kg} kg",
  },
  de: {
    tab_training: "Training", tab_history: "Verlauf", tab_plans: "Einstellungen", loading: "Lade …",
    conn_failed: "Verbindung zur Integration fehlgeschlagen: {err}. Ist TrainingAssistant eingerichtet?",
    st_planned: "geplant", st_pending: "Rückfrage …", st_confirmed: "bestätigt", st_corrected: "korrigiert",
    st_edited: "geändert", st_unconfirmed: "unbestätigt", st_skipped: "übersprungen",
    ph_ready: "Bereit", ph_active: "Training", ph_interval: "HIIT", ph_finished: "Fertig", ph_paused: "Pausiert",
    ty_warmup: "Aufwärmen", ty_circuit: "Zirkel", ty_sets: "Sätze", ty_interval: "HIIT", ty_flow: "Flow", ty_cooldown: "Cool Down",
    u_reps: "Wdh.", u_sec: "Sek.", per_side: "pro Seite", per_side_short: "/Seite",
    hold_max_short: "max. halten", amrap_short: "max. Wdh.", reps_n: "{n} Wdh.", tile_hold: "Sek. halten", goal_range: "Ziel {lo}–{hi}",
    pos_round_of: "Runde {r}/{n}", pos_round: "Runde {r}", pos_set_of: "Satz {s}/{n}", pos_set: "Satz {s}",
    no_plan: "Noch kein Trainingsplan vorhanden.", import_plan: "Plan importieren", start: "▶ Training starten",
    program: "Programm", workout: "Workout", wo_pos: "Workout {p} von {n}", wo_after: " · danach {name}",
    wo_auto: " · nach dem Beenden geht es im Programm automatisch weiter.", voice_via: "Ansagen über {sat}",
    no_sat: "Kein Standard-Satellit: Das Training läuft stumm über diese Karte (Satellit in den Optionen der Integration wählbar oder beim Start per Sprache).",
    pv_rounds: "{n} Runden", pv_cap: "{m} min im Wechsel", pv_between_ex: "{d} zw. Übungen",
    pv_between_rounds: "{d} zw. Runden", pv_sets: "{n} Sätze", pv_sets_until: "Sätze bis {n} Wdh.", pv_rest: "{d} Pause",
    pv_interval: "{w} s Arbeit / {r} s Pause", pv_block_rest: "⏸ {d} Pause", pv_flow: "{n} Abschnitte · etwa {m} min",
    flow_switch: "Wechsel", b_end_flow: "Flow beenden",
    tempo: "Tempo {t}", iv_work: "ARBEIT", iv_rest: "PAUSE", t_rest: "Pause", t_left: "Zeit übrig",
    t_up: "Zeit um – Übung beenden", t_question: "Rückfrage läuft … (Weiter = wie geplant)",
    b_resume: "▶ Fortsetzen", b_go: "▶ Los", b_end_hiit: "HIIT beenden", b_set_done: "✓ Satz fertig",
    b_set_done_changed: "✓ Satz fertig (geändert)", b_next: "Weiter", step: "Schritt {i}/{n}", b_back: "↶ Zurück",
    b_pause: "❚❚ Pause", b_continue: "▶ Weiter", b_skip: "⤼ Überspringen", b_finish: "⚑ Beenden", c_finish: "Wirklich beenden?",
    b_discard: "✕ Verwerfen", c_discard: "Wirklich verwerfen?", coming_up: "Danach", logged: "Erfasst (antippen zum Korrigieren)",
    un_done: "Training fertig", un_label: "Als Nächstes",
    a_seconds: "Sekunden", a_reps: "Wdh.", a_reps_side: "Wdh./Seite", a_weight: "Gewicht", a_less: "{l} weniger", a_more: "{l} mehr",
    e_save: "Speichern", e_skipped: "Übersprungen", e_cancel: "Abbrechen",
    h_loading: "Lade Verlauf …", h_empty: "Noch keine Trainings gespeichert.", h_ex_meta: "{n}× · zuletzt {d}", h_sets: "{n} Sätze",
    h_unconfirmed: "{n} unbestätigt", h_aborted: "abgebrochen", c_delete: "Wirklich löschen?", h_delete: "Training löschen",
    h_th_ex: "Übung", h_th_hist: "Verlauf", h_last8: "(letzte 8)", h_th_last: "Zuletzt", h_th_next: "Nächstes Mal",
    h_tab_ex: "Übungen", h_tab_sess: "Trainings",
    tpl_loading: "Lade Vorlagen …", n_workout: "{n} Workout", n_workouts: "{n} Workouts",
    tpl_reload_c: "Neu laden? Eigene Änderungen gehen verloren.", tpl_installed: "✓ Übernommen · neu laden", tpl_take: "Übernehmen",
    p_active: "aktives Programm", p_noimg: "Ohne Bild: {list}", p_edit: "Bearbeiten", p_delete: "Löschen",
    p_next_badge: "als Nächstes", p_set_next: "Als Nächstes", p_start: "Starten",
    p_tpl_intro: "Bewährte Programme zum Übernehmen – danach unter „Meine Pläne“ startklar. Gewichte sind Startwerte, die Progression passt sie an.",
    p_import_intro: "Unten steht ein kommentierter Beispielplan – anpassen und importieren. Ein Plan mit gleichem Namen wird ersetzt, der Verlauf bleibt. Die Anleitung erklärt alles und enthält einen fertigen Prompt, mit dem ChatGPT oder Claude dir einen Plan schreibt.",
    p_dl_guide: "⤓ Anleitung (.txt)", p_dl_example: "⤓ Beispielplan (.yaml)", p_insert: "Beispiel einsetzen", p_clear: "Leeren",
    p_placeholder: "schema_version: 1\nname: Mein Plan\n…", p_import: "Importieren", p_none: "Noch keine Pläne.",
    p_pick_tpl: "Vorlage auswählen", p_own: "Eigenen Plan anlegen",
    p_tab_mine: "Meine Pläne", p_tab_tpl: "Vorlagen", p_tab_own: "Eigener Plan",
    m_imported: "„{name}“ importiert ({n} Workouts). Bilder: {m} von {t} Übungen", m_missing: " – ohne Bild: {list}",
    m_tpl: "Vorlage „{name}“ übernommen ({n} Workouts). Gewichte sind Startwerte – bitte anpassen.",
    m_example: "Beispielplan eingesetzt – anpassen und importieren.",
    m_loaded: "Plan geladen – ändern und erneut importieren (gleicher Name ersetzt ihn).",
    c_first: "Erstes Training mit dieser Übung", c_last: "zuletzt {v} {u}", c_last_best: "zuletzt {v} · bestes {b} {u}",
    c_n: "{n} Trainings", c_1: "1 Training", c_aria: "Verlauf {l}",
    guide_file: "anleitung-eigene-plaene.txt", example_file: "beispiel-plan.yaml",
    guide_dl: "TrainingAssistant-Anleitung-eigene-Plaene.txt", example_dl: "TrainingAssistant-Beispielplan.yaml",
    "sug.no_progression_timed": "Ohne Progression (Zeit oder max.)", "sug.plan_values": "Planwerte (noch kein Verlauf)",
    "sug.harder_variant": "Alle Sätze mit {reps} Wdh. geschafft – schwerere Variante oder Zusatzgewicht",
    "sug.all_reps_add_weight": "Alle Sätze mit {reps} Wdh. geschafft → +{kg} kg",
    "sug.hold_weight_target": "Gewicht halten, Ziel {target} Wdh. (bis {max})",
    "sug.target_reps": "Ziel {target} Wdh. (bis {max})",
    "sug.cap_reached": "Obergrenze von {cap} Wdh. erreicht – schwerere Variante oder Zusatzgewicht",
    "sug.all_reps_add_reps": "Alle Sätze mit {reps} Wdh. geschafft → +{add} Wdh.",
    "sug.repeat_target": "Ziel {target} Wdh. noch nicht in allen Sätzen geschafft – nochmal",
    "sug.all_done": "Alle Sätze geschafft", "sug.all_done_add_weight": "Alle Sätze geschafft → +{kg} kg",
    "sug.not_all_hold": "Nicht alle Sätze geschafft → Gewicht halten", "sug.fixed": "Feste Vorgabe aus dem Plan (ohne Progression)",
    "tg.kraft": "Kraft & Hypertrophie",
    "tg.kraft.about": "Langhantel, Kurzhanteln, Geräte – Muskelaufbau und Maximalkraft im Studio oder Homegym.",
    "tg.bodyweight": "Bodyweight – ohne Geräte",
    "tg.bodyweight.about": "Zu Hause, im Hotel, unterwegs – Zirkel und Kraft mit Stuhl und Sofa.",
    "tg.calisthenics": "Calisthenics",
    "tg.calisthenics.about": "Klimmzugstange und Barren – Fortschritt über immer schwerere Varianten bis zu Skills.",
    "tg.kettlebell": "Kettlebell",
    "tg.kettlebell.about": "Eine oder zwei Kugeln – Kraft, Kraftausdauer und Kondition in kurzer Zeit.",
    "tg.hiit": "HIIT & Tabata",
    "tg.hiit.about": "Kurze, harte Intervalle – zeitgesteuert, mit Signaltönen oder Ansagen. Körpergewicht, Kettlebell, Rad, Rudergerät oder Laufen.",
    "tg.yoga": "Yoga & Mobilität",
    "tg.yoga.about": "Flows, Dehnen und Gleichgewicht – läuft von selbst, jede Haltung wird angesagt. Eine Matte genügt.",
    "tg.other": "Weitere",
    wk_title: "Diese Woche", wk_goal: "Ziel (Anzahl der Workouts)", wk_aria: "{d} von {n} Trainings diese Woche", wk_streak: "🔥 {n} Wochen am Stück",
    wk_streak1: "🔥 1 Woche", wk_bars: "Sätze pro Tag", wk_left: "noch {n}", wk_reached: "Wochenziel erreicht",
    wk_total: "{n} Trainings insgesamt", wk_goal_less: "Wochenziel senken", wk_goal_more: "Wochenziel erhöhen",
    "mg.chest": "Brust", "mg.back": "Rücken", "mg.shoulders": "Schultern", "mg.biceps": "Bizeps", "mg.triceps": "Trizeps",
    "mg.core": "Bauch", "mg.quads": "Oberschenkel vorn", "mg.hamstrings": "Oberschenkel hinten", "mg.glutes": "Po", "mg.calves": "Waden",
    h_tab_over: "Übersicht", tile_week: "Diese Woche", tile_streak: "Serie", tile_weeks: "{n} Wochen", tile_week1: "1 Woche",
    tile_total: "Trainings gesamt", tile_since: "seit {d}", tile_time: "Zeit diese Woche", tile_time_avg: "Ø {m} min/Woche",
    rec_title: "Letzte Rekorde", rec_none: "Noch keine Rekorde – sie kommen ab dem zweiten Training mit einer Übung.",
    rec_weight: "{v} kg", rec_e1rm: "geschätztes Max. {v} kg", rec_reps: "{v} Wdh.", rec_duration: "{v} s", rec_prev: "vorher {v}",
    vol_title: "Sätze pro Muskelgruppe diese Woche", vol_hint: "Richtwert: etwa 10 harte Sätze pro Muskel und Woche (Linie).",
    vol_last: "Vorwoche {n}", vol_none: "Diese Woche noch keine Sätze.",
    vol_unassigned: "Ohne Muskelgruppe: {n} Sätze ({list}) – im Plan bei der Übung muscles: […] ergänzen.",
    rc_title: "Erholung", rc_fresh: "Gerade trainiert", rc_recovering: "Erholt sich", rc_ready: "Bereit", rc_soon: "Bald wieder", rc_overdue: "Überfällig",
    rc_none: "Noch nicht trainiert", rc_h: "zuletzt vor {n} h", rc_d: "zuletzt vor {n} Tagen", rc_since_h: "seit {n} h",
    rc_since_d: "seit {n} Tagen",
    mt_primary: "Hauptmuskel", mt_secondary: "Arbeitet mit",
    ef_last: "Wie war's?", ef_easy: "Leicht", ef_normal: "Normal", ef_hard: "Schwer",
    st_wait: "Warte auf Los", st_go: "Los!", el_title: "Trainingszeit", el_last: "letztes Mal {d}",
    t_record: "🏆 Neuer Rekord: {name}", rest_less: "−15 s", rest_more: "+15 s",
    who: "Wer trainiert?", p_tab_people: "Personen",
    pp_intro: "Jede Person hat eigenen Verlauf, eigene Vorschläge, ein eigenes Wochenziel und eine eigene Programm-Position. Pläne sind gemeinsam.",
    pp_active: "ausgewählt", pp_select: "Auswählen", pp_rename: "Umbenennen", pp_delete: "Löschen", pp_c_delete: "Mit Verlauf löschen?",
    pp_add: "+ Person hinzufügen", pp_name: "Name", pp_save: "Speichern", pp_busy: "Eine andere Person auswählen geht nach dem Training.",
    pp_goal: "Wochenziel: {n} Trainings",
    pp_user: "Home-Assistant-Benutzer", pp_user_none: "– nicht verknüpft –",
    pp_user_hint: "Eine verknüpfte Person wird automatisch ausgewählt, wenn dieser Benutzer die Karte öffnet (z. B. auf dem eigenen Handy).",
    pp_linked: "🔗 {name}", pp_linked_anon: "🔗 verknüpft",
    "sug.hard_hold": "Zuletzt schwer → gleiche Vorgabe nochmal", "sug.easy_target": "Leicht → Ziel {target} Wdh. (bis {max})",
    "sug.easy_add_reps": "Alle Sätze leicht → +{add} Wdh.", "sug.easy_add_weight": "Alle Sätze leicht → +{kg} kg",
  },
};
let LANG = "en";
let LOCALE = undefined;
const setLanguage = (hass) => {
  const lang = (hass.locale && hass.locale.language) || hass.language || "en";
  LOCALE = lang;
  const base = lang.split(/[-_]/)[0].toLowerCase();
  LANG = I18N[base] ? base : "en";
};
const t = (key, p = {}) =>
  String(I18N[LANG][key] ?? I18N.en[key] ?? key).replace(/\{(\w+)\}/g, (_, n) => (p[n] ?? ""));
// Vorschlag (Progression) in der Kartensprache; ältere Daten ohne Schlüssel: Text der Integration
const sugText = (o) => (o && o.key ? t(`sug.${o.key}`, o.params || {}) : (o && o.text) || "");
const stepSug = (s) => sugText({ key: s.suggestion_key, params: s.suggestion_params, text: s.suggestion });
const reasonSug = (s) => sugText({ key: s.reason_key, params: s.reason_params, text: s.reason });

const EFFORT_PROMPT_MS = 5000; // so lange bleibt „Wie war's?“ nach einem Satz
const STATUS = { planned: "neutral", pending: "info", confirmed: "ok", corrected: "ok", edited: "ok", unconfirmed: "warn", skipped: "muted" };
const typeLabel = (type) => (type ? t(`ty_${type}`) : "");
// „Zirkel“ + „Zirkel A“ → nur „Zirkel A“; „Zirkel“ + „Hauptteil“ → „Zirkel · Hauptteil“
const blockTitle = (type, name) => {
  const label = typeLabel(type);
  if (!name || name === label) return label;
  return name.toLowerCase().startsWith(label.toLowerCase()) ? name : `${label} · ${name}`;
};
// Übungsbild (lokal von Home Assistant). Ohne Bild: leerer Platzhalter, damit alles bündig bleibt.
const IMG_BASE = "/training_assistant/images";
const GUIDE_BASE = "/training_assistant/guide";
const img = (cid, cls = "thumb", n = 0) =>
  cid ? `<img class="${cls}" src="${IMG_BASE}/${encodeURIComponent(cid)}/${n}.jpg" alt="" loading="lazy">`
      : `<span class="${cls} noimg"></span>`;
const dur = (s) => (s >= 60 ? (s % 60 ? `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")} min` : `${s / 60} min`) : `${s} s`);

const esc = (v) =>
  String(v ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const num = (v) => (v === null || v === undefined ? "" : String(Math.round(v * 100) / 100).replace(".", LANG === "de" ? "," : "."));
const kg = (v) => (v === null || v === undefined ? "" : `${num(v)} kg`);
const mmss = (s) => {
  s = Math.max(0, Math.round(s));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
};
// Laufende Dauer: 23:41 bzw. 1:05:12
const hms = (s) => {
  s = Math.max(0, Math.floor(s));
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = String(s % 60).padStart(2, "0");
  return h ? `${h}:${String(m).padStart(2, "0")}:${sec}` : `${m}:${sec}`;
};
const time = (iso) => (iso ? new Date(iso).toLocaleTimeString(LOCALE, { hour: "2-digit", minute: "2-digit" }) : "");
const sessionDuration = (s) => {
  if (!s.started_at || !s.finished_at) return "";
  const min = Math.round((new Date(s.finished_at) - new Date(s.started_at)) / 60000);
  if (min < 1) return "< 1 min";
  return min >= 60 ? `${Math.floor(min / 60)} h ${String(min % 60).padStart(2, "0")} min` : `${min} min`;
};
const date = (iso) =>
  iso ? new Date(iso).toLocaleDateString(LOCALE, { weekday: "short", day: "2-digit", month: "2-digit", year: "2-digit" }) : "";

function targetText(s) {
  let out;
  if (s.hold_max) out = t("hold_max_short");
  else if (s.duration_range) out = `${s.duration_range[0]}–${s.duration_range[1]} s`;
  else if (s.target_duration) out = `${s.target_duration} s`;
  else if (s.amrap) out = t("amrap_short");
  else if (s.target_reps) out = t("reps_n", { n: s.target_reps });
  else out = "";
  if (s.rep_range && s.rep_range[0] !== s.rep_range[1]) out += ` (${s.rep_range[0]}–${s.rep_range[1]})`;
  if (s.per_side) out += ` ${t("per_side")}`;
  if (s.target_weight !== null && s.target_weight !== undefined) out += ` · ${kg(s.target_weight)}`;
  return out;
}

/* Zielwerte als große Zahlen-Kacheln: „10 Wdh. × 12 kg“ */
function targetTiles(s) {
  const tile = (value, unit, hint = "") =>
    `<div class="tg-v"><b>${esc(value)}</b><span>${esc(unit)}</span>${hint ? `<em>${esc(hint)}</em>` : ""}</div>`;
  const parts = [];
  const side = s.per_side ? t("per_side") : "";
  if (s.hold_max) parts.push(tile("max", t("tile_hold")));
  else if (s.duration_range) parts.push(tile(`${s.duration_range[0]}–${s.duration_range[1]}`, t("u_sec"), side));
  else if (s.target_duration) parts.push(tile(s.target_duration, t("u_sec"), side));
  else if (s.amrap) parts.push(tile("max", t("u_reps"), side));
  else if (s.target_reps) {
    const range = s.rep_range && s.rep_range[0] !== s.rep_range[1] ? t("goal_range", { lo: s.rep_range[0], hi: s.rep_range[1] }) : "";
    parts.push(tile(s.target_reps, t("u_reps"), [range, side].filter(Boolean).join(" · ")));
  }
  if (s.target_weight !== null && s.target_weight !== undefined) {
    if (parts.length) parts.push(`<div class="tg-x">×</div>`);
    parts.push(tile(num(s.target_weight), "kg"));
  }
  return `<div class="tg">${parts.join("")}</div>`;
}

function position(s) {
  if (s.round) return s.rounds ? t("pos_round_of", { r: s.round, n: s.rounds }) : t("pos_round", { r: s.round });
  if (s.set_no) return s.sets ? t("pos_set_of", { s: s.set_no, n: s.sets }) : t("pos_set", { s: s.set_no });
  return "";
}

function setValue(x) {
  if (x.status === "skipped") return "–";
  const parts = [];
  if (x.reps !== null && x.reps !== undefined) parts.push(`${x.reps}${x.per_side ? t("per_side_short") : ""}`);
  if (x.duration_s !== null && x.duration_s !== undefined) parts.push(`${x.duration_s} s`);
  if (x.weight_kg !== null && x.weight_kg !== undefined) parts.push(kg(x.weight_kg));
  return parts.join(" × ") || "?";
}

class TrainingAssistantCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._tab = "training";
    this._histTab = "overview";
    this._stats = null;
    this._ppEdit = null;
    this._editing = null;
    this._importText = "";
    this._importMsg = null;
    this._history = null;
    this._preview = null;
    this._previewKey = null;
    this._openSessions = new Set();
    this._error = null;
    this.shadowRoot.addEventListener("click", (e) => this._onClick(e));
    this.shadowRoot.addEventListener("error", (e) => {
      if (e.target && e.target.tagName === "IMG") e.target.classList.add("broken");
    }, true);
    this.shadowRoot.addEventListener("input", (e) => this._onInput(e));
    this.shadowRoot.addEventListener("change", (e) => this._onChange(e));
    this.shadowRoot.addEventListener("focusout", () => setTimeout(() => this._dirty && this._render(), 50));
  }

  setConfig(config) {
    this._config = config || {};
    if (this._config.tab) this._tab = this._config.tab;
  }

  static getStubConfig() {
    return {};
  }

  getCardSize() {
    return 10;
  }

  set hass(hass) {
    const first = !this._hass;
    const lang = LANG;
    this._hass = hass;
    setLanguage(hass);
    if (!first && lang !== LANG) {
      // Unveränderten Beispielplan im Importfeld in der neuen Sprache neu laden
      if (this._starter && this._importText === this._starter) {
        this._importText = "";
        this._starterUsed = false;
      }
      this._starter = undefined;
      this._starterLoading = false;
      this._templates = null; // Gruppentexte kommen aus der Karte, Liste trotzdem frisch laden
      this._render();
    }
    if (first) {
      this._subscribe();
      this._render();
    }
  }

  connectedCallback() {
    if (this._hass && !this._unsubPromise) this._subscribe();
    this._timer = setInterval(() => this._tickTimers(), 1000);
  }

  disconnectedCallback() {
    clearInterval(this._timer);
    if (this._unsubPromise) {
      this._unsubPromise.then((unsub) => unsub()).catch(() => {});
      this._unsubPromise = null;
    }
  }

  _subscribe() {
    if (!this._hass || this._unsubPromise) return;
    this._unsubPromise = this._hass.connection.subscribeMessage(
      (state) => {
        const prev = this._state;
        const profileChanged = prev && prev.profile !== state.profile;
        const lastChanged = (prev && prev.last_session_id !== state.last_session_id) || profileChanged;
        if (!prev || lastChanged || prev.weekly_goal !== state.weekly_goal) this._stats = null;
        if (profileChanged) {
          this._history = null;
          this._previewKey = null;
        }
        this._state = state;
      this._watchLogged(prev, state);
        this._error = null;
        this._autoSelectProfile(state);
        if (this._tab === "history" && (lastChanged || !this._history)) this._loadHistory();
        if (!state.active) this._loadPreview();
        this._render();
      },
      { type: `${DOMAIN}/subscribe` }
    );
    this._unsubPromise.catch((err) => {
      this._error = t("conn_failed", { err: err.message || err.code || err });
      this._unsubPromise = null;
      this._render();
    });
  }

  async _ws(msg) {
    try {
      return await this._hass.callWS({ ...msg, type: `${DOMAIN}/${msg.type}` });
    } catch (err) {
      this._toast(err.message || String(err));
      throw err;
    }
  }

  async _service(name, data = {}) {
    try {
      await this._hass.callService(DOMAIN, name, data);
    } catch (err) {
      this._toast(err.message || String(err));
    }
  }

  _toast(message) {
    this.dispatchEvent(new CustomEvent("hass-notification", { detail: { message }, bubbles: true, composed: true }));
  }

  async _loadHistory() {
    try {
      this._history = await this._ws({ type: "history", limit: 50 });
    } catch (_) {
      this._history = { sessions: [], exercises: [] };
    }
    this._render();
  }

  async _loadPreview() {
    const nxt = this._state && this._state.next;
    const key = nxt ? `${nxt.plan_id}/${nxt.workout_id}/${this._state.last_session_id}` : null;
    if (!nxt || key === this._previewKey) return;
    this._previewKey = key;
    try {
      const res = await this._ws({ type: "preview", plan_id: nxt.plan_id, workout_id: nxt.workout_id });
      this._preview = res.steps;
    } catch (_) {
      this._preview = null;
    }
    this._render();
  }

  // ------------------------------------------------------------------ Events

  async _onClick(e) {
    const el = e.target.closest("[data-a]");
    if (!el) return;
    const a = el.dataset.a;
    const d = el.dataset;
    // Gefährliche Aktionen: erst antippen = „Wirklich …?“, nochmal antippen = ausführen.
    // (Browser-Dialoge wie confirm() werden in Apps/Kiosk-Browsern oft still unterdrückt.)
    if (d.confirm && !this._confirmed(d.ck)) return;
    if (a === "tab") {
      this._tab = d.tab;
      this._editing = null;
      if (this._tab === "history") this._loadHistory();
      this._render();
    } else if (a === "adj") {
      // Werte liegen in der Integration – dieselben wie bei Drehregler/Tasten-Entitäten
      await this._service("adjust", { field: d.k === "weight" ? "weight" : "reps", steps: Number(d.d) });
    } else if (a === "next") {
      await this._service("next");
    } else if (a === "svc") {
      await this._service(d.svc, d.keep ? { keep: d.keep === "1" } : {});
    } else if (a === "start") {
      await this._service("start", d.plan ? { plan_id: d.plan, workout_id: d.workout } : {});
      this._tab = "training";
      this._render();
    } else if (a === "next-workout") {
      await this._ws({ type: "set_next", plan_id: d.plan, workout_id: d.workout });
      this._tab = "training";
      this._render();
    } else if (a === "edit") {
      const set = this._findSet(d.session || null, Number(d.set));
      if (!set) return;
      this._editing = {
        session_id: d.session || null,
        set_id: set.id,
        reps: set.reps ?? set.target_reps ?? "",
        weight_kg: set.weight_kg ?? set.target_weight ?? "",
        duration_s: set.duration_s ?? set.target_duration ?? "",
        timed: !!(set.target_duration || set.hold_max),
        weighted: set.weight_kg !== null || set.target_weight !== null,
        effort: set.effort || "normal",
      };
      this._render();
    } else if (a === "edit-cancel") {
      this._editing = null;
      this._render();
    } else if (a === "edit-save" || a === "edit-skip") {
      const ed = this._editing;
      const msg = { type: "edit_set", set_id: ed.set_id };
      if (ed.session_id) msg.session_id = ed.session_id;
      if (a === "edit-skip") msg.skipped = true;
      else {
        const toNum = (v, f) => (v === "" || v === null ? null : f(String(v).replace(",", ".")));
        if (ed.timed) msg.duration_s = toNum(ed.duration_s, parseInt);
        else msg.reps = toNum(ed.reps, parseInt);
        if (ed.weighted || ed.weight_kg !== "") msg.weight_kg = toNum(ed.weight_kg, parseFloat);
        msg.effort = ed.effort || "normal";
      }
      try {
        await this._ws(msg);
        this._editing = null;
        if (ed.session_id) await this._loadHistory();
        this._render();
      } catch (_) {
        /* Toast kam schon */
      }
    } else if (a === "ptab") {
      this._planTab = d.tab;
      this._importMsg = null;
      this._render();
    } else if (a === "htab") {
      this._histTab = d.tab;
      this._render();
    } else if (a === "toggle-session") {
      this._openSessions.has(d.session) ? this._openSessions.delete(d.session) : this._openSessions.add(d.session);
      this._render();
    } else if (a === "delete-session") {
      await this._ws({ type: "delete_session", session_id: d.session });
      await this._loadHistory();
    } else if (a === "import") {
      try {
        const res = await this._ws({ type: "import_plan", text: this._importText, lang: LANG });
        const im = res.images || { matched: 0, total: 0, missing: [] };
        this._planTab = "mine";
        this._importMsg = {
          ok: true,
          text: t("m_imported", { name: res.name, n: res.workouts.length, m: im.matched, t: im.total }) +
            (im.missing.length ? t("m_missing", { list: im.missing.join(", ") }) : "") + ".",
        };
        this._importText = "";
        this._previewKey = null;
      } catch (err) {
        this._importMsg = { ok: false, text: err.message || String(err) };
      }
      this._render();
    } else if (a === "tpl-import") {
      try {
        const res = await this._ws({ type: "import_template", template_id: d.tpl });
        this._importMsg = { ok: true, text: t("m_tpl", { name: res.name, n: res.workouts.length }) };
        this._templates = null;
        this._previewKey = null;
      } catch (err) {
        this._importMsg = { ok: false, text: err.message || String(err) };
      }
      this._render();
    } else if (a === "starter") {
      await this._loadStarter(true);
      this._importMsg = { ok: true, text: t("m_example") };
      this._render();
    } else if (a === "clear-import") {
      this._importText = "";
      this._starterUsed = true;
      this._importMsg = null;
      this._render();
    } else if (a === "plan-edit") {
      const res = await this._ws({ type: "plan_source", plan_id: d.plan });
      this._importText = res.text;
      this._starterUsed = true;
      this._planTab = "import";
      this._importMsg = { ok: true, text: t("m_loaded") };
      this._render();
    } else if (a === "plan-delete") {
      await this._ws({ type: "delete_plan", plan_id: d.plan });
    } else if (a === "goal") {
      await this._ws({ type: "set_weekly_goal", goal: Math.max(1, (this._state.weekly_goal || 3) + Number(d.d)) });
    } else if (a === "rest") {
      await this._service("rest_adjust", { seconds: Number(d.d) });
    } else if (a === "effort") {
      const msg = { type: "edit_set", set_id: Number(d.set), effort: d.v };
      if (d.session) msg.session_id = d.session;
      await this._ws(msg).catch(() => {});
      if (this._prompt && this._prompt.setId === Number(d.set)) this._closePrompt();
    } else if (a === "ed-effort") {
      this._editing.effort = d.v;
      this._render();
    } else if (a === "pp-select") {
      await this._ws({ type: "profile", action: "select", profile: d.p }).catch(() => {});
    } else if (a === "pp-delete") {
      await this._ws({ type: "profile", action: "delete", profile: d.p }).catch(() => {});
    } else if (a === "pp-rename" || a === "pp-add") {
      const prof = (this._state.profiles || []).find((x) => x.id === d.p);
      this._ppEdit = { id: prof ? prof.id : null, name: prof ? prof.name : "" };
      this._render();
      const inp = this.shadowRoot.querySelector('[data-field="pp-name"]');
      if (inp) inp.focus();
    } else if (a === "pp-cancel") {
      this._ppEdit = null;
      this._render();
    } else if (a === "pp-save") {
      const ed = this._ppEdit;
      try {
        await this._ws(ed.id ? { type: "profile", action: "rename", profile: ed.id, name: ed.name }
                             : { type: "profile", action: "add", name: ed.name });
        this._ppEdit = null;
        this._render();
      } catch (_) {
        /* Toast kam schon */
      }
    }
  }

  _confirmed(key) {
    if (this._armed && this._armed.key === key && Date.now() < this._armed.until) {
      this._armed = null;
      clearTimeout(this._armTimer);
      return true;
    }
    // Nur den Knopf umbeschriften, nicht alles neu zeichnen – sonst springen Handy-Browser nach oben
    this._disarm();
    this._armed = { key, until: Date.now() + 4000 };
    clearTimeout(this._armTimer);
    this._armTimer = setTimeout(() => this._disarm(), 4000);
    this._applyArmed();
    return false;
  }

  _armedButton() {
    return this._armed ? this.shadowRoot.querySelector(`[data-ck="${CSS.escape(this._armed.key)}"]`) : null;
  }

  _applyArmed() {
    const btn = this._armedButton();
    if (!btn) return;
    if (btn.dataset.label === undefined) btn.dataset.label = btn.innerHTML;
    btn.classList.add("armed");
    btn.textContent = btn.dataset.confirm;
  }

  _disarm() {
    const btn = this._armedButton();
    this._armed = null;
    if (btn && btn.dataset.label !== undefined) {
      btn.innerHTML = btn.dataset.label;
      delete btn.dataset.label;
      btn.classList.remove("armed");
    }
  }

  _onInput(e) {
    const el = e.target;
    if (el.dataset.field === "import") {
      this._importText = el.value;
      // Während getippt wird, zeichnet die Karte nicht neu – Taste direkt freischalten
      const btn = this.shadowRoot.querySelector('[data-a="import"]');
      if (btn) btn.disabled = !el.value.trim();
    } else if (el.dataset.field === "pp-name" && this._ppEdit) {
      this._ppEdit.name = el.value;
    } else if (el.dataset.field && this._editing) this._editing[el.dataset.field] = el.value;
  }

  async _onChange(e) {
    const el = e.target;
    if (el.dataset.field === "pp-link") {
      await this._ws({ type: "link_profile", profile: el.dataset.p, user_id: el.value || null }).catch(() => {});
      el.blur();
      return;
    }
    if (el.dataset.field === "program-select" && el.value) {
      this._preview = null;
      await this._ws({ type: "set_program", plan_id: el.value });
      el.blur();
    } else if (el.dataset.field === "workout-select" && el.value && this._state.next) {
      this._preview = null;
      await this._ws({ type: "set_next", plan_id: this._state.next.plan_id, workout_id: el.value });
      el.blur();
    }
  }

  _findSet(sessionId, setId) {
    if (!sessionId) return (this._state.active?.sets || []).find((x) => x.id === setId);
    const sess = (this._history?.sessions || []).find((s) => s.id === sessionId);
    return sess && sess.sets.find((x) => x.id === setId);
  }

  // ----------------------------------------------------------------- Timers

  _tickTimers() {
    const now = Date.now();
    this.shadowRoot.querySelectorAll("[data-until]").forEach((el) => {
      const left = (new Date(el.dataset.until).getTime() - now) / 1000;
      el.textContent = mmss(left);
    });
    this.shadowRoot.querySelectorAll("[data-since]").forEach((el) => {
      el.textContent = hms((now - new Date(el.dataset.since).getTime()) / 1000);
    });
    // Balken: laufende Zeit im Verhältnis zur Dauer des letzten gleichen Workouts (darüber = gelb)
    this.shadowRoot.querySelectorAll("[data-since-of]").forEach((el) => {
      const ratio = (now - new Date(el.dataset.sinceOf).getTime()) / 1000 / Number(el.dataset.ref);
      el.style.width = `${Math.min(100, Math.max(0, ratio * 100))}%`;
      el.classList.toggle("over", ratio > 1);
      const box = el.closest(".elapsed"); // auf dem Handy ohne Balken: „letztes Mal“ wird gelb
      if (box) box.classList.toggle("over", ratio > 1);
    });
  }

  // ----------------------------------------------------------------- Render

  _render() {
    const focused = this.shadowRoot.activeElement;
    // Nicht neu zeichnen, während in ein Textfeld getippt wird (Auswahlfelder sind davon ausgenommen,
    // sonst bliebe z. B. die Workout-Vorschau nach einer Auswahl veraltet)
    if (focused && ["INPUT", "TEXTAREA"].includes(focused.tagName) && this._rendered) {
      this._dirty = true;
      return;
    }
    this._dirty = false;
    this._rendered = true;
    const scrollY0 = window.scrollY;
    let body;
    if (this._error) body = `<div class="msg err">${esc(this._error)}</div>`;
    else if (!this._state) body = `<div class="muted pad">${t("loading")}</div>`;
    else if (this._tab === "history") body = this._renderHistory();
    else if (this._tab === "plans") body = this._renderPlans();
    else body = this._state.active ? this._renderActive(this._state.active) : this._renderIdle();

    const tab = (id, label) =>
      `<button class="tab ${this._tab === id ? "on" : ""}" data-a="tab" data-tab="${id}">${label}</button>`;
    this.shadowRoot.innerHTML = `
      <style>${STYLE}</style>
      <ha-card>
        <div class="tabs">${tab("training", t("tab_training"))}${tab("history", t("tab_history"))}${tab("plans", t("tab_plans"))}</div>
        <div class="body">${body}</div>${this._renderEffortPrompt()}
      </ha-card>`;
    if (this._armed) this._applyArmed();
    // Scrollposition halten (Handy-Browser springen sonst nach oben, wenn der angetippte Knopf ersetzt wird)
    if (window.scrollY !== scrollY0) window.scrollTo(0, scrollY0);
    this._tickTimers();
  }

  _renderIdle() {
    const st = this._state;
    if (!st.plans.length)
      return `<div class="pad"><p>${t("no_plan")}</p>
        <button class="btn primary" data-a="tab" data-tab="plans">${t("import_plan")}</button></div>`;
    // Programm (in dem man sich bewegt) + Workout darin (vorgewählt = nächstes in der Reihe)
    const progOpts = st.plans
      .map((p) => `<option value="${esc(p.id)}" ${p.id === st.program ? "selected" : ""}>${esc(p.name)}</option>`)
      .join("");
    const pw = st.program_workouts || [];
    const cur = pw.find((w) => st.next && w.workout_id === st.next.workout_id);
    const after = cur ? pw[cur.position % pw.length] : null;
    const woOpts = pw
      .map((w) => `<option value="${esc(w.workout_id)}" ${cur && w.workout_id === cur.workout_id ? "selected" : ""}>${esc(w.name)} (${w.position}/${w.count})</option>`)
      .join("");
    this._ensureStats();
    const people = (st.profiles || []).length > 1
      ? `<div class="who"><span class="lbl">${t("who")}</span>${st.profiles
          .map((p) => `<button class="chip-btn ${p.id === st.profile ? "on" : ""}" data-a="pp-select" data-p="${esc(p.id)}">${esc(p.name)}</button>`)
          .join("")}</div>`
      : "";
    return `
      <div class="pad live">
        ${people}
        <div class="startrow">
          <button class="btn primary" data-a="start">${t("start")}</button>
          <label class="sel"><span class="lbl">${t("program")}</span><select data-field="program-select">${progOpts}</select></label>
          <label class="sel"><span class="lbl">${t("workout")}</span><select data-field="workout-select">${woOpts}</select></label>
        </div>
        ${cur ? `<div class="muted small">${t("wo_pos", { p: cur.position, n: cur.count })}${pw.length > 1 && after ? esc(t("wo_after", { name: after.name })) : ""}${t("wo_auto")}</div>` : ""}
        ${this._stats ? weekCard(this._stats) : ""}
        ${this._renderPreview()}
        ${st.default_satellite ? `<div class="muted small">${esc(t("voice_via", { sat: st.default_satellite }))}</div>` : `<div class="muted small">${t("no_sat")}</div>`}
      </div>`;
  }

  _renderPreview() {
    if (!this._preview) return "";
    const blocks = [];
    for (const s of this._preview) {
      let b = blocks[blocks.length - 1];
      if (!b || b.block !== s.block) {
        b = { block: s.block, name: s.block_name, type: s.block_type, items: [], step: s };
        blocks.push(b);
      }
      if (s.type === "set" && (s.round || 1) === 1 && (s.set_no || 1) === 1) b.items.push(s);
    }
    const parts = [];
    blocks.forEach((b, bi) => {
      const s = b.step;
      const meta = [];
      if (b.type === "circuit") {
        meta.push(s.rounds ? t("pv_rounds", { n: s.rounds }) : t("pv_cap", { m: num((s.block_end?.time_cap_s || 0) / 60) }));
        const first = b.items[0], last = b.items[b.items.length - 1];
        if (b.items.length > 1 && first.rest_after_s) meta.push(t("pv_between_ex", { d: dur(first.rest_after_s) }));
        if (s.rounds !== 1 && last && last.rest_after_s) meta.push(t("pv_between_rounds", { d: dur(last.rest_after_s) }));
      } else if (b.type === "sets") {
        meta.push(s.sets ? t("pv_sets", { n: s.sets }) : t("pv_sets_until", { n: s.block_end?.total_reps }));
        if (s.rest_after_s) meta.push(t("pv_rest", { d: dur(s.rest_after_s) }));
      } else if (b.type === "flow") {
        if (s.rounds > 1) meta.push(t("pv_rounds", { n: s.rounds }));
        meta.push(t("pv_flow", { n: (s.segments || []).length, m: Math.max(1, Math.round((s.total_s || 0) / 60)) }));
      } else if (b.type === "interval") {
        meta.push(t("pv_rounds", { n: s.rounds }), t("pv_interval", { w: s.work_s, r: s.rest_s }));
      } else if (s.duration_s) {
        meta.push(dur(s.duration_s));
      }
      let body = "";
      if (b.type === "flow") {
        body = `<ul>${(s.items || [])
          .map((i) => `<li><span class="exn">${img(this._imageFor(i.exercise, s))}<span>${esc(i.name)}</span></span>
            <span class="tgt">${esc(dur(i.duration_s))}${i.per_side ? ` ${esc(t("per_side"))}` : ""}</span></li>`)
          .join("")}</ul>`;
      } else if (b.type === "interval") {
        body = `<ul><li><span>${esc(s.exercise_names.join(" · "))}</span></li></ul>`;
      } else if (b.items.length) {
        body = `<ul>${b.items
          .map(
            (i) => `<li><span class="exn">${img(i.image)}<span>${esc(i.exercise_name)}</span></span><span class="tgt">${esc(targetText(i))}</span>
              ${i.suggestion && i.suggestion_key !== "plan_values" && i.suggestion !== "Planwerte (noch kein Verlauf)" ? `<div class="sug">${esc(stepSug(i))}</div>` : ""}</li>`
          )
          .join("")}</ul>`;
      }
      const note = s.block_note || ((b.type === "warmup" || b.type === "cooldown") ? s.note : null);
      parts.push(`<div class="pblock t-${esc(b.type)}">
          <div class="phead"><span class="ptype">${esc(blockTitle(b.type, b.name))}</span></div>
          ${meta.length ? `<div class="pmeta">${esc(meta.join(" · "))}</div>` : ""}
          ${note ? `<div class="pnote">${esc(note)}</div>` : ""}
          ${body}</div>`);
      const pause = s.block_rest_s;
      if (pause && bi < blocks.length - 1) parts.push(`<div class="pbreak">${esc(t("pv_block_rest", { d: dur(pause) }))}</div>`);
    });
    return `<div class="preview">${parts.join("")}</div>`;
  }

  _renderActive(a) {
    const step = a.steps[a.idx] || {};
    const total = a.steps.length;
    const pct = Math.round((100 * a.idx) / Math.max(1, total));
    const iv = a.interval;
    const phase = a.paused ? t("ph_paused")
      : a.phase === "interval" && step.block_type === "flow" ? t("ty_flow") : t(`ph_${a.phase}`);
    let main;
    if (step.type === "set") {
      main = `<div class="ex">${esc(step.exercise_name)}</div>
        ${this._muscleTags(step.muscles, step.muscles_secondary)}
        ${targetTiles(step)}
        ${step.tempo ? `<div class="chip">${esc(t("tempo", { t: step.tempo }))}</div>` : ""}
        ${step.suggestion ? `<div class="sug">${esc(stepSug(step))}</div>` : ""}`;
    } else if (step.type === "interval" && step.block_type === "flow") {
      // Flow: aktuelle Haltung groß, Countdown, beim Wechsel die nächste Haltung
      main = `<div class="ex">${esc(iv ? iv.exercise || "" : [...new Set(step.exercise_names)].join(" · "))}</div>
        ${iv ? "" : `<div class="tgt big">${esc(t("pv_flow", { n: (step.segments || []).length, m: Math.max(1, Math.round((step.total_s || 0) / 60)) }))}</div>`}`;
    } else if (step.type === "interval") {
      main = `<div class="ex">${esc(iv ? iv.exercise || "" : step.exercise_names.join(" / "))}</div>
        ${iv ? "" : `<div class="tgt big">${step.rounds}× ${step.work_s} s / ${step.rest_s} s</div>`}`;
    } else {
      // Aufwärmen / Cool Down: nur ein großer Titel, kein zusätzliches Etikett
      main = `<div class="ex">${esc(blockTitle(step.block_type, step.block_name))}</div>${step.duration_s ? `<div class="muted">${mmss(step.duration_s)} min</div>` : ""}`;
    }
    const showLabel = step.type === "set" || step.type === "interval";
    const note = step.block_note && a.phase === "ready" ? step.block_note : step.note;
    const lastSet = a.sets.length ? a.sets[a.sets.length - 1] : null;
    // Bild: Übung des Schritts, bei HIIT/Flow die gerade laufende (bzw. nächste) Übung
    const curImg = step.image || (iv && iv.image) || null;
    // Statuszeile: immer vorhanden und gleich hoch, damit die Tasten darunter nicht springen
    // Zustandsfeld: rot = wartet auf „Los“, gelb = Satzpause läuft, grün = Satz läuft, grau = pausiert
    const stateChip = a.paused
      ? `<div class="timer st st-paused">${t("ph_paused")}</div>`
      : a.phase === "interval" && iv && iv.ends_at
        ? (() => {
            const pos = step.block_type === "flow" ? `${iv.round}/${iv.rounds}` : t("pos_round_of", { r: iv.round, n: iv.rounds });
            return iv.phase === "work"
              ? `<div class="timer st st-go st-iv"><span>${t("st_go")} · ${esc(pos)}</span><span class="st-time" data-until="${esc(iv.ends_at)}"></span></div>`
              : `<div class="timer st st-rest st-iv"><span class="grow">${step.block_type === "flow" ? t("flow_switch") : t("t_rest")} <span class="st-time" data-until="${esc(iv.ends_at)}"></span></span></div>`;
          })()
      : a.rest_until
        ? `<div class="timer st st-rest"><button class="tbtn" data-a="rest" data-d="-15" aria-label="${t("rest_less")}">−15</button>
          <span class="grow">${t("t_rest")} <span data-until="${esc(a.rest_until)}"></span></span>
          <button class="tbtn" data-a="rest" data-d="15" aria-label="${t("rest_more")}">+15</button></div>`
        : a.phase === "ready"
          ? `<div class="timer st st-wait">${t("st_wait")}</div>`
          : a.phase === "active"
            ? `<div class="timer st st-go">${t("st_go")}</div>`
            : "";
    const timers = [
      stateChip,
      lastSet && lastSet.record && !a.rest_until ? `<div class="timer rec">${esc(t("t_record", { name: lastSet.exercise_name }))}</div>` : "",
      a.block_until ? `<div class="timer cap">${t("t_left")} <span data-until="${esc(a.block_until)}"></span></div>` : "",
      a.block_expired && step.block_end?.time_cap_s && a.phase === "active" ? `<div class="timer cap">${t("t_up")}</div>` : "",
      a.pending_question !== null && a.pending_question !== undefined ? `<div class="timer q">${t("t_question")}</div>` : "",
    ].join("");
    const adjust = this._renderAdjust(a, step);
    const nextLabel = a.paused
      ? t("b_resume")
      : a.phase === "ready"
        ? t("b_go")
        : a.phase === "interval"
          ? t(step.block_type === "flow" ? "b_end_flow" : "b_end_hiit")
          : step.type === "set"
            ? a.adjust && a.adjust.changed ? t("b_set_done_changed") : t("b_set_done")
            : t("b_next");
    const nxt = a.steps[a.idx + 1];
    const upnext = this._renderUpNext(nxt);
    const pts = step.exercise ? (this._state.exercise_history || {})[step.exercise] : null;
    const history = step.type === "set" ? historyCharts(pts) : "";
    const upcoming = a.steps
      .slice(a.idx + 2)
      .filter((s) => s.type === "set")
      .slice(0, 3)
      .map((s) => `<li><span class="exn">${img(s.image)}<span>${esc(s.exercise_name)}</span></span><span class="tgt">${esc(targetText(s))}</span></li>`)
      .join("");
    return `
      <div class="pad live">
        <div class="row between"><div><b>${esc(a.workout_name)}</b> <span class="muted"><span class="sep">· </span>${esc(a.plan_name)}</span></div>
          <span class="row"><span class="badge ${a.paused ? "warn" : "info"}">${esc(phase)}</span>
          <span class="elapsed" title="${esc(t("el_title"))}">
            <span class="el-time">⏱ <b data-since="${esc(a.started_at)}"></b></span>
            ${this._state.last_same_duration_s ? `<span class="el-ref">${esc(t("el_last", { d: hms(this._state.last_same_duration_s) }))}</span>
              <span class="el-bar"><i data-since-of="${esc(a.started_at)}" data-ref="${this._state.last_same_duration_s}"></i></span>` : ""}
          </span></span></div>
        <div class="bar"><div style="width:${pct}%"></div></div>
        <div class="muted small">${t("step", { i: Math.min(a.idx + 1, total), n: total })}</div>
        <div class="stage">
          <div class="current t-${esc(step.block_type || "")} ${curImg ? "has-img" : ""}">
            ${curImg ? `<div class="cur-img">${img(curImg, "pic")}${img(curImg, "pic alt", 1)}</div>` : ""}
            <div class="cur-txt">
              ${showLabel ? `<div class="ptype">${esc(blockTitle(step.block_type, step.block_name))}${step.type === "set" && position(step) ? ` · ${esc(position(step))}` : ""}</div>` : ""}
              ${main}${note ? `<div class="note">${esc(note)}</div>` : ""}
              ${history}
            </div></div>
          ${upnext}
        <div class="status">${timers}</div>
        <div class="controls">
          ${adjust}
          <button class="btn primary big" data-a="next">${nextLabel}</button>
        <div class="row btns">
          <button class="btn" data-a="svc" data-svc="undo">${t("b_back")}</button>
          <button class="btn" data-a="svc" data-svc="pause">${a.paused ? t("b_continue") : t("b_pause")}</button>
          <button class="btn" data-a="svc" data-svc="skip">${t("b_skip")}</button>
        </div>
        <div class="row btns">
          <button class="btn" data-a="svc" data-svc="finish" data-ck="finish" data-confirm="${esc(t("c_finish"))}">${t("b_finish")}</button>
          <button class="btn danger" data-a="svc" data-svc="abort" data-keep="0" data-ck="abort" data-confirm="${esc(t("c_discard"))}">${t("b_discard")}</button>
        </div>
        </div>
        ${upcoming ? `<div class="upc"><div class="lbl">${t("coming_up")}</div><ul class="list">${upcoming}</ul></div>` : ""}
        </div>
        ${a.sets.length ? `<div class="lbl">${t("logged")}</div>${this._renderSets(a.sets.slice().reverse(), null)}` : ""}
      </div>`;
  }

  /* Rechte Spalte: was als Nächstes kommt – groß, aber abgeschwächt. */
  _renderUpNext(nxt) {
    let body;
    if (!nxt) {
      body = `<div class="un-name">${t("un_done")}</div>`;
    } else if (nxt.type === "set") {
      body = `${nxt.image ? `<div class="un-img">${img(nxt.image, "pic")}</div>` : ""}
        <div class="un-name">${esc(nxt.exercise_name)}</div>
        <div class="un-tgt">${esc(targetText(nxt))}</div>
        <div class="un-pos">${esc(position(nxt))}</div>`;
    } else {
      body = `<div class="un-name">${esc(blockTitle(nxt.block_type, nxt.block_name))}</div>`;
    }
    return `<div class="upnext t-${esc(nxt ? nxt.block_type : "")}"><div class="un-lbl">${t("un_label")}</div>${body}</div>`;
  }

  /* Plus/Minus für den laufenden Satz. Die Werte kommen aus der Integration (a.adjust). */
  _renderAdjust(a, step) {
    const ghost = `<div class="adj-row ghost" aria-hidden="true"></div>`;
    const adj = a.adjust;
    if (step.type !== "set" || a.phase !== "active" || a.paused || !adj || !String(adj.key).startsWith(`${a.id}:${a.idx}:`)) {
      return `<div class="adj">${ghost}${ghost}</div>`; // Platz freihalten
    }
    const row = (k, label, value, unit, changed) => `
      <div class="adj-row">
        <span class="adj-lbl">${label}</span>
        <button class="btn round" data-a="adj" data-k="${k}" data-d="-1" aria-label="${esc(t("a_less", { l: label }))}">−</button>
        <span class="adj-val ${changed ? "chg" : ""}">${esc(num(value))}${unit ? ` <small>${unit}</small>` : ""}</span>
        <button class="btn round" data-a="adj" data-k="${k}" data-d="1" aria-label="${esc(t("a_more", { l: label }))}">+</button>
      </div>`;
    const rows = [
      adj.timed ? row("reps", t("a_seconds"), adj.duration, "s", adj.changed_reps)
                : row("reps", step.per_side ? t("a_reps_side") : t("a_reps"), adj.reps, "", adj.changed_reps),
      adj.weight !== null && adj.weight !== undefined ? row("weight", t("a_weight"), adj.weight, "kg", adj.changed_weight) : ghost,
    ].join("");
    return `<div class="adj">${rows}</div>`;
  }

  _renderSets(sets, sessionId) {
    return `<table class="sets">${sets
      .map((x) => {
        const cls = STATUS[x.status] || "neutral";
        const label = STATUS[x.status] ? t(`st_${x.status}`) : x.status;
        const ed = this._editing;
        if (ed && ed.set_id === x.id && (ed.session_id || null) === (sessionId || null)) {
          // Bearbeiten: eigener Kasten mit Luft – Werte, „Wie war's?“, dann Speichern groß, Nebenaktionen darunter
          return `<tr class="editing"><td colspan="3"><div class="edit-panel">
            <div class="ename">${esc(x.exercise_name)}${position(x) ? ` <span class="muted">· ${esc(position(x))}</span>` : ""}</div>
            <div class="edit-fields">
              ${ed.timed ? `<label>${t("a_seconds")}<input data-field="duration_s" inputmode="numeric" value="${esc(ed.duration_s)}"></label>`
                         : `<label>${t("a_reps")}<input data-field="reps" inputmode="numeric" value="${esc(ed.reps)}"></label>`}
              <label>kg<input data-field="weight_kg" inputmode="decimal" value="${esc(ed.weight_kg)}"></label>
            </div>
            <div class="edit-lbl">${t("ef_last")}</div>
            <div class="edit-effort">${["easy", "normal", "hard"]
              .map((v) => `<button class="chip-btn ef-${v} ${ed.effort === v ? "on" : ""}" data-a="ed-effort" data-v="${v}">${t(`ef_${v}`)}</button>`)
              .join("")}</div>
            <button class="btn primary edit-save" data-a="edit-save">${t("e_save")}</button>
            <div class="edit-sec">
              <button class="btn" data-a="edit-skip">${t("e_skipped")}</button>
              <button class="btn" data-a="edit-cancel">${t("e_cancel")}</button>
            </div></div></td></tr>`;
        }
        return `<tr data-a="edit" data-set="${x.id}" ${sessionId ? `data-session="${esc(sessionId)}"` : ""}>
          <td>${esc(x.exercise_name)}<div class="muted small">${esc(position(x))}</div></td>
          <td class="val">${x.record ? `<span class="trophy" title="${esc(t("t_record", { name: "" }))}">🏆</span> ` : ""}${esc(setValue(x))}${x.effort ? ` <span class="ef-dot ef-${x.effort}">${t(`ef_${x.effort}`)}</span>` : ""}</td><td><span class="badge ${cls}">${esc(label)}</span></td></tr>`;
      })
      .join("")}</table>`;
  }

  _renderHistory() {
    const h = this._history;
    if (!h) return `<div class="pad muted">${t("h_loading")}</div>`;
    if (!h.sessions.length) return `<div class="pad muted">${t("h_empty")}</div>`;
    const exRows = h.exercises
      .map((e) => {
        const last = e.last_sets.map(setValue).join(" · ");
        const s = e.suggestion;
        const next = s ? `${s.reps ? t("reps_n", { n: s.reps }) : ""}${s.weight_kg !== null && s.weight_kg !== undefined ? ` · ${kg(s.weight_kg)}` : ""}` : "";
        return `<tr><td><div class="exn">${img(e.image, "thumb lg")}<div><b>${esc(e.name)}</b><div class="muted small">${esc(t("h_ex_meta", { n: e.sessions, d: date(e.last_date) }))}${bestText(e.bests)}</div></div></div></td>
          <td data-label="${esc(t("h_th_hist"))}">${spark(e.points)}</td>
          <td class="small" data-label="${esc(t("h_th_last"))}">${esc(last)}</td>
          <td class="small" data-label="${esc(t("h_th_next"))}">${s ? `<b class="${s.increased ? "up" : ""}">${esc(next)}</b><div class="muted">${esc(reasonSug(s))}</div>` : ""}</td></tr>`;
      })
      .join("");
    const sessRows = h.sessions
      .map((s) => {
        const open = this._openSessions.has(s.id);
        const done = s.sets.filter((x) => x.status !== "skipped").length;
        const open_q = s.sets.filter((x) => x.status === "unconfirmed").length;
        return `<div class="sess">
          <div class="row between click" data-a="toggle-session" data-session="${esc(s.id)}">
            <div><b>${esc(date(s.started_at))}</b> <span class="muted">${esc(time(s.started_at))}</span> · ${esc(s.workout_name)} <span class="muted">(${esc(s.plan_name)})</span></div>
            <div>${sessionDuration(s) ? `<span class="dur">⏱ ${esc(sessionDuration(s))}</span> · ` : ""}${t("h_sets", { n: done })} ${open_q ? `<span class="badge warn">${t("h_unconfirmed", { n: open_q })}</span>` : ""}${s.status === "aborted" ? ` <span class="badge muted">${t("h_aborted")}</span>` : ""} ${open ? "▴" : "▾"}</div>
          </div>
          ${open ? `${this._renderSets(s.sets, s.id)}<button class="btn danger small" data-a="delete-session" data-session="${esc(s.id)}" data-ck="ses-${esc(s.id)}" data-confirm="${esc(t("c_delete"))}">${t("h_delete")}</button>` : ""}
        </div>`;
      })
      .join("");
    const htab = (id, label, count) =>
      `<button class="subtab ${this._histTab === id ? "on" : ""}" data-a="htab" data-tab="${id}">${label} <span class="cnt">${count}</span></button>`;
    const body = this._histTab === "overview"
      ? this._renderOverview()
      : this._histTab === "sessions"
      ? sessRows
      : `<table class="ex-table"><tr><th>${t("h_th_ex")}</th><th>${t("h_th_hist")} <span class="muted">${t("h_last8")}</span></th><th>${t("h_th_last")}</th><th>${t("h_th_next")}</th></tr>${exRows}</table>`;
    return `<div class="pad">
      <div class="subtabs">${htab("overview", t("h_tab_over"), "")}${htab("exercises", t("h_tab_ex"), h.exercises.length)}${htab("sessions", t("h_tab_sess"), h.sessions.length)}</div>
      ${body}</div>`;
  }

  async _loadTemplates() {
    try {
      this._templates = (await this._ws({ type: "templates" })).templates;
    } catch (_) {
      this._templates = [];
    }
    this._render();
  }

  _renderTemplates() {
    if (!this._templates) {
      if (!this._templatesLoading) {
        this._templatesLoading = true;
        this._loadTemplates().finally(() => (this._templatesLoading = false));
      }
      return `<div class="muted small">${t("tpl_loading")}</div>`;
    }
    const groups = {};
    this._templates.forEach((tp) => (groups[tp.group_key || tp.group] = groups[tp.group_key || tp.group] || []).push(tp));
    return Object.entries(groups)
      .map(([g, list]) => `<div class="tgroup">
          <div class="tghead"><ha-icon icon="${esc(list[0].group_icon || "mdi:dumbbell")}"></ha-icon>
            <div><div class="tgname">${esc(list[0].group_key ? t(`tg.${g}`) : g)} <span class="cnt">${list.length}</span></div>
            <div class="tgabout">${esc(list[0].group_key ? t(`tg.${g}.about`) : list[0].group_about || "")}</div></div></div>${list
        .map((tp) => `<div class="tpl">
            <div class="tpl-txt"><b>${esc(tp.name)}</b> <span class="muted small">· ${t(tp.workouts.length === 1 ? "n_workout" : "n_workouts", { n: tp.workouts.length })}</span>
              <div class="muted small">${esc(tp.description || "")}</div></div>
            <button class="btn small ${tp.installed ? "" : "primary"}" data-a="tpl-import" data-tpl="${esc(tp.id)}"
              ${tp.installed ? `data-ck="tpl-${esc(tp.id)}" data-confirm="${esc(t("tpl_reload_c"))}"` : ""}>
              ${tp.installed ? t("tpl_installed") : t("tpl_take")}</button>
          </div>`)
        .join("")}</div>`)
      .join("");
  }

  async _loadStarter(force = false) {
    try {
      const resp = await fetch(`${GUIDE_BASE}/${t("example_file")}`, { cache: "no-cache" });
      const text = await resp.text();
      this._starter = text;
      if (force || (!this._importText.trim() && !this._starterUsed)) {
        this._importText = text;
        this._starterUsed = true;
      }
    } catch (_) {
      this._starter = "";
    }
    this._render();
  }

  /* Muskelgruppen als Etiketten, eingefärbt nach Erholung (Stand vor diesem Training) */
  _muscleTags(primary, secondary) {
    primary = primary || [];
    secondary = secondary || [];
    if (!primary.length && !secondary.length) return "";
    this._ensureStats();
    const rec = {};
    ((this._stats && this._stats.recovery) || []).forEach((r) => (rec[r.group] = r.status));
    const tag = (g, sec) => {
      const st = rec[g] || "none";
      const tip = `${t(sec ? "mt_secondary" : "mt_primary")} · ${t(`rc_${st}`)}`;
      return `<span class="mt rc-${st} ${sec ? "sec" : ""}" title="${esc(tip)}">${esc(t(`mg.${g}`))}</span>`;
    };
    return `<div class="mtags">${primary.map((g) => tag(g, false)).join("")}${secondary.map((g) => tag(g, true)).join("")}</div>`;
  }

  _imageFor(exercise, step) {
    const i = (step.exercises || []).indexOf(exercise);
    return i >= 0 ? (step.images || [])[i] || null : null;
  }

  _ensureStats() {
    if (this._stats || this._statsLoading || !this._hass) return;
    this._statsLoading = true;
    this._ws({ type: "stats" })
      .then((r) => (this._stats = r))
      .catch(() => (this._stats = null))
      .finally(() => {
        this._statsLoading = false;
        this._render();
      });
  }

  /* „Wie war's?“: kurzer Dialog direkt nach „Satz fertig“ – nennt den Satz, verschwindet nach 5 Sekunden
     (die Linie unten schrumpft mit). Verpasst? In der Liste der erfassten Sätze bzw. im Verlauf änderbar. */
  _watchLogged(prev, state) {
    // Zuletzt gesehene Satz-Nummer selbst merken (der Zustand kann dasselbe, veränderte Objekt sein)
    const a = state && state.active;
    const last = a && a.sets.length ? a.sets[a.sets.length - 1].id : 0;
    const seen = this._seenSet;
    this._seenSet = a ? { session: a.id, last } : null;
    if (!a || !seen || seen.session !== a.id || last <= seen.last) return;
    const rec = a.sets[a.sets.length - 1];
    if (!rec || rec.status === "skipped") return;
    const step = a.steps[rec.step];
    if (!step || step.type !== "set") return; // HIIT/Flow-Abschnitte nicht abfragen
    this._prompt = { setId: rec.id, until: Date.now() + EFFORT_PROMPT_MS };
    clearTimeout(this._promptTimer);
    this._promptTimer = setTimeout(() => this._closePrompt(), EFFORT_PROMPT_MS);
  }

  _closePrompt() {
    clearTimeout(this._promptTimer);
    this._prompt = null;
    const el = this.shadowRoot.querySelector(".efp");
    if (el) el.remove(); // ohne Neuzeichnen – nichts springt
  }

  _renderEffortPrompt() {
    const p = this._prompt;
    const a = this._state && this._state.active;
    if (!p || !a) return "";
    const rec = a.sets.find((x) => x.id === p.setId);
    if (!rec) return "";
    const left = Math.max(0, p.until - Date.now());
    const cur = rec.effort || null;
    return `<div class="efp" role="dialog" aria-label="${esc(t("ef_last"))}">
      <div class="efp-head"><span class="muted small">${esc(t("ef_last"))}</span>
        <b>${esc(rec.exercise_name)}</b>
        <span class="muted small">${position(rec) ? `${esc(position(rec))} · ` : ""}${esc(setValue(rec))}</span></div>
      <div class="efp-btns">${["easy", "normal", "hard"]
        .map((v) => `<button class="chip-btn ef-${v} ${cur === v ? "on" : ""}" data-a="effort" data-set="${rec.id}" data-v="${v}">${t(`ef_${v}`)}</button>`)
        .join("")}</div>
      <div class="efp-bar"><i style="animation-duration:${EFFORT_PROMPT_MS}ms;animation-delay:-${EFFORT_PROMPT_MS - left}ms"></i></div>
    </div>`;
  }

  _renderOverview() {
    this._ensureStats();
    const s = this._stats;
    if (!s) return `<div class="muted">${t("loading")}</div>`;
    const st = this._state;
    const tile = (label, value, sub = "") =>
      `<div class="tile"><div class="tile-l">${label}</div><div class="tile-v">${value}</div>${sub ? `<div class="tile-s">${sub}</div>` : ""}</div>`;
    const tiles = `<div class="tiles">
      ${tile(t("tile_week"), `${s.week.done}<small>/${s.week.goal}</small>`)}
      ${tile(t("tile_streak"), `🔥 ${s.streak_weeks}`, s.streak_weeks === 1 ? t("tile_week1") : t("tile_weeks", { n: s.streak_weeks }))}
      ${tile(t("tile_total"), s.total, s.first ? t("tile_since", { d: date(s.first) }) : "")}
      ${tile(t("tile_time"), `${s.time.week_min}<small> min</small>`, s.time.avg_min !== null ? t("tile_time_avg", { m: s.time.avg_min }) : "")}
    </div>`;
    const recVal = (kind, v) => t(`rec_${kind}`, { v: num(v) });
    const records = s.records.length
      ? `<ul class="list recs">${s.records
          .map((r) => `<li><span>🏆 <b>${esc(r.name)}</b> <span class="muted small">${esc(date(r.date))}</span></span>
            <span>${esc(recVal(r.kind, r.value))} <span class="muted small">${esc(t("rec_prev", { v: num(r.previous) }))}</span></span></li>`)
          .join("")}</ul>`
      : `<div class="muted small">${t("rec_none")}</div>`;
    const groups = GROUPS.filter((g) => s.volume[g]);
    const maxv = Math.max(12, ...groups.map((g) => s.volume[g].week));
    const volume = groups.length && groups.some((g) => s.volume[g].week)
      ? `<div class="vol">${groups
          .map((g) => {
            const v = s.volume[g];
            return `<div class="vb"><span class="vb-n">${t(`mg.${g}`)}</span>
              <div class="vb-bar"><div style="width:${(100 * v.week) / maxv}%"></div><i style="left:${(100 * 10) / maxv}%"></i></div>
              <span class="vb-v"><b>${v.week}</b> <span class="muted small">${t("vol_last", { n: v.last_week })}</span></span></div>`;
          })
          .join("")}</div><div class="muted small">${t("vol_hint")}</div>`
      : `<div class="muted small">${t("vol_none")}</div>`;
    const un = s.unassigned || { sets: 0, names: [] };
    const unassigned = un.sets
      ? `<div class="msg warnmsg small">${esc(t("vol_unassigned", { n: un.sets, list: un.names.join(", ") }))}</div>` : "";
    // „seit 15 h“ solange die Gruppe sich erholt, danach „zuletzt vor 3 Tagen“
    const ago = (h, status) => {
      if (h === null) return "";
      const since = status === "fresh" || status === "recovering";
      if (h < 48) return t(since ? "rc_since_h" : "rc_h", { n: h });
      return t(since ? "rc_since_d" : "rc_d", { n: Math.round(h / 24) });
    };
    const recovery = s.recovery.length
      ? `<div class="rc">${s.recovery
          .map((r) => `<div class="rc-i rc-${r.status}"><b>${t(`mg.${r.group}`)}</b><span>${t(`rc_${r.status}`)}</span><small>${ago(r.hours, r.status)}</small></div>`)
          .join("")}</div>`
      : "";
    return `${weekCard(s)}${tiles}
      <div class="lbl">${t("rec_title")}</div>${records}
      <div class="lbl">${t("vol_title")}</div>${volume}${unassigned}
      ${recovery ? `<div class="lbl">${t("rc_title")}</div>${recovery}` : ""}`;
  }

  /* Einmal beim Öffnen: Person des angemeldeten HA-Benutzers auswählen (nicht während eines Trainings) */
  _autoSelectProfile(state) {
    if (this._autoProfileDone || !this._hass || !this._hass.user) return;
    this._autoProfileDone = true;
    const mine = (state.profiles || []).find((p) => p.user_id && p.user_id === this._hass.user.id);
    if (mine && mine.id !== state.profile && !state.active) {
      this._ws({ type: "profile", action: "select", profile: mine.id }).catch(() => {});
    }
  }

  _loadHaUsers() {
    if (this._haUsers !== undefined || !this._hass.user || !this._hass.user.is_admin) return;
    this._haUsers = null;
    this._ws({ type: "ha_users" })
      .then((r) => (this._haUsers = r.users))
      .catch(() => (this._haUsers = []))
      .finally(() => this._render());
  }

  _renderPeople() {
    const st = this._state;
    const ed = this._ppEdit;
    this._loadHaUsers();
    const users = this._haUsers || [];
    const userName = (id) => (users.find((u) => u.id === id) || {}).name;
    const link = (p) => {
      if (this._hass.user && this._hass.user.is_admin) {
        return `<label class="pp-link"><span class="muted small">${t("pp_user")}</span>
          <select data-field="pp-link" data-p="${esc(p.id)}"><option value="">${t("pp_user_none")}</option>${users
            .map((u) => `<option value="${esc(u.id)}" ${u.id === p.user_id ? "selected" : ""}>${esc(u.name)}</option>`)
            .join("")}</select></label>`;
      }
      return p.user_id ? `<div class="muted small">${esc(userName(p.user_id) ? t("pp_linked", { name: userName(p.user_id) }) : t("pp_linked_anon"))}</div>` : "";
    };
    const form = (id) => `<div class="row pp-form">
        <input data-field="pp-name" placeholder="${esc(t("pp_name"))}" value="${esc(ed.name)}">
        <button class="btn small primary" data-a="pp-save">${t("pp_save")}</button>
        <button class="btn small" data-a="pp-cancel">${t("e_cancel")}</button></div>`;
    const rows = (st.profiles || [])
      .map((p) => {
        const on = p.id === st.profile;
        if (ed && ed.id === p.id) return `<div class="plan">${form(p.id)}</div>`;
        return `<div class="plan row between"><div><b>${esc(p.name)}</b>${on ? ` <span class="badge ok">${t("pp_active")}</span>` : ""}
            ${on ? `<div class="muted small">${t("pp_goal", { n: st.weekly_goal })}</div>` : ""}${link(p)}</div>
          <div class="row">${on ? "" : `<button class="btn small primary" data-a="pp-select" data-p="${esc(p.id)}" ${st.active ? "disabled" : ""}>${t("pp_select")}</button>`}
            <button class="btn small" data-a="pp-rename" data-p="${esc(p.id)}">${t("pp_rename")}</button>
            ${on ? "" : `<button class="btn small danger" data-a="pp-delete" data-p="${esc(p.id)}" data-ck="pp-${esc(p.id)}" data-confirm="${esc(t("pp_c_delete"))}">${t("pp_delete")}</button>`}</div></div>`;
      })
      .join("");
    return `<div class="muted small">${t("pp_intro")} ${t("pp_user_hint")}${st.active ? ` ${t("pp_busy")}` : ""}</div>${rows}
      ${ed && !ed.id ? `<div class="plan">${form(null)}</div>` : `<button class="btn" data-a="pp-add">${t("pp_add")}</button>`}`;
  }

  _renderPlans() {
    const st = this._state;
    if (this._starter === undefined && !this._starterLoading) {
      this._starterLoading = true;
      this._loadStarter();
    }
    const plans = st.plans
      .map(
        (p) => `<div class="plan">
          <div class="row between"><div><b>${esc(p.name)}</b>${p.id === st.program ? ` <span class="badge ok">${t("p_active")}</span>` : ""}${p.description ? `<div class="muted small">${esc(p.description)}</div>` : ""}
            ${p.images_missing && p.images_missing.length ? `<div class="muted small">${esc(t("p_noimg", { list: p.images_missing.join(", ") }))}</div>` : ""}</div>
            <div class="row"><button class="btn small" data-a="plan-edit" data-plan="${esc(p.id)}">${t("p_edit")}</button>
            <button class="btn small danger" data-a="plan-delete" data-plan="${esc(p.id)}" data-name="${esc(p.name)}" data-ck="plan-${esc(p.id)}" data-confirm="${esc(t("c_delete"))}">${t("p_delete")}</button></div></div>
          <ul class="list">${p.workouts
            .map((w) => {
              const isNext = st.next && st.next.plan_id === p.id && st.next.workout_id === w.id;
              return `<li><span>${esc(w.name)} ${isNext ? `<span class="badge info">${t("p_next_badge")}</span>` : ""}</span>
                <span>${isNext ? "" : `<button class="btn small" data-a="next-workout" data-plan="${esc(p.id)}" data-workout="${esc(w.id)}">${t("p_set_next")}</button>`}
                ${st.active ? "" : `<button class="btn small primary" data-a="start" data-plan="${esc(p.id)}" data-workout="${esc(w.id)}">${t("p_start")}</button>`}</span></li>`;
            })
            .join("")}</ul></div>`
      )
      .join("");
    const msg = this._importMsg ? `<div class="msg ${this._importMsg.ok ? "ok" : "err"}">${esc(this._importMsg.text)}</div>` : "";
    // Unter-Reiter: Meine Pläne · Vorlagen · Eigener Plan
    if (!this._planTab) this._planTab = st.plans.length ? "mine" : "templates";
    if (!this._templates && !this._templatesLoading) {
      this._templatesLoading = true;
      this._loadTemplates().finally(() => (this._templatesLoading = false));
    }
    const ptab = (id, icon, label, count) =>
      `<button class="subtab ${this._planTab === id ? "on" : ""}" data-a="ptab" data-tab="${id}">
         <ha-icon icon="${icon}"></ha-icon> ${label}${count !== null ? ` <span class="cnt">${count}</span>` : ""}</button>`;
    let body;
    if (this._planTab === "people") {
      body = this._renderPeople();
    } else if (this._planTab === "templates") {
      body = `<div class="muted small">${t("p_tpl_intro")}</div>${this._renderTemplates()}`;
    } else if (this._planTab === "import") {
      body = `<div class="muted small">${t("p_import_intro")}</div>
      <div class="row dl">
        <a class="btn" href="${GUIDE_BASE}/${t("guide_file")}" download="${t("guide_dl")}" target="_blank" rel="noreferrer">${t("p_dl_guide")}</a>
        <a class="btn" href="${GUIDE_BASE}/${t("example_file")}" download="${t("example_dl")}" target="_blank" rel="noreferrer">${t("p_dl_example")}</a>
        <span class="grow"></span>
        <button class="btn small" data-a="starter">${t("p_insert")}</button>
        <button class="btn small" data-a="clear-import">${t("p_clear")}</button>
      </div>
      <textarea data-field="import" rows="22" spellcheck="false" placeholder="${esc(t("p_placeholder")).replace(/\n/g, "&#10;")}">${esc(this._importText)}</textarea>
      <button class="btn primary" data-a="import" ${this._importText.trim() ? "" : "disabled"}>${t("p_import")}</button>`;
    } else {
      body = plans || `<div class="empty">${t("p_none")}
        <div class="row"><button class="btn primary" data-a="ptab" data-tab="templates">${t("p_pick_tpl")}</button>
        <button class="btn" data-a="ptab" data-tab="import">${t("p_own")}</button></div></div>`;
    }
    return `<div class="pad">
      <div class="subtabs">
        ${ptab("mine", "mdi:clipboard-list-outline", t("p_tab_mine"), st.plans.length)}
        ${ptab("templates", "mdi:star-outline", t("p_tab_tpl"), this._templates ? this._templates.length : null)}
        ${ptab("import", "mdi:file-document-edit-outline", t("p_tab_own"), null)}
        ${ptab("people", "mdi:account-multiple-outline", t("p_tab_people"), (st.profiles || []).length)}
      </div>
      ${msg}
      ${body}
    </div>`;
  }
}

/* Mini-Diagramm pro Übung: Gewicht, bei Körpergewicht Wiederholungen, bei Zeit-Sätzen Sekunden.
   Ein Punkt pro Training (bester Wert), auch bei nur einem Training. */
/* Für die laufende Übung: Gewicht und Wiederholungen (bzw. Sekunden) nebeneinander. */
const GROUPS = ["chest", "back", "shoulders", "biceps", "triceps", "core", "quads", "hamstrings", "glutes", "calves"];

/* Bestwert einer Übung für die Verlaufsliste: „· 🏆 52,5 kg“ */
function bestText(b) {
  if (!b) return "";
  if (b.weight) return ` · 🏆 ${kg(b.weight)}`;
  if (b.reps) return ` · 🏆 ${t("reps_n", { n: b.reps })}`;
  if (b.duration) return ` · 🏆 ${b.duration} s`;
  return "";
}

/* Wochenansicht: Zielring (ein Abschnitt pro geplantem Training) + Sätze pro Tag als Balken */
function weekCard(stats) {
  const wk = stats && stats.week;
  if (!wk) return "";
  // Ring: Abschnitte = Wochenziel, gefüllt = absolvierte Trainings
  const R = 42, C = 2 * Math.PI * R, n = Math.max(1, wk.goal), gap = n > 1 ? 5 : 0;
  const seg = C / n - gap;
  const ring = Array.from({ length: n }, (_, i) =>
    `<circle r="${R}" cx="50" cy="50" class="${i < wk.done ? "on" : ""}"
      stroke-dasharray="${seg.toFixed(2)} ${(C - seg).toFixed(2)}" stroke-dashoffset="${(-i * C / n).toFixed(2)}"/>`).join("");
  const extra = wk.done > wk.goal ? `<span class="wr-extra">+${wk.done - wk.goal}</span>` : "";
  // Balken: Sätze pro Tag (relativ zum stärksten Tag der Woche)
  const max = Math.max(1, ...wk.days.map((d) => d.sets));
  const bars = wk.days
    .map((d) => {
      const name = new Date(`${d.date}T12:00:00`).toLocaleDateString(LOCALE, { weekday: "narrow" });
      const h = d.sets ? Math.max(10, Math.round((100 * d.sets) / max)) : 0;
      const tip = d.workouts ? `${(d.names || []).filter(Boolean).join(", ")} · ${t("h_sets", { n: d.sets })}` : "";
      return `<div class="wb ${d.date === wk.today ? "today" : ""} ${d.date > wk.today ? "future" : ""}" title="${esc(tip)}">
        <span class="wb-n">${d.sets || ""}</span>
        <div class="wb-col">${h ? `<div style="height:${h}%"></div>` : `<i></i>`}</div>
        <span class="wb-d">${esc(name)}</span></div>`;
    })
    .join("");
  const vol = stats.volume || {};
  const groups = Object.keys(vol).filter((g) => vol[g].week).sort((a, b) => vol[b].week - vol[a].week);
  const streak = stats.streak_weeks
    ? ` · ${stats.streak_weeks === 1 ? t("wk_streak1") : t("wk_streak", { n: stats.streak_weeks })}` : "";
  return `<div class="week">
    <div class="wr">
      <svg viewBox="0 0 100 100" class="wr-svg" role="img" aria-label="${esc(t("wk_aria", { d: wk.done, n: wk.goal }))}">${ring}</svg>
      <div class="wr-c"><b>${wk.done}</b><span>/${wk.goal}</span>${extra}</div>
    </div>
    <div class="wk-main">
      <div class="wk-top"><span class="wk-title">${t("wk_title")}</span>
        <span class="wk-goal"><button class="tbtn" data-a="goal" data-d="-1" aria-label="${t("wk_goal_less")}">−</button><span class="muted small">${t("wk_goal")}</span><button class="tbtn" data-a="goal" data-d="1" aria-label="${t("wk_goal_more")}">+</button></span></div>
      <div class="wk-cap">${t("wk_bars")}</div>
      <div class="wk-bars">${bars}</div>
      <div class="wk-sub">${wk.left ? t("wk_left", { n: wk.left }) : `✓ ${t("wk_reached")}`}${streak} · ${t("wk_total", { n: stats.total })}</div>
      ${groups.length ? `<div class="wk-tags">${groups.map((g) => `<span>${esc(t(`mg.${g}`))}</span>`).join("")}</div>` : ""}
    </div></div>`;
}

function historyCharts(points) {
  const pts = points || [];
  if (!pts.length) return `<div class="cur-chart muted small">${t("c_first")}</div>`;
  const has = (k) => pts.some((p) => p[k] !== null && p[k] !== undefined);
  // gleiche Reihenfolge wie die Kacheln darüber: links Wdh./Sekunden, rechts Gewicht
  const charts = [
    has("reps") ? spark(pts, ["reps", t("u_reps")], true) : has("duration_s") ? spark(pts, ["duration_s", "s"], true) : "",
    has("weight_kg") ? spark(pts, ["weight_kg", "kg"], true) : "",
  ].join("");
  return `<div class="cur-chart">${charts}</div>`;
}

function spark(points, forced = null, compact = false) {
  const pts = points || [];
  const auto = pts.some((p) => p.weight_kg !== null && p.weight_kg !== undefined)
    ? ["weight_kg", "kg"]
    : pts.some((p) => p.reps !== null && p.reps !== undefined)
      ? ["reps", t("u_reps")]
      : pts.some((p) => p.duration_s !== null && p.duration_s !== undefined)
        ? ["duration_s", "s"]
        : null;
  const metric = forced || auto;
  if (!metric) return "";
  const [key, unit] = metric;
  const vals = pts.map((p) => p[key]).filter((v) => v !== null && v !== undefined);
  const W = compact ? 120 : 150, H = compact ? 30 : 40, PX = 10, PY = compact ? 6 : 8;
  const min = Math.min(...vals), max = Math.max(...vals);
  const x = (i) => (vals.length === 1 ? W / 2 : PX + (i * (W - 2 * PX)) / (vals.length - 1));
  const y = (v) => (max === min ? H / 2 : PY + ((max - v) * (H - 2 * PY)) / (max - min));
  const line = vals.length > 1
    ? `<polyline points="${vals.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(" ")}"/>`
    : "";
  const dots = vals
    .map((v, i) => `<circle cx="${x(i).toFixed(1)}" cy="${y(v).toFixed(1)}" r="${i === vals.length - 1 ? 3.2 : 2.2}"
      class="${i === vals.length - 1 ? "last" : ""}"><title>${esc(date(pts[i]?.date))}: ${esc(num(v))} ${unit}</title></circle>`)
    .join("");
  const grid = max === min
    ? `<line x1="0" x2="${W}" y1="${H / 2}" y2="${H / 2}"/>`
    : `<line x1="0" x2="${W}" y1="${PY}" y2="${PY}"/><line x1="0" x2="${W}" y1="${H - PY}" y2="${H - PY}"/>`;
  const first = vals[0], last = vals[vals.length - 1];
  const best = Math.max(...vals);
  const label = compact
    ? vals.length === 1 || best === last ? t("c_last", { v: num(last), u: unit }) : t("c_last_best", { v: num(last), b: num(best), u: unit })
    : first === last ? `${num(last)} ${unit}` : `${num(first)} → ${num(last)} ${unit}`;
  const trend = last > first ? "up" : last < first ? "down" : "";
  return `<div class="chart"><svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img"
      aria-label="${esc(t("c_aria", { l: label }))}"><rect width="${W}" height="${H}" rx="6"/>
      <g class="grid">${grid}</g>${line}${dots}</svg>
    <div class="chart-lbl ${trend}">${esc(label)}${compact ? "" : ` · ${vals.length === 1 ? t("c_1") : t("c_n", { n: vals.length })}`}</div></div>`;
}

const STYLE = `
  :host { display: block; }
  ha-card { overflow: hidden; }
  .tabs { display: flex; border-bottom: 1px solid var(--divider-color); }
  .tab { flex: 1; padding: 12px; background: none; border: 0; border-bottom: 3px solid transparent;
         color: var(--secondary-text-color); font: inherit; cursor: pointer; }
  .tab.on { color: var(--primary-color); border-bottom-color: var(--primary-color); font-weight: 600; }
  .pad { padding: 16px; display: flex; flex-direction: column; gap: 10px; }
  .row { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
  .between { justify-content: space-between; }
  .btns > .btn { flex: 1; }
  .muted { color: var(--secondary-text-color); }
  .small { font-size: 0.85em; }
  .lbl { margin-top: 8px; font-size: 0.8em; text-transform: uppercase; letter-spacing: .05em; color: var(--secondary-text-color); }
  .btn { padding: 10px 12px; border-radius: 10px; border: 1px solid var(--divider-color); background: var(--card-background-color);
         color: var(--primary-text-color); font: inherit; cursor: pointer; }
  .btn:disabled { opacity: .5; cursor: default; }
  .btn.primary { background: var(--primary-color); color: var(--text-primary-color, #fff); border-color: var(--primary-color); }
  .btn.danger { color: var(--error-color); }
  .btn.armed { background: var(--error-color); color: #fff; border-color: var(--error-color); font-weight: 600; }
  .btn.big { padding: 18px; font-size: 1.25em; font-weight: 600; }
  .btn.small { padding: 4px 8px; font-size: 0.85em; }
  select, textarea, input { font: inherit; color: var(--primary-text-color); background: var(--card-background-color);
         border: 1px solid var(--divider-color); border-radius: 8px; padding: 8px; box-sizing: border-box; width: 100%; }
  textarea { font-family: var(--code-font-family, monospace); font-size: 0.85em; }
  .bar { height: 6px; background: var(--divider-color); border-radius: 3px; overflow: hidden; }
  .bar > div { height: 100%; background: var(--primary-color); transition: width .3s; }
  .current { padding: 12px 16px; border-radius: 12px; background: var(--secondary-background-color); text-align: center;
             height: 200px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: center;
             gap: 2px; overflow: hidden; }
  .current .ex { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.2; }
  .current .muted, .current .sug, .current .note, .current .ptype {
             white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex-shrink: 0; }
  .status { height: 40px; display: flex; gap: 8px; }
  .status .timer { flex: 1; display: flex; align-items: center; justify-content: center; gap: 6px; padding: 0 12px;
             white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .controls { display: flex; flex-direction: column; gap: 10px; }
  .adj-row.ghost { visibility: hidden; height: 48px; }
  .ex { font-size: 1.6em; font-weight: 700; }
  .tgt.big { font-size: 1.3em; margin: 4px 0; }
  .sug { font-size: 0.85em; color: var(--success-color, #2e7d32); }
  .note { margin-top: 6px; font-style: italic; color: var(--secondary-text-color); }
  .timer { padding: 8px 12px; border-radius: 10px; text-align: center; font-weight: 600; }
  .timer.rest { background: rgba(33,150,243,.15); }
  .timer.cap { background: rgba(255,152,0,.18); }
  .timer.q { background: rgba(156,39,176,.15); font-weight: 400; }
  .iv { margin-top: 6px; padding: 6px; border-radius: 10px; font-weight: 700; font-size: 1.1em; flex-shrink: 0; }
  .iv.work { background: rgba(244,67,54,.2); }
  .iv.rest { background: rgba(76,175,80,.2); }
  .badge { font-size: 0.75em; padding: 2px 8px; border-radius: 10px; white-space: nowrap; background: var(--divider-color); }
  .badge.ok { background: rgba(76,175,80,.2); }
  .badge.info { background: rgba(33,150,243,.2); }
  .badge.warn { background: rgba(255,152,0,.25); }
  .badge.muted { opacity: .6; }
  table { width: 100%; border-collapse: collapse; }
  .sets td, .ex-table td, .ex-table th { padding: 6px 4px; border-bottom: 1px solid var(--divider-color); vertical-align: top; text-align: left; }
  .ex-table th { font-size: .8em; color: var(--secondary-text-color); font-weight: 500; }
  .sets tr[data-a] { cursor: pointer; }
  .sets tr[data-a]:hover { background: var(--secondary-background-color); }
  .sets .val { font-weight: 600; white-space: nowrap; }
  .edit label { flex: 1; display: flex; flex-direction: column; font-size: .8em; color: var(--secondary-text-color); }
  .ename { font-weight: 600; margin-bottom: 6px; }
  .list { list-style: none; padding: 0; margin: 0; }
  .list li, .preview li { display: flex; justify-content: space-between; align-items: center; gap: 8px; padding: 4px 0; flex-wrap: wrap; }
  .preview { display: flex; flex-direction: column; gap: 6px; }
  .preview ul { list-style: none; padding: 0 0 0 8px; margin: 4px 0 0; }
  .preview .sug { width: 100%; }
  .t-warmup { --accent: #ff9800; }
  .t-circuit { --accent: var(--primary-color); }
  .t-sets { --accent: #9c6ade; }
  .t-interval { --accent: #ef5350; }
  .t-flow { --accent: #5c6bc0; }
  .iv.flow.work { background: color-mix(in srgb, #5c6bc0 18%, transparent); }
  .t-cooldown { --accent: #26a69a; }
  .pblock { border-left: 4px solid var(--accent, var(--divider-color)); border-radius: 10px; padding: 8px 12px;
            background: color-mix(in srgb, var(--accent, transparent) 9%, transparent); }
  .phead { display: flex; gap: 8px; align-items: baseline; flex-wrap: wrap; }
  .ptype { font-size: .75em; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; color: var(--accent); }
  .pblock .ptype { font-size: .8em; }
  .pname { font-weight: 600; }
  .pmeta { font-size: .85em; color: var(--secondary-text-color); margin-top: 2px; }
  .pnote { font-size: .85em; font-style: italic; color: var(--secondary-text-color); margin-top: 2px; }
  .pbreak { text-align: center; font-size: .8em; color: var(--secondary-text-color); }
  .current.t-warmup, .current.t-circuit, .current.t-sets, .current.t-interval, .current.t-flow, .current.t-cooldown {
    border-left: 6px solid var(--accent); background: color-mix(in srgb, var(--accent) 10%, var(--secondary-background-color)); }
  .current .ptype { margin-bottom: 4px; }
  .pad.live { container-type: inline-size; }
  /* Laufendes Training: auf dem Handy untereinander, ab 760 px zwei Spalten (Übung + Bedienung | Als Nächstes + Danach) */
  .stage { display: flex; flex-direction: column; gap: 10px; }
  .cur-chart { display: none; justify-content: center; gap: 12px; margin-top: 4px; flex-shrink: 0; }
  .current .ex, .current .tgt, .current .tg { flex-shrink: 0; }
  .tg { display: flex; justify-content: center; align-items: flex-start; gap: 14px; margin: 4px 0 2px; }
  .tg-v { display: flex; flex-direction: column; align-items: center; min-width: 56px; line-height: 1; }
  .tg-v b { font-size: 2.2em; font-weight: 700; font-variant-numeric: tabular-nums; }
  .tg-v span { font-size: .8em; color: var(--secondary-text-color); margin-top: 3px; }
  .tg-v em { font-style: normal; font-size: .72em; color: var(--secondary-text-color); margin-top: 2px; opacity: .8; }
  .tg-x { font-size: 1.4em; color: var(--secondary-text-color); padding-top: 6px; }
  .chip { align-self: center; font-size: .75em; padding: 2px 8px; border-radius: 10px; background: var(--divider-color);
          color: var(--secondary-text-color); flex-shrink: 0; }
  .cur-chart .chart { margin-top: 0; }
  .cur-chart .chart-lbl { text-align: center; }
  /* „Als Nächstes“: schmal untereinander auf dem Handy, rechte Spalte auf Tablet/Desktop */
  .upnext { height: 64px; box-sizing: border-box; border-radius: 12px; padding: 8px 12px; opacity: .6;
            border: 1px dashed var(--divider-color); display: grid; grid-template-columns: auto 1fr auto;
            grid-template-areas: "lbl lbl lbl" "img name tgt"; column-gap: 10px; align-items: center; overflow: hidden; }
  .un-lbl { grid-area: lbl; font-size: .7em; text-transform: uppercase; letter-spacing: .06em; color: var(--secondary-text-color); }
  .un-img { grid-area: img; width: 32px; height: 32px; border-radius: 6px; overflow: hidden; position: relative; background: #fff; }
  .un-img .pic { width: 100%; height: 100%; object-fit: cover; }
  .un-name { grid-area: name; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .un-tgt { grid-area: tgt; color: var(--secondary-text-color); white-space: nowrap; }
  .un-pos { display: none; }
  @container (min-width: 760px) {
    .stage { display: grid; grid-template-columns: 2fr 1fr; column-gap: 12px; row-gap: 10px;
             grid-template-rows: auto auto auto 1fr;
             grid-template-areas: "cur nxt" "st upc" "ctl upc" ". upc"; }
    .stage > .current { grid-area: cur; } .stage > .upnext { grid-area: nxt; } .stage > .status { grid-area: st; }
    .stage > .controls { grid-area: ctl; }
    .stage > .upc { grid-area: upc; align-self: start; } .stage > .upc .lbl { margin-top: 0; }
    .current, .upnext { height: 260px; }
    .cur-chart { display: flex; }
    .upnext { display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;
              gap: 4px; padding: 12px; }
    .un-img { width: 100%; height: 120px; border-radius: 10px; }
    .un-name { font-size: 1.25em; white-space: normal; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
    .un-pos { display: block; color: var(--secondary-text-color); font-size: .85em; }
    .ex { font-size: 1.9em; }
    .tg-v b { font-size: 2.8em; }
  }
  @container (min-width: 760px) {
    /* gleiche Spaltenaufteilung wie Übung | Als Nächstes */
    .live .controls .adj { flex-direction: row; gap: 24px; }
    .live .controls .adj-row { flex: 1; grid-template-columns: auto 52px minmax(70px, 1fr) 52px; gap: 6px; }
  }
  .subtabs { display: inline-flex; align-self: flex-start; gap: 4px; padding: 4px; border-radius: 12px;
             background: var(--secondary-background-color); }
  .subtab { border: 0; background: none; color: var(--secondary-text-color); font: inherit; padding: 8px 16px;
            border-radius: 9px; cursor: pointer; }
  .subtab.on { background: var(--card-background-color); color: var(--primary-text-color); font-weight: 600;
               box-shadow: 0 1px 3px rgba(0,0,0,.25); }
  .subtab .cnt { font-size: .8em; color: var(--secondary-text-color); margin-left: 4px; }
  .subtab ha-icon { --mdc-icon-size: 18px; margin-right: 2px; }

  /* Schmale Ansicht (Handy oder schmale Spalte): Reiter auf ganzer Breite, Symbol über dem Text */
  :host { container-type: inline-size; }
  .subtabs { max-width: 100%; }
  @container (max-width: 560px) {
    .subtabs { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(0, 1fr); align-self: stretch; }
    .subtab { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3px;
              padding: 7px 4px; font-size: .78em; line-height: 1.15; text-align: center; min-width: 0;
              hyphens: auto; }
    .subtab ha-icon { margin: 0; --mdc-icon-size: 20px; }
    .subtab .cnt { display: none; }
  }
  .empty { padding: 24px; text-align: center; color: var(--secondary-text-color); display: flex; flex-direction: column;
           gap: 12px; align-items: center; }
  .tpls summary { cursor: pointer; }
  .dl .grow { flex: 1; }
  a.btn { text-decoration: none; display: inline-flex; align-items: center; }
  .tgroup { margin-top: 16px; }
  .tghead { display: flex; gap: 12px; align-items: center; padding: 10px 12px; border-radius: 12px;
            background: var(--secondary-background-color); margin-bottom: 4px; }
  .tghead ha-icon { --mdc-icon-size: 28px; color: var(--primary-color); flex: none; }
  .tgname { font-size: 1.15em; font-weight: 700; }
  .tgname .cnt { font-size: .7em; font-weight: 500; color: var(--secondary-text-color); margin-left: 4px; }
  .tgabout { font-size: .85em; color: var(--secondary-text-color); }
  .tpl { padding-left: 12px; padding-right: 4px; }
  .tpl { display: flex; gap: 12px; align-items: center; justify-content: space-between; padding: 8px 0;
         border-bottom: 1px solid var(--divider-color); }
  .tpl-txt { min-width: 0; }
  .tpl .btn { flex: none; }
  .startrow { display: grid; grid-template-columns: 1fr 1.4fr 1fr; gap: 10px; align-items: end; }
  .startrow .sel { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
  .startrow .sel .lbl { margin: 0; }
  /* Programm/Workout-Auswahl: etwas kleiner, damit lange Namen hineinpassen */
  .startrow .sel select { font-size: .88em; padding-top: 8px; padding-bottom: 8px; text-overflow: ellipsis; }
  @container (max-width: 560px) { .startrow .sel select { font-size: .8em; } }
  @container (max-width: 560px) { .startrow { grid-template-columns: 1fr 1fr; } .startrow .btn { grid-column: 1 / -1; } }
  .startrow .btn { padding: 12px; font-size: 1.1em; font-weight: 600; }
  .exn { display: flex; align-items: center; gap: 10px; min-width: 0; }
  .thumb { width: 40px; height: 40px; flex: none; border-radius: 8px; object-fit: cover; background: var(--secondary-background-color); }
  .thumb.lg { width: 48px; height: 48px; }
  .thumb.noimg { background: transparent; }
  img.broken { visibility: hidden; }
  .current.has-img { flex-direction: row; align-items: stretch; gap: 14px; padding: 10px; }
  .cur-txt { flex: 1; min-width: 0; display: flex; flex-direction: column; justify-content: center; gap: 2px; }
  .cur-img { position: relative; width: 38%; flex: none; border-radius: 10px; overflow: hidden; background: #fff; }
  .cur-img .pic { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
  .cur-img .pic.alt { animation: ta-swap 4s infinite; }
  @keyframes ta-swap { 0%, 45% { opacity: 0; } 50%, 95% { opacity: 1; } 100% { opacity: 0; } }
  @media (prefers-reduced-motion: reduce) { .cur-img .pic.alt { animation: none; opacity: 0; } }
  .adj { display: flex; flex-direction: column; gap: 6px; }
  .adj-row { display: grid; grid-template-columns: 1fr 56px 110px 56px; align-items: center; gap: 8px; }
  .adj-lbl { color: var(--secondary-text-color); }
  .adj-val { text-align: center; font-size: 1.5em; font-weight: 700; }
  .adj-val small { font-size: .55em; font-weight: 400; color: var(--secondary-text-color); }
  .adj-val.chg { color: var(--warning-color, #ff9800); }
  .btn.round { height: 48px; font-size: 1.5em; padding: 0; border-radius: 12px; }
  .tgt { color: var(--secondary-text-color); }
  .plan, .sess { border: 1px solid var(--divider-color); border-radius: 12px; padding: 10px; }
  .click { cursor: pointer; }
  .msg { padding: 8px 12px; border-radius: 8px; white-space: pre-wrap; font-size: .9em; }
  .msg.ok { background: rgba(76,175,80,.15); }
  .msg.err { background: rgba(244,67,54,.15); }
  .msg.warnmsg { background: rgba(255,152,0,.12); color: var(--secondary-text-color); }
  .up { color: var(--success-color, #2e7d32); }
  .chart { margin-top: 6px; }
  .chart svg { display: block; }
  .chart rect { fill: var(--secondary-background-color); stroke: var(--divider-color); }
  .chart .grid line { stroke: var(--divider-color); stroke-dasharray: 3 3; }
  .chart polyline { fill: none; stroke: var(--primary-color); stroke-width: 2; stroke-linejoin: round; }
  .chart circle { fill: var(--card-background-color); stroke: var(--primary-color); stroke-width: 1.5; }
  .chart circle.last { fill: var(--primary-color); }
  .chart-lbl { font-size: .75em; color: var(--secondary-text-color); margin-top: 2px; }
  .chart-lbl.up { color: var(--success-color, #2e7d32); }
  /* Wochenansicht: Zielring + Balken */
  .week { display: flex; gap: 18px; align-items: center; border-radius: 16px; padding: 14px 16px;
          background: var(--secondary-background-color); }
  .wr { position: relative; width: 112px; height: 112px; flex: none; }
  .wr-svg { width: 100%; height: 100%; transform: rotate(-90deg); }
  .wr-svg circle { fill: none; stroke: var(--divider-color); stroke-width: 9; stroke-linecap: butt; }
  .wr-svg circle.on { stroke: var(--primary-color); }
  .wr-c { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; line-height: 1; }
  .wr-c b { font-size: 2.1em; font-weight: 700; }
  .wr-c span { font-size: 1.1em; color: var(--secondary-text-color); margin-left: 1px; }
  .wr-extra { position: absolute; bottom: 22px; font-size: .75em !important; color: var(--primary-color) !important; }
  .wk-main { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 6px; }
  .wk-top { display: flex; align-items: center; gap: 8px; }
  .wk-title { font-weight: 600; }
  .wk-goal { margin-left: auto; display: flex; align-items: center; gap: 6px; }
  .wk-cap { font-size: .75em; color: var(--secondary-text-color); margin-bottom: -4px; }
  .wk-bars { display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; align-items: end; }
  .wb { display: flex; flex-direction: column; align-items: center; gap: 3px; min-width: 0; }
  .wb-n { font-size: .7em; color: var(--secondary-text-color); height: 1.1em; }
  .wb-col { width: 100%; max-width: 30px; height: 56px; display: flex; flex-direction: column; justify-content: flex-end;
            align-items: center; }
  .wb-col > div { width: 100%; border-radius: 6px 6px 3px 3px;
                  background: linear-gradient(to top, var(--primary-color), color-mix(in srgb, var(--primary-color) 55%, transparent)); }
  .wb-col > i { width: 6px; height: 6px; border-radius: 50%; background: var(--divider-color); margin-bottom: 2px; }
  .wb.future .wb-col > i { opacity: .4; }
  .wb-d { font-size: .8em; color: var(--secondary-text-color); width: 22px; height: 22px; display: flex; align-items: center;
          justify-content: center; border-radius: 50%; }
  .wb.today .wb-d { background: var(--primary-color); color: var(--text-primary-color, #fff); font-weight: 700; }
  .wk-sub { font-size: .85em; color: var(--secondary-text-color); }
  .wk-tags { display: flex; flex-wrap: wrap; gap: 4px; }
  .wk-tags span { font-size: .75em; padding: 2px 8px; border-radius: 10px; background: var(--card-background-color);
                  border: 1px solid var(--divider-color); color: var(--secondary-text-color); }
  @container (max-width: 480px) { .week { flex-direction: column; align-items: stretch; } .wr { align-self: center; } }
  .tbtn { border: 1px solid var(--divider-color); background: var(--card-background-color); color: var(--primary-text-color);
          border-radius: 8px; min-width: 32px; height: 28px; font: inherit; cursor: pointer; }
  /* Kacheln, Rekorde, Volumen, Erholung */
  .tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
  @container (max-width: 560px) { .tiles { grid-template-columns: 1fr 1fr; } }
  .tile { border: 1px solid var(--divider-color); border-radius: 12px; padding: 10px; }
  .tile-l { font-size: .8em; color: var(--secondary-text-color); }
  .tile-v { font-size: 1.7em; font-weight: 700; }
  .tile-v small { font-size: .55em; color: var(--secondary-text-color); font-weight: 500; }
  .tile-s { font-size: .8em; color: var(--secondary-text-color); }
  .vol { display: flex; flex-direction: column; gap: 6px; }
  .vb { display: grid; grid-template-columns: 110px 1fr 120px; gap: 8px; align-items: center; }
  .vb-bar { position: relative; height: 12px; border-radius: 6px; background: var(--secondary-background-color); }
  .vb-bar > div { height: 100%; border-radius: 6px; background: var(--primary-color); }
  .vb-bar > i { position: absolute; top: -3px; bottom: -3px; width: 2px; background: var(--ta-gold); }
  .rc { display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 6px; }
  .rc-i { border-radius: 10px; padding: 6px 10px; display: flex; flex-direction: column; border-left: 4px solid var(--rc);
          background: color-mix(in srgb, var(--rc) 12%, transparent); }
  .rc-i span { font-size: .85em; } .rc-i small { color: var(--secondary-text-color); }
  .mtags { display: flex; justify-content: center; flex-wrap: wrap; gap: 4px; flex-shrink: 0; margin: 2px 0; }
  .mt { font-size: .72em; padding: 1px 8px; border-radius: 10px; border: 1px solid var(--rc);
        background: color-mix(in srgb, var(--rc) 22%, transparent); color: var(--primary-text-color); }
  .mt.sec { opacity: .6; border-style: dashed; font-size: .66em; }
  /* Handy: Übungskasten etwas höher, Etiketten einzeilig nur mit Hauptmuskeln – der Hinweis bleibt sichtbar */
  @container (max-width: 759px) {
    .current { height: 220px; }
    .mtags { flex-wrap: nowrap; overflow: hidden; }
    .mt { white-space: nowrap; }
    .mt.sec { display: none; }
  }
  .rc-fresh { --rc: #ef5350; } .rc-recovering { --rc: #fbc02d; } .rc-ready { --rc: #4caf50; }
  .rc-soon { --rc: #9ccc65; } .rc-overdue { --rc: #ab47bc; } .rc-none { --rc: var(--divider-color); }
  /* Anstrengung, Personen, Pause ±15, Rekord */
  .chip-btn { border: 1px solid var(--divider-color); background: var(--card-background-color); color: var(--primary-text-color);
              border-radius: 16px; padding: 6px 12px; font: inherit; cursor: pointer; }
  .chip-btn.on { background: var(--primary-color); border-color: var(--primary-color); color: var(--text-primary-color, #fff); }
  .chip-btn.ef-easy.on { background: #4caf50; border-color: #4caf50; }
  .chip-btn.ef-hard.on { background: #ef5350; border-color: #ef5350; }
  .chip-btn:disabled { opacity: .4; cursor: default; }
  .effort-row { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; min-height: 36px; }
  .effort-row > span { flex: 1; min-width: 140px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .effort-row.ghost { visibility: hidden; }
  .ef-dot { font-size: .75em; padding: 1px 6px; border-radius: 8px; background: var(--divider-color); }
  .ef-dot.ef-easy { background: rgba(76,175,80,.25); } .ef-dot.ef-hard { background: rgba(239,83,80,.25); }
  .who { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
  .who .lbl { margin: 0 6px 0 0; }
  .pp-form input { flex: 1; min-width: 160px; width: auto; }
  .pp-link { display: flex; align-items: center; gap: 8px; margin-top: 6px; }
  .pp-link select { width: auto; max-width: 220px; padding: 4px 8px; }
  .timer .grow { flex: 1; text-align: center; }
  .timer.rec { background: color-mix(in srgb, var(--ta-gold) 25%, transparent); }
  /* Zustandsanzeige – bewusst kein Knopf: nur leicht getönt, Farbkante links, farbiger Text mit Punkt */
  .timer.st { --st: var(--divider-color); background: color-mix(in srgb, var(--st) 13%, transparent);
              border-left: 5px solid var(--st); border-radius: 6px; color: var(--st); cursor: default;
              text-transform: uppercase; letter-spacing: .08em; font-size: .9em; user-select: none; }
  .timer.st > .grow, .timer.st:not(.st-rest) { gap: 8px; }
  .timer.st:not(.st-rest)::before, .timer.st-rest > .grow::before { content: ""; width: 9px; height: 9px; border-radius: 50%;
              background: var(--st); display: inline-block; margin-right: 8px; vertical-align: middle; }
  .timer.st:not(.st-rest)::before { margin-right: 0; }
  .elapsed { display: flex; flex-direction: column; align-items: flex-end; gap: 2px; font-variant-numeric: tabular-nums;
             white-space: nowrap; line-height: 1; }
  .el-time { font-size: 1.9em; font-weight: 700; }
  .el-ref { font-size: .8em; color: var(--secondary-text-color); }
  .el-bar { width: 100%; min-width: 110px; height: 4px; border-radius: 2px; background: var(--divider-color); overflow: hidden; }
  .el-bar i { display: block; height: 100%; width: 0; background: var(--primary-color); transition: width 1s linear; }
  .el-bar i.over { background: #fbc02d; }
  .timer.st-wait { --st: #ef5350; }
  .timer.st-rest { --st: #fbc02d; }
  .timer.st-go { --st: #66bb6a; }
  .timer.st-paused { --st: var(--secondary-text-color); }
  .timer.st-wait::before, .timer.st-go::before { animation: ta-pulse 1.4s ease-in-out infinite; }
  @keyframes ta-pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: .35; transform: scale(.7); } }
  @media (prefers-reduced-motion: reduce) { .timer.st::before { animation: none !important; } }
  .timer.st-rest .tbtn { text-transform: none; letter-spacing: 0; }
  .trophy { font-size: .95em; }
  :host { --ta-gold: #e8b44f; }
  /* HIIT/Flow in der Statusleiste: Countdown etwas größer */
  .timer.st-iv .st-time { font-size: 1.35em; margin-left: 4px; font-variant-numeric: tabular-nums; letter-spacing: 0; }
  /* Laufendes Intervall/Flow: Phase und Runde klein, Countdown groß */
  .iv { display: flex; flex-direction: column; align-items: center; gap: 0; line-height: 1.15; }
  .iv-lbl { font-size: .8em; letter-spacing: .03em; }
  .iv-time { font-size: 1.7em; font-variant-numeric: tabular-nums; }
  @container (max-width: 560px) {
    .current.t-interval, .current.t-flow { height: auto; min-height: 132px; }
    .current.t-interval .ex, .current.t-flow .ex { font-size: 1.2em; }
    .iv-time { font-size: 1.5em; }
  }
  /* Satz bearbeiten (laufendes Training und Verlauf) */
  tr.editing > td { padding: 8px 0 12px; }
  .edit-panel { display: flex; flex-direction: column; gap: 12px; padding: 14px; border-radius: 12px; max-width: 480px;
                background: var(--secondary-background-color); border: 1px solid var(--divider-color); }
  .edit-panel .ename { margin: 0; font-size: 1.05em; }
  .edit-fields { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .edit-fields label { display: flex; flex-direction: column; gap: 4px; font-size: .8em; color: var(--secondary-text-color); }
  .edit-fields input { font-size: 1.25em; padding: 10px 12px; border-radius: 10px; width: 100%; box-sizing: border-box; }
  .edit-lbl { font-size: .8em; color: var(--secondary-text-color); margin-bottom: -6px; }
  .edit-effort { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
  .edit-effort .chip-btn { padding: 10px 4px; text-align: center; }
  .edit-panel .edit-save { width: 100%; padding: 13px; font-weight: 600; }
  .edit-sec { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: -4px; }
  .edit-sec .btn { padding: 10px 6px; }
  /* Übungsverlauf auf schmalen Bildschirmen: eine Karte pro Übung statt vier Spalten */
  @container (max-width: 560px) {
    .ex-table, .ex-table tbody, .ex-table tr, .ex-table td { display: block; width: 100%; box-sizing: border-box; }
    .ex-table tr:first-child { display: none; }
    .ex-table tr { padding: 12px 0; border-bottom: 1px solid var(--divider-color); }
    .ex-table td { border: 0; padding: 4px 0; }
    .ex-table td[data-label]::before { content: attr(data-label); display: block; margin-bottom: 2px; font-size: .7em;
                                       text-transform: uppercase; letter-spacing: .05em; color: var(--secondary-text-color); }
    .ex-table td[data-label]:empty { display: none; }
    .ex-table .chart svg { width: 100%; height: auto; }
  }
  /* „Wie war's?“-Dialog nach einem Satz */
  .efp { position: fixed; left: 50%; bottom: calc(16px + env(safe-area-inset-bottom)); transform: translateX(-50%);
         width: min(440px, calc(100vw - 24px)); z-index: 20; box-sizing: border-box; padding: 12px 14px 0;
         background: var(--card-background-color); color: var(--primary-text-color); border: 1px solid var(--divider-color);
         border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,.45); overflow: hidden; animation: efp-in .18s ease-out; }
  .efp-head { display: flex; flex-direction: column; gap: 2px; margin-bottom: 10px; }
  .efp-head b { font-size: 1.05em; }
  .efp-btns { display: flex; gap: 8px; margin-bottom: 12px; }
  .efp-btns .chip-btn { flex: 1; padding: 11px 6px; font-size: 1em; text-align: center; }
  .efp-bar { height: 4px; margin: 0 -14px; background: var(--divider-color); }
  .efp-bar i { display: block; height: 100%; background: var(--primary-color); transform-origin: left center;
               animation-name: efp-shrink; animation-timing-function: linear; animation-fill-mode: forwards; }
  @keyframes efp-shrink { from { transform: scaleX(1); } to { transform: scaleX(0); } }
  @keyframes efp-in { from { opacity: 0; transform: translate(-50%, 12px); } }
  @media (prefers-reduced-motion: reduce) { .efp { animation: none; } }

  /* Kleine Bildschirme im Training: alles Wichtige ohne Scrollen – Übung, Pause, Plus/Minus,
     „Wie war's?“ und der große Knopf passen auf ein Handy (ab ca. 640 px Höhe). */
  @container (max-width: 560px) {
    .live { gap: 8px; }
    /* Kopfzeile: Workout-Name (gekürzt) und Uhr in einer Zeile; Phase zeigt die Statusleiste */
    .live > .row.between:first-child { flex-wrap: nowrap; }
    .live > .row.between:first-child { align-items: flex-start; }
    /* Workout-Name fett, Programm klein darunter; rechts Uhr und „letztes Mal“ – ohne zweiten Balken */
    .live > .row.between:first-child > div { min-width: 0; display: flex; flex-direction: column; }
    .live > .row.between:first-child > div > b { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .live > .row.between:first-child > div > .muted { font-size: .8em; white-space: nowrap; overflow: hidden;
                                                       text-overflow: ellipsis; }
    .el-bar { display: none; }
    .live > .row.between:first-child .sep { display: none; }
    .elapsed.over .el-ref { color: #fbc02d; font-weight: 600; }
    .live > .row.between:first-child .badge { display: none; }
    .live > .bar + .muted.small { display: none; }
    .el-time { font-size: 1.4em; }
    .current { height: 132px; }
    .current.has-img { gap: 10px; padding: 8px; }
    .cur-img { width: 32%; }
    .current .ex { font-size: 1.35em; }
    .current .sug { display: none; }
    .current .note { font-size: .8em; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .upnext { height: auto; min-height: 44px; padding: 5px 10px; row-gap: 0; }
    .un-lbl { font-size: .62em; }
    .status { height: 36px; }
    /* Plus/Minus: Wiederholungen und Gewicht nebeneinander, Beschriftung klein darüber */
    .adj { flex-direction: row; gap: 10px; min-height: 66px; }
    .adj-row { flex: 1; min-width: 0; grid-template-columns: 40px 1fr 40px; column-gap: 4px; row-gap: 2px; }
    .adj-row.ghost { height: auto; }
    .adj-lbl { grid-column: 1 / -1; font-size: .75em; text-align: center; white-space: nowrap; overflow: hidden;
               text-overflow: ellipsis; }
    .btn.round { height: 40px; font-size: 1.3em; }
    .adj-val { font-size: 1.3em; white-space: nowrap; }
    /* „Wie war's?“: drei gleich breite Knöpfe in einer Zeile, ohne Übungsnamen */
    .effort-row { flex-wrap: nowrap; gap: 4px; min-height: 34px; }
    .effort-row > span { flex: none; min-width: 0; font-size: .78em; }
    .effort-row > span b { display: none; }
    .effort-row .chip-btn { flex: 1; min-width: 0; padding: 6px 4px; text-align: center; }
    .btn.big { padding: 14px; font-size: 1.15em; }
    .controls { gap: 8px; }
    .controls .btns { gap: 6px; flex-wrap: nowrap; }
    .controls .btns > .btn[data-svc="skip"] { flex: 1.4; }
    .controls .btns > .btn { padding: 9px 4px; font-size: .84em; white-space: nowrap; min-width: 0; overflow: hidden;
                             text-overflow: ellipsis; }
  }
`;

if (!customElements.get("training-assistant-card")) {
  customElements.define("training-assistant-card", TrainingAssistantCard);
  window.customCards = window.customCards || [];
  window.customCards.push({
    type: "training-assistant-card",
    name: "TrainingAssistant",
    description: "Live workout, history and training plans",
    preview: false,
  });
  console.info(`%c TRAINING-ASSISTANT-CARD %c ${CARD_VERSION} `, "background:#03a9f4;color:#fff", "");
}
