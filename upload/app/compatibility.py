def check_compatibility(parts):
    by_category = {p["category"]: p for p in parts}
    checks = []
    cpu, board = by_category.get("CPU"), by_category.get("메인보드")
    if cpu and board:
        checks.append({"item": "CPU 소켓 ↔ 메인보드", "status": "확인" if cpu.get("socket") == board.get("socket") else "불일치", "detail": f'{cpu.get("socket")} / {board.get("socket")}'})
    ram = by_category.get("RAM")
    if board and ram:
        checks.append({"item": "메모리 규격", "status": "확인" if board.get("memory") == ram.get("memory") else "불일치", "detail": f'{board.get("memory")} / {ram.get("memory")}'})
    case, gpu = by_category.get("케이스"), by_category.get("GPU")
    if case and gpu:
        checks.append({"item": "GPU 길이 ↔ 케이스", "status": "확인" if gpu.get("length", 9999) <= case.get("gpu_max_length", 0) else "불일치", "detail": f'{gpu.get("length")}mm / {case.get("gpu_max_length")}mm'})
    cooler = by_category.get("CPU 쿨러")
    if case and cooler:
        checks.append({"item": "쿨러 높이 ↔ 케이스", "status": "확인" if cooler.get("height", 9999) <= case.get("cooler_max_height", 0) else "불일치", "detail": f'{cooler.get("height")}mm / {case.get("cooler_max_height")}mm'})
    psu = by_category.get("파워")
    if psu and gpu:
        estimated = gpu.get("power", 0) + 300
        checks.append({"item": "예상 소비전력 ↔ 파워", "status": "확인" if psu.get("wattage", 0) >= estimated else "정보 부족", "detail": f'예상 {estimated}W / 파워 {psu.get("wattage")}W'})
    return checks
