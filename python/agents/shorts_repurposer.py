from typing import List, Dict, Any
from python.schemas.script import ScriptPlan, ScriptSegment

class ShortsRepurposer:
    def repurpose_long_form_to_shorts(self, long_script: ScriptPlan) -> List[ScriptPlan]:
        # Extract highest-impact self-contained 30-50s clips from long form per Section 48 & 120
        shorts = []
        if len(long_script.segments) >= 3:
            sub_segments = long_script.segments[:3]
            short_plan = ScriptPlan(
                title_candidate=f"{long_script.title_candidate} (Short Clip)",
                hook=long_script.hook,
                context=long_script.context,
                core_value="Extracted key takeaway.",
                proof=long_script.proof,
                payoff=long_script.payoff,
                cta="Watch full tutorial on our channel!",
                segments=sub_segments,
                format="shorts",
                estimated_duration_seconds=sum(s.duration for s in sub_segments)
            )
            shorts.append(short_plan)
        return shorts

shorts_repurposer = ShortsRepurposer()
