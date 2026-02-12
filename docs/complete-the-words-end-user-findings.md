# Complete the Words — End-user findings (what needs to change)

Viewed as an end user, here’s what should be improved.

## Fixed in code

1. **Timer hits 0:00 and nothing happens**  
   - **Issue:** Countdown goes red at 30s, then 0:00, but the page doesn’t check or tell you “time’s up.”  
   - **Change:** When the countdown reaches 0, auto-run **Check** and show “Time’s up!” so the user isn’t left wondering.

2. **Wrong answers: correct answer not visible in the passage**  
   - **Issue:** After **Check**, wrong boxes stay red with your wrong text; the correct word only appears in “Why these answers?” below.  
   - **Change:** After **Check**, fill each wrong box with the correct answer (keep it red) so the passage reads correctly and the user sees the right word in place.

3. **Set selector: unclear that it restarts practice**  
   - **Issue:** Changing “Set” reloads the page and starts a new practice; not obvious.  
   - **Change:** Add a short note: “Changing set starts a new practice.”

## Recommended next (optional)

4. **Progress bar with 15 passages**  
   - Many dots and connectors can feel cramped on small screens. Consider a compact mode (e.g. “3 / 15” text) or horizontal scroll for the bar.

5. **Instructions**  
   - Slightly clarify: e.g. “From the second sentence, every 2nd word is half-blank. Type only the missing letters in each box. One wrong letter = wrong.”

6. **Result screen placeholder**  
   - HTML shows “0 / 5” before JS runs. Could use “0 / —” or keep as is (updates quickly).

7. **Hints before Check**  
   - Some users may expect a “Hint” button per gap (e.g. reveal one letter or the hint text). Currently hints appear only in the explanation after **Check** for wrong answers.
