# Task Plot Review

## Evidence Match

- Pass: title and construct match the investor-side Trust Game.
- Pass: rows match configured high, medium, and low return partner profiles.
- Pass: phase order matches README and `src/run_trial.py`: Partner cue -> Fixation -> Trust decision -> Confirmation -> Outcome feedback -> ITI.
- Pass: timing labels match config: 600 ms cue, 600 ms fixation, 2000 ms decision, 500 ms confirmation, 1000 ms feedback, 800 ms ITI.
- Pass: decision key mapping shows F invest and J keep.
- Pass: outcome feedback shows invested x3, returned amount, trial earnings, and cumulative total without invented fixed earnings values.

## Visual Quality

- Pass: labels and timings are readable.
- Pass: generated timeline content stays below the header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
