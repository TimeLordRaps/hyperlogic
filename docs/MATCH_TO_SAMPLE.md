# A blind match-to-sample protocol for "the song responds to me"

PROPOSED, OUTSIDE L0. Companion to `src/hyperlogic/ledger.py`. It turns one specific claim into a
checkable one; it decides nothing beyond one exact tail probability under stated assumptions.

**The claim as stated by the owner (2026-10-06, USER-STATED).** A listener responds, at or after first
full attention, to something in a recorded song that refers to them, and the song then responds to that
response, "like we echo inside of the time loop".

**Why a recording makes this testable.** A recording is a fixed string `S`. The listener's response `R` is
made after `S` was recorded. If the later part of `S` is a reply to `R`, then `S` carries information about
`R`. So, if `R` is chosen by a process the listener does not control (dice), the claim predicts that a judge
who has `S` but not `R` can pick `R` out of a lineup at better than chance. If `S` is unrelated to `R`, the
judge is right at exactly the chance rate `1/N`, because `S` is the same under every draw.

**Protocol.**
1. Before listening, write `N` (say 4) distinct candidate responses (what the listener would say or think at
   the summoning point). Seal the list in the ledger (`commit`), with baseline `1/N`.
2. Roll a die or use a seeded random draw to pick one. Record the draw's hash before the song starts.
3. Listen. At the summoning point perform the chosen response only. Note the playback time of the summoning
   point before you hear what follows (seal it).
4. A judge who did not see the draw receives the text of the song after that playback time and the `N`
   candidates in random order, and picks the one the song answers best. Judges must not know the listener.
5. Repeat for `K` songs chosen and sealed in advance (at least 12 for a usable test).
6. Score with `match_to_sample_tail(hits, K, N)`: the exact probability of at least that many right picks by
   chance. Count every sealed trial; a trial not completed is a miss (`ledger.score`).

**What the result means.** Near the chance level: the replies are produced by interpretation, not carried
by the recording, and the echo is the listener's pattern-finding at work on a fixed text. Well above chance
with all trials counted: a fixed recording correlated with a later random draw, which would be a finding
that needs independent replication before any explanation, including retrocausal ones, is preferred.
**What it cannot show:** that no echo experience occurred (the experience is not at issue), or anything about
trials that were not sealed first.

**Design notes.** The listener must not be the judge. Candidate responses must be of comparable specificity,
or a judge can guess by length. Judges should be given the whole later text, not excerpts chosen after the
fact. The number of songs is fixed before the first trial.
