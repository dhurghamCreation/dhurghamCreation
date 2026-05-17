import sys
import json
import re

# 1. Parse the action sent by the GitHub Issue click
action = sys.argv[1].upper() if len(sys.argv) > 1 else "FIRE"

# 2. Load current game state variables
try:
    with open(".github/game/state.json", "r") as f:
        state = json.load(f)
except FileNotFoundError:
    state = {"score": 14520, "player_x": 4, "boss_health": 70, "wave": 3}

# 3. Game Loop Logic Processors
if "LEFT" in action:
    state["player_x"] = max(1, state["player_x"] - 1)
    state["score"] += 10
elif "RIGHT" in action:
    state["player_x"] = min(7, state["player_x"] + 1)
    state["score"] += 10
elif "FIRE" in action:
    state["boss_health"] = max(0, state["boss_health"] - 5)
    state["score"] += 150
    if state["boss_health"] <= 0:
        state["boss_health"] = 100
        state["wave"] += 1

# 4. Save updated engine states
with open(".github/game/state.json", "w") as f:
    json.dump(state, f, indent=2)

# 5. Read the current main README file
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

# 6. Dynamically rewrite the capsule-render URL parameters in the markdown file
new_url = f"capsule-render.vercel.app/api?type=waving&color=auto&height=320&section=header&text=SECTOR%207%20ONLINE&fontSize=32&animation=twinkling&theme=tokyonight&desc=💥%20SCORE:%20{state['score']}%20%7C%20👾%20MALWARE%20WAVES:%20{state['wave']}/10%20%7C%20🛡️%20SHIELDS:%20{state['boss_health']}%25"

# Regex structural patch replacement targeting the game block banner link
updated_readme = re.sub(r"capsule-render\.vercel\.app/api\?type=waving[^\s\"']*", new_url, readme)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated_readme)
