import random
import time

verb = ["Starting up", "Booting", "Repairing", "Loading", "Checking"]
adjective = ["master", "radiant", "silent", "harmonic", "fast"]
noun = ["solar array", "particle reshaper", "cosmic ray", "orbiter", "bit"]
message = ""
total = random.randint(10, 50)
for i in range(total):
    if not message or random.random() < 0.25:
        message = "{0} {1} {2}...".format(
            random.choice(verb), random.choice(adjective), random.choice(noun)
        )
    print({"current": i, "total": total, "status": message})
    time.sleep(1)
