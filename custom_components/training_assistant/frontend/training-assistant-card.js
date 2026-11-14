/* TrainingAssistant card 0.12.1 – built from the shared UI (Hero Upgrade). Do not edit by hand. */
// src/ui/texts.js
var EXTRA_I18N = {
	en: {
		p_tab_data: "Other",
		d_sound: "Beeps",
		d_sound_on: "On",
		d_sound_off: "Off",
		d_glow: "Glowing edge",
		d_glow_hint: "The screen edge glows during a workout: red while waiting for “Go”, green while you train, yellow during rests, pulsing red in the last seconds before you go, gold for a new record.",
		d_theme: "Design",
		d_theme_auto: "Automatic",
		d_theme_light: "Light",
		d_theme_dark: "Dark",
		d_theme_hint: "Automatic follows the setting of your device.",
		d_sound_hint: "Countdown beeps in the last 3 seconds of a rest or interval, a start tone when it's time to go. Turn up the volume; on iPhone the silent switch must be off.",
		d_backup: "Backup",
		d_backup_hint: "Your data is stored only in this browser on this device – there is no account and no server. Save a backup now and then, e.g. to move to a new phone. Clearing the browser data deletes everything.",
		d_export: "⟦down⟧ Save backup",
		d_import: "⟦up⟧ Restore backup",
		d_restore_c: "Replace all data?",
		d_last_backup: "Last backup: {d}",
		d_restored: "Backup restored.",
		d_saved: "Backup saved.",
		d_install: "Use as an app",
		d_install_hint: "Add Hero Upgrade to your home screen (Safari: Share → Add to Home Screen; Chrome: menu → Install app). It then opens full screen, works offline, and the browser keeps its data.",
		d_about: "About",
		d_privacy: "Hero Upgrade has no accounts, no tracking and no cookies. Your workouts never leave your device.",
		d_disclaimer: "Disclaimer",
		disc_title: "Before you start",
		disc_text: "Hero Upgrade is a free training log, not medical advice. Training is at your own risk. If you have health problems, injuries, are pregnant or have not exercised in a long time, talk to a doctor first. Stop immediately if you feel pain, dizziness or shortness of breath. Weights and suggestions are only starting points – listen to your body.",
		disc_ok: "Understood – let's go",
		upd_text: "New version available",
		upd_reload: "Reload",
		ed_preview: "Show {name}",
		rec_toast: "⟦trophy⟧ New record: {name}",
		side_left: "left side",
		side_right: "right side",
		foot: "Free training log without an account. Not medical advice – training at your own risk.",
		"err.template_not_found": "Program not found.",
		"err.plan_not_found": "Program not found.",
		"err.workout_not_found": "Workout not found.",
		"err.session_not_found": "Workout not found in the history.",
		"err.set_not_found": "Set not found.",
		"err.no_training": "No workout running.",
		"err.no_plan": "Choose a program first.",
		"err.already_running": "A workout is already running.",
		"err.no_active_set": "No set running.",
		"err.no_weight": "This exercise has no weight.",
		"err.profile_not_found": "Person not found.",
		"err.profile_busy": "Finish the workout before switching people.",
		"err.profile_name_missing": "Please enter a name.",
		"err.profile_exists": "“{profile}” already exists.",
		"err.profile_delete_active": "The selected person can't be deleted.",
		"err.figure_invalid": "Unknown figure.",
		"err.invalid_backup": "This file is not a Hero Upgrade backup.",
		"err.unknown_command": "Unknown action.",
		"p_tab_editor": "Editor",
		"p_short_mine": "Plans",
		"p_short_tpl": "Templates",
		"p_short_editor": "Editor",
		"p_short_import": "Import",
		"p_short_people": "People",
		"p_short_data": "Other",
		"ed_intro": "Build your own program or change one you have. Programs from the templates are edited as your own copy – the template stays as it is, and your history carries over because it belongs to the exercise.",
		"ed_new": "New program",
		"ed_existing": "Edit a program",
		"ed_edit": "Edit",
		"ed_edit_copy": "Edit as copy",
		"ed_tpl_badge": "Template",
		"ed_n_workouts": "{n} workouts",
		"ed_saved": "Saved: {name}. You'll find it under My plans and on the start page.",
		"ed_overview": "Overview",
		"ed_copy_badge": "Copy",
		"ed_copy_hint": "This is a copy of a template. When saved, it becomes your own program next to the template.",
		"ed_copy_name": "{name} (copy)",
		"ed_c_discard": "Discard changes?",
		"ed_c_delete": "Really delete?",
		"ed_name": "Name",
		"ed_name_ph": "e.g. My full body",
		"ed_desc": "Description",
		"ed_desc_ph": "Optional – what is it for?",
		"ed_rest_default": "Set rest (s)",
		"ed_prog": "Progression",
		"ed_inc_kg": "Step (kg)",
		"ed_inc_reps": "Step (reps)",
		"ed_p_inherit": "As program",
		"ed_p_double": "Double",
		"ed_p_linear": "Linear",
		"ed_p_reps": "More reps",
		"ed_p_none": "None",
		"ed_prog_double": "First more reps up to the top of the range, then more weight and back to the bottom. Needs a rep range (e.g. 8–12).",
		"ed_prog_linear": "If all sets succeed, next time a bit more weight (classic 5×5).",
		"ed_prog_reps": "If all sets succeed, next time one rep more – good for bodyweight exercises.",
		"ed_prog_none": "No suggestions – the values from the program stay as they are.",
		"ed_workouts": "Workouts",
		"ed_add_workout": "Workout",
		"ed_wo_name": "Workout name",
		"ed_default_wo": "Workout {n}",
		"ed_up": "Move up",
		"ed_down": "Move down",
		"ed_duplicate": "Duplicate",
		"ed_delete": "Delete",
		"ed_remove": "Remove",
		"ed_blocks": "Blocks",
		"ed_no_blocks": "No blocks yet.",
		"ed_add_block": "Add block",
		"ed_unnamed": "Unnamed",
		"ed_block_name": "Block name",
		"ed_optional": "optional",
		"ed_note": "Hint",
		"ed_duration_s": "Duration (s)",
		"ed_until_next": "until you tap Next",
		"ed_count": "Length",
		"ed_m_sets": "Number of sets",
		"ed_m_total": "Up to a total",
		"ed_sets": "Sets",
		"ed_total_reps": "Total reps",
		"ed_total": "total",
		"ed_rest_s": "Set rest (s)",
		"ed_rest_after_s": "Rest after block (s)",
		"ed_default": "default",
		"ed_tempo": "Tempo",
		"ed_m_rounds": "Rounds",
		"ed_m_cap": "Time limit",
		"ed_rounds": "Rounds",
		"ed_cap_s": "Time limit (s)",
		"ed_rest_ex_s": "Exercise rest (s)",
		"ed_rest_round_s": "Round rest (s)",
		"ed_n_rounds": "{n} rounds",
		"ed_add_exercise": "Add exercise",
		"ed_no_exercise": "No exercise yet",
		"ed_interval_hint": "Timed: work and rest alternate, exercises take turns round by round. Beeps mark every change.",
		"ed_flow_hint": "Timed sequence: every exercise has its own duration and runs on automatically.",
		"ed_work_s": "Work (s)",
		"ed_irest_s": "Rest (s)",
		"ed_transition_s": "Transition (s)",
		"ed_per_side": "Per side",
		"ed_per_side_lc": "per side",
		"ed_duration_side_s": "Duration per side (s)",
		"ed_reps_side": "Reps per side",
		"ed_side_hint_reps": "The reps count for each side: 10 means 10 left and 10 right.",
		"ed_side_hint": "Left first, then {s} s to switch, then right – the time counts for each side.",
		"ed_unilateral": "One-sided (left and right separately)",
		"ed_unilateral_tag": "one-sided",
		"ed_target": "Target",
		"ed_tm_reps": "Reps",
		"ed_tm_range": "Rep range",
		"ed_tm_max": "As many as possible",
		"ed_tm_time": "Time",
		"ed_tm_timemax": "Hold as long as possible",
		"ed_t_max": "max",
		"ed_t_timemax": "max time",
		"ed_reps": "Reps",
		"ed_min": "From",
		"ed_max": "To",
		"ed_weight": "Weight (kg)",
		"ed_bodyweight": "bodyweight",
		"ed_pick_title": "Choose exercise",
		"ed_search": "Search exercise",
		"ed_custom": "Own exercise",
		"ed_custom_hint": "Not in the list? Create it – without a picture, with the muscle groups for the weekly overview.",
		"ed_equipment": "Equipment",
		"ed_muscles": "Muscle groups (max. 3)",
		"ed_custom_add": "Use own exercise",
		"ed_save": "Save program",
		"ed_where": "{w} · block {n} ({type})",
		"ed_err_name": "Give the program a name.",
		"ed_err_wname": "Every workout needs a name.",
		"ed_err_noblocks": "{w}: add at least one block.",
		"ed_err_noex": "choose an exercise.",
		"ed_err_double": "double progression needs a rep range (e.g. 8–12) – or choose another progression.",
		"ed_err_range": "the range must go from low to high (e.g. 8–12).",
		"ed_err_ex_name": "Enter a name for the exercise.",
		"ed_err_check": "The program could not be saved:",
		"eq_bodyweight": "Bodyweight",
		"eq_dumbbell": "Dumbbell",
		"eq_kettlebell": "Kettlebell",
		"eq_barbell": "Barbell",
		"eq_band": "Band",
		"eq_machine": "Machine",
		"eq_cable": "Cable",
		"eq_other": "Other",
		"err.plan_invalid": "The program has errors.",
		"err.plan_readonly": "Templates can't be changed – edit a copy instead.",
		"err.plan_in_use": "This program is being trained right now. Save after the workout.",
		"l_all": "All",
		"l_own": "Own",
		"l_no_own": "No own programs yet – build one in the editor.",
		"l_to_editor": "Open editor",
		"l_no_hit": "Nothing found.",
		"l_search_plans": "Search my plans",
		"l_search_tpl": "Search templates",
		"ed_category": "Category",
		"ed_cat_pick": "Choose category",
		"ed_err_cat": "Choose a category for the program.",
		"ed_prog_info": "Progression types",
		"ed_prog_info_more": "Progression decides what the app suggests for the next workout. Timed sets get 5 s more once all were done (10 s if all felt easy) – switch it off for a single exercise with \"None\". \"As many as possible\" runs without suggestions. A block can use a different type than the program.",
		"sug.time_add": "All times done → +{add} s ({target} s)",
		"sug.time_easy_add": "All felt easy → +{add} s ({target} s)",
		"sug.time_repeat": "Not every set reached {target} s yet – repeat",
		"tg.other.about": "Your own programs without a matching category.",
		"err.category_missing": "Choose a category for the program.",
		"err.unknown": "Something went wrong.",
		"err.not_your_workout": "This is another person's workout – you can watch, but not control it.",
		"err.person_required": "Please choose whose workout this is.",
		"hold_ready": "Get ready",
		"hold_run": "Keep going!",
		"b_hold_now": "⟦play⟧ Start now",
		"b_hold_running": "⟦timer⟧ Running – continues by itself",
		"b_hold_end_rest": "⟦play⟧ End rest – start countdown",
		"fin_h1": "Strong work!",
		"fin_h2": "That's a wrap.",
		"fin_h3": "Another step forward.",
		"fin_h4": "Done – and done well.",
		"fin_h5": "Good work today.",
		"fin_h6": "Workout in the bag.",
		"fin_s1": "You did what you set out to do.",
		"fin_s2": "Every workout like this one adds up.",
		"fin_s3": "Your body takes it from here – rest well.",
		"fin_early_h": "That counts too.",
		"fin_early_s": "Not everything today – but you showed up, and it's saved.",
		"fin_saved": "⟦check⟧ Saved",
		"fin_duration": "Duration",
		"fin_exercises": "Exercises",
		"fin_sets": "Sets",
		"fin_reps": "Reps",
		"fin_time": "Time under tension",
		"fin_volume": "Weight moved",
		"fin_muscles": "Trained",
		"fin_records": "⟦trophy⟧ New personal bests",
		"fin_rec_weight": "{name}: {v} (before {p})",
		"fin_rec_e1rm": "{name}: estimated max {v} (before {p})",
		"fin_rec_reps": "{name}: {v} reps (before {p})",
		"fin_rec_duration": "{name}: {v} s (before {p} s)",
		"fin_better": "Better than last time",
		"fin_vs_last": "Last time ({date}): {d} · {n} sets",
		"fin_vs_volume": "Weight moved: {before} → {now}",
		"fin_next": "Next time",
		"fin_next_hint": "What the progression suggests for this workout next time:",
		"fin_week": "{n} of {g} workouts this week",
		"fin_week_done": "Weekly goal reached – {n} workouts",
		"fin_streak": "⟦streak⟧ {n} weeks in a row on target",
		"fin_streak1": "⟦streak⟧ 1 week on target",
		"fin_total": "Workout no. {n} overall",
		"fin_done": "⟦check⟧ Done",
		"hold_ready_sides": "Get ready – left side first",
		"hold_side_1": "Left side · 1/2",
		"hold_side_2": "Right side · 2/2",
		"hold_switch": "Switch sides",
		"side_now_1": "Left",
		"side_now_2": "Right",
		"side_next_2": "Next: right side",
		"b_hold_side2": "⟦play⟧ Start right side now",
		"ef_close": "Close"
	},
	de: {
		p_tab_data: "Sonstiges",
		d_sound: "Signaltöne",
		d_sound_on: "An",
		d_sound_off: "Aus",
		d_glow: "Leuchtrand",
		d_glow_hint: "Der Bildschirmrand leuchtet im Training: rot, solange es auf „Los“ wartet, grün beim Trainieren, gelb in der Pause, rot pulsierend in den letzten Sekunden vor dem Start, golden bei einem neuen Rekord.",
		d_theme: "Design",
		d_theme_auto: "Automatisch",
		d_theme_light: "Hell",
		d_theme_dark: "Dunkel",
		d_theme_hint: "Automatisch richtet sich nach der Einstellung deines Geräts.",
		d_sound_hint: "Countdown-Töne in den letzten 3 Sekunden einer Pause oder eines Intervalls, ein Startton, wenn es losgeht. Lautstärke aufdrehen; am iPhone muss der Stumm-Schalter aus sein.",
		d_backup: "Sicherung",
		d_backup_hint: "Deine Daten liegen nur in diesem Browser auf diesem Gerät – es gibt kein Konto und keinen Server. Speichere ab und zu eine Sicherung, z. B. für den Umzug auf ein neues Handy. Wer die Browserdaten löscht, löscht alles.",
		d_export: "⟦down⟧ Sicherung speichern",
		d_import: "⟦up⟧ Sicherung laden",
		d_restore_c: "Alle Daten ersetzen?",
		d_last_backup: "Letzte Sicherung: {d}",
		d_restored: "Sicherung geladen.",
		d_saved: "Sicherung gespeichert.",
		d_install: "Als App nutzen",
		d_install_hint: "Lege Hero Upgrade auf den Home-Bildschirm (Safari: Teilen → Zum Home-Bildschirm; Chrome: Menü → App installieren). Dann öffnet es im Vollbild, läuft offline, und der Browser behält die Daten.",
		d_about: "Über",
		d_privacy: "Hero Upgrade hat keine Konten, kein Tracking und keine Cookies. Deine Trainings verlassen nie dein Gerät.",
		d_disclaimer: "Haftungshinweis",
		disc_title: "Bevor du loslegst",
		disc_text: "Hero Upgrade ist ein kostenloses Trainingstagebuch, keine medizinische Beratung. Training erfolgt auf eigenes Risiko. Bei gesundheitlichen Beschwerden, Verletzungen, Schwangerschaft oder langer Trainingspause sprich vorher mit einer Ärztin oder einem Arzt. Hör sofort auf bei Schmerzen, Schwindel oder Atemnot. Gewichte und Vorschläge sind nur Ausgangswerte – hör auf deinen Körper.",
		disc_ok: "Verstanden – los geht's",
		upd_text: "Neue Version verfügbar",
		upd_reload: "Neu laden",
		ed_preview: "{name} ansehen",
		rec_toast: "⟦trophy⟧ Neuer Rekord: {name}",
		side_left: "linke Seite",
		side_right: "rechte Seite",
		foot: "Kostenloses Trainingstagebuch ohne Konto. Keine medizinische Beratung – Training auf eigenes Risiko.",
		"err.template_not_found": "Programm nicht gefunden.",
		"err.plan_not_found": "Programm nicht gefunden.",
		"err.workout_not_found": "Workout nicht gefunden.",
		"err.session_not_found": "Training nicht im Verlauf gefunden.",
		"err.set_not_found": "Satz nicht gefunden.",
		"err.no_training": "Es läuft kein Training.",
		"err.no_plan": "Wähle zuerst ein Programm.",
		"err.already_running": "Es läuft bereits ein Training.",
		"err.no_active_set": "Gerade läuft kein Satz.",
		"err.no_weight": "Diese Übung hat kein Gewicht.",
		"err.profile_not_found": "Person nicht gefunden.",
		"err.profile_busy": "Beende erst das Training, dann die Person wechseln.",
		"err.profile_name_missing": "Bitte einen Namen eingeben.",
		"err.profile_exists": "„{profile}“ gibt es schon.",
		"err.profile_delete_active": "Die ausgewählte Person kann nicht gelöscht werden.",
		"err.figure_invalid": "Unbekannte Figur.",
		"err.invalid_backup": "Diese Datei ist keine Hero-Upgrade-Sicherung.",
		"err.unknown_command": "Unbekannte Aktion.",
		"p_tab_editor": "Editor",
		"p_short_mine": "Pläne",
		"p_short_tpl": "Vorlagen",
		"p_short_editor": "Editor",
		"p_short_import": "Import",
		"p_short_people": "Personen",
		"p_short_data": "Sonstiges",
		"ed_intro": "Bau dir ein eigenes Programm oder ändere ein vorhandenes. Programme aus den Vorlagen bearbeitest du als eigene Kopie – die Vorlage bleibt, wie sie ist, und dein Verlauf geht mit, weil er an der Übung hängt.",
		"ed_new": "Neues Programm",
		"ed_existing": "Programm bearbeiten",
		"ed_edit": "Bearbeiten",
		"ed_edit_copy": "Als Kopie bearbeiten",
		"ed_tpl_badge": "Vorlage",
		"ed_n_workouts": "{n} Workouts",
		"ed_saved": "Gespeichert: {name}. Du findest es unter Meine Pläne und auf der Startseite.",
		"ed_overview": "Übersicht",
		"ed_copy_badge": "Kopie",
		"ed_copy_hint": "Das ist eine Kopie einer Vorlage. Beim Speichern wird daraus ein eigenes Programm neben der Vorlage.",
		"ed_copy_name": "{name} (Kopie)",
		"ed_c_discard": "Änderungen verwerfen?",
		"ed_c_delete": "Wirklich löschen?",
		"ed_name": "Name",
		"ed_name_ph": "z. B. Mein Ganzkörper",
		"ed_desc": "Beschreibung",
		"ed_desc_ph": "Optional – wofür ist es gedacht?",
		"ed_rest_default": "Satzpause (s)",
		"ed_prog": "Progression",
		"ed_inc_kg": "Schritt (kg)",
		"ed_inc_reps": "Schritt (Wdh.)",
		"ed_p_inherit": "Wie Programm",
		"ed_p_double": "Doppelt",
		"ed_p_linear": "Linear",
		"ed_p_reps": "Mehr Wdh.",
		"ed_p_none": "Keine",
		"ed_prog_double": "Erst mehr Wiederholungen bis zur Obergrenze, dann mehr Gewicht und wieder unten anfangen. Braucht einen Bereich (z. B. 8–12).",
		"ed_prog_linear": "Klappen alle Sätze, gibt es beim nächsten Mal etwas mehr Gewicht (klassisches 5×5).",
		"ed_prog_reps": "Klappen alle Sätze, beim nächsten Mal eine Wiederholung mehr – gut für Körpergewichtsübungen.",
		"ed_prog_none": "Keine Vorschläge – es bleibt bei den Werten aus dem Programm.",
		"ed_workouts": "Workouts",
		"ed_add_workout": "Workout",
		"ed_wo_name": "Name des Workouts",
		"ed_default_wo": "Workout {n}",
		"ed_up": "Nach oben",
		"ed_down": "Nach unten",
		"ed_duplicate": "Duplizieren",
		"ed_delete": "Löschen",
		"ed_remove": "Entfernen",
		"ed_blocks": "Blöcke",
		"ed_no_blocks": "Noch keine Blöcke.",
		"ed_add_block": "Block hinzufügen",
		"ed_unnamed": "Ohne Namen",
		"ed_block_name": "Name des Blocks",
		"ed_optional": "optional",
		"ed_note": "Hinweis",
		"ed_duration_s": "Dauer (s)",
		"ed_until_next": "bis du auf Weiter tippst",
		"ed_count": "Umfang",
		"ed_m_sets": "Anzahl Sätze",
		"ed_m_total": "Bis zu einer Summe",
		"ed_sets": "Sätze",
		"ed_total_reps": "Wdh. insgesamt",
		"ed_total": "insgesamt",
		"ed_rest_s": "Satzpause (s)",
		"ed_rest_after_s": "Pause danach (s)",
		"ed_default": "Standard",
		"ed_tempo": "Tempo",
		"ed_m_rounds": "Runden",
		"ed_m_cap": "Zeitlimit",
		"ed_rounds": "Runden",
		"ed_cap_s": "Zeitlimit (s)",
		"ed_rest_ex_s": "Übungspause (s)",
		"ed_rest_round_s": "Rundenpause (s)",
		"ed_n_rounds": "{n} Runden",
		"ed_add_exercise": "Übung hinzufügen",
		"ed_no_exercise": "Noch keine Übung",
		"ed_interval_hint": "Zeitgesteuert: Arbeit und Pause wechseln sich ab, die Übungen kommen Runde für Runde reihum. Signaltöne markieren jeden Wechsel.",
		"ed_flow_hint": "Zeitgesteuerte Abfolge: Jede Übung hat ihre eigene Dauer und es geht von selbst weiter.",
		"ed_work_s": "Arbeit (s)",
		"ed_irest_s": "Pause (s)",
		"ed_transition_s": "Übergang (s)",
		"ed_per_side": "Pro Seite",
		"ed_per_side_lc": "pro Seite",
		"ed_duration_side_s": "Dauer pro Seite (s)",
		"ed_reps_side": "Wdh. pro Seite",
		"ed_side_hint_reps": "Die Wiederholungen gelten pro Seite: 10 heißt 10 links und 10 rechts.",
		"ed_side_hint": "Erst links, dann {s} s Seitenwechsel, dann rechts – die Zeit gilt für jede Seite.",
		"ed_unilateral": "Einseitig (links und rechts getrennt)",
		"ed_unilateral_tag": "einseitig",
		"ed_target": "Ziel",
		"ed_tm_reps": "Wiederholungen",
		"ed_tm_range": "Wdh.-Bereich",
		"ed_tm_max": "So viele wie möglich",
		"ed_tm_time": "Zeit",
		"ed_tm_timemax": "So lange wie möglich halten",
		"ed_t_max": "max.",
		"ed_t_timemax": "max. Zeit",
		"ed_reps": "Wiederholungen",
		"ed_min": "Von",
		"ed_max": "Bis",
		"ed_weight": "Gewicht (kg)",
		"ed_bodyweight": "Körpergewicht",
		"ed_pick_title": "Übung wählen",
		"ed_search": "Übung suchen",
		"ed_custom": "Eigene Übung",
		"ed_custom_hint": "Nicht in der Liste? Leg sie an – ohne Bild, mit den Muskelgruppen für die Wochenübersicht.",
		"ed_equipment": "Gerät",
		"ed_muscles": "Muskelgruppen (max. 3)",
		"ed_custom_add": "Eigene Übung verwenden",
		"ed_save": "Programm speichern",
		"ed_where": "{w} · Block {n} ({type})",
		"ed_err_name": "Gib dem Programm einen Namen.",
		"ed_err_wname": "Jedes Workout braucht einen Namen.",
		"ed_err_noblocks": "{w}: Füge mindestens einen Block hinzu.",
		"ed_err_noex": "Wähle eine Übung.",
		"ed_err_double": "Doppelte Progression braucht einen Wdh.-Bereich (z. B. 8–12) – oder wähle eine andere Progression.",
		"ed_err_range": "Der Bereich muss von klein nach groß gehen (z. B. 8–12).",
		"ed_err_ex_name": "Gib der Übung einen Namen.",
		"ed_err_check": "Das Programm konnte nicht gespeichert werden:",
		"eq_bodyweight": "Körpergewicht",
		"eq_dumbbell": "Kurzhantel",
		"eq_kettlebell": "Kettlebell",
		"eq_barbell": "Langhantel",
		"eq_band": "Band",
		"eq_machine": "Gerät",
		"eq_cable": "Kabelzug",
		"eq_other": "Sonstiges",
		"err.plan_invalid": "Das Programm hat Fehler.",
		"err.plan_readonly": "Vorlagen lassen sich nicht ändern – bearbeite eine Kopie.",
		"err.plan_in_use": "Mit diesem Programm läuft gerade ein Training. Speichere nach dem Training.",
		"l_all": "Alle",
		"l_own": "Eigene",
		"l_no_own": "Noch keine eigenen Programme – bau dir eins im Editor.",
		"l_to_editor": "Zum Editor",
		"l_no_hit": "Nichts gefunden.",
		"l_search_plans": "Meine Pläne durchsuchen",
		"l_search_tpl": "Vorlagen durchsuchen",
		"ed_category": "Kategorie",
		"ed_cat_pick": "Kategorie wählen",
		"ed_err_cat": "Wähle eine Kategorie für das Programm.",
		"ed_prog_info": "Progressionsarten",
		"ed_prog_info_more": "Die Progression bestimmt, was die App fürs nächste Training vorschlägt. Sätze nach Zeit bekommen 5 s mehr, wenn alle geschafft waren (10 s, wenn alle leicht waren) – für eine einzelne Übung mit „Keine“ abschaltbar. „So viele wie möglich“ läuft ohne Vorschläge. Ein Block kann eine andere Art nutzen als das Programm.",
		"sug.time_add": "Alle Zeiten geschafft → +{add} s ({target} s)",
		"sug.time_easy_add": "Alles leicht → +{add} s ({target} s)",
		"sug.time_repeat": "{target} s noch nicht in jedem Satz geschafft – nochmal",
		"tg.other.about": "Eigene Programme ohne passende Kategorie.",
		"err.category_missing": "Wähle eine Kategorie für das Programm.",
		"err.unknown": "Da ist etwas schiefgegangen.",
		"err.not_your_workout": "Das ist das Training einer anderen Person – zuschauen ja, bedienen nein.",
		"err.person_required": "Bitte auswählen, wessen Training gemeint ist.",
		"hold_ready": "Gleich geht's los",
		"hold_run": "Durchhalten!",
		"b_hold_now": "⟦play⟧ Jetzt los",
		"b_hold_running": "⟦timer⟧ Läuft – geht von selbst weiter",
		"b_hold_end_rest": "⟦play⟧ Pause beenden – Countdown",
		"fin_h1": "Stark gemacht!",
		"fin_h2": "Das sitzt.",
		"fin_h3": "Wieder ein Schritt nach vorn.",
		"fin_h4": "Erledigt – und zwar richtig.",
		"fin_h5": "Gute Arbeit heute.",
		"fin_h6": "Training im Kasten.",
		"fin_s1": "Du hast durchgezogen, was du dir vorgenommen hast.",
		"fin_s2": "Jedes Training wie dieses zahlt ein.",
		"fin_s3": "Den Rest erledigt jetzt dein Körper – gute Erholung.",
		"fin_early_h": "Auch das zählt.",
		"fin_early_s": "Heute nicht alles – aber du warst da, und es ist gespeichert.",
		"fin_saved": "⟦check⟧ Gespeichert",
		"fin_duration": "Dauer",
		"fin_exercises": "Übungen",
		"fin_sets": "Sätze",
		"fin_reps": "Wiederholungen",
		"fin_time": "Zeit unter Spannung",
		"fin_volume": "Bewegtes Gewicht",
		"fin_muscles": "Trainiert",
		"fin_records": "⟦trophy⟧ Neue Bestwerte",
		"fin_rec_weight": "{name}: {v} (vorher {p})",
		"fin_rec_e1rm": "{name}: geschätztes Maximum {v} (vorher {p})",
		"fin_rec_reps": "{name}: {v} Wdh. (vorher {p})",
		"fin_rec_duration": "{name}: {v} s (vorher {p} s)",
		"fin_better": "Besser als letztes Mal",
		"fin_vs_last": "Letztes Mal ({date}): {d} · {n} Sätze",
		"fin_vs_volume": "Bewegtes Gewicht: {before} → {now}",
		"fin_next": "Nächstes Mal",
		"fin_next_hint": "Das schlägt die Progression für dieses Workout beim nächsten Mal vor:",
		"fin_week": "{n} von {g} Trainings diese Woche",
		"fin_week_done": "Wochenziel erreicht – {n} Trainings",
		"fin_streak": "⟦streak⟧ {n} Wochen am Stück im Ziel",
		"fin_streak1": "⟦streak⟧ 1 Woche im Ziel",
		"fin_total": "Training Nr. {n} insgesamt",
		"fin_done": "⟦check⟧ Fertig",
		"hold_ready_sides": "Gleich geht's los – erst links",
		"hold_side_1": "Linke Seite · 1/2",
		"hold_side_2": "Rechte Seite · 2/2",
		"hold_switch": "Seite wechseln",
		"side_now_1": "Links",
		"side_now_2": "Rechts",
		"side_next_2": "Gleich: rechte Seite",
		"b_hold_side2": "⟦play⟧ Rechte Seite jetzt starten",
		"ef_close": "Schließen"
	}
};
// src/ui/editor.js
var BLOCK_TYPES = [
	"warmup",
	"sets",
	"circuit",
	"interval",
	"flow",
	"cooldown"
];
var EQUIPMENT = [
	"bodyweight",
	"dumbbell",
	"kettlebell",
	"barbell",
	"band",
	"machine",
	"cable",
	"other"
];
var MUSCLES = [
	"chest",
	"back",
	"shoulders",
	"biceps",
	"triceps",
	"core",
	"quads",
	"hamstrings",
	"glutes",
	"calves"
];
var PROGRESSIONS = [
	"double",
	"linear",
	"reps",
	"none"
];
var NEEDS_EXERCISES = {
	sets: 1,
	circuit: 1,
	interval: 1,
	flow: 1
};
function slugify(text) {
	let s = String(text || "").toLowerCase();
	for (const [a, b] of [
		["ä", "ae"],
		["ö", "oe"],
		["ü", "ue"],
		["ß", "ss"]
	]) s = s.split(a).join(b);
	s = s.replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
	return /^[a-z]/.test(s) ? s : `x_${s || "item"}`;
}
var clone = (o) => JSON.parse(JSON.stringify(o));
function createEditor(helpers) {
	return new Editor(helpers);
}
var Editor = class {
	constructor(h) {
		this.h = h;
		this.ed = null;
		this.lib = null;
		this.groups = null;
		this.progInfo = false;
		this.open = null;
		this.adding = false;
		this.pick = null;
		this.custom = null;
		this.errors = null;
		this.saved = null;
		this.scroll = false;
	}
	get active() {
		return !!this.ed;
	}
	render(state) {
		const { t, esc } = this.h;
		if (!this.ed) return this.renderStart(state);
		if (this.pick) return `<div class="ed">${this.renderPicker()}</div>`;
		const plan = this.ed.plan;
		const wo = plan.workouts[this.ed.wi];
		const prog = plan.defaults && plan.defaults.progression || { type: "none" };
		const chips = plan.workouts.map((w, i) => `<button class="chip-btn ${i === this.ed.wi ? "on" : ""}" data-a="ed-wo" data-i="${i}">${esc(w.name || t("ed_unnamed"))}</button>`).join("");
		const blocks = wo.blocks.map((b, bi) => this.renderBlock(b, bi, wo.blocks.length)).join("");
		const addRow = this.adding ? `<div class="lbl">${t("ed_add_block")}</div><div class="ed-add">${BLOCK_TYPES.map((ty) => `<button class="btn small t-${ty} ed-addb" data-a="ed-add-b" data-type="${ty}">${esc(t(`ty_${ty}`))}</button>`).join("")}
          <button class="btn small" data-a="ed-add-cancel">${t("e_cancel")}</button></div>` : `<button class="btn" data-a="ed-add">⟦plus⟧ ${t("ed_add_block")}</button>`;
		const errors = this.errors ? `<div class="msg err">${esc(this.errors)}</div>` : "";
		return `<div class="ed">
      <div class="row between"><button class="btn small" data-a="ed-close" ${this.ed.dirty ? `data-ck="ed-close" data-confirm="${esc(t("ed_c_discard"))}"` : ""}>⟦back⟧ ${t("ed_overview")}</button>
        ${this.ed.fromTemplate ? `<span class="badge info">${t("ed_copy_badge")}</span>` : ""}</div>
      ${this.ed.fromTemplate ? `<div class="muted small">${t("ed_copy_hint")}</div>` : ""}
      <div class="ed-sec">
        ${this.field(t("ed_name"), `<input data-ef="name" value="${esc(plan.name)}" placeholder="${esc(t("ed_name_ph"))}">`)}
        ${this.field(t("ed_category"), this.categorySelect())}
        ${this.field(t("ed_desc"), `<textarea data-ef="description" rows="2" placeholder="${esc(t("ed_desc_ph"))}">${esc(plan.description || "")}</textarea>`)}
        <div class="ed-grid">
          ${this.field(t("ed_rest_default"), this.secInput("defaults.rest_s", plan.defaults && plan.defaults.rest_s, 90))}
          ${this.field(this.progLabel(), this.progSelect("defaults", prog.type, false))}
          ${prog.type !== "none" ? this.field(prog.type === "reps" ? t("ed_inc_reps") : t("ed_inc_kg"), this.incInput("defaults.progression", prog)) : ""}
        </div>
        ${this.progInfo ? this.progInfoBox() : `<div class="muted small">${t(`ed_prog_${prog.type}`)}</div>`}
      </div>
      <div class="lbl">${t("ed_workouts")}</div>
      <div class="row ed-chips">${chips}<button class="chip-btn" data-a="ed-wo-add">⟦plus⟧ ${t("ed_add_workout")}</button></div>
      <div class="ed-sec">
        ${this.field(t("ed_wo_name"), `<input data-ef="W.name" value="${esc(wo.name)}">`)}
        <div class="row ed-tools">
          <button class="btn small" data-a="ed-wo-move" data-d="-1" ${this.ed.wi === 0 ? "disabled" : ""} aria-label="${esc(t("ed_up"))}">⟦chev_up⟧</button>
          <button class="btn small" data-a="ed-wo-move" data-d="1" ${this.ed.wi === plan.workouts.length - 1 ? "disabled" : ""} aria-label="${esc(t("ed_down"))}">⟦chev_down⟧</button>
          <button class="btn small" data-a="ed-wo-copy">⟦copy⟧ ${t("ed_duplicate")}</button>
          ${plan.workouts.length > 1 ? `<button class="btn small danger" data-a="ed-wo-del" data-ck="ed-wo-${this.ed.wi}" data-confirm="${esc(t("ed_c_delete"))}">⟦trash⟧ ${t("ed_delete")}</button>` : ""}
        </div>
      </div>
      <div class="lbl">${t("ed_blocks")}</div>
      <div class="ed-blocks">${blocks || `<div class="muted small">${t("ed_no_blocks")}</div>`}</div>
      ${addRow}
      ${errors}
      <div class="ed-save">
        <button class="btn primary" data-a="ed-save">⟦check⟧ ${t("ed_save")}</button>
      </div>
    </div>`;
	}
	renderStart(state) {
		const { t, esc } = this.h;
		const plans = (state.plans || []).map((p) => `<div class="plan row between"><div><b>${esc(p.name)}</b>
          ${p.template ? ` <span class="badge">${t("ed_tpl_badge")}</span>` : ""}
          <div class="muted small">${esc(t("ed_n_workouts", { n: p.workouts.length }))}</div></div>
          <button class="btn small" data-a="ed-open" data-plan="${esc(p.id)}">${p.template ? `⟦copy⟧ ${t("ed_edit_copy")}` : `⟦editor⟧ ${t("ed_edit")}`}</button></div>`).join("");
		return `<div class="ed">${this.saved ? `<div class="msg ok">${esc(t("ed_saved", { name: this.saved }))}</div>` : ""}
      <div class="muted small">${t("ed_intro")}</div>
      <div class="row"><button class="btn primary" data-a="ed-new">⟦plus⟧ ${t("ed_new")}</button></div>
      ${plans ? `<div class="lbl">${t("ed_existing")}</div>${plans}` : ""}
    </div>`;
	}
	field(label, control, cls = "") {
		return `<label class="fld ${cls}"><span>${label}</span>${control}</label>`;
	}
	secInput(path, value, placeholder) {
		return `<input data-ef="${path}" data-k="int" inputmode="numeric" value="${value ?? ""}" placeholder="${placeholder ?? ""}">`;
	}
	numInput(path, value, kind = "int", placeholder = "") {
		const v = value === void 0 || value === null ? "" : String(value).replace(".", this.h.lang() === "de" ? "," : ".");
		return `<input data-ef="${path}" data-k="${kind}" inputmode="${kind === "num" ? "decimal" : "numeric"}" value="${this.h.esc(v)}" placeholder="${placeholder}">`;
	}
	incInput(path, prog) {
		return prog.type === "reps" ? this.numInput(`${path}.increment`, prog.increment ?? 1) : this.numInput(`${path}.increment_kg`, prog.increment_kg ?? 2.5, "num");
	}
	/** Beschriftung „Progression“ mit Info-Knopf (klappt die Erklärung aller Arten auf) */
	progLabel() {
		const { t, esc } = this.h;
		return `<span class="fld-lbl">${t("ed_prog")}<button type="button" class="info-btn ${this.progInfo ? "on" : ""}" data-a="ed-prog-info"
      aria-label="${esc(t("ed_prog_info"))}" aria-expanded="${this.progInfo}">⟦help⟧</button></span>`;
	}
	progInfoBox() {
		const { t } = this.h;
		return `<div class="info-box"><b>${t("ed_prog_info")}</b>
      ${PROGRESSIONS.map((p) => `<div><b>${t(`ed_p_${p}`)}</b> – ${t(`ed_prog_${p}`)}</div>`).join("")}
      <div class="muted">${t("ed_prog_info_more")}</div></div>`;
	}
	categorySelect() {
		const { t } = this.h;
		const cur = this.ed.category;
		const opts = (this.groups || []).map((g) => `<option value="${g}" ${g === cur ? "selected" : ""}>${t(`tg.${g}`)}</option>`).join("");
		return `<select data-ecat class="${cur ? "" : "unset"}"><option value="" ${cur ? "" : "selected"} disabled>${t("ed_cat_pick")}</option>${opts}</select>`;
	}
	progSelect(path, value, inherit) {
		const { t } = this.h;
		return `<select data-ep="${path}">${[...inherit ? ["inherit"] : [], ...PROGRESSIONS].map((p) => `<option value="${p}" ${p === value ? "selected" : ""}>${t(`ed_p_${p}`)}</option>`).join("")}</select>`;
	}
	exName(id) {
		const ex = this.ed.plan.exercises[id];
		return ex ? ex.name : id ? id : this.h.t("ed_no_exercise");
	}
	exImage(id) {
		const ex = this.ed.plan.exercises[id];
		if (!ex || ex.image === false) return null;
		const known = (this.lib || []).find((e) => e.id === id);
		return known ? known.image : null;
	}
	/** Pro Seite? Eintrag `per_side`, sonst Markierung `unilateral` der Übung (wie plan.ts `perSide`) */
	perSide(o) {
		if (typeof o.per_side === "boolean") return o.per_side;
		const ex = this.ed.plan.exercises[o.exercise];
		return !!(ex && ex.unilateral);
	}
	targetText(o) {
		const { t } = this.h;
		if (o.duration_s !== void 0) {
			const d = o.duration_s;
			const time = d === "max" ? t("ed_t_timemax") : d && typeof d === "object" ? `${d.min}–${d.max} s` : this.h.dur(d);
			return this.perSide(o) ? `${time} ${t("ed_per_side_lc")}` : time;
		}
		const side = this.perSide(o) ? ` ${t("ed_per_side_lc")}` : "";
		if (o.reps === "max") return t("ed_t_max") + side;
		if (o.reps && typeof o.reps === "object") return `${o.reps.min}–${o.reps.max}${side}`;
		return o.reps !== void 0 ? String(o.reps) + side : "";
	}
	summary(b) {
		const { t, dur } = this.h;
		const names = (list) => list.map((x) => this.exName(typeof x === "string" ? x : x.exercise)).join(", ");
		switch (b.type) {
			case "warmup":
			case "cooldown": return b.duration_s ? dur(b.duration_s) : t("ed_until_next");
			case "sets": {
				const count = b.sets ? `${b.sets} × ` : `${t("ed_total")} ${b.total_reps} · `;
				const w = b.weight_kg ? ` · ${String(b.weight_kg).replace(".", this.h.lang() === "de" ? "," : ".")} kg` : "";
				return `${this.exName(b.exercise)} · ${count}${this.targetText(b)}${w}`;
			}
			case "circuit": return `${b.rounds ? t("ed_n_rounds", { n: b.rounds }) : dur(b.time_cap_s || 0)} · ${names(b.exercises || []) || t("ed_no_exercise")}`;
			case "interval": return `${b.rounds} × ${b.work_s}/${b.rest_s} s · ${names(b.exercises || []) || t("ed_no_exercise")}`;
			case "flow": {
				const segs = (b.exercises || []).reduce((a, x) => a + (this.perSide(x) ? 2 : 1), 0) * (b.rounds || 1);
				return `${dur((b.exercises || []).reduce((a, x) => a + (x.duration_s || 0) * (this.perSide(x) ? 2 : 1), 0) * (b.rounds || 1) + Math.max(0, segs - 1) * (b.rest_s || 0))} · ${names(b.exercises || []) || t("ed_no_exercise")}`;
			}
			default: return "";
		}
	}
	renderBlock(b, bi, count) {
		const { t, esc } = this.h;
		const isOpen = this.open === bi;
		const head = `<div class="eb-head click" data-a="ed-toggle" data-i="${bi}">
        <div class="eb-txt"><span class="ptype">${esc(t(`ty_${b.type}`))}</span>${b.name ? ` <b>${esc(b.name)}</b>` : ""}
          <div class="pmeta">${esc(this.summary(b))}</div></div>
        <span class="eb-chev">${isOpen ? "⟦chev_up⟧" : "⟦chev_down⟧"}</span></div>`;
		if (!isOpen) return `<div class="eblock pblock t-${b.type}">${head}</div>`;
		const P = `B.${bi}`;
		let body = "";
		const nameField = this.field(t("ed_block_name"), `<input data-ef="${P}.name" value="${esc(b.name || "")}" placeholder="${esc(t("ed_optional"))}">`);
		const noteField = this.field(t("ed_note"), `<textarea data-ef="${P}.note" rows="2" placeholder="${esc(t("ed_optional"))}">${esc(b.note || "")}</textarea>`);
		if (b.type === "warmup" || b.type === "cooldown") body = `<div class="ed-grid">${nameField}${this.field(t("ed_duration_s"), this.numInput(`${P}.duration_s`, b.duration_s, "int", t("ed_until_next")))}</div>${noteField}`;
		else if (b.type === "sets") {
			const prog = b.progression ? b.progression.type : "inherit";
			body = `${this.exRow(b.exercise, `${P}`, null)}
        <div class="ed-grid">
          ${this.field(t("ed_count"), `<select data-esm="${P}"><option value="sets" ${b.sets ? "selected" : ""}>${t("ed_m_sets")}</option><option value="total" ${b.sets ? "" : "selected"}>${t("ed_m_total")}</option></select>`)}
          ${b.sets ? this.field(t("ed_sets"), this.numInput(`${P}.sets`, b.sets)) : this.field(t("ed_total_reps"), this.numInput(`${P}.total_reps`, b.total_reps))}
        </div>
        ${this.targetFields(b, P)}
        <div class="ed-grid">
          ${this.field(t("ed_rest_s"), this.numInput(`${P}.rest_s`, b.rest_s, "int", t("ed_default")))}
          ${this.field(t("ed_rest_after_s"), this.numInput(`${P}.rest_after_s`, b.rest_after_s, "int", t("ed_default")))}
          ${this.field(this.progLabel(), this.progSelect(P, prog, true))}
          ${b.progression && b.progression.type !== "none" ? this.field(b.progression.type === "reps" ? t("ed_inc_reps") : t("ed_inc_kg"), this.incInput(`${P}.progression`, b.progression)) : ""}
        </div>
        ${this.progInfo ? this.progInfoBox() : ""}
        <div class="ed-grid">${nameField}${this.field(t("ed_tempo"), `<input data-ef="${P}.tempo" value="${esc(b.tempo || "")}" placeholder="3-0-1">`)}</div>
        ${noteField}`;
		} else if (b.type === "circuit") body = `<div class="ed-items">${(b.exercises || []).map((it, ii) => `<div class="ed-item">${this.exRow(it.exercise, `${P}.exercises.${ii}`, {
			ii,
			n: b.exercises.length
		})}
          ${this.targetFields(it, `${P}.exercises.${ii}`)}</div>`).join("")}</div>
        <button class="btn small" data-a="ed-pick-open" data-target="${P}.exercises">⟦plus⟧ ${t("ed_add_exercise")}</button>
        <div class="ed-grid">
          ${this.field(t("ed_count"), `<select data-ecm="${P}"><option value="rounds" ${b.time_cap_s ? "" : "selected"}>${t("ed_m_rounds")}</option><option value="cap" ${b.time_cap_s ? "selected" : ""}>${t("ed_m_cap")}</option></select>`)}
          ${b.time_cap_s ? this.field(t("ed_cap_s"), this.numInput(`${P}.time_cap_s`, b.time_cap_s)) : this.field(t("ed_rounds"), this.numInput(`${P}.rounds`, b.rounds))}
          ${this.field(t("ed_rest_ex_s"), this.numInput(`${P}.rest_after_exercise_s`, b.rest_after_exercise_s, "int", "0"))}
          ${this.field(t("ed_rest_round_s"), this.numInput(`${P}.rest_after_round_s`, b.rest_after_round_s, "int", t("ed_default")))}
          ${this.field(t("ed_rest_after_s"), this.numInput(`${P}.rest_after_s`, b.rest_after_s, "int", t("ed_default")))}
        </div>
        ${nameField}${noteField}`;
		else if (b.type === "interval") {
			const items = (b.exercises || []).map((id, ii) => `<div class="ed-item">${this.exRow(id, `${P}.exercises.${ii}`, {
				ii,
				n: b.exercises.length
			})}</div>`).join("");
			body = `<div class="muted small">${t("ed_interval_hint")}</div>
        <div class="ed-items">${items}</div>
        <button class="btn small" data-a="ed-pick-open" data-target="${P}.exercises">⟦plus⟧ ${t("ed_add_exercise")}</button>
        <div class="ed-grid">
          ${this.field(t("ed_rounds"), this.numInput(`${P}.rounds`, b.rounds))}
          ${this.field(t("ed_work_s"), this.numInput(`${P}.work_s`, b.work_s))}
          ${this.field(t("ed_irest_s"), this.numInput(`${P}.rest_s`, b.rest_s))}
          ${this.field(t("ed_rest_after_s"), this.numInput(`${P}.rest_after_s`, b.rest_after_s, "int", t("ed_default")))}
        </div>
        ${nameField}${noteField}`;
		} else if (b.type === "flow") {
			const items = (b.exercises || []).map((it, ii) => `<div class="ed-item">${this.exRow(it.exercise, `${P}.exercises.${ii}`, {
				ii,
				n: b.exercises.length
			})}
          <div class="ed-grid">${this.field(t(this.perSide(it) ? "ed_duration_side_s" : "ed_duration_s"), this.numInput(`${P}.exercises.${ii}.duration_s`, it.duration_s))}
          ${this.check(`${P}.exercises.${ii}.per_side`, this.perSide(it), t("ed_per_side"))}</div></div>`).join("");
			body = `<div class="muted small">${t("ed_flow_hint")}</div>
        <div class="ed-items">${items}</div>
        <button class="btn small" data-a="ed-pick-open" data-target="${P}.exercises">⟦plus⟧ ${t("ed_add_exercise")}</button>
        <div class="ed-grid">
          ${this.field(t("ed_rounds"), this.numInput(`${P}.rounds`, b.rounds, "int", "1"))}
          ${this.field(t("ed_transition_s"), this.numInput(`${P}.rest_s`, b.rest_s, "int", "0"))}
          ${this.field(t("ed_rest_round_s"), this.numInput(`${P}.rest_after_round_s`, b.rest_after_round_s, "int", t("ed_default")))}
          ${this.field(t("ed_rest_after_s"), this.numInput(`${P}.rest_after_s`, b.rest_after_s, "int", t("ed_default")))}
        </div>
        ${nameField}${noteField}`;
		}
		return `<div class="eblock pblock t-${b.type} open">${head}
      <div class="eb-body">${body}
        <div class="row ed-tools">
          <button class="btn small" data-a="ed-b-move" data-i="${bi}" data-d="-1" ${bi === 0 ? "disabled" : ""} aria-label="${esc(t("ed_up"))}">⟦chev_up⟧</button>
          <button class="btn small" data-a="ed-b-move" data-i="${bi}" data-d="1" ${bi === count - 1 ? "disabled" : ""} aria-label="${esc(t("ed_down"))}">⟦chev_down⟧</button>
          <button class="btn small" data-a="ed-b-copy" data-i="${bi}">⟦copy⟧ ${t("ed_duplicate")}</button>
          <button class="btn small danger" data-a="ed-b-del" data-i="${bi}" data-ck="ed-b-${bi}" data-confirm="${esc(t("ed_c_delete"))}">⟦trash⟧ ${t("ed_delete")}</button>
        </div></div></div>`;
	}
	/** Bild einer Übung als eigene Schaltfläche: Tippen öffnet die Vorschau (Start/Ende im Wechsel) */
	imgButton(cid, name) {
		const { t, esc, img } = this.h;
		if (!cid) return img(null);
		return `<button class="ex-img" type="button" data-a="ed-preview" data-img="${esc(cid)}" data-name="${esc(name)}"
      aria-label="${esc(t("ed_preview", { name }))}">${img(cid)}</button>`;
	}
	/** Übungszeile: Bild, Name, Tauschen; bei Listen zusätzlich hoch/runter/entfernen */
	exRow(id, path, list) {
		const { t, esc, img } = this.h;
		const tools = list ? `<button class="btn small icon" data-a="ed-item-move" data-path="${path}" data-d="-1" ${list.ii === 0 ? "disabled" : ""} aria-label="${esc(t("ed_up"))}">⟦chev_up⟧</button>
         <button class="btn small icon" data-a="ed-item-move" data-path="${path}" data-d="1" ${list.ii === list.n - 1 ? "disabled" : ""} aria-label="${esc(t("ed_down"))}">⟦chev_down⟧</button>
         <button class="btn small icon danger" data-a="ed-item-del" data-path="${path}" aria-label="${esc(t("ed_remove"))}">⟦trash⟧</button>` : "";
		return `<div class="ed-ex">${this.imgButton(this.exImage(id), this.exName(id))}
      <button class="ed-exname click" data-a="ed-pick-open" data-target="${path}">${esc(this.exName(id))}</button>${tools}</div>`;
	}
	check(path, value, label) {
		return `<label class="fld fld-check"><input type="checkbox" data-ef="${path}" data-k="bool" ${value ? "checked" : ""}><span>${label}</span></label>`;
	}
	/** Ziel eines Satzes: Wiederholungen (fest/Bereich/max) oder Zeit, Gewicht, pro Seite */
	targetFields(o, path) {
		const { t } = this.h;
		const mode = o.duration_s !== void 0 ? o.duration_s === "max" ? "timemax" : "time" : o.reps === "max" ? "max" : o.reps && typeof o.reps === "object" ? "range" : "reps";
		const opts = [
			"reps",
			"range",
			"max",
			"time",
			"timemax"
		].map((m) => `<option value="${m}" ${m === mode ? "selected" : ""}>${t(`ed_tm_${m}`)}</option>`).join("");
		let vals = "";
		if (mode === "reps") vals = this.field(t(this.perSide(o) ? "ed_reps_side" : "ed_reps"), this.numInput(`${path}.reps`, o.reps));
		else if (mode === "range") vals = `${this.field(t("ed_min"), this.numInput(`${path}.reps.min`, o.reps.min))}${this.field(t("ed_max"), this.numInput(`${path}.reps.max`, o.reps.max))}`;
		else if (mode === "time" && o.duration_s && typeof o.duration_s === "object") vals = `${this.field(`${t(this.perSide(o) ? "ed_duration_side_s" : "ed_duration_s")} · ${t("ed_min")}`, this.numInput(`${path}.duration_s.min`, o.duration_s.min))}${this.field(t("ed_max"), this.numInput(`${path}.duration_s.max`, o.duration_s.max))}`;
		else if (mode === "time") vals = this.field(t(this.perSide(o) ? "ed_duration_side_s" : "ed_duration_s"), this.numInput(`${path}.duration_s`, o.duration_s));
		return `<div class="ed-grid">
      ${this.field(t("ed_target"), `<select data-et="${path}">${opts}</select>`)}
      ${vals}
      ${this.field(t("ed_weight"), this.numInput(`${path}.weight_kg`, o.weight_kg, "num", t("ed_bodyweight")))}
      ${this.check(`${path}.per_side`, this.perSide(o), t("ed_per_side"))}
    </div>${!this.perSide(o) ? "" : o.duration_s !== void 0 ? `<div class="muted small">${t("ed_side_hint", { s: this.h.sideSwitchS })}</div>` : `<div class="muted small">${t("ed_side_hint_reps")}</div>`}`;
	}
	renderPicker() {
		const { t, esc, img } = this.h;
		if (!this.lib) return `<div class="muted">${t("loading")}</div>`;
		const c = this.custom || {
			name: "",
			equipment: "bodyweight",
			muscles: []
		};
		const items = this.lib.map((e) => {
			const q = [
				e.name,
				...e.aliases || [],
				e.id.replace(/_/g, " ")
			].join(" ").toLowerCase();
			const meta = [
				e.equipment ? t(`eq_${e.equipment}`) : "",
				e.unilateral ? t("ed_unilateral_tag") : "",
				...(e.muscles || []).map((m) => t(`mg.${m}`))
			].filter(Boolean).join(" · ");
			return `<div class="exitem" data-q="${esc(q)}">${this.imgButton(e.image, e.name)}
          <button class="exitem-pick" type="button" data-a="ed-pick" data-ex="${esc(e.id)}"><b>${esc(e.name)}</b><span class="muted small">${esc(meta)}</span></button></div>`;
		}).join("");
		const eq = EQUIPMENT.map((x) => `<option value="${x}" ${x === c.equipment ? "selected" : ""}>${t(`eq_${x}`)}</option>`).join("");
		const mus = MUSCLES.map((m) => `<button class="chip-btn ${c.muscles.includes(m) ? "on" : ""}" data-a="ed-cm" data-m="${m}">${t(`mg.${m}`)}</button>`).join("");
		return `<div class="row between"><b>${t("ed_pick_title")}</b><button class="btn small" data-a="ed-pick-cancel">${t("e_cancel")}</button></div>
      <label class="ed-search">⟦search⟧<input data-ed-search placeholder="${esc(t("ed_search"))}" autocomplete="off"></label>
      <div class="exlist">${items}</div>
      <div class="lbl">${t("ed_custom")}</div>
      <div class="muted small">${t("ed_custom_hint")}</div>
      <div class="ed-grid">
        ${this.field(t("ed_name"), `<input data-ec="name" value="${esc(c.name)}">`)}
        ${this.field(t("ed_equipment"), `<select data-ec="equipment">${eq}</select>`)}
      </div>
      <label class="fld fld-check"><input type="checkbox" data-ec="unilateral" ${c.unilateral ? "checked" : ""}><span>${t("ed_unilateral")}</span></label>
      <div class="lbl">${t("ed_muscles")}</div>
      <div class="row">${mus}</div>
      <div class="row"><button class="btn primary" data-a="ed-pick-custom">⟦plus⟧ ${t("ed_custom_add")}</button></div>`;
	}
	/** "B.2.exercises.1.reps" → [Elternobjekt, Schlüssel] im Entwurf (W = aktuelles Workout, B = seine Blöcke) */
	resolve(path) {
		const parts = path.split(".");
		let obj = this.ed.plan;
		const first = parts[0];
		if (first === "W" || first === "B") {
			obj = this.ed.plan.workouts[this.ed.wi];
			if (first === "B") obj = obj.blocks;
			parts.shift();
		}
		for (let i = 0; i < parts.length - 1; i++) {
			const k = parts[i];
			if (obj[k] === void 0 || obj[k] === null || typeof obj[k] !== "object") obj[k] = {};
			obj = obj[k];
		}
		return [obj, parts[parts.length - 1]];
	}
	get(path) {
		const [o, k] = this.resolve(path);
		return o[k];
	}
	setValue(path, raw, kind) {
		const [o, k] = this.resolve(path);
		let v = raw;
		if (kind === "int") v = raw === "" ? void 0 : parseInt(raw, 10);
		else if (kind === "num") v = raw === "" ? void 0 : parseFloat(String(raw).replace(",", "."));
		else if (kind === "bool") v = raw ? true : void 0;
		else v = raw === "" ? void 0 : raw;
		if (v === void 0 || typeof v === "number" && Number.isNaN(v)) delete o[k];
		else o[k] = v;
		this.ed.dirty = true;
		this.errors = null;
	}
	/** Tippen in Felder: nur den Entwurf ändern (gezeichnet wird beim Verlassen des Felds) */
	input(el) {
		if (!this.ed) return false;
		if (el.dataset.edSearch !== void 0) {
			const q = el.value.trim().toLowerCase();
			el.closest(".ed").querySelectorAll(".exitem").forEach((b) => b.hidden = !!q && !b.dataset.q.includes(q));
			return true;
		}
		if (el.dataset.ec) {
			this.custom = this.custom || {
				name: "",
				equipment: "bodyweight",
				muscles: []
			};
			this.custom[el.dataset.ec] = el.type === "checkbox" ? el.checked : el.value;
			return true;
		}
		if (el.dataset.ef && el.type !== "checkbox") {
			this.setValue(el.dataset.ef, el.value, el.dataset.k || "text");
			return true;
		}
		return false;
	}
	/** Auswahlfelder und Häkchen: Entwurf ändern und neu zeichnen. Rückgabe true = erledigt */
	change(el) {
		if (!this.ed) return false;
		const d = el.dataset;
		if (d.ef && el.type === "checkbox") this.setValue(d.ef, el.checked, "bool");
		else if (d.ec) {
			this.custom = this.custom || {
				name: "",
				equipment: "bodyweight",
				muscles: []
			};
			this.custom[d.ec] = el.type === "checkbox" ? el.checked : el.value;
		} else if (d.ecat !== void 0) this.ed.category = el.value || null;
		else if (d.ep) this.setProgression(d.ep, el.value);
		else if (d.et) this.setTarget(d.et, el.value);
		else if (d.esm) {
			const b = this.get(d.esm);
			if (el.value === "sets") {
				delete b.total_reps;
				b.sets = 3;
				if (b.reps === "max") b.reps = 10;
			} else {
				delete b.sets;
				b.total_reps = 50;
				delete b.duration_s;
				b.reps = "max";
			}
		} else if (d.ecm) {
			const b = this.get(d.ecm);
			if (el.value === "rounds") {
				delete b.time_cap_s;
				b.rounds = 3;
			} else {
				delete b.rounds;
				b.time_cap_s = 600;
			}
		} else return d.ef !== void 0;
		this.ed.dirty = true;
		this.errors = null;
		return true;
	}
	setProgression(path, type) {
		const target = path === "defaults" ? this.ed.plan.defaults = this.ed.plan.defaults || {} : this.get(path);
		if (type === "inherit") delete target.progression;
		else if (type === "reps") target.progression = {
			type,
			increment: 1
		};
		else if (type === "none") target.progression = { type };
		else target.progression = {
			type,
			increment_kg: target.progression && target.progression.increment_kg || 2.5
		};
	}
	setTarget(path, mode) {
		const o = this.get(path);
		delete o.reps;
		delete o.duration_s;
		if (mode === "reps") o.reps = 10;
		else if (mode === "range") o.reps = {
			min: 8,
			max: 12
		};
		else if (mode === "max") o.reps = "max";
		else if (mode === "time") o.duration_s = 30;
		else o.duration_s = "max";
	}
	async click(a, d, el) {
		const { t } = this.h;
		const plan = this.ed && this.ed.plan;
		const wo = plan && plan.workouts[this.ed.wi];
		switch (a) {
			case "ed-new":
				this.begin(null, false, null, {
					schema_version: 1,
					name: "",
					exercises: {},
					defaults: {
						rest_s: 90,
						progression: {
							type: "double",
							increment_kg: 2.5
						}
					},
					workouts: [{
						id: "workout_a",
						name: t("ed_default_wo", { n: "A" }),
						blocks: [{
							type: "warmup",
							duration_s: 300
						}]
					}]
				});
				this.open = null;
				break;
			case "ed-open": {
				const src = await this.h.ws({
					type: "plan_source",
					plan_id: d.plan
				});
				const p = src.plan;
				if (src.template) p.name = t("ed_copy_name", { name: p.name });
				this.begin(src.template ? null : d.plan, src.template, src.category, p);
				break;
			}
			case "ed-close":
				this.ed = null;
				this.pick = null;
				this.errors = null;
				break;
			case "ed-wo":
				this.ed.wi = Number(d.i);
				this.open = null;
				this.adding = false;
				break;
			case "ed-wo-add": {
				const letter = String.fromCharCode(65 + plan.workouts.length);
				plan.workouts.push({
					id: this.uniqueWorkoutId(`workout_${letter.toLowerCase()}`),
					name: t("ed_default_wo", { n: letter }),
					blocks: [{
						type: "warmup",
						duration_s: 300
					}]
				});
				this.ed.wi = plan.workouts.length - 1;
				this.open = null;
				this.dirty();
				break;
			}
			case "ed-wo-copy": {
				const copy = clone(wo);
				copy.id = this.uniqueWorkoutId(`${wo.id}_2`);
				copy.name = t("ed_copy_name", { name: wo.name });
				plan.workouts.splice(this.ed.wi + 1, 0, copy);
				this.ed.wi += 1;
				this.dirty();
				break;
			}
			case "ed-wo-move": {
				const to = this.ed.wi + Number(d.d);
				if (to < 0 || to >= plan.workouts.length) break;
				[plan.workouts[this.ed.wi], plan.workouts[to]] = [plan.workouts[to], plan.workouts[this.ed.wi]];
				this.ed.wi = to;
				this.dirty();
				break;
			}
			case "ed-wo-del":
				plan.workouts.splice(this.ed.wi, 1);
				this.ed.wi = Math.max(0, this.ed.wi - 1);
				this.open = null;
				this.dirty();
				break;
			case "ed-toggle":
				this.open = this.open === Number(d.i) ? null : Number(d.i);
				break;
			case "ed-add":
				this.adding = true;
				break;
			case "ed-add-cancel":
				this.adding = false;
				break;
			case "ed-add-b": {
				const defaults = {
					warmup: {
						type: "warmup",
						duration_s: 300
					},
					cooldown: {
						type: "cooldown",
						duration_s: 300
					},
					sets: {
						type: "sets",
						exercise: null,
						sets: 3,
						reps: {
							min: 8,
							max: 12
						}
					},
					circuit: {
						type: "circuit",
						rounds: 3,
						rest_after_exercise_s: 15,
						rest_after_round_s: 90,
						exercises: []
					},
					interval: {
						type: "interval",
						rounds: 8,
						work_s: 20,
						rest_s: 10,
						exercises: []
					},
					flow: {
						type: "flow",
						rounds: 1,
						rest_s: 5,
						exercises: []
					}
				};
				const cd = wo.blocks.length && wo.blocks[wo.blocks.length - 1].type === "cooldown" && d.type !== "cooldown" ? wo.blocks.length - 1 : wo.blocks.length;
				wo.blocks.splice(cd, 0, clone(defaults[d.type]));
				this.open = cd;
				this.adding = false;
				this.dirty();
				if (NEEDS_EXERCISES[d.type]) await this.openPicker(d.type === "sets" ? `B.${cd}` : `B.${cd}.exercises`);
				break;
			}
			case "ed-b-move": {
				const i = Number(d.i), to = i + Number(d.d);
				if (to < 0 || to >= wo.blocks.length) break;
				[wo.blocks[i], wo.blocks[to]] = [wo.blocks[to], wo.blocks[i]];
				this.open = to;
				this.dirty();
				break;
			}
			case "ed-b-copy": {
				const i = Number(d.i);
				wo.blocks.splice(i + 1, 0, clone(wo.blocks[i]));
				this.open = i + 1;
				this.dirty();
				break;
			}
			case "ed-b-del":
				wo.blocks.splice(Number(d.i), 1);
				this.open = null;
				this.dirty();
				break;
			case "ed-item-move": {
				const parts = d.path.split(".");
				const ii = Number(parts.pop());
				const list = this.get(parts.join("."));
				const to = ii + Number(d.d);
				if (to < 0 || to >= list.length) break;
				[list[ii], list[to]] = [list[to], list[ii]];
				this.dirty();
				break;
			}
			case "ed-item-del": {
				const parts = d.path.split(".");
				const ii = Number(parts.pop());
				this.get(parts.join(".")).splice(ii, 1);
				this.dirty();
				break;
			}
			case "ed-pick-open":
				await this.openPicker(d.target);
				break;
			case "ed-preview":
				this.h.preview(d.img, d.name, el);
				return false;
			case "ed-pick-cancel":
				this.pick = null;
				this.scroll = "block";
				break;
			case "ed-pick": {
				const e = this.lib.find((x) => x.id === d.ex);
				if (!e) break;
				if (!plan.exercises[e.id]) {
					const def = { name: e.name };
					if (e.aliases && e.aliases.length) def.aliases = e.aliases;
					if (e.equipment) def.equipment = e.equipment;
					if (e.note) def.note = e.note;
					if (e.unilateral) def.unilateral = true;
					if (e.catalog) def.image = e.catalog;
					if (!e.catalog || e.explicit_muscles) def.muscles = e.muscles || [];
					plan.exercises[e.id] = def;
				}
				this.applyPick(e.id);
				break;
			}
			case "ed-cm": {
				const c = this.custom = this.custom || {
					name: "",
					equipment: "bodyweight",
					muscles: []
				};
				c.muscles = c.muscles.includes(d.m) ? c.muscles.filter((m) => m !== d.m) : [...c.muscles, d.m];
				break;
			}
			case "ed-pick-custom": {
				const c = this.custom || {
					name: "",
					equipment: "bodyweight",
					muscles: []
				};
				const name = (c.name || "").trim();
				if (!name) {
					this.h.toast(t("ed_err_ex_name"));
					break;
				}
				let id = slugify(name);
				const taken = (x) => plan.exercises[x] || (this.lib || []).some((e) => e.id === x);
				if (taken(id) && !(plan.exercises[id] && plan.exercises[id].name === name)) {
					let n = 2;
					while (taken(`${id}_${n}`)) n++;
					id = `${id}_${n}`;
				}
				plan.exercises[id] = plan.exercises[id] || {
					name,
					equipment: c.equipment,
					muscles: c.muscles.slice(0, 3),
					...c.unilateral ? { unilateral: true } : {}
				};
				this.custom = null;
				this.applyPick(id);
				break;
			}
			case "ed-prog-info":
				this.progInfo = !this.progInfo;
				break;
			case "ed-save":
				await this.save();
				break;
			default: return false;
		}
		return true;
	}
	begin(planId, fromTemplate, category, plan) {
		plan.exercises = plan.exercises || {};
		plan.workouts = plan.workouts && plan.workouts.length ? plan.workouts : [{
			id: "workout_a",
			name: "A",
			blocks: []
		}];
		this.ed = {
			planId,
			fromTemplate,
			category,
			plan,
			wi: 0,
			dirty: fromTemplate || !planId
		};
		this.open = null;
		this.adding = false;
		this.pick = null;
		this.errors = null;
		this.saved = null;
		this.scroll = true;
		if (!this.lib) this.loadLibrary();
	}
	async loadLibrary() {
		try {
			const res = await this.h.ws({ type: "exercise_library" });
			this.lib = res.exercises;
			this.groups = res.groups;
		} catch (_) {
			this.lib = [];
		}
		this.h.render();
	}
	async openPicker(target) {
		this.pick = { target };
		this.custom = null;
		this.scroll = true;
		if (!this.lib) await this.loadLibrary();
	}
	/** Gewählte Übung an der Zielstelle eintragen */
	applyPick(id) {
		const parts = this.pick.target.split(".");
		const blockIdx = Number(parts[1]);
		const block = this.ed.plan.workouts[this.ed.wi].blocks[blockIdx];
		if (parts.length === 2) block.exercise = id;
		else if (parts.length === 3) {
			if (block.type === "interval") block.exercises.push(id);
			else if (block.type === "flow") block.exercises.push({
				exercise: id,
				duration_s: 30
			});
			else {
				const prog = this.ed.plan.defaults && this.ed.plan.defaults.progression;
				block.exercises.push({
					exercise: id,
					reps: prog && prog.type === "double" ? {
						min: 8,
						max: 12
					} : 10
				});
			}
		} else {
			const ii = Number(parts[3]);
			if (block.type === "interval") block.exercises[ii] = id;
			else block.exercises[ii].exercise = id;
		}
		this.pick = null;
		this.open = blockIdx;
		this.scroll = "block";
		this.dirty();
	}
	dirty() {
		this.ed.dirty = true;
		this.errors = null;
	}
	uniqueWorkoutId(base) {
		const ids = new Set(this.ed.plan.workouts.map((w) => w.id));
		let id = slugify(base), n = 2;
		while (ids.has(id)) id = `${slugify(base)}_${n++}`;
		return id;
	}
	/** Häufige Fehler verständlich melden, bevor der Trainer streng prüft */
	friendlyErrors(plan) {
		const { t } = this.h;
		const out = [];
		if (!(plan.name || "").trim()) out.push(t("ed_err_name"));
		if (!this.ed.category) out.push(t("ed_err_cat"));
		const defProg = plan.defaults && plan.defaults.progression;
		plan.workouts.forEach((w) => {
			const wn = w.name || t("ed_unnamed");
			if (!(w.name || "").trim()) out.push(t("ed_err_wname"));
			if (!w.blocks.length) out.push(t("ed_err_noblocks", { w: wn }));
			w.blocks.forEach((b, bi) => {
				const where = t("ed_where", {
					w: wn,
					n: bi + 1,
					type: t(`ty_${b.type}`)
				});
				if (b.type === "sets" && !b.exercise) out.push(`${where}: ${t("ed_err_noex")}`);
				if ([
					"circuit",
					"interval",
					"flow"
				].includes(b.type) && !(b.exercises || []).length) out.push(`${where}: ${t("ed_err_noex")}`);
				const items = b.type === "sets" ? [b] : b.type === "circuit" ? b.exercises || [] : [];
				for (const it of items) {
					const prog = it.progression || (b.type === "sets" ? b.progression : null) || defProg;
					if (prog && prog.type === "double" && typeof it.reps === "number") {
						out.push(`${where}: ${t("ed_err_double")}`);
						break;
					}
					if (it.reps && typeof it.reps === "object" && !(it.reps.min >= 1 && it.reps.max >= it.reps.min)) {
						out.push(`${where}: ${t("ed_err_range")}`);
						break;
					}
				}
			});
		});
		return out;
	}
	/** Entwurf aufräumen: leere Texte weg, unbenutzte Übungen weg */
	cleaned() {
		const plan = clone(this.ed.plan);
		plan.schema_version = 1;
		plan.name = (plan.name || "").trim();
		if (!(plan.description || "").trim()) delete plan.description;
		const used = /* @__PURE__ */ new Set();
		for (const w of plan.workouts) {
			w.name = (w.name || "").trim();
			for (const b of w.blocks) {
				for (const k of [
					"name",
					"note",
					"tempo"
				]) if (typeof b[k] === "string" && !b[k].trim()) delete b[k];
				if (b.exercise) used.add(b.exercise);
				for (const it of b.exercises || []) used.add(typeof it === "string" ? it : it.exercise);
			}
		}
		for (const id of Object.keys(plan.exercises)) if (!used.has(id)) delete plan.exercises[id];
		return plan;
	}
	async save() {
		const plan = this.cleaned();
		const friendly = this.friendlyErrors(plan);
		if (friendly.length) {
			this.errors = friendly.join("\n");
			return;
		}
		try {
			const res = await this.h.ws({
				type: "save_plan",
				plan,
				plan_id: this.ed.planId,
				category: this.ed.category
			});
			this.saved = res.name;
			this.ed = null;
			this.scroll = true;
		} catch (err) {
			this.errors = err && err.params && err.params.errors ? `${this.h.t("ed_err_check")}\n${err.params.errors}` : null;
		}
	}
};
// src/ui/preview.js
var FRAME_MS = 800;
var TAG = "hero-exercise-preview";
var STYLE$1 = `
  :host { position: fixed; inset: 0; z-index: 100; display: flex; align-items: center; justify-content: center;
    padding: calc(16px + env(safe-area-inset-top)) 16px calc(16px + env(safe-area-inset-bottom));
    background: rgba(0, 0, 0, .6); animation: fade .15s ease-out; }
  @keyframes fade { from { opacity: 0; } }
  .box { position: relative; width: min(92vw, 440px); background: #fff; border-radius: 16px; overflow: hidden;
    box-shadow: 0 12px 40px rgba(0, 0, 0, .35); }
  .stage { position: relative; width: 100%; aspect-ratio: 1 / 1; background: #fff; }
  .stage img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; object-position: center;
    opacity: 0; }
  .stage img.on { opacity: 1; }
  .title { margin: 0; padding: 10px 52px 12px 16px; font: 600 1rem/1.3 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    color: #141414; border-top: 1px solid #e6e8e6; }
  .x { position: absolute; top: 8px; right: 8px; width: 40px; height: 40px; border: 0; border-radius: 50%;
    background: rgba(20, 20, 20, .08); color: #141414; font-size: 22px; line-height: 1; cursor: pointer; }
  .x:hover, .x:focus-visible { background: rgba(20, 20, 20, .16); outline: none; }
`;
var ExercisePreview = class extends HTMLElement {
	constructor() {
		super();
		this.attachShadow({ mode: "open" });
		this._onKey = (e) => {
			if (e.key === "Escape") this.close();
		};
	}
	/** Inhalt setzen und Wechsel starten */
	show({ urls, title = "", closeLabel = "Close" }) {
		const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({
			"&": "&amp;",
			"<": "&lt;",
			">": "&gt;",
			"\"": "&quot;",
			"'": "&#39;"
		})[c]);
		this.setAttribute("role", "dialog");
		this.setAttribute("aria-modal", "true");
		this.setAttribute("aria-label", title);
		this.shadowRoot.innerHTML = `<style>${STYLE$1}</style>
      <div class="box">
        <div class="stage">${urls.map((u, i) => `<img src="${esc(u)}" alt="${i ? "" : esc(title)}" class="${i ? "" : "on"}">`).join("")}</div>
        ${title ? `<p class="title">${esc(title)}</p>` : ""}
        <button class="x" type="button" aria-label="${esc(closeLabel)}">✕</button>
      </div>`;
		this.shadowRoot.querySelector(".x").addEventListener("click", () => this.close());
		this.addEventListener("click", (e) => {
			if (e.composedPath()[0] === this) this.close();
		});
		document.addEventListener("keydown", this._onKey);
		clearInterval(this._loop);
		const imgs = [...this.shadowRoot.querySelectorAll(".stage img")];
		if (imgs.length > 1) {
			let i = 0;
			this._loop = setInterval(() => {
				imgs[i].classList.remove("on");
				i = (i + 1) % imgs.length;
				imgs[i].classList.add("on");
			}, FRAME_MS);
		}
		this.shadowRoot.querySelector(".x").focus();
	}
	close() {
		clearInterval(this._loop);
		document.removeEventListener("keydown", this._onKey);
		this.remove();
		if (this._returnFocus && this._returnFocus.focus) this._returnFocus.focus();
	}
};
if (!customElements.get(TAG)) customElements.define(TAG, ExercisePreview);
/** Vorschau öffnen (eine offene Vorschau wird ersetzt). urls: 1 oder 2 Bildadressen. */
function openExercisePreview({ urls, title, closeLabel, returnFocus } = {}) {
	if (!urls || !urls.length) return null;
	document.querySelectorAll(TAG).forEach((el) => el.close());
	const el = document.createElement(TAG);
	el._returnFocus = returnFocus || null;
	document.body.append(el);
	el.show({
		urls,
		title,
		closeLabel
	});
	return el;
}
// src/ui/confetti.js
var COLORS = [
	"#25cc1d",
	"#1fa818",
	"#fbc02d",
	"#ff9a2e",
	"#4fc3f7",
	"#ffffff"
];
function celebrate(pieces = 70) {
	if (typeof window === "undefined" || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
	const box = document.createElement("div");
	box.setAttribute("aria-hidden", "true");
	box.style.cssText = "position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:90";
	const style = document.createElement("style");
	style.textContent = `@keyframes hero-confetti { to { transform: translate3d(var(--dx), 105vh, 0) rotate(var(--r)); opacity: .9; } }`;
	box.append(style);
	for (let i = 0; i < pieces; i++) {
		const p = document.createElement("i");
		const size = 6 + Math.random() * 6;
		p.style.cssText = `position:absolute;top:-16px;left:${Math.random() * 100}%;width:${size}px;height:${size * .45}px;background:${COLORS[i % COLORS.length]};border-radius:2px;opacity:1;--dx:${(Math.random() - .5) * 160}px;--r:${(Math.random() - .5) * 900}deg;animation:hero-confetti ${1.4 + Math.random() * 1.1}s cubic-bezier(.2,.6,.4,1) ${Math.random() * .35}s forwards`;
		box.append(p);
	}
	document.body.append(box);
	setTimeout(() => box.remove(), 3200);
}
// src/ui/icons.js
var P = {
	play: "<path d=\"M7 4v16l13 -8z\"/>",
	pause: "<path d=\"M6 5m0 1a1 1 0 0 1 1 -1h2a1 1 0 0 1 1 1v12a1 1 0 0 1 -1 1h-2a1 1 0 0 1 -1 -1z\"/><path d=\"M14 5m0 1a1 1 0 0 1 1 -1h2a1 1 0 0 1 1 1v12a1 1 0 0 1 -1 1h-2a1 1 0 0 1 -1 -1z\"/>",
	check: "<path d=\"M5 12l5 5l10 -10\"/>",
	x: "<path d=\"M18 6l-12 12\"/><path d=\"M6 6l12 12\"/>",
	undo: "<path d=\"M9 14l-4 -4l4 -4\"/><path d=\"M5 10h11a4 4 0 1 1 0 8h-1\"/>",
	skip: "<path d=\"M3 5v14l8 -7z\"/><path d=\"M14 5v14l8 -7z\"/>",
	flag: "<path d=\"M5 5a5 5 0 0 1 7 0a5 5 0 0 0 7 0v9a5 5 0 0 1 -7 0a5 5 0 0 0 -7 0v-9z\"/><path d=\"M5 21v-7\"/>",
	down: "<path d=\"M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2\"/><path d=\"M7 11l5 5l5 -5\"/><path d=\"M12 4l0 12\"/>",
	up: "<path d=\"M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2\"/><path d=\"M7 9l5 -5l5 5\"/><path d=\"M12 4l0 12\"/>",
	timer: "<path d=\"M5 13a7 7 0 1 0 14 0a7 7 0 0 0 -14 0z\"/><path d=\"M14.5 10.5l-2.5 2.5\"/><path d=\"M17 8l1 -1\"/><path d=\"M14 3h-4\"/>",
	trophy: "<path d=\"M8 21l8 0\"/><path d=\"M12 17l0 4\"/><path d=\"M7 4l10 0\"/><path d=\"M17 4v8a5 5 0 0 1 -10 0v-8\"/><path d=\"M5 9m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0\"/><path d=\"M19 9m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0\"/>",
	streak: "<circle cx=\"12\" cy=\"12\" r=\"9\"/><path d=\"M9.2 16.5L12 8l2.8 8.5\"/>",
	help: "<path d=\"M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0\"/><path d=\"M12 16v.01\"/><path d=\"M12 13a2 2 0 0 0 .914 -3.782a1.98 1.98 0 0 0 -2.414 .483\"/>",
	hero: "<circle cx=\"12\" cy=\"12\" r=\"9\"/><path d=\"M9.2 16.5L12 8l2.8 8.5\"/>",
	start: "<path d=\"M15 12l-4 -4v8z\"/><path d=\"M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0\"/>",
	rest: "<path d=\"M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0\"/><path d=\"M12 7v5l3 3\"/>",
	chart: "<path d=\"M3 13a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v6a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z\"/><path d=\"M15 9a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v10a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z\"/><path d=\"M9 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v14a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z\"/><path d=\"M4 20h14\"/>",
	week: "<path d=\"M11.5 21h-5.5a2 2 0 0 1 -2 -2v-12a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v6\"/><path d=\"M16 3v4\"/><path d=\"M8 3v4\"/><path d=\"M4 11h16\"/><path d=\"M15 19l2 2l4 -4\"/>",
	phone: "<path d=\"M6 5a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2v-14z\"/><path d=\"M11 4h2\"/><path d=\"M12 17v.01\"/>",
	kraft: "<path d=\"M2 12h1\"/><path d=\"M6 8h-2a1 1 0 0 0 -1 1v6a1 1 0 0 0 1 1h2\"/><path d=\"M6 7v10a1 1 0 0 0 1 1h1a1 1 0 0 0 1 -1v-10a1 1 0 0 0 -1 -1h-1a1 1 0 0 0 -1 1z\"/><path d=\"M9 12h6\"/><path d=\"M15 7v10a1 1 0 0 0 1 1h1a1 1 0 0 0 1 -1v-10a1 1 0 0 0 -1 -1h-1a1 1 0 0 0 -1 1z\"/><path d=\"M18 8h2a1 1 0 0 1 1 1v6a1 1 0 0 1 -1 1h-2\"/><path d=\"M22 12h-1\"/>",
	bodyweight: "<path d=\"M4 8v-2a2 2 0 0 1 2 -2h2\"/><path d=\"M4 16v2a2 2 0 0 0 2 2h2\"/><path d=\"M16 4h2a2 2 0 0 1 2 2v2\"/><path d=\"M16 20h2a2 2 0 0 0 2 -2v-2\"/><path d=\"M12 8m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0\"/><path d=\"M10 17v-1a2 2 0 1 1 4 0v1\"/><path d=\"M8 10c.666 .666 1.334 1 2 1h4c.666 0 1.334 -.334 2 -1\"/><path d=\"M12 11v3\"/>",
	calisthenics: "<path d=\"M7 7a1 1 0 1 0 2 0a1 1 0 0 0 -2 0\"/><path d=\"M13 21l1 -9l7 -6\"/><path d=\"M3 11h6l5 1\"/><path d=\"M11.5 8.5l4.5 -3.5\"/>",
	kettlebell: "<path d=\"M12 6m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0\"/><path d=\"M6.835 9h10.33a1 1 0 0 1 .984 .821l1.637 9a1 1 0 0 1 -.984 1.179h-13.604a1 1 0 0 1 -.984 -1.179l1.637 -9a1 1 0 0 1 .984 -.821z\"/>",
	hiit: "<path d=\"M5 13a7 7 0 1 0 14 0a7 7 0 0 0 -14 0z\"/><path d=\"M14.5 10.5l-2.5 2.5\"/><path d=\"M17 8l1 -1\"/><path d=\"M14 3h-4\"/>",
	ausdauer: "<path d=\"M19.5 13.572l-7.5 7.428l-2.896 -2.868m-6.117 -8.104a5 5 0 0 1 9.013 -3.022a5 5 0 1 1 7.5 6.572\"/><path d=\"M3 13h2l2 3l2 -6l1 3h3\"/>",
	yoga: "<path d=\"M12 4m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0\"/><path d=\"M4 20h4l1.5 -3\"/><path d=\"M17 20l-1 -5h-5l1 -7\"/><path d=\"M4 10l4 -1l4 -1l4 1.5l4 1.5\"/>",
	other: "<path d=\"M3 12h4l3 8l4 -16l3 8h4\"/>",
	editor: "<path d=\"M4 20h4l10.5 -10.5a2.828 2.828 0 1 0 -4 -4l-10.5 10.5v4\"/><path d=\"M13.5 6.5l4 4\"/>",
	chev_up: "<path d=\"M6 15l6 -6l6 6\"/>",
	chev_down: "<path d=\"M6 9l6 6l6 -6\"/>",
	trash: "<path d=\"M4 7l16 0\"/><path d=\"M10 11l0 6\"/><path d=\"M14 11l0 6\"/><path d=\"M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12\"/><path d=\"M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3\"/>",
	copy: "<path d=\"M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z\"/><path d=\"M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1\"/>",
	plus: "<path d=\"M12 5l0 14\"/><path d=\"M5 12l14 0\"/>",
	search: "<path d=\"M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0\"/><path d=\"M21 21l-6 -6\"/>",
	back: "<path d=\"M5 12l14 0\"/><path d=\"M5 12l6 6\"/><path d=\"M5 12l6 -6\"/>",
	plans: "<path d=\"M9 5h-2a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-12a2 2 0 0 0 -2 -2h-2\"/><path d=\"M9 3m0 2a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v0a2 2 0 0 1 -2 2h-2a2 2 0 0 1 -2 -2z\"/><path d=\"M9 12l.01 0\"/><path d=\"M13 12l2 0\"/><path d=\"M9 16l.01 0\"/><path d=\"M13 16l2 0\"/>",
	templates: "<path d=\"M4 4m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z\"/><path d=\"M14 4m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z\"/><path d=\"M4 14m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z\"/><path d=\"M14 14m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z\"/>",
	people: "<path d=\"M9 7m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0\"/><path d=\"M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2\"/><path d=\"M16 3.13a4 4 0 0 1 0 7.75\"/><path d=\"M21 21v-2a4 4 0 0 0 -3 -3.85\"/>",
	data: "<path d=\"M12 6m-8 0a8 3 0 1 0 16 0a8 3 0 1 0 -16 0\"/><path d=\"M4 6v6a8 3 0 0 0 16 0v-6\"/><path d=\"M4 12v6a8 3 0 0 0 16 0v-6\"/>"
};
/** SVG eines Piktogramms. ring = im Kreis wie das Logo-Symbol. */
function icon(name, { ring = false, cls = "pi" } = {}) {
	const body = P[name] || P.other;
	if (!ring) return `<svg class="${cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${body}</svg>`;
	return `<svg class="${cls} ring" viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="16" cy="16" r="14.5" stroke-width="2.2"/><g transform="translate(6.4 6.4) scale(.8)" stroke-width="2.3">${body}</g></svg>`;
}
var TOKEN = /⟦(\w+)⟧/g;
/** Platzhalter im fertigen HTML ersetzen (in Attributen nur entfernen). */
function renderIcons(html) {
	return html.replace(/="([^"]*⟦\w+⟧[^"]*)"/g, (_, v) => `="${v.replace(TOKEN, "").trim()}"`).replace(TOKEN, (_, name) => icon(name));
}
/** Gruppen-Schlüssel und Reiter → Piktogramm-Name */
var ICON_OF = {
	kraft: "kraft",
	bodyweight: "bodyweight",
	calisthenics: "calisthenics",
	kettlebell: "kettlebell",
	hiit: "hiit",
	ausdauer: "ausdauer",
	yoga: "yoga",
	other: "other",
	"mdi:clipboard-list-outline": "plans",
	"mdi:star-outline": "templates",
	"mdi:account-multiple-outline": "people",
	data: "data",
	editor: "editor",
	import: "down"
};
// src/ui/app.js
var I18N = {
	en: {
		tab_training: "Training",
		tab_history: "History",
		tab_plans: "Settings",
		loading: "Loading …",
		conn_failed: "Could not connect to the integration: {err}. Is TrainingAssistant set up?",
		st_planned: "planned",
		st_pending: "asking …",
		st_confirmed: "confirmed",
		st_corrected: "corrected",
		st_edited: "edited",
		st_unconfirmed: "unconfirmed",
		st_skipped: "skipped",
		ph_ready: "Ready",
		ph_active: "Training",
		ph_interval: "HIIT",
		ph_finished: "Done",
		ph_paused: "Paused",
		ty_warmup: "Warm-up",
		ty_circuit: "Circuit",
		ty_sets: "Sets",
		ty_interval: "HIIT",
		ty_flow: "Flow",
		ty_cooldown: "Cool-down",
		u_reps: "reps",
		u_sec: "sec",
		per_side: "per side",
		per_side_short: "/side",
		hold_max_short: "hold max",
		amrap_short: "max reps",
		reps_n: "{n} reps",
		tile_hold: "sec hold",
		goal_range: "goal {lo}–{hi}",
		pos_round_of: "Round {r}/{n}",
		pos_round: "Round {r}",
		pos_set_of: "Set {s}/{n}",
		pos_set: "Set {s}",
		no_plan: "No training plan yet.",
		import_plan: "Import plan",
		start: "⟦play⟧ Start workout",
		program: "Program",
		workout: "Workout",
		wo_pos: "Workout {p} of {n}",
		wo_after: " · then {name}",
		wo_auto: " · after finishing, the program moves on automatically.",
		voice_via: "Announcements via {sat}",
		no_sat: "No default satellite: the workout runs silently on this card (choose a satellite in the integration options or when starting by voice).",
		pv_rounds: "{n} rounds",
		pv_cap: "{m} min alternating",
		pv_between_ex: "{d} between exercises",
		pv_between_rounds: "{d} between rounds",
		pv_sets: "{n} sets",
		pv_set1: "1 set",
		pv_sets_until: "Sets until {n} reps",
		pv_rest: "{d} rest",
		pv_interval: "{w} s work / {r} s rest",
		pv_block_rest: "⟦pause⟧ {d} rest",
		pv_flow: "{n} steps · about {m} min",
		flow_switch: "Switch",
		b_end_flow: "End flow",
		tempo: "Tempo {t}",
		iv_work: "WORK",
		iv_rest: "REST",
		t_rest: "Rest",
		t_left: "Time left",
		t_up: "Time's up – finish the exercise",
		t_question: "Voice question … (Next = as planned)",
		b_resume: "⟦play⟧ Resume",
		b_go: "⟦play⟧ Go",
		b_end_hiit: "End HIIT",
		b_set_done: "⟦check⟧ Set done",
		b_set_done_changed: "⟦check⟧ Set done (changed)",
		b_next: "Next",
		step: "Step {i}/{n}",
		b_back: "⟦undo⟧ Back",
		b_pause: "⟦pause⟧ Pause",
		b_continue: "⟦play⟧ Continue",
		b_skip: "⟦skip⟧ Skip",
		b_finish: "⟦flag⟧ Finish",
		c_finish: "Really finish?",
		b_discard: "⟦x⟧ Discard",
		c_discard: "Really discard?",
		coming_up: "Coming up",
		logged: "Logged (tap to correct)",
		un_done: "Workout complete",
		un_label: "Up next",
		a_seconds: "Seconds",
		a_reps: "Reps",
		a_reps_side: "Reps/side",
		a_weight: "Weight",
		a_less: "{l} less",
		a_more: "{l} more",
		e_save: "Save",
		e_skipped: "Skipped",
		e_cancel: "Cancel",
		h_loading: "Loading history …",
		h_empty: "No workouts saved yet.",
		h_ex_meta: "{n}× · last {d}",
		h_sets: "{n} sets",
		h_unconfirmed: "{n} unconfirmed",
		h_aborted: "aborted",
		c_delete: "Really delete?",
		h_delete: "Delete workout",
		h_th_ex: "Exercise",
		h_th_hist: "History",
		h_last8: "(last 8)",
		h_th_last: "Last",
		h_th_next: "Next time",
		h_tab_ex: "Exercises",
		h_tab_sess: "Workouts",
		tpl_loading: "Loading templates …",
		n_workout: "{n} workout",
		n_workouts: "{n} workouts",
		tpl_reload_c: "Reload? Your own changes will be lost.",
		tpl_installed: "⟦check⟧ Added · reload",
		tpl_take: "Add",
		tpl_open: "Show workouts and exercises of {name}",
		tpl_loading_one: "Loading …",
		p_active: "active program",
		p_noimg: "No image: {list}",
		p_edit: "Edit",
		p_delete: "Delete",
		p_next_badge: "up next",
		p_set_next: "Up next",
		p_start: "Start",
		p_tpl_intro: "Proven programs ready to add – afterwards they're ready to start under “My plans”. Weights are starting values; progression adjusts them.",
		p_import_intro: "Below is a commented example plan – adjust it and import. A plan with the same name is replaced, your history is kept. The guide explains everything and includes a ready-made prompt that lets ChatGPT or Claude write a plan for you.",
		p_dl_guide: "⟦down⟧ Guide (.txt)",
		p_dl_example: "⟦down⟧ Example plan (.yaml)",
		p_insert: "Insert example",
		p_clear: "Clear",
		p_placeholder: "schema_version: 1\nname: My plan\n…",
		p_import: "Import",
		p_none: "No plans yet.",
		p_pick_tpl: "Choose a template",
		p_own: "Create your own plan",
		p_tab_mine: "My plans",
		p_tab_tpl: "Templates",
		p_tab_own: "Own plan",
		m_imported: "“{name}” imported ({n} workouts). Images: {m} of {t} exercises",
		m_missing: " – no image: {list}",
		m_tpl: "Template “{name}” added ({n} workouts). Weights are starting values – please adjust.",
		m_example: "Example plan inserted – adjust it and import.",
		m_loaded: "Plan loaded – change it and import again (the same name replaces it).",
		c_first: "First workout with this exercise",
		c_last: "last {v} {u}",
		c_last_best: "last {v} · best {b} {u}",
		c_n: "{n} workouts",
		c_1: "1 workout",
		c_aria: "History {l}",
		guide_file: "guide-custom-plans.txt",
		example_file: "example-plan.yaml",
		guide_dl: "TrainingAssistant-Guide-Custom-Plans.txt",
		example_dl: "TrainingAssistant-Example-Plan.yaml",
		"sug.no_progression_timed": "No progression (time or max.)",
		"sug.plan_values": "Plan values (no history yet)",
		"sug.harder_variant": "All sets with {reps} reps done – harder variation or added weight",
		"sug.all_reps_add_weight": "All sets with {reps} reps done → +{kg} kg",
		"sug.hold_weight_target": "Keep the weight, aim for {target} reps (up to {max})",
		"sug.target_reps": "Aim for {target} reps (up to {max})",
		"sug.cap_reached": "Limit of {cap} reps reached – harder variation or added weight",
		"sug.all_reps_add_reps": "All sets with {reps} reps done → +{add} reps",
		"sug.repeat_target": "Target of {target} reps not yet reached in every set – repeat",
		"sug.all_done": "All sets done",
		"sug.all_done_add_weight": "All sets done → +{kg} kg",
		"sug.not_all_hold": "Not all sets done → keep the weight",
		"sug.fixed": "Fixed value from the plan (no progression)",
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
		"tg.ausdauer": "Endurance",
		"tg.ausdauer.about": "Running and steady cardio – step by step to more stamina. Timed, runs on its own.",
		"tg.yoga": "Yoga & mobility",
		"tg.yoga.about": "Flows, stretching and balance – runs on its own, every pose is announced. A mat is enough.",
		"tg.other": "More",
		wk_title: "This week",
		wk_goal: "Goal (number of workouts)",
		wk_goal_short: "workouts per week",
		wk_aria: "{d} of {n} workouts this week",
		wk_streak: "⟦streak⟧ Streak: {n} weeks",
		wk_streak1: "⟦streak⟧ Streak: 1 week",
		wk_streak_lbl: "⟦streak⟧ Streak",
		wk_bars: "Sets per day",
		wk_left: "{n} to go",
		wk_reached: "Goal reached",
		wk_total: "{n} workouts logged in total",
		wk_goal_less: "Lower weekly goal",
		wk_goal_more: "Raise weekly goal",
		"mg.chest": "Chest",
		"mg.back": "Back",
		"mg.shoulders": "Shoulders",
		"mg.biceps": "Biceps",
		"mg.triceps": "Triceps",
		"mg.core": "Abs",
		"mg.quads": "Quads",
		"mg.hamstrings": "Hamstrings",
		"mg.glutes": "Glutes",
		"mg.calves": "Calves",
		h_tab_over: "Overview",
		tile_week: "This week",
		tile_streak: "Streak",
		tile_weeks: "{n} weeks",
		tile_week1: "1 week",
		tile_total: "Workouts in total",
		tile_since: "since {d}",
		tile_time: "Time this week",
		tile_time_avg: "Ø {m} min/week",
		rec_title: "Recent records",
		rec_none: "No records yet – they appear from your second workout with an exercise.",
		rec_weight: "{v} kg",
		rec_e1rm: "est. max {v} kg",
		rec_reps: "{v} reps",
		rec_duration: "{v} s",
		rec_prev: "before {v}",
		vol_title: "Sets per muscle group this week",
		vol_hint: "Guide: about 10 hard sets per muscle and week (line).",
		vol_last: "last week {n}",
		vol_none: "No sets this week yet.",
		vol_unassigned: "Without muscle group: {n} sets ({list}) – add muscles: […] to the exercise in the plan.",
		rc_title: "Recovery",
		rc_fresh: "Just trained",
		rc_recovering: "Recovering",
		rc_ready: "Ready",
		rc_soon: "Train soon",
		rc_overdue: "Overdue",
		rc_none: "Not trained yet",
		rc_h: "last {n} h ago",
		rc_d: "last {n} days ago",
		rc_since_h: "for {n} h",
		rc_since_d: "for {n} days",
		mt_primary: "Main muscle",
		mt_secondary: "Also worked",
		ef_last: "How did it feel?",
		ef_easy: "Easy",
		ef_normal: "Normal",
		ef_hard: "Hard",
		st_wait: "Waiting for Go",
		st_go: "Go!",
		el_title: "Workout time",
		el_last: "last time {d}",
		t_record: "⟦trophy⟧ New record: {name}",
		rest_less: "−15 s",
		rest_more: "+15 s",
		who: "Who's training?",
		p_tab_people: "People",
		pp_intro: "Every person has their own history, suggestions, weekly goal and program position. Plans are shared.",
		pp_figure: "Figure in pictures",
		fig_m: "Male",
		fig_w: "Female",
		pp_active: "selected",
		pp_select: "Select",
		pp_rename: "Rename",
		pp_delete: "Delete",
		pp_c_delete: "Delete incl. history?",
		pp_add: "+ Add person",
		pp_name: "Name",
		pp_save: "Save",
		pp_busy: "You can select someone else after the workout.",
		who_view: "Whose workout?",
		pp_view: "Show",
		pp_viewing: "shown",
		pp_training: "training now",
		pp_intro_multi: "Everyone has their own history, suggestions, weekly goal and program position – and trains on their own, at the same time if you like. Here you choose whose workout the card shows. Plans are shared.",
		ro_note: "This is {name}'s workout – you can watch, but only {name} can control it.",
		pp_sat: "Satellite",
		pp_light: "Light",
		pp_notify: "Phone notification",
		pp_default: "– default –",
		pp_goal: "Weekly goal: {n} workouts",
		pp_user: "Home Assistant user",
		pp_user_none: "– not linked –",
		pp_user_hint: "A linked person is selected automatically when that user opens the card (e.g. on their own phone).",
		pp_linked: "{name}",
		pp_linked_anon: "linked",
		"sug.hard_hold": "Felt hard last time → same again",
		"sug.easy_target": "Felt easy → aim for {target} reps (up to {max})",
		"sug.easy_add_reps": "All sets felt easy → +{add} reps",
		"sug.easy_add_weight": "All sets felt easy → +{kg} kg"
	},
	de: {
		tab_training: "Training",
		tab_history: "Verlauf",
		tab_plans: "Einstellungen",
		loading: "Lade …",
		conn_failed: "Verbindung zur Integration fehlgeschlagen: {err}. Ist TrainingAssistant eingerichtet?",
		st_planned: "geplant",
		st_pending: "Rückfrage …",
		st_confirmed: "bestätigt",
		st_corrected: "korrigiert",
		st_edited: "geändert",
		st_unconfirmed: "unbestätigt",
		st_skipped: "übersprungen",
		ph_ready: "Bereit",
		ph_active: "Training",
		ph_interval: "HIIT",
		ph_finished: "Fertig",
		ph_paused: "Pausiert",
		ty_warmup: "Aufwärmen",
		ty_circuit: "Zirkel",
		ty_sets: "Sätze",
		ty_interval: "HIIT",
		ty_flow: "Flow",
		ty_cooldown: "Cool Down",
		u_reps: "Wdh.",
		u_sec: "Sek.",
		per_side: "pro Seite",
		per_side_short: "/Seite",
		hold_max_short: "max. halten",
		amrap_short: "max. Wdh.",
		reps_n: "{n} Wdh.",
		tile_hold: "Sek. halten",
		goal_range: "Ziel {lo}–{hi}",
		pos_round_of: "Runde {r}/{n}",
		pos_round: "Runde {r}",
		pos_set_of: "Satz {s}/{n}",
		pos_set: "Satz {s}",
		no_plan: "Noch kein Trainingsplan vorhanden.",
		import_plan: "Plan importieren",
		start: "⟦play⟧ Training starten",
		program: "Programm",
		workout: "Workout",
		wo_pos: "Workout {p} von {n}",
		wo_after: " · danach {name}",
		wo_auto: " · nach dem Beenden geht es im Programm automatisch weiter.",
		voice_via: "Ansagen über {sat}",
		no_sat: "Kein Standard-Satellit: Das Training läuft stumm über diese Karte (Satellit in den Optionen der Integration wählbar oder beim Start per Sprache).",
		pv_rounds: "{n} Runden",
		pv_cap: "{m} min im Wechsel",
		pv_between_ex: "{d} zw. Übungen",
		pv_between_rounds: "{d} zw. Runden",
		pv_sets: "{n} Sätze",
		pv_set1: "1 Satz",
		pv_sets_until: "Sätze bis {n} Wdh.",
		pv_rest: "{d} Pause",
		pv_interval: "{w} s Arbeit / {r} s Pause",
		pv_block_rest: "⟦pause⟧ {d} Pause",
		pv_flow: "{n} Abschnitte · etwa {m} min",
		flow_switch: "Wechsel",
		b_end_flow: "Flow beenden",
		tempo: "Tempo {t}",
		iv_work: "ARBEIT",
		iv_rest: "PAUSE",
		t_rest: "Pause",
		t_left: "Zeit übrig",
		t_up: "Zeit um – Übung beenden",
		t_question: "Rückfrage läuft … (Weiter = wie geplant)",
		b_resume: "⟦play⟧ Fortsetzen",
		b_go: "⟦play⟧ Los",
		b_end_hiit: "HIIT beenden",
		b_set_done: "⟦check⟧ Satz fertig",
		b_set_done_changed: "⟦check⟧ Satz fertig (geändert)",
		b_next: "Weiter",
		step: "Schritt {i}/{n}",
		b_back: "⟦undo⟧ Zurück",
		b_pause: "⟦pause⟧ Pause",
		b_continue: "⟦play⟧ Weiter",
		b_skip: "⟦skip⟧ Überspringen",
		b_finish: "⟦flag⟧ Beenden",
		c_finish: "Wirklich beenden?",
		b_discard: "⟦x⟧ Verwerfen",
		c_discard: "Wirklich verwerfen?",
		coming_up: "Danach",
		logged: "Erfasst (antippen zum Korrigieren)",
		un_done: "Training fertig",
		un_label: "Als Nächstes",
		a_seconds: "Sekunden",
		a_reps: "Wdh.",
		a_reps_side: "Wdh./Seite",
		a_weight: "Gewicht",
		a_less: "{l} weniger",
		a_more: "{l} mehr",
		e_save: "Speichern",
		e_skipped: "Übersprungen",
		e_cancel: "Abbrechen",
		h_loading: "Lade Verlauf …",
		h_empty: "Noch keine Trainings gespeichert.",
		h_ex_meta: "{n}× · zuletzt {d}",
		h_sets: "{n} Sätze",
		h_unconfirmed: "{n} unbestätigt",
		h_aborted: "abgebrochen",
		c_delete: "Wirklich löschen?",
		h_delete: "Training löschen",
		h_th_ex: "Übung",
		h_th_hist: "Verlauf",
		h_last8: "(letzte 8)",
		h_th_last: "Zuletzt",
		h_th_next: "Nächstes Mal",
		h_tab_ex: "Übungen",
		h_tab_sess: "Trainings",
		tpl_loading: "Lade Vorlagen …",
		n_workout: "{n} Workout",
		n_workouts: "{n} Workouts",
		tpl_reload_c: "Neu laden? Eigene Änderungen gehen verloren.",
		tpl_installed: "⟦check⟧ Übernommen · neu laden",
		tpl_take: "Übernehmen",
		tpl_open: "Workouts und Übungen von {name} anzeigen",
		tpl_loading_one: "Lade …",
		p_active: "aktives Programm",
		p_noimg: "Ohne Bild: {list}",
		p_edit: "Bearbeiten",
		p_delete: "Löschen",
		p_next_badge: "als Nächstes",
		p_set_next: "Als Nächstes",
		p_start: "Starten",
		p_tpl_intro: "Bewährte Programme zum Übernehmen – danach unter „Meine Pläne“ startklar. Gewichte sind Startwerte, die Progression passt sie an.",
		p_import_intro: "Unten steht ein kommentierter Beispielplan – anpassen und importieren. Ein Plan mit gleichem Namen wird ersetzt, der Verlauf bleibt. Die Anleitung erklärt alles und enthält einen fertigen Prompt, mit dem ChatGPT oder Claude dir einen Plan schreibt.",
		p_dl_guide: "⟦down⟧ Anleitung (.txt)",
		p_dl_example: "⟦down⟧ Beispielplan (.yaml)",
		p_insert: "Beispiel einsetzen",
		p_clear: "Leeren",
		p_placeholder: "schema_version: 1\nname: Mein Plan\n…",
		p_import: "Importieren",
		p_none: "Noch keine Pläne.",
		p_pick_tpl: "Vorlage auswählen",
		p_own: "Eigenen Plan anlegen",
		p_tab_mine: "Meine Pläne",
		p_tab_tpl: "Vorlagen",
		p_tab_own: "Eigener Plan",
		m_imported: "„{name}“ importiert ({n} Workouts). Bilder: {m} von {t} Übungen",
		m_missing: " – ohne Bild: {list}",
		m_tpl: "Vorlage „{name}“ übernommen ({n} Workouts). Gewichte sind Startwerte – bitte anpassen.",
		m_example: "Beispielplan eingesetzt – anpassen und importieren.",
		m_loaded: "Plan geladen – ändern und erneut importieren (gleicher Name ersetzt ihn).",
		c_first: "Erstes Training mit dieser Übung",
		c_last: "zuletzt {v} {u}",
		c_last_best: "zuletzt {v} · bestes {b} {u}",
		c_n: "{n} Trainings",
		c_1: "1 Training",
		c_aria: "Verlauf {l}",
		guide_file: "anleitung-eigene-plaene.txt",
		example_file: "beispiel-plan.yaml",
		guide_dl: "TrainingAssistant-Anleitung-eigene-Plaene.txt",
		example_dl: "TrainingAssistant-Beispielplan.yaml",
		"sug.no_progression_timed": "Ohne Progression (Zeit oder max.)",
		"sug.plan_values": "Planwerte (noch kein Verlauf)",
		"sug.harder_variant": "Alle Sätze mit {reps} Wdh. geschafft – schwerere Variante oder Zusatzgewicht",
		"sug.all_reps_add_weight": "Alle Sätze mit {reps} Wdh. geschafft → +{kg} kg",
		"sug.hold_weight_target": "Gewicht halten, Ziel {target} Wdh. (bis {max})",
		"sug.target_reps": "Ziel {target} Wdh. (bis {max})",
		"sug.cap_reached": "Obergrenze von {cap} Wdh. erreicht – schwerere Variante oder Zusatzgewicht",
		"sug.all_reps_add_reps": "Alle Sätze mit {reps} Wdh. geschafft → +{add} Wdh.",
		"sug.repeat_target": "Ziel {target} Wdh. noch nicht in allen Sätzen geschafft – nochmal",
		"sug.all_done": "Alle Sätze geschafft",
		"sug.all_done_add_weight": "Alle Sätze geschafft → +{kg} kg",
		"sug.not_all_hold": "Nicht alle Sätze geschafft → Gewicht halten",
		"sug.fixed": "Feste Vorgabe aus dem Plan (ohne Progression)",
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
		"tg.ausdauer": "Ausdauer",
		"tg.ausdauer.about": "Laufen und Ausdauertraining – Schritt für Schritt zu mehr Kondition. Zeitgesteuert, läuft von selbst.",
		"tg.yoga": "Yoga & Mobilität",
		"tg.yoga.about": "Flows, Dehnen und Gleichgewicht – läuft von selbst, jede Haltung wird angesagt. Eine Matte genügt.",
		"tg.other": "Weitere",
		wk_title: "Diese Woche",
		wk_goal: "Ziel (Anzahl der Workouts)",
		wk_goal_short: "Workouts pro Woche",
		wk_aria: "{d} von {n} Trainings diese Woche",
		wk_streak: "⟦streak⟧ Streak: {n} Wochen",
		wk_streak1: "⟦streak⟧ Streak: 1 Woche",
		wk_streak_lbl: "⟦streak⟧ Streak",
		wk_bars: "Sätze pro Tag",
		wk_left: "noch {n}",
		wk_reached: "Ziel erreicht",
		wk_total: "{n} Trainings insgesamt",
		wk_goal_less: "Wochenziel senken",
		wk_goal_more: "Wochenziel erhöhen",
		"mg.chest": "Brust",
		"mg.back": "Rücken",
		"mg.shoulders": "Schultern",
		"mg.biceps": "Bizeps",
		"mg.triceps": "Trizeps",
		"mg.core": "Bauch",
		"mg.quads": "Oberschenkel vorn",
		"mg.hamstrings": "Oberschenkel hinten",
		"mg.glutes": "Po",
		"mg.calves": "Waden",
		h_tab_over: "Übersicht",
		tile_week: "Diese Woche",
		tile_streak: "Streak",
		tile_weeks: "{n} Wochen",
		tile_week1: "1 Woche",
		tile_total: "Trainings gesamt",
		tile_since: "seit {d}",
		tile_time: "Zeit diese Woche",
		tile_time_avg: "Ø {m} min/Woche",
		rec_title: "Letzte Rekorde",
		rec_none: "Noch keine Rekorde – sie kommen ab dem zweiten Training mit einer Übung.",
		rec_weight: "{v} kg",
		rec_e1rm: "geschätztes Max. {v} kg",
		rec_reps: "{v} Wdh.",
		rec_duration: "{v} s",
		rec_prev: "vorher {v}",
		vol_title: "Sätze pro Muskelgruppe diese Woche",
		vol_hint: "Richtwert: etwa 10 harte Sätze pro Muskel und Woche (Linie).",
		vol_last: "Vorwoche {n}",
		vol_none: "Diese Woche noch keine Sätze.",
		vol_unassigned: "Ohne Muskelgruppe: {n} Sätze ({list}) – im Plan bei der Übung muscles: […] ergänzen.",
		rc_title: "Erholung",
		rc_fresh: "Gerade trainiert",
		rc_recovering: "Erholt sich",
		rc_ready: "Bereit",
		rc_soon: "Bald wieder",
		rc_overdue: "Überfällig",
		rc_none: "Noch nicht trainiert",
		rc_h: "zuletzt vor {n} h",
		rc_d: "zuletzt vor {n} Tagen",
		rc_since_h: "seit {n} h",
		rc_since_d: "seit {n} Tagen",
		mt_primary: "Hauptmuskel",
		mt_secondary: "Arbeitet mit",
		ef_last: "Wie war's?",
		ef_easy: "Leicht",
		ef_normal: "Normal",
		ef_hard: "Schwer",
		st_wait: "Warte auf Los",
		st_go: "Los!",
		el_title: "Trainingszeit",
		el_last: "letztes Mal {d}",
		t_record: "⟦trophy⟧ Neuer Rekord: {name}",
		rest_less: "−15 s",
		rest_more: "+15 s",
		who: "Wer trainiert?",
		p_tab_people: "Personen",
		pp_intro: "Jede Person hat eigenen Verlauf, eigene Vorschläge, ein eigenes Wochenziel und eine eigene Programm-Position. Pläne sind gemeinsam.",
		pp_figure: "Figur auf den Bildern",
		fig_m: "Männlich",
		fig_w: "Weiblich",
		pp_active: "ausgewählt",
		pp_select: "Auswählen",
		pp_rename: "Umbenennen",
		pp_delete: "Löschen",
		pp_c_delete: "Mit Verlauf löschen?",
		pp_add: "+ Person hinzufügen",
		pp_name: "Name",
		pp_save: "Speichern",
		pp_busy: "Eine andere Person auswählen geht nach dem Training.",
		who_view: "Wessen Training?",
		pp_view: "Ansehen",
		pp_viewing: "angezeigt",
		pp_training: "trainiert gerade",
		pp_intro_multi: "Jede Person hat eigenen Verlauf, eigene Vorschläge, ein eigenes Wochenziel und eine eigene Programm-Position – und trainiert für sich, auch gleichzeitig. Hier wählst du, wessen Training die Karte zeigt. Pläne sind gemeinsam.",
		ro_note: "Das ist das Training von {name} – zuschauen geht, bedienen kann nur {name}.",
		pp_sat: "Satellit",
		pp_light: "Lampe",
		pp_notify: "Handy-Hinweis",
		pp_default: "– Standard –",
		pp_goal: "Wochenziel: {n} Trainings",
		pp_user: "Home-Assistant-Benutzer",
		pp_user_none: "– nicht verknüpft –",
		pp_user_hint: "Eine verknüpfte Person wird automatisch ausgewählt, wenn dieser Benutzer die Karte öffnet (z. B. auf dem eigenen Handy).",
		pp_linked: "{name}",
		pp_linked_anon: "verknüpft",
		"sug.hard_hold": "Zuletzt schwer → gleiche Vorgabe nochmal",
		"sug.easy_target": "Leicht → Ziel {target} Wdh. (bis {max})",
		"sug.easy_add_reps": "Alle Sätze leicht → +{add} Wdh.",
		"sug.easy_add_weight": "Alle Sätze leicht → +{kg} kg"
	}
};
var LANG = "en";
var LOCALE = void 0;
for (const [k, v] of Object.entries(EXTRA_I18N)) Object.assign(I18N[k], v);
var setLanguage = (wanted) => {
	const lang = wanted || navigator.languages && navigator.languages[0] || navigator.language || "en";
	LANG = lang.toLowerCase().startsWith("de") ? "de" : "en";
	LOCALE = LANG === "de" ? lang : "en";
	return LANG;
};
var t = (key, p = {}) => String(I18N[LANG][key] ?? I18N.en[key] ?? key).replace(/\{(\w+)\}/g, (_, n) => p[n] ?? "");
var sugText = (o) => o && o.key ? t(`sug.${o.key}`, Object.fromEntries(Object.entries(o.params || {}).map(([k, v]) => [k, typeof v === "number" ? num(v) : v]))) : o && o.text || "";
var stepSug = (s) => sugText({
	key: s.suggestion_key,
	params: s.suggestion_params,
	text: s.suggestion
});
var reasonSug = (s) => sugText({
	key: s.reason_key,
	params: s.reason_params,
	text: s.reason
});
var EFFORT_PROMPT_MS = 1e4;
var STATUS = {
	planned: "neutral",
	pending: "info",
	confirmed: "ok",
	corrected: "ok",
	edited: "ok",
	unconfirmed: "warn",
	skipped: "muted"
};
var typeLabel = (type) => type ? t(`ty_${type}`) : "";
var blockTitle = (type, name) => {
	const label = typeLabel(type);
	if (!name || name === label) return label;
	return name.toLowerCase().startsWith(label.toLowerCase()) ? name : `${label} · ${name}`;
};
var IMG_BASE = "./pictos";
var tierClass = (r) => r && r.tier !== null && r.tier !== void 0 ? `rt-${r.tier}` : "rc-none";
var tierLegend = (b) => {
	if (!b || !b.length) return "";
	return `<div class="rt-legend muted small">${[
		`< ${b[0]} h`,
		...b.slice(1).map((h, i) => `${b[i]}–${h} h`),
		`≥ ${b[b.length - 1]} h`
	].map((l, i) => `<span><i class="rt-${i}"></i>${l}</span>`).join("")}</div>`;
};
var FIGURE = "m";
var SINGLE = /* @__PURE__ */ new Set();
var imgUrl = (cid, n) => `${IMG_BASE}/${FIGURE}/${encodeURIComponent(cid)}/${n}.jpg`;
var imgUrls = (cid) => cid ? SINGLE.has(cid) ? [imgUrl(cid, 0)] : [imgUrl(cid, 0), imgUrl(cid, 1)] : [];
var img = (cid, cls = "thumb", n = null) => {
	if (!cid) return n ? "" : `<span class="${cls} noimg"></span>`;
	if (n === null) n = SINGLE.has(cid) ? 0 : 1;
	else if (n > 0 && SINGLE.has(cid)) return "";
	return `<img class="${cls}" src="${imgUrl(cid, n)}" alt="" loading="lazy">`;
};
var thumbBtn = (cid, name, cls = "thumb") => cid ? `<button class="ex-img" type="button" data-a="ex-preview" data-img="${esc(cid)}" data-name="${esc(name)}"
        aria-label="${esc(t("ed_preview", { name }))}">${img(cid, cls)}</button>` : img(null, cls);
var dur = (s) => s >= 60 ? s % 60 ? `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")} min` : `${s / 60} min` : `${s} s`;
var esc = (v) => String(v ?? "").replace(/[&<>"']/g, (c) => ({
	"&": "&amp;",
	"<": "&lt;",
	">": "&gt;",
	"\"": "&quot;",
	"'": "&#39;"
})[c]);
var num = (v) => v === null || v === void 0 ? "" : String(Math.round(v * 100) / 100).replace(".", LANG === "de" ? "," : ".");
var kg = (v) => v === null || v === void 0 ? "" : `${num(v)} kg`;
var mmss = (s) => {
	s = Math.max(0, Math.round(s));
	return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
};
var hms = (s) => {
	s = Math.max(0, Math.floor(s));
	const h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), sec = String(s % 60).padStart(2, "0");
	return h ? `${h}:${String(m).padStart(2, "0")}:${sec}` : `${m}:${sec}`;
};
var time = (iso) => iso ? new Date(iso).toLocaleTimeString(LOCALE, {
	hour: "2-digit",
	minute: "2-digit"
}) : "";
var sessionDuration = (s) => {
	if (!s.started_at || !s.finished_at) return "";
	const min = Math.round((new Date(s.finished_at) - new Date(s.started_at)) / 6e4);
	if (min < 1) return "< 1 min";
	return min >= 60 ? `${Math.floor(min / 60)} h ${String(min % 60).padStart(2, "0")} min` : `${min} min`;
};
var date = (iso) => iso ? new Date(iso).toLocaleDateString(LOCALE, {
	weekday: "short",
	day: "2-digit",
	month: "2-digit",
	year: "2-digit"
}) : "";
var ivName = (iv) => iv.exercise ? `${iv.exercise}${iv.side ? `, ${t(`side_${iv.side}`)}` : ""}` : "";
function targetText(s) {
	let out;
	if (s.hold_max) out = t("hold_max_short");
	else if (s.target_duration) out = `${s.target_duration} s`;
	else if (s.duration_range) out = `${s.duration_range[0]}–${s.duration_range[1]} s`;
	else if (s.amrap) out = t("amrap_short");
	else if (s.target_reps) out = s.per_side ? String(s.target_reps) : t("reps_n", { n: s.target_reps });
	else out = "";
	if (s.per_side) out += t("per_side_short");
	if (s.rep_range && s.rep_range[0] !== s.rep_range[1]) out += ` (${s.rep_range[0]}–${s.rep_range[1]})`;
	if (s.target_weight !== null && s.target_weight !== void 0) out += ` · ${kg(s.target_weight)}`;
	return out;
}
function targetTiles(s) {
	const side = s.per_side ? t("per_side_short") : "";
	const tile = (value, unit, hint = "", suffix = side) => `<div class="tg-v"><b>${esc(value)}${suffix ? `<small class="tg-side">${esc(suffix)}</small>` : ""}</b><span>${esc(unit)}</span>${hint ? `<em>${esc(hint)}</em>` : ""}</div>`;
	const parts = [];
	if (s.hold_max) parts.push(tile("max", t("tile_hold")));
	else if (s.target_duration) parts.push(tile(s.target_duration, t("u_sec"), s.duration_range ? `${s.duration_range[0]}–${s.duration_range[1]} s` : ""));
	else if (s.duration_range) parts.push(tile(`${s.duration_range[0]}–${s.duration_range[1]}`, t("u_sec")));
	else if (s.amrap) parts.push(tile("max", t("u_reps")));
	else if (s.target_reps) {
		const range = s.rep_range && s.rep_range[0] !== s.rep_range[1] ? t("goal_range", {
			lo: s.rep_range[0],
			hi: s.rep_range[1]
		}) : "";
		parts.push(tile(s.target_reps, t("u_reps"), range));
	}
	if (s.target_weight !== null && s.target_weight !== void 0) {
		if (parts.length) parts.push(`<div class="tg-x">×</div>`);
		parts.push(tile(num(s.target_weight), "kg", "", ""));
	}
	return `<div class="tg">${parts.join("")}</div>`;
}
function position(s) {
	if (s.round) return s.rounds ? t("pos_round_of", {
		r: s.round,
		n: s.rounds
	}) : t("pos_round", { r: s.round });
	if (s.set_no) return s.sets ? t("pos_set_of", {
		s: s.set_no,
		n: s.sets
	}) : t("pos_set", { s: s.set_no });
	return "";
}
function setValue(x) {
	if (x.status === "skipped") return "–";
	const parts = [];
	if (x.reps !== null && x.reps !== void 0) parts.push(`${x.reps}${x.per_side ? t("per_side_short") : ""}`);
	if (x.duration_s !== null && x.duration_s !== void 0) parts.push(`${x.duration_s} s${x.per_side ? t("per_side_short") : ""}`);
	if (x.weight_kg !== null && x.weight_kg !== void 0) parts.push(kg(x.weight_kg));
	return parts.join(" × ") || "?";
}
var TrainerUI = class extends HTMLElement {
	constructor() {
		super();
		this.attachShadow({ mode: "open" });
		this._tab = "training";
		this._histTab = "overview";
		this._stats = null;
		this._ppEdit = null;
		this._editing = null;
		this._importMsg = null;
		this._history = null;
		this._preview = null;
		this._previewKey = null;
		this._openSessions = /* @__PURE__ */ new Set();
		this._error = null;
		this._caps = {};
		this._importText = "";
		const app = this;
		this._editor = createEditor({
			t,
			esc,
			img,
			dur,
			lang: () => LANG,
			ws: (msg) => this._ws(msg),
			toast: (m) => this._toast(m),
			render: () => this._render(),
			get sideSwitchS() {
				return app._state ? app._state.side_switch_s : null;
			},
			preview: (cid, name, el) => openExercisePreview({
				urls: imgUrls(cid),
				title: name,
				closeLabel: t("ef_close"),
				returnFocus: el
			})
		});
		this.shadowRoot.addEventListener("click", (e) => this._onClick(e));
		this.shadowRoot.addEventListener("error", (e) => {
			if (e.target && e.target.tagName === "IMG") e.target.classList.add("broken");
		}, true);
		this.shadowRoot.addEventListener("input", (e) => this._onInput(e));
		this.shadowRoot.addEventListener("change", (e) => this._onChange(e));
		this.shadowRoot.addEventListener("focusout", () => setTimeout(() => this._dirty && this._render(), 50));
	}
	/** Mit dem Anschluss verbinden (HU: Trainer im Browser, TA: Home Assistant) */
	connect(backend) {
		this._backend = backend;
		this._caps = backend.caps || {};
		if (backend.imgBase) IMG_BASE = backend.imgBase;
		this._render();
		this._subscribe();
	}
	get _effortMs() {
		return this._caps && this._caps.effortMs || EFFORT_PROMPT_MS;
	}
	/** Nur zuschauen: TA mit mehreren Personen, angezeigt wird das Training einer anderen Person */
	get _readOnly() {
		return !!(this._state && this._state.multi && this._state.can_control === false);
	}
	/** TA: andere Person ansehen (jede Person trainiert für sich – umschalten ändert nichts an den Daten) */
	_viewPerson(pid) {
		if (!this._backend.setPerson) return;
		this._backend.setPerson(pid);
		if (this._unsub) this._unsub();
		this._unsub = null;
		this._subscribed = false;
		this._stats = null;
		this._history = null;
		this._previewKey = null;
		this._summary = null;
		this._editing = null;
		this._closePrompt();
		this._subscribe();
	}
	connectedCallback() {
		this._timer = setInterval(() => this._tickTimers(), 1e3);
		this._onWake = () => {
			if (document.visibilityState === "visible") this._refreshStats();
		};
		document.addEventListener("visibilitychange", this._onWake);
		window.addEventListener("focus", this._onWake);
		window.addEventListener("pageshow", this._onWake);
		this._statsTimer = setInterval(() => this._onWake(), 6e4);
		if (this._backend && !this._unsub) this._subscribe();
	}
	disconnectedCallback() {
		clearInterval(this._statsTimer);
		document.removeEventListener("visibilitychange", this._onWake);
		window.removeEventListener("focus", this._onWake);
		window.removeEventListener("pageshow", this._onWake);
		clearInterval(this._timer);
		if (this._unsub) this._unsub();
		this._unsub = null;
		this._subscribed = false;
	}
	_subscribe() {
		if (!this._backend || this._subscribed) return;
		this._subscribed = true;
		this._unsub = this._backend.subscribe((state) => {
			const prev = this._state;
			const profileChanged = prev && prev.profile !== state.profile;
			const lastChanged = prev && prev.last_session_id !== state.last_session_id || profileChanged;
			if (!prev || lastChanged || prev.weekly_goal !== state.weekly_goal) this._stats = null;
			if (profileChanged) {
				this._history = null;
				this._previewKey = null;
			}
			const ended = prev && !profileChanged && prev.active && !state.active && state.last_session_id ? state.last_session_id : null;
			this._state = state;
			if (ended && !(state.multi && state.can_control === false)) this._openSummary(ended);
			FIGURE = state.figure === "w" ? "w" : "m";
			if (!prev || prev.single_images !== state.single_images) SINGLE = new Set(state.single_images || []);
			this._watchLogged(prev, state);
			this._error = null;
			this._autoSelectProfile(state);
			if (this._tab === "history" && (lastChanged || !this._history)) this._loadHistory();
			if (!state.active) this._loadPreview();
			this._render();
		}, (err) => {
			this._error = t("conn_failed", { err: err && (err.message || err.code) || err });
			this._subscribed = false;
			this._unsub = null;
			this._render();
		});
	}
	_errText(err) {
		if (err && err.key && t(`err.${err.key}`) !== `err.${err.key}`) return t(`err.${err.key}`, err.params || {});
		if (err && typeof err.message === "string" && err.message) return err.message;
		if (err && err.code) return String(err.code);
		return typeof err === "string" ? err : t("err.unknown");
	}
	async _ws(msg) {
		try {
			return await this._backend.ws(msg);
		} catch (err) {
			this._toast(this._errText(err));
			throw err;
		}
	}
	async _service(name, data = {}) {
		try {
			await this._backend.service(name, data);
		} catch (err) {
			if (!this._backend.serviceErrorsShown) this._toast(this._errText(err));
		}
	}
	_toast(message) {
		this._backend.toast(message);
	}
	async _loadHistory() {
		try {
			this._history = await this._ws({
				type: "history",
				limit: 50
			});
		} catch (_) {
			this._history = {
				sessions: [],
				exercises: []
			};
		}
		this._render();
	}
	async _loadPreview() {
		const nxt = this._state && this._state.next;
		const key = nxt ? `${nxt.plan_id}/${nxt.workout_id}/${this._state.last_session_id}` : null;
		if (!nxt || key === this._previewKey) return;
		this._previewKey = key;
		try {
			const res = await this._ws({
				type: "preview",
				plan_id: nxt.plan_id,
				workout_id: nxt.workout_id
			});
			this._preview = res.steps;
		} catch (_) {
			this._preview = null;
		}
		this._render();
	}
	async _onClick(e) {
		const el = e.target.closest("[data-a]");
		if (!el) return;
		const a = el.dataset.a;
		const d = el.dataset;
		if (d.confirm && !this._confirmed(d.ck)) return;
		if (a === "ex-preview") {
			openExercisePreview({
				urls: imgUrls(d.img),
				title: d.name,
				closeLabel: t("ef_close"),
				returnFocus: el
			});
			return;
		}
		if (a === "pfilter") {
			this._planFilter = d.f;
			this._render();
			return;
		}
		if (a.startsWith("ed-")) {
			this._planTab = "editor";
			if (await this._editor.click(a, d, el)) this._renderEditor();
			return;
		}
		if (a === "efp-close") {
			this._closePrompt();
			return;
		}
		if (a === "note") el.classList.toggle("open");
		else if (a === "go-templates") {
			this._tab = "plans";
			this._planTab = "templates";
			this._render();
		} else if (a === "tab") {
			this._tab = d.tab;
			this._editing = null;
			if (this._tab === "history") this._loadHistory();
			this._render();
		} else if (a === "adj") await this._service("adjust", {
			field: d.k === "weight" ? "weight" : "reps",
			steps: Number(d.d)
		});
		else if (a === "next") await this._service("next");
		else if (a === "svc") await this._service(d.svc, d.keep ? { keep: d.keep === "1" } : {});
		else if (a === "start") {
			await this._service("start", d.plan ? {
				plan_id: d.plan,
				workout_id: d.workout
			} : {});
			this._tab = "training";
			this._render();
		} else if (a === "next-workout") {
			await this._ws({
				type: "set_next",
				plan_id: d.plan,
				workout_id: d.workout
			});
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
				effort: set.effort || "normal"
			};
			this._render();
		} else if (a === "edit-cancel") {
			this._editing = null;
			this._render();
		} else if (a === "edit-save" || a === "edit-skip") {
			const ed = this._editing;
			const msg = {
				type: "edit_set",
				set_id: ed.set_id
			};
			if (ed.session_id) msg.session_id = ed.session_id;
			if (a === "edit-skip") msg.skipped = true;
			else {
				const toNum = (v, f) => v === "" || v === null ? null : f(String(v).replace(",", "."));
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
			} catch (_) {}
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
			await this._ws({
				type: "delete_session",
				session_id: d.session
			});
			await this._loadHistory();
		} else if (a === "tg-toggle") {
			this._tgOpen = this._tgOpen || /* @__PURE__ */ new Set();
			this._tgOpen.has(d.g) ? this._tgOpen.delete(d.g) : this._tgOpen.add(d.g);
			this._render();
		} else if (a === "fin-done") {
			this._summary = null;
			this._render();
			window.scrollTo(0, 0);
		} else if (a === "tpl-open") {
			this._tplOpen = this._tplOpen === d.tpl ? null : d.tpl;
			this._tplWorkout = 0;
			this._render();
			this._tplPreviews = this._tplPreviews || {};
			if (this._tplOpen && !this._tplPreviews[d.tpl]) {
				try {
					this._tplPreviews[d.tpl] = await this._ws({
						type: "template_preview",
						template_id: d.tpl
					});
				} catch (err) {
					this._tplOpen = null;
					this._importMsg = {
						ok: false,
						text: err.message || String(err)
					};
				}
				this._render();
			}
		} else if (a === "tpl-wo") {
			this._tplWorkout = Number(d.i) || 0;
			this._render();
		} else if (a === "tpl-import") {
			try {
				const res = await this._ws({
					type: "import_template",
					template_id: d.tpl
				});
				this._importMsg = {
					ok: true,
					text: t("m_tpl", {
						name: res.name,
						n: res.workouts.length
					})
				};
				this._templates = null;
				this._previewKey = null;
			} catch (err) {
				this._importMsg = {
					ok: false,
					text: err.message || String(err)
				};
			}
			this._render();
		} else if (a === "import") {
			try {
				const res = await this._ws({
					type: "import_plan",
					text: this._importText,
					lang: LANG
				});
				const im = res.images || {
					matched: 0,
					total: 0,
					missing: []
				};
				this._planTab = "mine";
				this._importMsg = {
					ok: true,
					text: t("m_imported", {
						name: res.name,
						n: res.workouts.length,
						m: im.matched,
						t: im.total
					}) + (im.missing.length ? t("m_missing", { list: im.missing.join(", ") }) : "") + "."
				};
				this._importText = "";
				this._previewKey = null;
			} catch (err) {
				this._importMsg = {
					ok: false,
					text: this._errText(err)
				};
			}
			this._render();
		} else if (a === "starter") {
			await this._loadStarter(true);
			this._importMsg = {
				ok: true,
				text: t("m_example")
			};
			this._render();
		} else if (a === "clear-import") {
			this._importText = "";
			this._starterUsed = true;
			this._importMsg = null;
			this._render();
		} else if (a === "plan-edit") {
			const res = await this._ws({
				type: "plan_source",
				plan_id: d.plan
			});
			this._importText = res.text;
			this._starterUsed = true;
			this._planTab = "import";
			this._importMsg = {
				ok: true,
				text: t("m_loaded")
			};
			this._render();
		} else if (a === "plan-delete") await this._ws({
			type: "delete_plan",
			plan_id: d.plan
		});
		else if (a === "goal") await this._ws({
			type: "set_weekly_goal",
			goal: Math.max(1, (this._state.weekly_goal || 3) + Number(d.d))
		});
		else if (a === "rest") await this._service("rest_adjust", { seconds: Number(d.d) });
		else if (a === "effort") {
			const msg = {
				type: "edit_set",
				set_id: Number(d.set),
				effort: d.v
			};
			if (d.session) msg.session_id = d.session;
			await this._ws(msg).catch(() => {});
			if (this._prompt && this._prompt.setId === Number(d.set)) this._closePrompt();
		} else if (a === "ed-effort") {
			this._editing.effort = d.v;
			this._render();
		} else if (a === "pp-select") {
			if (this._state && this._state.multi) this._viewPerson(d.p);
			else await this._ws({
				type: "profile",
				action: "select",
				profile: d.p
			}).catch(() => {});
		} else if (a === "pp-figure") await this._ws({
			type: "profile",
			action: "figure",
			profile: d.p,
			figure: d.v
		}).catch(() => {});
		else if (a === "pp-delete") await this._ws({
			type: "profile",
			action: "delete",
			profile: d.p
		}).catch(() => {});
		else if (a === "pp-rename" || a === "pp-add") {
			const prof = (this._state.profiles || []).find((x) => x.id === d.p);
			this._ppEdit = {
				id: prof ? prof.id : null,
				name: prof ? prof.name : ""
			};
			this._render();
			const inp = this.shadowRoot.querySelector("[data-field=\"pp-name\"]");
			if (inp) inp.focus();
		} else if (a === "pp-cancel") {
			this._ppEdit = null;
			this._render();
		} else if (a === "theme") this.dispatchEvent(new CustomEvent("hero-theme", {
			detail: d.v,
			bubbles: true,
			composed: true
		}));
		else if (a === "sound") this.dispatchEvent(new CustomEvent("hero-sound", {
			detail: d.on === "1",
			bubbles: true,
			composed: true
		}));
		else if (a === "glow") {
			this.dispatchEvent(new CustomEvent("hero-glow", {
				detail: d.on === "1",
				bubbles: true,
				composed: true
			}));
			this._render();
		} else if (a === "export") this.dispatchEvent(new CustomEvent("hero-export", {
			bubbles: true,
			composed: true
		}));
		else if (a === "import-backup") {
			const inp = this.shadowRoot.querySelector("[data-field=\"backup-file\"]");
			if (inp) inp.click();
		} else if (a === "disclaimer") this.dispatchEvent(new CustomEvent("hero-disclaimer", {
			bubbles: true,
			composed: true
		}));
		else if (a === "pp-save") {
			const ed = this._ppEdit;
			try {
				await this._ws(ed.id ? {
					type: "profile",
					action: "rename",
					profile: ed.id,
					name: ed.name
				} : {
					type: "profile",
					action: "add",
					name: ed.name
				});
				this._ppEdit = null;
				this._render();
			} catch (_) {}
		}
	}
	_confirmed(key) {
		if (this._armed && this._armed.key === key && Date.now() < this._armed.until) {
			this._armed = null;
			clearTimeout(this._armTimer);
			return true;
		}
		this._disarm();
		this._armed = {
			key,
			until: Date.now() + 4e3
		};
		clearTimeout(this._armTimer);
		this._armTimer = setTimeout(() => this._disarm(), 4e3);
		this._applyArmed();
		return false;
	}
	_armedButton() {
		return this._armed ? this.shadowRoot.querySelector(`[data-ck="${CSS.escape(this._armed.key)}"]`) : null;
	}
	_applyArmed() {
		const btn = this._armedButton();
		if (!btn) return;
		if (btn.dataset.label === void 0) btn.dataset.label = btn.innerHTML;
		btn.classList.add("armed");
		btn.textContent = btn.dataset.confirm;
	}
	_disarm() {
		const btn = this._armedButton();
		this._armed = null;
		if (btn && btn.dataset.label !== void 0) {
			btn.innerHTML = btn.dataset.label;
			delete btn.dataset.label;
			btn.classList.remove("armed");
		}
	}
	_onInput(e) {
		const el = e.target;
		if (el.dataset.field === "import") {
			this._importText = el.value;
			const btn = this.shadowRoot.querySelector("[data-a=\"import\"]");
			if (btn) btn.disabled = !el.value.trim();
			return;
		}
		if (el.dataset.lsearch) {
			this._q = this._q || {};
			this._q[el.dataset.lsearch] = el.value;
			this._applyListSearch(el.dataset.lsearch);
			return;
		}
		if (this._editor.input(el)) return;
		if (el.dataset.field === "pp-name" && this._ppEdit) this._ppEdit.name = el.value;
		else if (el.dataset.field && this._editing) this._editing[el.dataset.field] = el.value;
	}
	async _onChange(e) {
		const el = e.target;
		if (el.dataset.field === "pp-dev") {
			await this._ws({
				type: "profile",
				action: "devices",
				profile: el.dataset.p,
				[el.dataset.k]: el.value || null
			}).catch(() => {});
			el.blur();
			return;
		}
		if (el.dataset.field === "pp-link") {
			await this._ws({
				type: "link_profile",
				profile: el.dataset.p,
				user_id: el.value || null
			}).catch(() => {});
			el.blur();
			return;
		}
		if (this._editor.change(el)) {
			this._renderEditor();
			return;
		}
		if (el.dataset.field === "backup-file" && el.files && el.files[0]) {
			this.dispatchEvent(new CustomEvent("hero-import", {
				detail: el.files[0],
				bubbles: true,
				composed: true
			}));
			el.value = "";
			return;
		}
		if (el.dataset.field === "program-select" && el.value) {
			this._preview = null;
			await this._ws({
				type: "set_program",
				plan_id: el.value
			});
			el.blur();
		} else if (el.dataset.field === "workout-select" && el.value && this._state.next) {
			this._preview = null;
			await this._ws({
				type: "set_next",
				plan_id: this._state.next.plan_id,
				workout_id: el.value
			});
			el.blur();
		}
	}
	_findSet(sessionId, setId) {
		if (!sessionId) return (this._state.active?.sets || []).find((x) => x.id === setId);
		const sess = (this._history?.sessions || []).find((s) => s.id === sessionId);
		return sess && sess.sets.find((x) => x.id === setId);
	}
	_tickTimers() {
		const now = Date.now();
		this.shadowRoot.querySelectorAll("[data-until]").forEach((el) => {
			el.textContent = mmss((new Date(el.dataset.until).getTime() - now) / 1e3);
		});
		this.shadowRoot.querySelectorAll("[data-until-s]").forEach((el) => {
			el.textContent = Math.max(0, Math.ceil((new Date(el.dataset.untilS).getTime() - now) / 1e3));
		});
		this.shadowRoot.querySelectorAll("[data-fill-until]").forEach((el) => {
			const left = (new Date(el.dataset.fillUntil).getTime() - now) / 1e3;
			el.style.width = `${Math.min(100, Math.max(0, left / Number(el.dataset.total) * 100))}%`;
		});
		const active = (el, since) => {
			let ms = now - new Date(since).getTime() - Number(el.dataset.pausedS || 0) * 1e3;
			if (el.dataset.pausedAt) ms -= now - new Date(el.dataset.pausedAt).getTime();
			return Math.max(0, ms / 1e3);
		};
		this.shadowRoot.querySelectorAll("[data-since]").forEach((el) => {
			el.textContent = hms(active(el, el.dataset.since));
		});
		this.shadowRoot.querySelectorAll("[data-since-of]").forEach((el) => {
			const ratio = active(el, el.dataset.sinceOf) / Number(el.dataset.ref);
			el.style.width = `${Math.min(100, Math.max(0, ratio * 100))}%`;
			el.classList.toggle("over", ratio > 1);
			const box = el.closest(".elapsed");
			if (box) box.classList.toggle("over", ratio > 1);
		});
	}
	_render() {
		const focused = this.shadowRoot.activeElement;
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
		else body = this._state.active ? this._renderActive(this._state.active) : this._summary ? this._renderSummary() : this._renderIdle();
		const tab = (id, label) => `<button class="tab ${this._tab === id ? "on" : ""}" data-a="tab" data-tab="${id}">${label}</button>`;
		const shell = this._caps.shell === "ha-card" ? "ha-card" : "div";
		this.shadowRoot.innerHTML = renderIcons(`
      <style>${STYLE}</style>
      <${shell} class="card">
        <div class="tabs">${tab("training", t("tab_training"))}${tab("history", t("tab_history"))}${tab("plans", t("tab_plans"))}</div>
        <div class="body">${body}</div>${this._renderEffortPrompt()}
      </${shell}>`);
		if (this._armed) this._applyArmed();
		this._applyListSearch("plans");
		this._applyListSearch("templates");
		if (window.scrollY !== scrollY0) window.scrollTo(0, scrollY0);
		this._tickTimers();
	}
	_renderEditor() {
		const active = this.shadowRoot.activeElement;
		if (active && active.blur && active.tagName !== "SELECT") active.blur();
		this._render();
		if (this._editor.scroll) {
			const target = this._editor.scroll === "block" ? this.shadowRoot.querySelector(".eblock.open") : this.shadowRoot.querySelector(".subtabs");
			this._editor.scroll = false;
			if (target) target.scrollIntoView({
				block: "start",
				behavior: "instant"
			});
		}
	}
	async _openSummary(sessionId) {
		this._summary = {
			loading: true,
			id: sessionId
		};
		this._tab = "training";
		try {
			const res = await this._ws({
				type: "session_summary",
				session_id: sessionId
			});
			this._summary = res.summary;
		} catch (_) {
			this._summary = null;
		}
		this._render();
		window.scrollTo(0, 0);
		const s = this._summary;
		if (s && s.status === "finished" && !s.ended_early && this._caps.confetti) celebrate();
	}
	_renderSummary() {
		const s = this._summary;
		if (s.loading) return `<div class="pad muted">${t("loading")}</div>`;
		const early = s.status === "aborted" || s.ended_early;
		const head = early ? t("fin_early_h") : t(`fin_h${1 + s.seed % 6}`);
		const sub = early ? t("fin_early_s") : t(`fin_s${1 + Math.floor(s.seed / 6) % 3}`);
		const mins = (sec) => {
			const m = Math.max(1, Math.round(sec / 60));
			return m >= 60 ? `${Math.floor(m / 60)} h ${String(m % 60).padStart(2, "0")} min` : `${m} min`;
		};
		const bigKg = (v) => `${Math.round(v).toLocaleString(LOCALE)} kg`;
		const tile = (value, label) => `<div class="fin-tile"><b>${esc(value)}</b><span>${esc(label)}</span></div>`;
		const tiles = [
			tile(mins(s.duration_s), t("fin_duration")),
			early ? "" : tile(String(s.exercises), t("fin_exercises")),
			tile(String(s.sets), t("fin_sets")),
			s.reps ? tile(String(s.reps), t("fin_reps")) : "",
			s.time_s ? tile(s.time_s >= 60 ? mmss(s.time_s) + " min" : `${s.time_s} s`, t("fin_time")) : "",
			s.volume_kg ? tile(bigKg(s.volume_kg), t("fin_volume")) : ""
		].join("");
		const muscles = s.muscles.length ? `<div class="fin-sec"><div class="lbl">${t("fin_muscles")}</div><div class="fin-chips">${s.muscles.map((m) => `<span class="chip">${esc(t(`mg.${m}`))}</span>`).join("")}</div></div>` : "";
		const val = (kind, v) => kind === "weight" || kind === "e1rm" ? kg(v) : kind === "duration" ? `${v} s` : String(v);
		const records = s.records.length ? `<div class="fin-sec fin-rec"><div class="lbl">${t("fin_records")}</div><ul>${s.records.map((r) => `<li>${esc(t(`fin_rec_${r.kind}`, {
			name: r.name,
			v: r.kind === "weight" || r.kind === "e1rm" ? kg(r.value) : r.value,
			p: r.kind === "weight" || r.kind === "e1rm" ? kg(r.previous) : r.previous
		}))}</li>`).join("")}</ul></div>` : "";
		const better = s.improved.length ? `<div class="fin-sec"><div class="lbl">${t("fin_better")}</div><ul>${s.improved.map((x) => `<li><span>${esc(x.name)}</span><span class="fin-up">${esc(val(x.kind, x.before))} → <b>${esc(val(x.kind, x.now))}</b></span></li>`).join("")}</ul></div>` : "";
		const c = s.comparison;
		const vs = c ? `<div class="muted small">${esc(t("fin_vs_last", {
			date: date(c.date),
			d: mins(c.duration_s),
			n: c.sets
		}))}${c.volume_kg && s.volume_kg ? ` · ${esc(t("fin_vs_volume", {
			before: bigKg(c.volume_kg),
			now: bigKg(s.volume_kg)
		}))}` : ""}</div>` : "";
		const outlook = !early && s.outlook.length ? `<div class="fin-sec"><div class="lbl">${t("fin_next")}</div><div class="muted small">${t("fin_next_hint")}</div><ul>${s.outlook.map((o) => `<li class="${o.up ? "up" : ""}"><span>${esc(o.name)}</span><span class="muted small">${esc(sugText({
			key: o.key,
			params: o.params
		}))}</span></li>`).join("")}</ul></div>` : "";
		const week = s.week_done >= s.week_goal ? t("fin_week_done", { n: s.week_done }) : t("fin_week", {
			n: s.week_done,
			g: s.week_goal
		});
		const streak = s.streak_weeks ? t(s.streak_weeks === 1 ? "fin_streak1" : "fin_streak", { n: s.streak_weeks }) : "";
		return `<div class="pad fin ${early ? "early" : ""}">
        <div class="fin-head">
          ${early ? "" : `<div class="fin-badge">⟦trophy⟧</div>`}
          <h2>${esc(head)}</h2>
          <p>${esc(sub)}</p>
          <div class="fin-meta"><span class="badge ok">${t("fin_saved")}</span> <span class="muted small">${esc(s.workout_name)} · ${esc(s.plan_name)}</span></div>
        </div>
        <div class="fin-tiles">${tiles}</div>
        ${records}${better}${vs ? `<div class="fin-sec">${vs}</div>` : ""}${muscles}${outlook}
        <div class="fin-sec fin-cont"><span>${esc(week)}</span>${streak ? `<span>${streak}</span>` : ""}<span>${esc(t("fin_total", { n: s.total }))}</span></div>
        <button class="btn primary big fin-done" data-a="fin-done">${t("fin_done")}</button>
      </div>`;
	}
	_renderIdle() {
		const st = this._state;
		if (!st.plans.length) return `<div class="pad"><p>${t("no_plan")}</p>
        <button class="btn primary" data-a="go-templates">${t("import_plan")}</button></div>`;
		const progOpts = st.plans.map((p) => `<option value="${esc(p.id)}" ${p.id === st.program ? "selected" : ""}>${esc(p.name)}</option>`).join("");
		const pw = st.program_workouts || [];
		const cur = pw.find((w) => st.next && w.workout_id === st.next.workout_id);
		const after = cur ? pw[cur.position % pw.length] : null;
		const woOpts = pw.map((w) => `<option value="${esc(w.workout_id)}" ${cur && w.workout_id === cur.workout_id ? "selected" : ""}>${esc(w.name)} (${w.position}/${w.count})</option>`).join("");
		this._ensureStats();
		return `
      <div class="pad live">
        ${this._renderWho(st)}
        ${this._stats ? weekCard(this._stats) : ""}
        <div class="startrow">
          <label class="sel"><span class="lbl">${t("program")}</span><select data-field="program-select">${progOpts}</select></label>
          <label class="sel"><span class="lbl">${t("workout")}</span><select data-field="workout-select">${woOpts}</select></label>
          ${cur ? `<div class="wo-hint muted small"><span class="wo-pos">${t("wo_pos", {
			p: cur.position,
			n: cur.count
		})}</span>${pw.length > 1 && after ? `<span class="wo-sep"> · </span><span>${esc(t("wo_after", { name: after.name }).replace(/^\s*·\s*/, ""))}</span>` : ""}<span class="wo-auto">${t("wo_auto")}</span></div>` : ""}
          <button class="btn primary" data-a="start" ${this._readOnly ? "disabled" : ""}>${t("start")}</button>
        </div>
        ${this._renderPreview()}
        ${this._caps.voice ? st.default_satellite ? `<div class="muted small">${esc(t("voice_via", { sat: st.default_satellite }))}</div>` : `<div class="muted small">${t("no_sat")}</div>` : ""}
      </div>`;
	}
	_renderPreview(steps = this._preview) {
		if (!steps) return "";
		const blocks = [];
		for (const s of steps) {
			let b = blocks[blocks.length - 1];
			if (!b || b.block !== s.block) {
				b = {
					block: s.block,
					name: s.block_name,
					type: s.block_type,
					items: [],
					step: s
				};
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
				meta.push(s.sets ? t(s.sets === 1 ? "pv_set1" : "pv_sets", { n: s.sets }) : t("pv_sets_until", { n: s.block_end?.total_reps }));
				if (s.rest_after_s) meta.push(t("pv_rest", { d: dur(s.rest_after_s) }));
			} else if (b.type === "flow") {
				if (s.rounds > 1) meta.push(t("pv_rounds", { n: s.rounds }));
				meta.push(t("pv_flow", {
					n: (s.segments || []).length,
					m: Math.max(1, Math.round((s.total_s || 0) / 60))
				}));
			} else if (b.type === "interval") meta.push(t("pv_rounds", { n: s.rounds }), t("pv_interval", {
				w: s.work_s,
				r: s.rest_s
			}));
			else if (s.duration_s) meta.push(dur(s.duration_s));
			let body = "";
			if (b.type === "flow") body = `<ul>${(s.items || []).map((i) => `<li><span class="exn">${thumbBtn(this._imageFor(i.exercise, s), i.name)}<span>${esc(i.name)}</span></span>
            <span class="tgt">${esc(dur(i.duration_s))}${i.per_side ? ` ${esc(t("per_side"))}` : ""}</span></li>`).join("")}</ul>`;
			else if (b.type === "interval") {
				const seen = /* @__PURE__ */ new Set();
				body = `<ul>${(s.exercises || []).map((e, i) => [e, s.exercise_names[i]]).filter(([e]) => !seen.has(e) && seen.add(e)).map(([e, n]) => `<li><span class="exn">${thumbBtn(this._imageFor(e, s), n)}<span>${esc(n)}</span></span></li>`).join("") || `<li><span>${esc(s.exercise_names.join(" · "))}</span></li>`}</ul>`;
			} else if (b.items.length) body = `<ul>${b.items.map((i) => `<li><span class="exn">${thumbBtn(i.image, i.exercise_name)}<span>${esc(i.exercise_name)}</span></span><span class="tgt">${esc(targetText(i))}</span>
              ${i.suggestion && i.suggestion_key !== "plan_values" && i.suggestion !== "Planwerte (noch kein Verlauf)" ? `<div class="sug">${esc(stepSug(i))}</div>` : ""}</li>`).join("")}</ul>`;
			const note = s.block_note || (b.type === "warmup" || b.type === "cooldown" ? s.note : null);
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
		const pct = Math.round(100 * a.idx / Math.max(1, total));
		const iv = a.interval;
		const phase = a.paused ? t("ph_paused") : a.phase === "interval" && step.block_type === "flow" ? t("ty_flow") : t(`ph_${a.phase}`);
		let main;
		if (step.type === "set") {
			const h = a.hold && a.hold.sides === 2 && !a.rest_until ? a.hold : null;
			const sideNow = h && h.phase === "work" ? `<div class="side-now s${h.side}">${esc(t(`side_now_${h.side}`))}<span>${h.side}/2</span></div>` : h && h.phase === "switch" ? `<div class="side-now next">${esc(t("side_next_2"))}</div>` : "";
			main = `<div class="ex">${esc(step.exercise_name)}</div>${sideNow}
        ${this._muscleTags(step.muscles, step.muscles_secondary)}
        ${targetTiles(step)}
        ${step.tempo ? `<div class="chip">${esc(t("tempo", { t: step.tempo }))}</div>` : ""}
        ${step.suggestion ? `<div class="sug">${esc(stepSug(step))}</div>` : ""}`;
		} else if (step.type === "interval" && step.block_type === "flow") main = `<div class="ex">${esc(iv ? ivName(iv) : [...new Set(step.exercise_names)].join(" · "))}</div>
        ${iv ? "" : `<div class="tgt big">${esc(t("pv_flow", {
			n: (step.segments || []).length,
			m: Math.max(1, Math.round((step.total_s || 0) / 60))
		}))}</div>`}`;
		else if (step.type === "interval") main = `<div class="ex">${esc(iv ? ivName(iv) : step.exercise_names.join(" / "))}</div>
        ${iv ? "" : `<div class="tgt big">${step.rounds}× ${step.work_s} s / ${step.rest_s} s</div>`}`;
		else main = `<div class="ex">${esc(blockTitle(step.block_type, step.block_name))}</div>${step.duration_s ? `<div class="muted">${mmss(step.duration_s)} min</div>` : ""}`;
		const showLabel = step.type === "set" || step.type === "interval";
		const note = step.block_note && a.phase === "ready" ? step.block_note : step.note;
		const curImg = step.image || iv && iv.image || null;
		const timers = [
			a.paused ? `<div class="timer st st-paused">${t("ph_paused")}</div>` : a.phase === "interval" && iv && iv.ends_at ? (() => {
				const pos = step.block_type === "flow" ? `${iv.round}/${iv.rounds}` : t("pos_round_of", {
					r: iv.round,
					n: iv.rounds
				});
				return iv.phase === "work" ? `<div class="timer st st-go st-iv"><span>${t("st_go")} · ${esc(pos)}</span><span class="st-time" data-until="${esc(iv.ends_at)}"></span></div>` : `<div class="timer st st-rest st-iv"><span class="grow">${step.block_type === "flow" ? t("flow_switch") : t("t_rest")} <span class="st-time" data-until="${esc(iv.ends_at)}"></span></span></div>`;
			})() : a.hold && a.phase === "active" && !a.rest_until ? a.hold.phase === "ready" ? `<div class="timer st st-wait st-hold"><span class="grow">${t(step.per_side ? "hold_ready_sides" : "hold_ready")} <span class="st-time" data-until-s="${esc(a.hold.until)}"></span></span></div>` : a.hold.phase === "switch" ? `<div class="timer st st-rest st-hold st-switch"><span class="grow">${t("hold_switch")} <span class="st-time" data-until-s="${esc(a.hold.until)}"></span></span>
                <i class="st-fill" data-fill-until="${esc(a.hold.until)}" data-total="${a.hold.switch_total}"></i></div>` : `<div class="timer st st-go st-hold"><span>${a.hold.sides === 2 ? t(`hold_side_${a.hold.side}`) : t("hold_run")}</span><span class="st-time" data-until="${esc(a.hold.until)}"></span>
                <i class="st-fill" data-fill-until="${esc(a.hold.until)}" data-total="${a.hold.total}"></i></div>` : a.rest_until ? `<div class="timer st st-rest"><button class="tbtn" data-a="rest" data-d="-15" aria-label="${t("rest_less")}">−15</button>
          <span class="grow">${t("t_rest")} <span data-until="${esc(a.rest_until)}"></span></span>
          <button class="tbtn" data-a="rest" data-d="15" aria-label="${t("rest_more")}">+15</button></div>` : a.phase === "ready" ? `<div class="timer st st-wait">${t("st_wait")}</div>` : a.phase === "active" ? `<div class="timer st st-go">${t("st_go")}</div>` : "",
			a.block_until ? `<div class="timer cap">${t("t_left")} <span data-until="${esc(a.block_until)}"></span></div>` : "",
			a.block_expired && step.block_end?.time_cap_s && a.phase === "active" ? `<div class="timer cap">${t("t_up")}</div>` : "",
			a.pending_question !== null && a.pending_question !== void 0 ? `<div class="timer q">${t("t_question")}</div>` : ""
		].join("");
		const adjust = this._renderAdjust(a, step);
		const nextLabel = a.paused ? t("b_resume") : a.phase === "ready" ? t("b_go") : a.phase === "interval" ? t(step.block_type === "flow" ? "b_end_flow" : "b_end_hiit") : a.hold && a.hold.phase === "ready" && !a.rest_until ? t("b_hold_now") : a.hold && a.hold.phase === "switch" ? t("b_hold_side2") : a.hold && a.hold.phase === "work" ? t("b_hold_running") : a.rest_until && step.type === "set" && (step.target_duration || step.hold_max) ? t("b_hold_end_rest") : step.type === "set" ? a.adjust && a.adjust.changed && !(a.hold && a.hold.phase === "work") ? t("b_set_done_changed") : t("b_set_done") : t("b_next");
		const nxt = a.steps[a.idx + 1];
		const upnext = this._renderUpNext(nxt);
		const pts = step.exercise ? (this._state.exercise_history || {})[step.exercise] : null;
		const history = step.type === "set" ? historyCharts(pts) : "";
		const upcoming = a.steps.slice(a.idx + 2).filter((s) => s.type === "set").slice(0, 3).map((s) => `<li><span class="exn">${img(s.image)}<span>${esc(s.exercise_name)}</span></span><span class="tgt">${esc(targetText(s))}</span></li>`).join("");
		return `
      <div class="pad live">
        ${this._state.multi ? this._renderWho(this._state) : ""}
        <div class="row between"><div><b>${esc(a.workout_name)}</b> <span class="muted"><span class="sep">· </span>${esc(a.plan_name)}</span></div>
          <span class="row"><span class="badge ${a.paused ? "warn" : "info"}">${esc(phase)}</span>
          <span class="elapsed" title="${esc(t("el_title"))}">
            <span class="el-time">⟦timer⟧ <b data-since="${esc(a.started_at)}" data-paused-s="${a.paused_s || 0}" data-paused-at="${esc(a.paused_at || "")}"></b></span>
            ${this._state.last_same_duration_s ? `<span class="el-ref">${esc(t("el_last", { d: hms(this._state.last_same_duration_s) }))}</span>
              <span class="el-bar"><i data-since-of="${esc(a.started_at)}" data-paused-s="${a.paused_s || 0}" data-paused-at="${esc(a.paused_at || "")}" data-ref="${this._state.last_same_duration_s}"></i></span>` : ""}
          </span></span></div>
        <div class="bar"><div style="width:${pct}%"></div></div>
        <div class="blk-line"><span class="blk-info">${showLabel || step.block_name ? esc(blockTitle(step.block_type, step.block_name)) : ""}${step.type === "set" && position(step) ? ` · ${esc(position(step))}` : ""}</span>
          <span class="blk-step">${t("step", {
			i: Math.min(a.idx + 1, total),
			n: total
		})}</span></div>
        <div class="stage">
          <div class="current t-${esc(step.block_type || "")} ${curImg ? "has-img" : ""}">
            ${curImg ? `<div class="cur-img">${img(curImg, "pic", 0)}${img(curImg, "pic alt", 1)}</div>` : ""}
            <div class="cur-txt">
              ${main}${note ? `<div class="note" data-a="note" title="${esc(note)}">${esc(note)}</div>` : ""}
              ${history}
            </div></div>
          ${upnext}
        <div class="status">${timers}</div>
        ${this._readOnly ? `<div class="msg ro">${esc(t("ro_note", { name: this._personName() }))}</div><div class="controls" hidden>` : `<div class="controls">`}
          ${adjust}
          <button class="btn primary big" data-a="next" ${a.hold && a.hold.phase === "work" && !a.paused ? "disabled" : ""}>${nextLabel}</button>
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
	_renderUpNext(nxt) {
		let body;
		if (!nxt) body = `<div class="un-name">${t("un_done")}</div>`;
		else if (nxt.type === "set") body = `${nxt.image ? `<div class="un-img">${img(nxt.image, "pic")}</div>` : ""}
        <div class="un-name">${esc(nxt.exercise_name)}</div>
        <div class="un-tgt">${esc(targetText(nxt))}</div>
        <div class="un-pos">${esc(position(nxt))}</div>`;
		else body = `<div class="un-name">${esc(blockTitle(nxt.block_type, nxt.block_name))}</div>`;
		return `<div class="upnext t-${esc(nxt ? nxt.block_type : "")}"><div class="un-lbl">${t("un_label")}</div>${body}</div>`;
	}
	_renderAdjust(a, step) {
		const ghost = `<div class="adj-row ghost" aria-hidden="true"></div>`;
		const adj = a.adjust;
		if (step.type !== "set" || a.phase !== "active" || a.paused || !adj || !String(adj.key).startsWith(`${a.id}:${a.idx}:`)) return `<div class="adj">${ghost}${ghost}</div>`;
		const locked = a.hold && a.hold.phase === "work" ? "disabled" : "";
		const row = (k, label, value, unit, changed) => `
      <div class="adj-row">
        <span class="adj-lbl">${label}</span>
        <button class="btn round" data-a="adj" data-k="${k}" data-d="-1" ${locked} aria-label="${esc(t("a_less", { l: label }))}">−</button>
        <span class="adj-val ${changed ? "chg" : ""}">${esc(num(value))}${unit ? ` <small>${unit}</small>` : ""}</span>
        <button class="btn round" data-a="adj" data-k="${k}" data-d="1" ${locked} aria-label="${esc(t("a_more", { l: label }))}">+</button>
      </div>`;
		return `<div class="adj">${[adj.timed ? row("reps", t("a_seconds"), adj.duration, "s", adj.changed_reps) : row("reps", step.per_side ? t("a_reps_side") : t("a_reps"), adj.reps, "", adj.changed_reps), adj.weight !== null && adj.weight !== void 0 ? row("weight", t("a_weight"), adj.weight, "kg", adj.changed_weight) : ghost].join("")}</div>`;
	}
	_renderSets(sets, sessionId) {
		return `<table class="sets">${sets.map((x) => {
			const cls = STATUS[x.status] || "neutral";
			const label = STATUS[x.status] ? t(`st_${x.status}`) : x.status;
			const ed = this._editing;
			if (ed && ed.set_id === x.id && (ed.session_id || null) === (sessionId || null)) return `<tr class="editing"><td colspan="3"><div class="edit-panel">
            <div class="ename">${esc(x.exercise_name)}${position(x) ? ` <span class="muted">· ${esc(position(x))}</span>` : ""}</div>
            <div class="edit-fields">
              ${ed.timed ? `<label>${t("a_seconds")}<input data-field="duration_s" inputmode="numeric" value="${esc(ed.duration_s)}"></label>` : `<label>${t("a_reps")}<input data-field="reps" inputmode="numeric" value="${esc(ed.reps)}"></label>`}
              <label>kg<input data-field="weight_kg" inputmode="decimal" value="${esc(ed.weight_kg)}"></label>
            </div>
            <div class="edit-lbl">${t("ef_last")}</div>
            <div class="edit-effort">${[
				"easy",
				"normal",
				"hard"
			].map((v) => `<button class="chip-btn ef-${v} ${ed.effort === v ? "on" : ""}" data-a="ed-effort" data-v="${v}">${t(`ef_${v}`)}</button>`).join("")}</div>
            <button class="btn primary edit-save" data-a="edit-save">${t("e_save")}</button>
            <div class="edit-sec">
              <button class="btn" data-a="edit-skip">${t("e_skipped")}</button>
              <button class="btn" data-a="edit-cancel">${t("e_cancel")}</button>
            </div></div></td></tr>`;
			return `<tr ${this._readOnly ? "" : `data-a="edit"`} data-set="${x.id}" ${sessionId ? `data-session="${esc(sessionId)}"` : ""}>
          <td>${esc(x.exercise_name)}<div class="muted small">${esc(position(x))}</div></td>
          <td class="val">${x.record ? `<span class="trophy" title="${esc(t("t_record", { name: "" }))}">⟦trophy⟧</span> ` : ""}${esc(setValue(x))}${x.effort ? ` <span class="ef-dot ef-${x.effort}">${t(`ef_${x.effort}`)}</span>` : ""}</td><td><span class="badge ${cls}">${esc(label)}</span></td></tr>`;
		}).join("")}</table>`;
	}
	_renderHistory() {
		const h = this._history;
		if (!h) return `<div class="pad muted">${t("h_loading")}</div>`;
		if (!h.sessions.length) return `<div class="pad muted">${t("h_empty")}</div>`;
		const exRows = h.exercises.map((e) => {
			const last = e.last_sets.map(setValue).join(" · ");
			const s = e.suggestion;
			const next = s ? `${s.reps ? t("reps_n", { n: s.reps }) : ""}${s.weight_kg !== null && s.weight_kg !== void 0 ? ` · ${kg(s.weight_kg)}` : ""}` : "";
			return `<tr><td><div class="exn">${thumbBtn(e.image, e.name, "thumb lg")}<div><b>${esc(e.name)}</b><div class="muted small">${esc(t("h_ex_meta", {
				n: e.sessions,
				d: date(e.last_date)
			}))}${bestText(e.bests)}</div></div></div></td>
          <td data-label="${esc(t("h_th_hist"))}">${spark(e.points)}</td>
          <td class="small" data-label="${esc(t("h_th_last"))}">${esc(last)}</td>
          <td class="small" data-label="${esc(t("h_th_next"))}">${s ? `<b class="${s.increased ? "up" : ""}">${esc(next)}</b><div class="muted">${esc(reasonSug(s))}</div>` : ""}</td></tr>`;
		}).join("");
		const sessRows = h.sessions.map((s) => {
			const open = this._openSessions.has(s.id);
			const done = s.sets.filter((x) => x.status !== "skipped").length;
			const open_q = s.sets.filter((x) => x.status === "unconfirmed").length;
			return `<div class="sess">
          <div class="row between click" data-a="toggle-session" data-session="${esc(s.id)}">
            <div><b>${esc(date(s.started_at))}</b> <span class="muted">${esc(time(s.started_at))}</span> · ${esc(s.workout_name)} <span class="muted">(${esc(s.plan_name)})</span></div>
            <div>${sessionDuration(s) ? `<span class="dur">⟦timer⟧ ${esc(sessionDuration(s))}</span> · ` : ""}${t("h_sets", { n: done })} ${open_q ? `<span class="badge warn">${t("h_unconfirmed", { n: open_q })}</span>` : ""}${s.status === "aborted" ? ` <span class="badge muted">${t("h_aborted")}</span>` : ""} ${open ? "▴" : "▾"}</div>
          </div>
          ${open ? `${this._renderSets(s.sets, s.id)}<button class="btn danger small" data-a="delete-session" data-session="${esc(s.id)}" data-ck="ses-${esc(s.id)}" data-confirm="${esc(t("c_delete"))}">${t("h_delete")}</button>` : ""}
        </div>`;
		}).join("");
		const htab = (id, label, count) => `<button class="subtab ${this._histTab === id ? "on" : ""}" data-a="htab" data-tab="${id}">${label} <span class="cnt">${count}</span></button>`;
		const body = this._histTab === "overview" ? this._renderOverview() : this._histTab === "sessions" ? sessRows : `<table class="ex-table"><tr><th>${t("h_th_ex")}</th><th>${t("h_th_hist")} <span class="muted">${t("h_last8")}</span></th><th>${t("h_th_last")}</th><th>${t("h_th_next")}</th></tr>${exRows}</table>`;
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
				this._loadTemplates().finally(() => this._templatesLoading = false);
			}
			return `<div class="muted small">${t("tpl_loading")}</div>`;
		}
		const groups = {};
		this._tgOpen = this._tgOpen || /* @__PURE__ */ new Set();
		this._templates.forEach((tp) => (groups[tp.group_key || tp.group] = groups[tp.group_key || tp.group] || []).push(tp));
		return `${this._listTools("templates", `<div class="muted small">${t("p_tpl_intro")}</div>`)}<div data-list="templates">` + Object.entries(groups).map(([g, list]) => `<div class="tgroup ${this._tgOpen.has(g) ? "open" : ""}" data-group>
          <button class="tghead tg-toggle" data-a="tg-toggle" data-g="${esc(g)}" aria-expanded="${this._tgOpen.has(g)}"><span class="ico">${icon(ICON_OF[g] || "other", { ring: true })}</span>
            <span class="tg-txt"><span class="tgname">${esc(list[0].group_key ? t(`tg.${g}`) : g)} <span class="cnt">${list.length}</span></span>
            <span class="tgabout">${esc(list[0].group_key ? t(`tg.${g}.about`) : list[0].group_about || "")}</span></span>
            <span class="tg-chev" aria-hidden="true">›</span></button><div class="tg-body">${list.map((tp) => `<div class="tplw ${this._tplOpen === tp.id ? "open" : ""}" data-q="${esc([
			tp.name,
			tp.description || "",
			...tp.workouts
		].join(" ").toLowerCase())}"><div class="tpl">
            <button class="tpl-txt" data-a="tpl-open" data-tpl="${esc(tp.id)}" aria-expanded="${this._tplOpen === tp.id}"
              aria-label="${esc(t("tpl_open", { name: tp.name }))}"><span class="tpl-chev" aria-hidden="true">›</span><span>
              <b>${esc(tp.name)}</b> <span class="muted small">· ${t(tp.workouts.length === 1 ? "n_workout" : "n_workouts", { n: tp.workouts.length })}</span>
              <span class="muted small tpl-desc">${esc(tp.description || "")}</span></span></button>
            <button class="btn small ${tp.installed ? "" : "primary"}" data-a="tpl-import" data-tpl="${esc(tp.id)}"
              ${tp.installed ? `data-ck="tpl-${esc(tp.id)}" data-confirm="${esc(t("tpl_reload_c"))}"` : ""}>
              ${tp.installed ? t("tpl_installed") : t("tpl_take")}</button>
          </div>${this._tplOpen === tp.id ? this._renderTplDetail(tp.id) : ""}</div>`).join("")}</div></div>`).join("") + `<div class="empty" data-nohit hidden>${t("l_no_hit")}</div></div>`;
	}
	/** Aufgeklappte Vorlage: Workouts zum Umschalten, darunter Blöcke und Übungen mit Wdh./Gewicht/Zeit */
	_renderTplDetail(id) {
		const pv = (this._tplPreviews || {})[id];
		if (!pv) return `<div class="tpl-detail muted small">${t("tpl_loading_one")}</div>`;
		const wi = Math.min(this._tplWorkout || 0, pv.workouts.length - 1);
		const wo = pv.workouts[wi];
		return `<div class="tpl-detail">${pv.workouts.length > 1 ? `<div class="tpl-wos" role="tablist">${pv.workouts.map((w, i) => `<button class="chip-btn ${i === wi ? "on" : ""}" role="tab" aria-selected="${i === wi}"
            data-a="tpl-wo" data-i="${i}">${esc(w.name)}</button>`).join("")}</div>` : ""}
      ${pv.workouts.length > 1 ? "" : `<div class="tpl-woname">${esc(wo.name)}</div>`}
      ${wo.description ? `<div class="muted small">${esc(wo.description)}</div>` : ""}
      ${this._renderPreview(wo.steps)}</div>`;
	}
	/** Suchfeld (und optional Filter) über einer Liste; gefiltert wird direkt in der Seite, ohne neu zu zeichnen */
	_listTools(kind, extra) {
		this._q = this._q || {};
		return `<div class="ltools"><label class="ed-search">⟦search⟧<input type="search" data-lsearch="${kind}" value="${esc(this._q[kind] || "")}"
      placeholder="${esc(t(kind === "plans" ? "l_search_plans" : "l_search_tpl"))}" autocomplete="off"></label>${extra}</div>`;
	}
	_applyListSearch(kind) {
		const q = ((this._q || {})[kind] || "").trim().toLowerCase();
		const list = this.shadowRoot.querySelector(`[data-list="${kind}"]`);
		if (!list) return;
		let any = false;
		list.classList.toggle("searching", !!q);
		list.querySelectorAll("[data-q]").forEach((el) => {
			el.hidden = !!q && !q.split(/\s+/).every((w) => el.dataset.q.includes(w));
			any = any || !el.hidden;
		});
		list.querySelectorAll("[data-group]").forEach((g) => {
			const n = [...g.querySelectorAll("[data-q]")].filter((el) => !el.hidden).length;
			g.hidden = !n;
			const cnt = g.querySelector(".tgname .cnt");
			if (cnt) cnt.textContent = n;
		});
		const nohit = list.querySelector("[data-nohit]");
		if (nohit) nohit.hidden = any || !list.querySelector("[data-q]");
	}
	_muscleTags(primary, secondary) {
		primary = primary || [];
		secondary = secondary || [];
		if (!primary.length && !secondary.length) return "";
		this._ensureStats();
		const rec = {};
		(this._stats && this._stats.recovery || []).forEach((r) => rec[r.group] = r);
		const tag = (g, sec) => {
			const r = rec[g] || {
				status: "none",
				tier: null
			};
			const tip = `${t(sec ? "mt_secondary" : "mt_primary")} · ${t(`rc_${r.status}`)}`;
			return `<span class="mt ${tierClass(r)} ${sec ? "sec" : ""}" title="${esc(tip)}">${esc(t(`mg.${g}`))}</span>`;
		};
		return `<div class="mtags">${primary.map((g) => tag(g, false)).join("")}${secondary.map((g) => tag(g, true)).join("")}</div>`;
	}
	_imageFor(exercise, step) {
		const i = (step.exercises || []).indexOf(exercise);
		return i >= 0 ? (step.images || [])[i] || null : null;
	}
	/** Statistik neu berechnen, ohne sie vorher zu leeren; neu zeichnen nur bei Änderungen */
	_refreshStats() {
		if (!this._backend || this._statsLoading || !this._stats) return;
		this._statsLoading = true;
		const before = JSON.stringify(this._stats);
		this._ws({ type: "stats" }).then((r) => {
			this._stats = r;
			if (JSON.stringify(r) !== before) this._render();
		}).catch(() => {}).finally(() => this._statsLoading = false);
	}
	_ensureStats() {
		if (this._stats || this._statsLoading || !this._backend) return;
		this._statsLoading = true;
		this._ws({ type: "stats" }).then((r) => this._stats = r).catch(() => this._stats = null).finally(() => {
			this._statsLoading = false;
			this._render();
		});
	}
	_watchLogged(prev, state) {
		const a = state && state.active;
		const last = a && a.sets.length ? a.sets[a.sets.length - 1].id : 0;
		const seen = this._seenSet;
		this._seenSet = a ? {
			session: a.id,
			last
		} : null;
		if (!a || !seen || seen.session !== a.id || last <= seen.last) return;
		const rec = a.sets[a.sets.length - 1];
		if (!rec || rec.status === "skipped") return;
		const step = a.steps[rec.step];
		if (!step || step.type !== "set") return;
		this._prompt = {
			setId: rec.id,
			until: Date.now() + this._effortMs
		};
		clearTimeout(this._promptTimer);
		this._promptTimer = setTimeout(() => this._closePrompt(), this._effortMs);
	}
	_closePrompt() {
		clearTimeout(this._promptTimer);
		this._prompt = null;
		const el = this.shadowRoot.querySelector(".efp");
		if (el) el.remove();
	}
	_renderEffortPrompt() {
		const p = this._prompt;
		const a = this._state && this._state.active;
		if (!p || !a || this._readOnly) return "";
		const rec = a.sets.find((x) => x.id === p.setId);
		if (!rec) return "";
		const left = Math.max(0, p.until - Date.now());
		const cur = rec.effort || null;
		return `<div class="efp" role="dialog" aria-label="${esc(t("ef_last"))}">
      <button class="efp-x" data-a="efp-close" aria-label="${esc(t("ef_close"))}">⟦x⟧</button>
      <div class="efp-head"><span class="efp-q">${esc(t("ef_last"))}</span>
        <b>${esc(rec.exercise_name)}</b>
        <span class="muted small">${position(rec) ? `${esc(position(rec))} · ` : ""}${esc(setValue(rec))}</span></div>
      <div class="efp-btns">${[
			"easy",
			"normal",
			"hard"
		].map((v) => `<button class="chip-btn ef-${v} ${cur === v ? "on" : ""}" data-a="effort" data-set="${rec.id}" data-v="${v}">${t(`ef_${v}`)}</button>`).join("")}</div>
      <div class="efp-bar"><i style="animation-duration:${this._effortMs}ms;animation-delay:-${this._effortMs - left}ms"></i></div>
    </div>`;
	}
	_renderOverview() {
		this._ensureStats();
		const s = this._stats;
		if (!s) return `<div class="muted">${t("loading")}</div>`;
		this._state;
		const tile = (label, value, sub = "") => `<div class="tile"><div class="tile-l">${label}</div><div class="tile-v">${value}</div>${sub ? `<div class="tile-s">${sub}</div>` : ""}</div>`;
		const tiles = `<div class="tiles">
      ${tile(t("tile_week"), `${s.week.done}<small>/${s.week.goal}</small>`)}
      ${tile(t("tile_streak"), `⟦streak⟧ ${s.streak_weeks}`, s.streak_weeks === 1 ? t("tile_week1") : t("tile_weeks", { n: s.streak_weeks }))}
      ${tile(t("tile_total"), s.total, s.first ? t("tile_since", { d: date(s.first) }) : "")}
      ${tile(t("tile_time"), `${s.time.week_min}<small> min</small>`, s.time.avg_min !== null ? t("tile_time_avg", { m: s.time.avg_min }) : "")}
    </div>`;
		const recVal = (kind, v) => t(`rec_${kind}`, { v: num(v) });
		const records = s.records.length ? `<ul class="list recs">${s.records.map((r) => `<li><span>⟦trophy⟧ <b>${esc(r.name)}</b> <span class="muted small">${esc(date(r.date))}</span></span>
            <span>${esc(recVal(r.kind, r.value))} <span class="muted small">${esc(t("rec_prev", { v: num(r.previous) }))}</span></span></li>`).join("")}</ul>` : `<div class="muted small">${t("rec_none")}</div>`;
		const groups = GROUPS.filter((g) => s.volume[g]);
		const maxv = Math.max(12, ...groups.map((g) => s.volume[g].week));
		const volume = groups.length && groups.some((g) => s.volume[g].week) ? `<div class="vol">${groups.map((g) => {
			const v = s.volume[g];
			return `<div class="vb"><span class="vb-n">${t(`mg.${g}`)}</span>
              <div class="vb-bar"><div style="width:${100 * v.week / maxv}%"></div><i style="left:${1e3 / maxv}%"></i></div>
              <span class="vb-v"><b>${v.week}</b> <span class="muted small">${t("vol_last", { n: v.last_week })}</span></span></div>`;
		}).join("")}</div><div class="muted small">${t("vol_hint")}</div>` : `<div class="muted small">${t("vol_none")}</div>`;
		const un = s.unassigned || {
			sets: 0,
			names: []
		};
		const unassigned = un.sets ? `<div class="msg warnmsg small">${esc(t("vol_unassigned", {
			n: un.sets,
			list: un.names.join(", ")
		}))}</div>` : "";
		const ago = (h, status) => {
			if (h === null) return "";
			const since = status === "fresh" || status === "recovering";
			if (h < 48) return t(since ? "rc_since_h" : "rc_h", { n: h });
			return t(since ? "rc_since_d" : "rc_d", { n: Math.round(h / 24) });
		};
		const recovery = s.recovery.length ? `<div class="rc">${s.recovery.map((r) => `<div class="rc-i ${tierClass(r)}"><b>${t(`mg.${r.group}`)}</b><span>${t(`rc_${r.status}`)}</span><small>${ago(r.hours, r.status)}</small></div>`).join("")}</div>` : "";
		return `${weekCard(s)}${tiles}
      <div class="lbl">${t("rec_title")}</div>${records}
      <div class="lbl">${t("vol_title")}</div>${volume}${unassigned}
      ${recovery ? `<div class="lbl">${t("rc_title")}</div>${recovery}${tierLegend(s.recovery_tier_hours)}` : ""}`;
	}
	_autoSelectProfile(state) {
		const user = this._backend && this._backend.user;
		if (this._autoProfileDone || !this._caps.linkUsers || !user || state.multi) return;
		this._autoProfileDone = true;
		const mine = (state.profiles || []).find((p) => p.user_id && p.user_id === user.id);
		if (mine && mine.id !== state.profile && !state.active) this._ws({
			type: "profile",
			action: "select",
			profile: mine.id
		}).catch(() => {});
	}
	_loadHaUsers() {
		const user = this._backend && this._backend.user;
		if (this._haUsers !== void 0 || !user || !user.is_admin) return;
		this._haUsers = null;
		this._ws({ type: "ha_users" }).then((r) => this._haUsers = r.users).catch(() => this._haUsers = []).finally(() => this._render());
	}
	_personName(pid) {
		const st = this._state || {};
		return ((st.profiles || []).find((p) => p.id === (pid || st.profile)) || {}).name || "";
	}
	/** „Wer trainiert?“ – HU: Person wechseln; TA (mehrere gleichzeitig): ansehen, wer gezeigt wird */
	_renderWho(st) {
		if ((st.profiles || []).length < 2) return "";
		return `<div class="who"><span class="lbl">${t(st.multi ? "who_view" : "who")}</span>${st.profiles.map((p) => `<button class="chip-btn ${p.id === st.profile ? "on" : ""}" data-a="pp-select" data-p="${esc(p.id)}">${esc(p.name)}${st.multi && p.training ? ` <span class="dot-live" title="${esc(t("pp_training"))}"></span>` : ""}</button>`).join("")}</div>`;
	}
	_renderPeople() {
		const st = this._state;
		const ed = this._ppEdit;
		const user = this._backend && this._backend.user;
		if (this._caps.linkUsers) this._loadHaUsers();
		const users = this._haUsers || [];
		const userName = (id) => (users.find((u) => u.id === id) || {}).name;
		const link = (p) => {
			if (!this._caps.linkUsers) return "";
			if (user && user.is_admin) return `<label class="pp-link"><span class="muted small">${t("pp_user")}</span>
          <select data-field="pp-link" data-p="${esc(p.id)}"><option value="">${t("pp_user_none")}</option>${users.map((u) => `<option value="${esc(u.id)}" ${u.id === p.user_id ? "selected" : ""}>${esc(u.name)}</option>`).join("")}</select></label>`;
			return p.user_id ? `<div class="muted small">${esc(userName(p.user_id) ? t("pp_linked", { name: userName(p.user_id) }) : t("pp_linked_anon"))}</div>` : "";
		};
		const figure = (p) => `<div class="pp-fig"><span class="muted small">${t("pp_figure")}</span>${["m", "w"].map((f) => `<button class="chip-btn ${(p.figure || "m") === f ? "on" : ""}" data-a="pp-figure" data-p="${esc(p.id)}" data-v="${f}">${t(`fig_${f}`)}</button>`).join("")}</div>`;
		const form = (id) => `<div class="row pp-form">
        <input data-field="pp-name" placeholder="${esc(t("pp_name"))}" value="${esc(ed.name)}">
        <button class="btn small primary" data-a="pp-save">${t("pp_save")}</button>
        <button class="btn small" data-a="pp-cancel">${t("e_cancel")}</button></div>`;
		const multi = !!st.multi;
		const devices = (p) => {
			if (!this._caps.personDevices || !this._backend.entityOptions) return "";
			const sel = (field, list, label) => `<label class="pp-link"><span class="muted small">${label}</span>
        <select data-field="pp-dev" data-k="${field}" data-p="${esc(p.id)}"><option value="">${t("pp_default")}</option>${list.map((o) => `<option value="${esc(o.id)}" ${o.id === p[field] ? "selected" : ""}>${esc(o.name)}</option>`).join("")}
          ${p[field] && !list.some((o) => o.id === p[field]) ? `<option value="${esc(p[field])}" selected>${esc(p[field])}</option>` : ""}</select></label>`;
			return `<div class="pp-devs">${sel("satellite", this._backend.entityOptions("assist_satellite"), t("pp_sat"))}
        ${sel("light", this._backend.entityOptions("light"), t("pp_light"))}
        ${sel("notify", this._backend.entityOptions("notify"), t("pp_notify"))}</div>`;
		};
		const rows = (st.profiles || []).map((p) => {
			const on = p.id === st.profile;
			if (ed && ed.id === p.id) return `<div class="plan">${form(p.id)}</div>`;
			const pick = multi ? on ? "" : `<button class="btn small primary" data-a="pp-select" data-p="${esc(p.id)}">${t("pp_view")}</button>` : on ? "" : `<button class="btn small primary" data-a="pp-select" data-p="${esc(p.id)}" ${st.active ? "disabled" : ""}>${t("pp_select")}</button>`;
			return `<div class="plan row between"><div><b>${esc(p.name)}</b>${on ? ` <span class="badge ok">${t(multi ? "pp_viewing" : "pp_active")}</span>` : ""}
            ${multi && p.training ? ` <span class="badge info">${t("pp_training")}</span>` : ""}
            ${on ? `<div class="muted small">${t("pp_goal", { n: st.weekly_goal })}</div>` : ""}${link(p)}${figure(p)}${devices(p)}</div>
          <div class="row">${pick}
            <button class="btn small" data-a="pp-rename" data-p="${esc(p.id)}">${t("pp_rename")}</button>
            ${on || multi && p.training ? "" : `<button class="btn small danger" data-a="pp-delete" data-p="${esc(p.id)}" data-ck="pp-${esc(p.id)}" data-confirm="${esc(t("pp_c_delete"))}">${t("pp_delete")}</button>`}</div></div>`;
		}).join("");
		return `<div class="muted small">${t(multi ? "pp_intro_multi" : "pp_intro")}${this._caps.linkUsers ? ` ${t("pp_user_hint")}` : ""}${st.active && !multi ? ` ${t("pp_busy")}` : ""}</div>${rows}
      ${ed && !ed.id ? `<div class="plan">${form(null)}</div>` : `<button class="btn" data-a="pp-add">${t("pp_add")}</button>`}`;
	}
	_renderData() {
		const opts = this._options || {};
		const theme = opts.theme || "auto";
		return `
      <div class="lbl">${t("d_theme")}</div>
      <div class="row">${[
			"auto",
			"light",
			"dark"
		].map((v) => `<button class="chip-btn ${theme === v ? "on" : ""}" data-a="theme" data-v="${v}">${t(`d_theme_${v}`)}</button>`).join("")}</div>
      <div class="muted small">${t("d_theme_hint")}</div>
      <div class="lbl">${t("d_sound")}</div>
      <div class="row"><button class="chip-btn ${opts.sound ? "on" : ""}" data-a="sound" data-on="1">${t("d_sound_on")}</button>
        <button class="chip-btn ${opts.sound ? "" : "on"}" data-a="sound" data-on="0">${t("d_sound_off")}</button></div>
      <div class="muted small">${t("d_sound_hint")}</div>
      <div class="lbl">${t("d_glow")}</div>
      <div class="row"><button class="chip-btn ${opts.glow !== false ? "on" : ""}" data-a="glow" data-on="1">${t("d_sound_on")}</button>
        <button class="chip-btn ${opts.glow !== false ? "" : "on"}" data-a="glow" data-on="0">${t("d_sound_off")}</button></div>
      <div class="muted small">${t("d_glow_hint")}</div>
      <div class="lbl">${t("d_backup")}</div>
      <div class="muted small">${t("d_backup_hint")}</div>
      <div class="row"><button class="btn" data-a="export">${t("d_export")}</button>
        <button class="btn" data-a="import-backup" data-ck="restore" data-confirm="${esc(t("d_restore_c"))}">${t("d_import")}</button>
        <input type="file" accept="application/json,.json" data-field="backup-file" hidden></div>
      ${opts.lastBackup ? `<div class="muted small">${esc(t("d_last_backup", { d: date(opts.lastBackup) }))}</div>` : ""}
      <div class="lbl">${t("d_install")}</div>
      <div class="muted small">${t("d_install_hint")}</div>
      <div class="lbl">${t("d_about")}</div>
      <div class="muted small">${t("d_privacy")}</div>
      <div class="row"><button class="btn small" data-a="disclaimer">${t("d_disclaimer")}</button></div>`;
	}
	setOptions(options) {
		this._options = options;
		this._render();
	}
	/** Knopf „Eigenen Plan anlegen“: zum Editor bzw. (ohne Editor) zum Text-Import */
	_ownPlanButton(cls) {
		if (this._caps.editor) return `<button class="btn ${cls}" data-a="ptab" data-tab="editor">⟦editor⟧ ${t("l_to_editor")}</button>`;
		if (this._caps.yamlImport) return `<button class="btn ${cls}" data-a="ptab" data-tab="import">${t("p_own")}</button>`;
		return "";
	}
	_renderImport() {
		const base = this._backend.guideBase;
		if (this._starter === void 0 && !this._starterLoading) {
			this._starterLoading = true;
			this._loadStarter();
		}
		return `<div class="muted small">${t("p_import_intro")}</div>
      <div class="row dl">
        <a class="btn" href="${base}/${t("guide_file")}" download="${t("guide_dl")}" target="_blank" rel="noreferrer">${t("p_dl_guide")}</a>
        <a class="btn" href="${base}/${t("example_file")}" download="${t("example_dl")}" target="_blank" rel="noreferrer">${t("p_dl_example")}</a>
        <span class="grow"></span>
        <button class="btn small" data-a="starter">${t("p_insert")}</button>
        <button class="btn small" data-a="clear-import">${t("p_clear")}</button>
      </div>
      <textarea data-field="import" rows="22" spellcheck="false" placeholder="${esc(t("p_placeholder")).replace(/\n/g, "&#10;")}">${esc(this._importText)}</textarea>
      <button class="btn primary" data-a="import" ${this._importText.trim() ? "" : "disabled"}>${t("p_import")}</button>`;
	}
	async _loadStarter(force = false) {
		try {
			const text = await (await fetch(`${this._backend.guideBase}/${t("example_file")}`, { cache: "no-cache" })).text();
			this._starter = text;
			if (force || !this._importText.trim() && !this._starterUsed) {
				this._importText = text;
				this._starterUsed = true;
			}
		} catch (_) {
			this._starter = "";
		}
		this._render();
	}
	/** Sprache gewechselt (TA: Profil in Home Assistant): Texte, Vorlagen und unveränderten Beispielplan neu laden */
	languageChanged() {
		if (this._starter && this._importText === this._starter) {
			this._importText = "";
			this._starterUsed = false;
		}
		this._starter = void 0;
		this._starterLoading = false;
		this._templates = null;
		this._render();
	}
	_renderPlans() {
		const st = this._state;
		const filter = this._planFilter || "all";
		const shown = st.plans.filter((p) => filter === "all" || !p.template);
		const planHtml = (p) => `<div class="plan" data-q="${esc([
			p.name,
			p.description || "",
			...p.workouts.map((w) => w.name)
		].join(" ").toLowerCase())}">
          <div class="row between"><div><b>${esc(p.name)}</b>${p.id === st.program ? ` <span class="badge ok">${t("p_active")}</span>` : ""}${p.description ? `<div class="muted small">${esc(p.description)}</div>` : ""}
            ${p.images_missing && p.images_missing.length ? `<div class="muted small">${esc(t("p_noimg", { list: p.images_missing.join(", ") }))}</div>` : ""}</div>
            <div class="row">
            ${this._caps.editor ? `<button class="btn small" data-a="ed-open" data-plan="${esc(p.id)}">${p.template ? `⟦copy⟧ ${t("ed_edit_copy")}` : `⟦editor⟧ ${t("ed_edit")}`}</button>` : this._caps.yamlImport ? `<button class="btn small" data-a="plan-edit" data-plan="${esc(p.id)}">${t("p_edit")}</button>` : ""}
            <button class="btn small danger" data-a="plan-delete" data-plan="${esc(p.id)}" data-name="${esc(p.name)}" data-ck="plan-${esc(p.id)}" data-confirm="${esc(t("c_delete"))}">${t("p_delete")}</button></div></div>
          <ul class="list">${p.workouts.map((w) => {
			const isNext = st.next && st.next.plan_id === p.id && st.next.workout_id === w.id;
			return `<li><span>${esc(w.name)} ${isNext ? `<span class="badge info">${t("p_next_badge")}</span>` : ""}</span>
                <span>${isNext || this._readOnly ? "" : `<button class="btn small" data-a="next-workout" data-plan="${esc(p.id)}" data-workout="${esc(w.id)}">${t("p_set_next")}</button>`}
                ${st.active || this._readOnly ? "" : `<button class="btn small primary" data-a="start" data-plan="${esc(p.id)}" data-workout="${esc(w.id)}">${t("p_start")}</button>`}</span></li>`;
		}).join("")}</ul></div>`;
		const order = [.../* @__PURE__ */ new Set([...(this._templates || []).map((x) => x.group_key), "other"])];
		const byCat = {};
		shown.forEach((p) => (byCat[p.category || "other"] = byCat[p.category || "other"] || []).push(p));
		const plans = Object.keys(byCat).sort((a, b) => (order.indexOf(a) + 1 || 99) - (order.indexOf(b) + 1 || 99)).map((c) => `<div class="tgroup" data-group>
          <div class="tghead small"><span class="ico">${icon(ICON_OF[c] || "other", { ring: true })}</span>
            <div class="tgname">${esc(t(`tg.${c}`))} <span class="cnt">${byCat[c].length}</span></div></div>
          ${byCat[c].map(planHtml).join("")}</div>`).join("");
		const msg = this._importMsg ? `<div class="msg ${this._importMsg.ok ? "ok" : "err"}">${esc(this._importMsg.text)}</div>` : "";
		if (!this._planTab) this._planTab = st.plans.length ? "mine" : "templates";
		if (!this._templates && !this._templatesLoading) {
			this._templatesLoading = true;
			this._loadTemplates().finally(() => this._templatesLoading = false);
		}
		const ptab = (id, iconName, label, short, count) => `<button class="subtab ${this._planTab === id ? "on" : ""}" data-a="ptab" data-tab="${id}" aria-label="${esc(label)}">
         <span class="ico">${icon(ICON_OF[iconName] || "other")}</span> <span class="l-long">${label}</span><span class="l-short">${short}</span>${count !== null ? ` <span class="cnt">${count}</span>` : ""}</button>`;
		let body;
		if (this._planTab === "editor") body = this._editor.render(st);
		else if (this._planTab === "people") body = this._renderPeople();
		else if (this._planTab === "templates") body = this._renderTemplates();
		else if (this._planTab === "data" && this._caps.data) body = this._renderData();
		else if (this._planTab === "import" && this._caps.yamlImport) body = this._renderImport();
		else if (st.plans.length) body = `${this._listTools("plans", `<div class="row seg">
          <button class="chip-btn ${filter === "all" ? "on" : ""}" data-a="pfilter" data-f="all">${t("l_all")} <span class="cnt">${st.plans.length}</span></button>
          <button class="chip-btn ${filter === "own" ? "on" : ""}" data-a="pfilter" data-f="own">${t("l_own")} <span class="cnt">${st.plans.filter((p) => !p.template).length}</span></button></div>`)}<div data-list="plans">${plans || `<div class="empty">${t("l_no_own")}
        <div class="row">${this._ownPlanButton("primary")}</div></div>`}
        <div class="empty" data-nohit hidden>${t("l_no_hit")}</div></div>`;
		else body = `<div class="empty">${t("p_none")}
        <div class="row"><button class="btn primary" data-a="ptab" data-tab="templates">${t("p_pick_tpl")}</button>
        ${this._ownPlanButton("")}</div></div>`;
		return `<div class="pad">
      <div class="subtabs">
        ${ptab("mine", "mdi:clipboard-list-outline", t("p_tab_mine"), t("p_short_mine"), st.plans.length)}
        ${ptab("templates", "mdi:star-outline", t("p_tab_tpl"), t("p_short_tpl"), this._templates ? this._templates.length : null)}
        ${this._caps.editor ? ptab("editor", "editor", t("p_tab_editor"), t("p_short_editor"), null) : ""}
        ${this._caps.yamlImport ? ptab("import", "import", t("p_tab_own"), t("p_short_import"), null) : ""}
        ${ptab("people", "mdi:account-multiple-outline", t("p_tab_people"), t("p_short_people"), (st.profiles || []).length)}
        ${this._caps.data ? ptab("data", "data", t("p_tab_data"), t("p_short_data"), null) : ""}
      </div>
      ${msg}
      ${body}
    </div>`;
	}
};
var GROUPS = [
	"chest",
	"back",
	"shoulders",
	"biceps",
	"triceps",
	"core",
	"quads",
	"hamstrings",
	"glutes",
	"calves"
];
function bestText(b) {
	if (!b) return "";
	if (b.weight) return ` · ⟦trophy⟧ ${kg(b.weight)}`;
	if (b.reps) return ` · ⟦trophy⟧ ${t("reps_n", { n: b.reps })}`;
	if (b.duration) return ` · ⟦trophy⟧ ${b.duration} s`;
	return "";
}
function weekCard(stats) {
	const wk = stats && stats.week;
	if (!wk) return "";
	const R = 42, C = 2 * Math.PI * R, n = Math.max(1, wk.goal), gap = n > 1 ? 5 : 0;
	const seg = C / n - gap;
	const ring = Array.from({ length: n }, (_, i) => `<circle r="${R}" cx="50" cy="50" class="${i < wk.done ? "on" : ""}"
      stroke-dasharray="${seg.toFixed(2)} ${(C - seg).toFixed(2)}" stroke-dashoffset="${(-i * C / n).toFixed(2)}"/>`).join("");
	const extra = wk.done > wk.goal ? `<span class="wr-extra">+${wk.done - wk.goal}</span>` : "";
	const max = Math.max(1, ...wk.days.map((d) => d.sets));
	const bars = wk.days.map((d) => {
		const name = (/* @__PURE__ */ new Date(`${d.date}T12:00:00`)).toLocaleDateString(LOCALE, { weekday: "narrow" });
		const h = d.sets ? Math.max(10, Math.round(100 * d.sets / max)) : 0;
		const tip = d.workouts ? `${(d.names || []).filter(Boolean).join(", ")} · ${t("h_sets", { n: d.sets })}` : "";
		return `<div class="wb ${d.date === wk.today ? "today" : ""} ${d.date > wk.today ? "future" : ""}" title="${esc(tip)}">
        <span class="wb-n">${d.sets || ""}</span>
        <div class="wb-col">${h ? `<div style="height:${h}%"></div>` : `<i></i>`}</div>
        <span class="wb-d">${esc(name)}</span></div>`;
	}).join("");
	const vol = stats.volume || {};
	const groups = Object.keys(vol).filter((g) => vol[g].week).sort((a, b) => vol[b].week - vol[a].week);
	stats.streak_weeks && `${stats.streak_weeks === 1 ? t("wk_streak1") : t("wk_streak", { n: stats.streak_weeks })}`;
	return `<div class="week">
    <div class="wk-label">${t("wk_title")}</div>
    <div class="wk-head">
      <div class="wr">
        <svg viewBox="0 0 100 100" class="wr-svg" role="img" aria-label="${esc(t("wk_aria", {
		d: wk.done,
		n: wk.goal
	}))}">${ring}</svg>
        <div class="wr-c"><b>${wk.done}</b><span>/${wk.goal}</span>${extra}</div>
      </div>
      <div class="wk-info">
        ${stats.streak_weeks ? `<div class="wk-streak"><span class="wk-streak-l">${t("wk_streak_lbl")}</span>
          <b>${stats.streak_weeks === 1 ? t("tile_week1") : t("tile_weeks", { n: stats.streak_weeks })}</b></div>` : ""}
      </div>
      <div class="wk-goal" title="${esc(t("wk_goal"))}">
        <span class="wk-step"><button class="tbtn" data-a="goal" data-d="-1" aria-label="${t("wk_goal_less")}">−</button><b>${wk.goal}</b><button class="tbtn" data-a="goal" data-d="1" aria-label="${t("wk_goal_more")}">+</button></span>
        <span class="wk-goal-l">${t("wk_goal_short")}</span>
      </div>
    </div>
    <div class="wk-body">
      <div class="wk-cap">${t("wk_bars")}</div>
      <div class="wk-bars">${bars}</div>
      <div class="wk-foot"><span>${t("wk_total", { n: stats.total })}</span>
        ${groups.length ? `<span class="wk-tags">${groups.map((g) => `<span>${esc(t(`mg.${g}`))}</span>`).join("")}</span>` : ""}</div>
    </div></div>`;
}
function historyCharts(points) {
	const pts = points || [];
	if (!pts.length) return `<div class="cur-chart muted small">${t("c_first")}</div>`;
	const has = (k) => pts.some((p) => p[k] !== null && p[k] !== void 0);
	return `<div class="cur-chart">${[has("reps") ? spark(pts, ["reps", t("u_reps")], true) : has("duration_s") ? spark(pts, ["duration_s", "s"], true) : "", has("weight_kg") ? spark(pts, ["weight_kg", "kg"], true) : ""].join("")}</div>`;
}
function spark(points, forced = null, compact = false) {
	const pts = points || [];
	const auto = pts.some((p) => p.weight_kg !== null && p.weight_kg !== void 0) ? ["weight_kg", "kg"] : pts.some((p) => p.reps !== null && p.reps !== void 0) ? ["reps", t("u_reps")] : pts.some((p) => p.duration_s !== null && p.duration_s !== void 0) ? ["duration_s", "s"] : null;
	const metric = forced || auto;
	if (!metric) return "";
	const [key, unit] = metric;
	const vals = pts.map((p) => p[key]).filter((v) => v !== null && v !== void 0);
	const W = compact ? 120 : 150, H = compact ? 30 : 40, PX = 10, PY = compact ? 6 : 8;
	const min = Math.min(...vals), max = Math.max(...vals);
	const x = (i) => vals.length === 1 ? W / 2 : PX + i * (W - 20) / (vals.length - 1);
	const y = (v) => max === min ? H / 2 : PY + (max - v) * (H - 2 * PY) / (max - min);
	const line = vals.length > 1 ? `<polyline points="${vals.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(" ")}"/>` : "";
	const dots = vals.map((v, i) => `<circle cx="${x(i).toFixed(1)}" cy="${y(v).toFixed(1)}" r="${i === vals.length - 1 ? 3.2 : 2.2}"
      class="${i === vals.length - 1 ? "last" : ""}"><title>${esc(date(pts[i]?.date))}: ${esc(num(v))} ${unit}</title></circle>`).join("");
	const grid = max === min ? `<line x1="0" x2="${W}" y1="${H / 2}" y2="${H / 2}"/>` : `<line x1="0" x2="${W}" y1="${PY}" y2="${PY}"/><line x1="0" x2="${W}" y1="${H - PY}" y2="${H - PY}"/>`;
	const first = vals[0], last = vals[vals.length - 1];
	const best = Math.max(...vals);
	const label = compact ? vals.length === 1 || best === last ? t("c_last", {
		v: num(last),
		u: unit
	}) : t("c_last_best", {
		v: num(last),
		b: num(best),
		u: unit
	}) : first === last ? `${num(last)} ${unit}` : `${num(first)} → ${num(last)} ${unit}`;
	const trend = last > first ? "up" : last < first ? "down" : "";
	return `<div class="chart"><svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img"
      aria-label="${esc(t("c_aria", { l: label }))}"><rect width="${W}" height="${H}" rx="6"/>
      <g class="grid">${grid}</g>${line}${dots}</svg>
    <div class="chart-lbl ${trend}">${esc(label)}${compact ? "" : ` · ${vals.length === 1 ? t("c_1") : t("c_n", { n: vals.length })}`}</div></div>`;
}
var STYLE = `
  :host { display: block; }
  .card { overflow: clip; }
  .ico { line-height: 1; display: inline-flex; }
  .pi { width: 1.2em; height: 1.2em; vertical-align: -0.22em; flex: none; }
  .btn .pi, .tab .pi { margin-right: 2px; }
  .trophy .pi, .rec .pi { color: var(--ta-gold); }
  .wk-status .pi, .tile .pi { color: var(--primary-color); }
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
  textarea[data-field="import"] { font-family: var(--code-font-family, monospace); font-size: 0.85em; }
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
  .tg-side { font-size: .42em; font-weight: 600; margin-left: 3px; color: var(--primary-text-color); opacity: .85; }
  /* Liste „Danach“: Name darf kürzen, die Zielangabe bleibt rechts in derselben Zeile */
  .upc .list li { flex-wrap: nowrap; }
  .upc .exn > span:last-child { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .upc .tgt { flex-shrink: 0; white-space: nowrap; }
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
  .un-img .pic { width: 100%; height: 100%; object-fit: contain; }
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
  .subtab .ico { margin-right: 2px; }
  .subtab .l-short { display: none; }

  /* Schmale Ansicht (Handy oder schmale Spalte): Reiter auf ganzer Breite, Symbol über dem Text */
  :host { container-type: inline-size; }
  .subtabs { max-width: 100%; }
  @container (max-width: 560px) {
    .subtabs { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(0, 1fr); align-self: stretch; }
    .subtab { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3px;
              padding: 7px 4px; font-size: .78em; line-height: 1.15; text-align: center; min-width: 0;
              hyphens: auto; }
    .subtab .ico { margin: 0; }
    .subtab .cnt { display: none; }
    .subtab .l-long { display: none; }
    .subtab .l-short { display: inline; }
    .subtab { padding: 7px 2px; font-size: .74em; }
  }
  /* Listen: Suche, Filter, Gruppen */
  .ltools { display: flex; flex-direction: column; gap: 8px; }
  .ltools .seg { gap: 6px; }
  [data-q][hidden], [data-group][hidden], [data-nohit][hidden] { display: none; }
  .tghead.small { padding: 8px 10px; gap: 10px; }
  .tghead.small .tgname { font-size: 1em; }
  .tghead.small .pi.ring { width: 28px; height: 28px; }
  .tgroup > .plan { margin-top: 8px; }
  /* Editor */
  .ed { display: flex; flex-direction: column; gap: 10px; }
  .ed-sec { display: flex; flex-direction: column; gap: 10px; padding: 12px; border-radius: 12px;
            background: var(--secondary-background-color); }
  .fld { display: flex; flex-direction: column; gap: 4px; min-width: 0; font-size: .85em; color: var(--secondary-text-color); }
  .fld input, .fld select, .fld textarea { font-size: 1.1em; padding: 9px 10px; border-radius: 9px; width: 100%;
            box-sizing: border-box; border: 1px solid var(--divider-color); color: var(--primary-text-color); }
  .fld textarea { resize: vertical; }
  .fld-check { flex-direction: row; align-items: center; gap: 8px; align-self: end; padding-bottom: 10px; }
  .fld-check input { width: 20px; height: 20px; flex: none; accent-color: var(--primary-color); }
  .ed-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 10px; align-items: end; }
  .ed-chips .chip-btn { white-space: nowrap; }
  .ed-tools { gap: 6px; }
  .ed-tools .btn, .ed-ex .btn.icon { padding: 6px 10px; }
  .ed-blocks { display: flex; flex-direction: column; gap: 8px; }
  .eblock { padding: 0; }
  .eb-head { display: flex; align-items: center; gap: 8px; padding: 10px 12px; }
  .eb-txt { flex: 1; min-width: 0; }
  .eb-txt .pmeta { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .eblock.open .eb-txt .pmeta { white-space: normal; }
  .eb-chev { color: var(--secondary-text-color); }
  .eb-body { display: flex; flex-direction: column; gap: 12px; padding: 4px 12px 12px; }
  .ed-items { display: flex; flex-direction: column; gap: 10px; }
  .ed-item { display: flex; flex-direction: column; gap: 8px; padding: 10px; border-radius: 10px;
             background: var(--card-background-color); }
  .ed-ex { display: flex; align-items: center; gap: 8px; min-width: 0; }
  .ed-exname { flex: 1; min-width: 0; text-align: left; font: inherit; font-weight: 600; color: var(--primary-text-color);
               background: none; border: 0; border-bottom: 1px dashed var(--divider-color); padding: 6px 0; cursor: pointer; }
  .ed-add { display: flex; flex-wrap: wrap; gap: 8px; }
  .ed-addb { border-left: 4px solid var(--accent); }
  .fld-lbl { display: inline-flex; align-items: center; gap: 6px; }
  .info-btn { border: 0; background: none; padding: 0; color: var(--secondary-text-color); cursor: pointer; display: inline-flex; }
  .info-btn.on, .info-btn:hover { color: var(--primary-color); }
  .info-box { display: flex; flex-direction: column; gap: 6px; padding: 10px 12px; border-radius: 10px; font-size: .85em;
              border: 1px solid var(--divider-color); background: var(--card-background-color); }
  .fld select.unset { color: var(--secondary-text-color); }
  .ed-save { position: sticky; bottom: 0; padding: 10px 0 calc(10px + env(safe-area-inset-bottom));
             background: var(--card-background-color); display: flex; }
  .ed-save .btn { flex: 1; }
  .ed-search { display: flex; align-items: center; gap: 8px; padding: 0 12px; border-radius: 10px;
               border: 1px solid var(--divider-color); background: var(--card-background-color); color: var(--secondary-text-color); }
  .ed-search input { flex: 1; border: 0; background: none; padding: 11px 0; font-size: 1.05em; outline: none; }
  .exlist { display: flex; flex-direction: column; max-height: 50vh; overflow-y: auto; border-radius: 10px;
            border: 1px solid var(--divider-color); }
  .exitem { display: flex; align-items: stretch; gap: 4px; padding: 0 10px 0 6px; border-bottom: 1px solid var(--divider-color); }
  .exitem-pick { flex: 1; min-width: 0; display: flex; flex-direction: column; justify-content: center; padding: 8px 6px;
            border: 0; background: none; font: inherit; color: var(--primary-text-color); text-align: left; cursor: pointer; }
  .exitem-pick:hover { background: color-mix(in srgb, var(--primary-color) 8%, transparent); }
  /* Bild als eigene Schaltfläche (Vorschau) – klar getrennt von der Auswahl-Fläche daneben */
  .ex-img { flex: none; align-self: center; display: inline-flex; padding: 3px; margin: 3px 0; border: 1px solid transparent;
            border-radius: 10px; background: none; cursor: zoom-in; }
  .ex-img:hover, .ex-img:focus-visible { border-color: var(--primary-color); outline: none; }
  /* In Listen (Workout-Vorschau, Verlauf) ohne Abstand, damit alles bündig bleibt wie bei Zeilen ohne Bild */
  .exn .ex-img { padding: 0; margin: 0; border-radius: 9px; }
  .exitem[hidden] { display: none; }
  .empty { padding: 24px; text-align: center; color: var(--secondary-text-color); display: flex; flex-direction: column;
           gap: 12px; align-items: center; }
  .tpls summary { cursor: pointer; }
  .dl .grow { flex: 1; }
  a.btn { text-decoration: none; display: inline-flex; align-items: center; }
  .tgroup { margin-top: 16px; }
  .tghead { display: flex; gap: 12px; align-items: center; padding: 10px 12px; border-radius: 12px;
            background: var(--secondary-background-color); margin-bottom: 4px; }
  .tghead .ico { flex: none; color: var(--primary-color); }
  .tg-toggle { width: 100%; border: 0; font: inherit; color: inherit; text-align: left; cursor: pointer; }
  .tg-toggle:focus-visible { outline: 2px solid var(--primary-color); outline-offset: 2px; }
  .tg-txt { flex: 1; min-width: 0; display: flex; flex-direction: column; }
  .tg-chev { flex: none; font-size: 1.5em; line-height: 1; color: var(--secondary-text-color); transition: transform .15s; }
  .tgroup.open .tg-chev { transform: rotate(90deg); }
  .tgroup:not(.open) .tg-body { display: none; }
  .searching .tgroup .tg-body { display: block; }
  .searching .tg-chev { visibility: hidden; }
  [data-list="templates"] .tgroup + .tgroup { margin-top: 8px; }
  .tghead .ico .pi { width: 38px; height: 38px; }
  .tgname { font-size: 1.15em; font-weight: 700; }
  .tgname .cnt { font-size: .7em; font-weight: 500; color: var(--secondary-text-color); margin-left: 4px; }
  .tgabout { font-size: .85em; color: var(--secondary-text-color); }
  .tpl { padding-left: 12px; padding-right: 4px; }
  .tpl { display: flex; gap: 12px; align-items: center; justify-content: space-between; padding: 8px 0;
         border-bottom: 1px solid var(--divider-color); }
  .tpl { flex-wrap: wrap; row-gap: 4px; }
  .tpl .btn { margin-left: auto; }
  .tpl-txt { min-width: 0; flex: 1 1 240px; display: flex; gap: 8px; align-items: flex-start; text-align: left; padding: 4px 0;
             background: none; border: 0; font: inherit; color: inherit; cursor: pointer; border-radius: 8px; }
  .tpl-txt:focus-visible { outline: 2px solid var(--primary-color); outline-offset: 2px; }
  .tpl-desc { display: block; }
  .tpl-chev { flex: none; width: 1em; font-size: 1.3em; line-height: 1.1; color: var(--secondary-text-color);
              transition: transform .15s; }
  .tplw.open .tpl-chev { transform: rotate(90deg); }
  .tplw.open .tpl { border-bottom: 0; }
  .tpl-detail { padding: 4px 4px 14px 12px; border-bottom: 1px solid var(--divider-color); display: flex;
                flex-direction: column; gap: 8px; }
  .tpl-wos { display: flex; flex-wrap: wrap; gap: 6px; }
  .tpl-woname { font-weight: 600; }
  .tpl .btn { flex: none; }
  .startrow { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; align-items: end; }
  .startrow .btn, .startrow .wo-hint { grid-column: 1 / -1; }
  .wo-hint { margin-top: -4px; }
  .startrow .sel { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
  .startrow .sel .lbl { margin: 0; }
  /* Programm/Workout-Auswahl: etwas kleiner, damit lange Namen hineinpassen */
  .startrow .sel select { font-size: .88em; padding-top: 8px; padding-bottom: 8px; text-overflow: ellipsis; }
  @container (max-width: 560px) { .startrow .sel select { font-size: .8em; } }
  @container (max-width: 560px) { .startrow { grid-template-columns: 1fr 1fr; } .startrow .btn { grid-column: 1 / -1; } }
  .startrow .btn { padding: 12px; font-size: 1.1em; font-weight: 600; }
  .exn { display: flex; align-items: center; gap: 10px; min-width: 0; }
  .thumb { width: 40px; height: 40px; flex: none; border-radius: 8px; object-fit: contain; background: #fff; }
  .thumb.lg { width: 48px; height: 48px; }
  .thumb.noimg { background: transparent; }
  img.broken { visibility: hidden; }
  .current.has-img { flex-direction: row; align-items: stretch; gap: 14px; padding: 10px; }
  .cur-txt { flex: 1; min-width: 0; display: flex; flex-direction: column; justify-content: center; gap: 2px; }
  .cur-img { position: relative; width: 38%; flex: none; border-radius: 10px; overflow: hidden; background: #fff; }
  .cur-img .pic { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; object-position: center; }
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
  .week { display: grid; grid-template-columns: auto 1fr; gap: 14px 24px; align-items: center; border-radius: 16px;
          padding: 14px 16px; }
  .wr { position: relative; width: 104px; height: 104px; flex: none; }
  .week { background: var(--secondary-background-color); }
  .wk-label { grid-column: 1 / -1; margin-bottom: -6px; font-size: .75em; text-transform: uppercase;
               letter-spacing: .06em; color: var(--secondary-text-color); }
  .wk-head { display: grid; grid-template-columns: auto 1fr auto; align-items: center; gap: 16px; min-width: 0; }
  .wk-info { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
  .wk-title { font-weight: 700; font-size: 1.1em; }
  .wk-streak { display: flex; flex-direction: column; gap: 1px; line-height: 1.2; }
  .wk-streak-l { font-size: .75em; color: var(--secondary-text-color); white-space: nowrap; }
  .wk-streak b { font-size: 1.05em; white-space: nowrap; }
  .wk-streak .pi { color: var(--primary-color); }
  .wk-status { font-size: .85em; color: var(--secondary-text-color); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  /* Ziel oben rechts: Beschriftung über dem Regler, bündig mit „Diese Woche“ */
  .wk-goal { display: flex; flex-direction: column; align-items: center; gap: 4px; align-self: start; margin-top: -18px; }
  .wk-goal-l { order: -1; }
  .wk-goal-l { font-size: .72em; color: var(--secondary-text-color); line-height: 1.2; white-space: nowrap; }
  .wk-step { display: inline-flex; align-items: center; gap: 4px; padding: 2px; border-radius: 10px;
             background: var(--card-background-color); border: 1px solid var(--divider-color); }
  .wk-step b { min-width: 1.6em; text-align: center; font-size: 1.05em; }
  .wk-step .tbtn { width: 30px; height: 30px; }
  .wk-body { display: flex; flex-direction: column; gap: 6px; min-width: 0; }
  .wk-foot { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; font-size: .8em; color: var(--secondary-text-color); }
  @container (max-width: 560px) {
    .week { grid-template-columns: 1fr; gap: 14px; }
    .wr { width: 88px; height: 88px; }
    .wr-c b { font-size: 1.8em; }
  }
  .wr-svg { width: 100%; height: 100%; transform: rotate(-90deg); }
  .wr-svg circle { fill: none; stroke: var(--divider-color); stroke-width: 9; stroke-linecap: butt; }
  .wr-svg circle.on { stroke: var(--primary-color); }
  .wr-c { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; line-height: 1; }
  .wr-c b { font-size: 2.1em; font-weight: 700; }
  .wr-c span { font-size: 1.1em; color: var(--secondary-text-color); margin-left: 1px; }
  .wr-extra { position: absolute; bottom: 22px; font-size: .75em !important; color: var(--primary-color) !important; }
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
  .wk-tags { display: flex; flex-wrap: wrap; gap: 4px; }
  .wk-tags span { font-size: .75em; padding: 2px 8px; border-radius: 10px; background: var(--card-background-color);
                  border: 1px solid var(--divider-color); color: var(--secondary-text-color); }
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
  /* Erholung in 6 Stufen (rot → grün), hell und dunkel getrennt abgestimmt */
  /* Werte in styles.css (--rt-0 … --rt-5, je für hell und dunkel); Rückfall = helle Fassung */
  .rt-0 { --rc: var(--rt-0, #d32f2f); } .rt-1 { --rc: var(--rt-1, #ef6c00); } .rt-2 { --rc: var(--rt-2, #e0a800); }
  .rt-3 { --rc: var(--rt-3, #a4b400); } .rt-4 { --rc: var(--rt-4, #66bb3a); } .rt-5 { --rc: var(--rt-5, #1b7f2a); }
  .rc-none { --rc: var(--divider-color); }
  .rt-legend { display: flex; flex-wrap: wrap; gap: 4px 12px; margin-top: 6px; }
  .rt-legend span { display: inline-flex; align-items: center; gap: 5px; }
  .rt-legend i { width: 10px; height: 10px; border-radius: 50%; background: var(--rc); display: inline-block; }
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
  .pp-fig { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; margin-top: 6px; }
  .pp-link { display: flex; align-items: center; gap: 8px; margin-top: 6px; }
  .pp-devs { display: flex; flex-direction: column; gap: 2px; }
  .controls[hidden] { display: none; }
  .msg.ro { text-align: center; }
  .dot-live { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #66bb6a; margin-left: 4px;
              vertical-align: 1px; animation: ta-pulse 1.4s ease-in-out infinite; }
  .pp-link select { width: auto; max-width: 220px; padding: 4px 8px; }
  .timer .grow { flex: 1; text-align: center; }
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
  .timer.st-hold { position: relative; overflow: hidden; justify-content: space-between; }
  /* Abschluss nach dem Training */
  .fin { display: flex; flex-direction: column; gap: 14px; }
  .fin-head { text-align: center; padding: 8px 0 4px; }
  .fin-head h2 { margin: 6px 0 4px; font-size: 1.7em; line-height: 1.2; }
  .fin-head p { margin: 0 0 10px; color: var(--secondary-text-color); }
  .fin.early .fin-head h2 { font-size: 1.4em; }
  .fin-badge { display: inline-flex; color: var(--primary-color); animation: fin-pop .5s ease-out both; }
  .fin-badge .pi { width: 56px; height: 56px; }
  @keyframes fin-pop { from { transform: scale(.4); opacity: 0; } 70% { transform: scale(1.1); } }
  @media (prefers-reduced-motion: reduce) { .fin-badge { animation: none; } }
  .fin-meta { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; align-items: center; }
  .fin-tiles { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
  @container (max-width: 560px) { .fin-tiles { grid-template-columns: 1fr 1fr; } }
  .fin-tile { display: flex; flex-direction: column; gap: 2px; padding: 10px 12px; border-radius: 12px;
              background: var(--secondary-background-color); min-width: 0; }
  .fin-tile b { font-size: 1.35em; font-variant-numeric: tabular-nums; }
  .fin-tile span { font-size: .8em; color: var(--secondary-text-color); }
  .fin-sec ul { list-style: none; margin: 4px 0 0; padding: 0; }
  .fin-sec li { display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap; padding: 5px 0;
                border-bottom: 1px solid var(--divider-color); }
  .fin-sec li:last-child { border-bottom: 0; }
  .fin-sec li.up > span:first-child::before { content: "↑ "; color: var(--primary-color); font-weight: 700; }
  .fin-up b { color: var(--primary-color); }
  .fin-rec { border-radius: 12px; padding: 10px 12px; background: color-mix(in srgb, var(--primary-color) 12%, transparent); }
  .fin-rec .lbl { color: var(--primary-color); }
  .fin-chips { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }
  .fin-cont { display: flex; flex-direction: column; gap: 4px; align-items: center; text-align: center;
              color: var(--secondary-text-color); font-size: .9em; }
  .fin-cont .pi { width: 1.1em; height: 1.1em; vertical-align: -0.18em; color: var(--primary-color); }
  .fin-done { width: 100%; }
  .side-now { align-self: center; display: inline-flex; align-items: baseline; gap: 6px; margin: 2px auto 4px; padding: 2px 12px;
              border-radius: 999px; font-size: .95em; font-weight: 700; color: var(--primary-color);
              border: 1px solid color-mix(in srgb, var(--primary-color) 45%, transparent); }
  .side-now span { font-size: .8em; font-weight: 500; color: var(--secondary-text-color); }
  .side-now.next { color: var(--secondary-text-color); border-color: var(--divider-color); font-weight: 600; }
  .timer.st-hold .st-time { font-size: 1.35em; font-weight: 800; letter-spacing: 0; font-variant-numeric: tabular-nums; }
  .timer.st-hold.st-wait .grow { display: flex; align-items: center; justify-content: center; gap: 10px; }
  .st-fill { position: absolute; left: 0; bottom: 0; height: 4px; width: 100%; background: var(--st);
             transition: width .25s linear; }
  .trophy { font-size: .95em; }
  :host { --ta-gold: #e8b44f; }
  /* Unter dem Fortschrittsbalken: Block und Position (wie der Programmname, klein), rechts der Schritt */
  .blk-line { display: flex; justify-content: space-between; gap: 8px; margin-top: -4px; font-size: .85em;
              color: var(--secondary-text-color); }
  .blk-info { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .blk-step { white-space: nowrap; flex: none; }
  .current .note.open { -webkit-line-clamp: unset; display: block; overflow: visible; }
  /* Startseite auf dem Handy: Woche kompakt, Hinweis kurz – damit „Training starten“ ohne Scrollen sichtbar ist */
  @container (max-width: 560px) {
    .week { gap: 10px; padding: 12px 14px; }
    .wk-head { gap: 8px; }
    .wr { width: 68px; height: 68px; }
    .wr-c b { font-size: 1.4em; }
    .wr-c span { font-size: .9em; }
    .wr-extra { bottom: 12px; }
    .wk-title { font-size: 1em; }
    .wk-status { font-size: .8em; line-height: 1.3; }
    .wk-step .tbtn { width: 26px; height: 26px; }
    .wk-cap { display: none; }
    .wb-col { height: 30px; }
    .wb-n { height: .9em; }
    .wb-d { width: 18px; height: 18px; font-size: .72em; }
    .wk-foot { display: none; }
    .wo-pos, .wo-sep, .wo-auto { display: none; }
  }
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
         /* invertierte Farben: im dunklen Design hell (im hellen dunkel) – sticht hervor */
         --efp-bg: var(--primary-text-color); --efp-fg: var(--card-background-color);
         background: var(--efp-bg); color: var(--efp-fg); border: 0;
         border-radius: 16px; box-shadow: 0 12px 40px rgba(0,0,0,.6), 0 0 0 4px color-mix(in srgb, var(--primary-color) 55%, transparent);
         overflow: hidden; animation: efp-in .18s ease-out; }
  .efp .muted { color: color-mix(in srgb, var(--efp-fg) 65%, var(--efp-bg)); }
  .efp-head { display: flex; flex-direction: column; gap: 2px; margin-bottom: 10px; }
  .efp-head b { font-size: 1.15em; }
  .efp-q { font-size: 1.25em; font-weight: 800; margin-bottom: 2px; padding-right: 36px; }
  .efp-x { position: absolute; top: 8px; right: 8px; width: 36px; height: 36px; border: 0; border-radius: 50%;
           background: none; color: var(--efp-fg); display: flex; align-items: center; justify-content: center; cursor: pointer; }
  .efp-x:hover { background: color-mix(in srgb, var(--efp-fg) 10%, var(--efp-bg)); }
  .efp-x .pi { width: 1.3em; height: 1.3em; }
  .efp-btns { display: flex; gap: 8px; margin-bottom: 12px; }
  .efp-btns .chip-btn { flex: 1; padding: 12px 6px; font-size: 1.02em; font-weight: 700; text-align: center;
                        background: transparent; color: var(--efp-fg); border: 2px solid color-mix(in srgb, var(--efp-fg) 25%, var(--efp-bg)); }
  .efp-btns .chip-btn.ef-easy { border-color: #4caf50; color: #2e7d32; }
  .efp-btns .chip-btn.ef-hard { border-color: #ef5350; color: #c62828; }
  .efp-btns .chip-btn.on { color: #fff; }
  .efp-bar { height: 5px; margin: 0 -14px; background: color-mix(in srgb, var(--efp-fg) 15%, var(--efp-bg)); }
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
    .blk-step { display: none; }
    .el-time { font-size: 1.4em; }
    .current { height: auto; min-height: 132px; } /* wächst mit, statt Text abzuschneiden */
    .current.has-img { align-items: center; }
    .current.has-img .cur-img { align-self: stretch; min-height: 116px; max-height: 150px; }
    .current .note { white-space: normal; cursor: pointer; }
    .mtags { margin: 0; }
    /* Zielwert kompakt: Zahl groß, darunter „Wdh. · Ziel 15–30“ in einer Zeile */
    .tg-v { display: grid; grid-template-columns: auto auto; justify-content: center; column-gap: 4px; }
    .tg-v b { grid-column: 1 / -1; justify-self: center; }
    .tg-v em::before { content: "· "; }
    .current.has-img { gap: 10px; padding: 8px; }
    .cur-img { width: 32%; }
    .current .ex { font-size: 1.15em; }
    .current .sug { display: none; }
    .current .note { font-size: .8em; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; }
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
// src/card/card.js
var DOMAIN = "training_assistant";
var CARD_VERSION = "0.12.1";
var CAPS = {
	voice: true,
	yamlImport: true,
	linkUsers: true,
	editor: true,
	personDevices: true,
	data: false,
	confetti: false,
	effortMs: 5e3,
	shell: "ha-card"
};
/** Fehler von Home Assistant ({code, message, translation_key, translation_placeholders}) → Error mit Text */
function haError(err) {
	if (err instanceof Error) return err;
	const message = err && (err.message || err.code) || String(err);
	return Object.assign(new Error(message), {
		code: err && err.code,
		key: err && err.translation_key,
		params: err && err.translation_placeholders || {}
	});
}
function haBackend(card) {
	let person = null;
	const withPerson = (data) => person ? {
		person,
		...data
	} : data;
	return {
		setPerson(pid) {
			person = pid;
		},
		async ws(msg) {
			try {
				return await card._hass.callWS(withPerson({
					...msg,
					type: `${DOMAIN}/${msg.type}`
				}));
			} catch (err) {
				if (err && err.code === "invalid_plan") throw Object.assign(new Error(err.message), {
					key: "plan_invalid",
					params: { errors: err.message }
				});
				throw haError(err);
			}
		},
		serviceErrorsShown: true,
		service: (name, data = {}) => card._hass.callService(DOMAIN, name, withPerson(data)).catch((err) => {
			throw haError(err);
		}),
		subscribe(cb, onError) {
			const sub = card._hass.connection.subscribeMessage((state) => {
				if (!person) person = state.profile;
				cb(state);
			}, withPerson({ type: `${DOMAIN}/subscribe` }));
			sub.catch((err) => onError && onError(err));
			return () => sub.then((unsub) => unsub()).catch(() => {});
		},
		toast: (message) => card.dispatchEvent(new CustomEvent("hass-notification", {
			detail: { message },
			bubbles: true,
			composed: true
		})),
		imgBase: `/${DOMAIN}/pictos/${CARD_VERSION}`,
		guideBase: `/${DOMAIN}/guide`,
		/** Auswahl für Satellit/Lampe/Handy-Hinweis einer Person */
		entityOptions(domain) {
			const hass = card._hass;
			if (domain === "notify") return Object.keys(hass.services && hass.services.notify || {}).sort().map((id) => ({
				id,
				name: id
			}));
			return Object.values(hass.states || {}).filter((st) => st.entity_id.startsWith(`${domain}.`)).map((st) => ({
				id: st.entity_id,
				name: st.attributes && st.attributes.friendly_name || st.entity_id
			})).sort((a, b) => a.name.localeCompare(b.name));
		},
		get user() {
			const u = card._hass && card._hass.user;
			return u ? {
				id: u.id,
				is_admin: !!u.is_admin
			} : null;
		},
		caps: CAPS
	};
}
var TrainingAssistantCard = class extends TrainerUI {
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
		this._hass = hass;
		const before = this._lang;
		this._lang = setLanguage(hass.locale && hass.locale.language || hass.language || "en");
		if (first) this.connect(haBackend(this));
		else if (before !== this._lang) this.languageChanged();
	}
};
if (!customElements.get("training-assistant-card")) {
	customElements.define("training-assistant-card", TrainingAssistantCard);
	window.customCards = window.customCards || [];
	window.customCards.push({
		type: "training-assistant-card",
		name: "TrainingAssistant",
		description: "Live workout, history and training plans",
		preview: false
	});
	console.info(`%c TRAINING-ASSISTANT-CARD %c ${CARD_VERSION} `, "background:#03a9f4;color:#fff", "");
}
