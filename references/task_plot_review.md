# Task Plot Review

## Evidence Match

- Pass: title and construct match the Antisaccade Task.
- Pass: rows reflect prosaccade, antisaccade, and timeout behavior.
- Pass: phase order matches README and `src/run_trial.py`: Fixation -> Rule cue -> Gap -> Saccade response -> ITI.
- Pass: timing labels match config: 800-1200 ms fixation, 400-600 ms rule cue, 150-250 ms gap, 1000 ms response, 600 ms ITI.
- Pass: response mapping shows F=left and J=right.
- Pass: pro/anti rules distinguish same-side and opposite-side target responses.
- Pass: no feedback stage or extra response keys are shown.

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
