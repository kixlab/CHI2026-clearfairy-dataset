# Datasheet — ClearFairy Cognitive Decision Steps

This datasheet follows the [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) framework (Gebru et al., 2021).

## Motivation

**For what purpose was the dataset created?**
The dataset was created as part of the ClearFairy research project, which studies how to capture and structure the cognitive workflow of designers as they work in Figma. The dataset releases the *inferred decision steps* that ClearFairy produces from raw Figma action logs, enabling other researchers to study designer reasoning, build models of creative cognition, or evaluate alternative rationale-inference methods.

**Who created the dataset and on behalf of which entity?**
The dataset was created by the authors of the ClearFairy paper (Son et al., CHI 2026). Corresponding author: Kihoon Son, KAIST (kihoon.son@kaist.ac.kr).

**Who funded the creation of the dataset?**
See the acknowledgments section of the ClearFairy paper.

## Composition

**What do the instances represent?**
Each instance is a single *cognitive decision step* inferred from a designer's activity. A step bundles a description of the designer's actions, an inferred rationale, and a narrative of how the step fits into the broader design progression.

**How many instances are there in total?**
417 decision steps across 12 participants.

**Does the dataset contain all possible instances or is it a sample?**
It is a sample. Each participant completed one design session, and the system inferred decision steps from that session's action log. The number of steps per session ranges from 21 to 45.

**What data does each instance consist of?**
Each instance is a JSON object with the following fields:

- `participant_id` (string) — anonymous participant identifier
- `task_type` (string) — `lab_website` or `shopping_site`
- `step_index` (integer) — ordinal position within the session
- `decision_and_actions` (string) — description of the actions
- `rationale` (string) — inferred reasoning
- `progression` (string) — inferred narrative of how the step fits the workflow

**Is there a label or target associated with each instance?**
No. The dataset is descriptive, not predictive.

**Is any information missing from individual instances?**
The original raw action log timestamps were intentionally removed during anonymization (see *Preprocessing* below). Participant demographics were collected during the study but are not released.

**Are relationships between individual instances made explicit?**
Steps within a participant file are ordered by `step_index` and form a sequence. There are no cross-participant relationships.

**Are there recommended data splits?**
No predefined splits. With only 12 participants, users should be cautious about train/test partitioning and prefer participant-level cross-validation.

**Are there any errors, sources of noise, or redundancies in the dataset?**
- The text fields are LLM-generated and may contain inaccuracies that do not perfectly reflect the actual designer's reasoning.
- The `rationale` field is left as an empty string in approximately 17% of records (71/417). This is by design: when no sufficiently grounded rationale could be established for a step, even if the designer offered some explanation, the field is left empty rather than filled with a low-confidence guess.
- See the ClearFairy paper for the rationale-grounding criteria and evaluation.

**Does the dataset rely on external resources?**
No. The release is self-contained.

**Does the dataset contain data that might be considered confidential?**
No. All identifying information has been replaced with fictional substitutes (see *Preprocessing*).

**Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety?**
No.

## Collection process

**How was the data associated with each instance acquired?**
Participants used Figma to complete one of two web design tasks while ClearFairy recorded their action log. The system then used a large language model to segment the log into decision steps and to infer the `decision_and_actions`, `rationale`, and `progression` fields for each step.

**What mechanisms or procedures were used to collect the data?**
A Figma plugin captured action logs in real time. LLM inference was performed offline after each session. See the ClearFairy paper for full methodological detail.

**Who was involved in the data collection process?**
The study authors recruited participants and ran sessions.

**Over what timeframe was the data collected?**
During the ClearFairy user study. Specific dates have been removed from the release to reduce re-identification risk.

**Were any ethical review processes conducted?**
Yes. The study was approved by the KAIST Institutional Review Board (IRB approval number **KH2022-115**).

**Did you collect the data from the individuals in question directly, or obtain it via third parties?**
Directly from participants who consented to participation in the study.

**Were the individuals in question notified about the data collection?**
Yes. Participants provided informed consent.

**Did the individuals in question consent to the collection and use of their data?**
Yes.

**If consent was obtained, were the consenting individuals provided with a mechanism to revoke their consent in the future?**
Yes, per the study's IRB protocol. Contact the corresponding author to request data removal.

## Preprocessing / cleaning / labeling

**Was any preprocessing/cleaning/labeling of the data done?**
Yes. The released data has been processed in two stages:

1. **LLM-based generation.** Raw Figma action logs were transformed into the three natural-language fields (`decision_and_actions`, `rationale`, `progression`) by a large language model.
2. **Anonymization for release.** Before release, all references that could identify participants, institutions, or third-party products were replaced with plausible fictional substitutes:
   - Real participant names → fictional names
   - Real lab and university names → fictional ones (e.g., *Pinewood Interaction Lab*, *Northbridge University*)
   - Real conference and paper titles → fictional substitutes (e.g., *InterConf 2025*, *AdaptUI 2023*)
   - Real brand and product names from the shopping task → fictional brand names (e.g., *Spire*, *AcoustiCore*, *ATELIER29*, *QuietWave*)
   - The original `timestamps` field linking back to raw action logs was removed.
   - Participant demographic information was not included.

Substitution was performed by deterministic regex rules applied uniformly across all files, so the same source token always maps to the same fictional token throughout the dataset.

**Was the "raw" data saved in addition to the preprocessed data?**
The raw Figma action logs and pre-anonymization decision steps are retained privately by the authors and are not part of this release.

## Uses

**Has the dataset been used for any tasks already?**
Yes — for the analysis presented in the ClearFairy paper.

**What other tasks could the dataset be used for?**
- Studying linguistic patterns in inferred design rationale
- Comparing rationale-inference methods against ClearFairy's
- Building models of design workflow segmentation
- Qualitative analysis of designer behavior across task types

**Is there anything about the composition of the dataset or the way it was collected and preprocessed that might impact future uses?**
- Sample size (n=12) limits statistical generalizability.
- LLM-generated `rationale` is inferred, not ground truth — analyses should treat it as model output rather than as a record of actual cognition.
- Anonymization replaces brand and lab names with fictional substitutes; analyses that depend on real-world brand semantics will not be valid on this release.

**Are there tasks for which the dataset should not be used?**
- It should not be used to make claims about specific real individuals, labs, or brands.
- It should not be used as ground truth for designer cognition without independent validation.

## Distribution

**Will the dataset be distributed to third parties outside of the entity on behalf of which the dataset was created?**
Yes. The dataset is released publicly.

**How will the dataset be distributed?**
Via a public Git repository, with a citable archive (e.g., Zenodo) planned for the camera-ready release.

**When will the dataset be distributed?**
Alongside the publication of the ClearFairy paper.

**Will the dataset be distributed under a copyright or other intellectual property (IP) license, and/or under applicable terms of use?**
Yes. Released under Creative Commons Attribution 4.0 International (CC BY 4.0). See `LICENSE`.

**Have any third parties imposed IP-based or other restrictions on the data?**
No.

## Maintenance

**Who will be supporting/hosting/maintaining the dataset?**
The authors of the ClearFairy paper.

**How can the owner/curator/manager of the dataset be contacted?**
Kihoon Son, KAIST — kihoon.son@kaist.ac.kr

**Will the dataset be updated?**
The dataset may receive minor updates to fix errors. Versioned releases will be tagged in the Git repository.

**If the dataset relates to people, are there applicable limits on the retention of the data associated with the instances?**
Per the study's IRB protocol. Contact the corresponding author for details.

**Will older versions of the dataset continue to be supported/hosted/maintained?**
Yes. Older tagged releases will remain accessible in the Git repository.

**If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so?**
Yes. Issues and pull requests are welcome on the Git repository.
