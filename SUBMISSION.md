SUBMISSION: Analytics Intern Take-Home Task
My Approach: Finding the Signal in the Noise
When I first looked at the 103 call transcripts, I saw over 2,000 extractions. While the volume was impressive, the data was messy a mix of roadmap dreams, administrative features, and actual safety wins.

Instead of just counting these entries, I built a Python pipeline to audit the AI’s logic. My goal was to move beyond the raw numbers and find the real story: What is actually working, what is a "hallucination," and where is the untapped business value?

1. Normalization
The AI was creating a new label for almost every variation of a topic (e.g., "PIT safety" vs. "Forklift behavior"). To make this data useful for a Product Manager, I consolidated these into six core pillars. This allowed me to see that while "Other" categories dominate, the real data lies in Vehicle Operations and Ergonomics.

2. Quality Control
I believe data is only as good as it is honest. I built a Filter to catch two major issues:

Roadmap vs. Reality: I flagged cases where the AI labeled something as a "Use Case" even though the customer said they were only working toward it. Catching these 7 roadmap hallucinations is vital for keeping our promises to customers.

Environmental Noise: I searched for junk data patterns, like the instance where a stationary rug was flagged as a hazard. Identifying these false positives helps us understand where the AI needs better sense.

My Key Assumptions
I assume that when customers keep asking about efficiency and security, they are practically begging Voxel to solve more than just safety problems.

I treated the speaker's actual words as the ground truth. If a speaker says a feature is planned, I assume any AI label calling it current is an error.

Insights over Admin: I separated software tools (like task workflows) from AI detections. This ensures our Safety Use Case counts represent real-world hazards, not just people using a dashboard.

What I Found
353 items were actually administrative software features, not AI insights.

7 instances showed the AI over-promising on future features.

38 clear signals showed customers want Voxel to help with trailer turnaround and facility security.