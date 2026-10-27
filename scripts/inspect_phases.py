with open("/tmp/hafal_kartu_full_segments.txt") as f:
    lines = f.readlines()

print("=== ANGEL MATCHING PHASE (190s -> 310s) ===")
for l in lines:
    parts = l.strip().split()
    if len(parts) >= 2 and parts[1].startswith("["):
        try:
            t0 = float(parts[1].replace("[", ""))
            if 195.0 <= t0 <= 312.0:
                print(l.strip())
        except:
            pass

print("\n=== ARTHUR MATCHING PHASE (430s -> 530s) ===")
for l in lines:
    parts = l.strip().split()
    if len(parts) >= 2 and parts[1].startswith("["):
        try:
            t0 = float(parts[1].replace("[", ""))
            if 430.0 <= t0 <= 530.0:
                print(l.strip())
        except:
            pass
