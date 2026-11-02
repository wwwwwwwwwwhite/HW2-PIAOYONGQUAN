import json
from pathlib import Path
from .models import Request
from .compatibility import check_compatibility

PRODUCTS = json.loads((Path(__file__).parent / "data/products.json").read_text())

def _pick(category, items, **filters):
    choices = [p for p in PRODUCTS if p["category"] == category]
    for key, value in filters.items():
        choices = [p for p in choices if p.get(key) == value]
    return next((p for p in choices if p["price"] <= items), choices[-1] if choices else None)

def recommend(req: Request):
    cpu = next((p for p in PRODUCTS if p["category"] == "CPU" and (req.cpu_preference == "any" or p["maker"] == req.cpu_preference)), None)
    cpus = [p for p in PRODUCTS if p["category"] == "CPU" and (req.cpu_preference == "any" or p["maker"] == req.cpu_preference)]
    cpu = sorted(cpus, key=lambda p: p["performance"])[0]
    if req.purpose in ("dev", "creative", "ai") and req.budget >= 1200000: cpu = sorted(cpus, key=lambda p: p["performance"])[-1]
    gpu_choices = [p for p in PRODUCTS if p["category"] == "GPU" and (req.gpu_preference == "any" or p["gpu_brand"] == req.gpu_preference)]
    target = 4 if req.resolution == "4K" else 3 if req.resolution == "1440p" else 2
    gpu = min(gpu_choices, key=lambda p: abs(p["power"] / 60 - target))
    if req.budget >= 1500000 and req.resolution != "1080p": gpu = max(gpu_choices, key=lambda p: p["price"])
    board = next(p for p in PRODUCTS if p["category"] == "메인보드" and p["socket"] == cpu["socket"])
    ram = next(p for p in PRODUCTS if p["category"] == "RAM" and p["memory"] == board["memory"] and p["capacity"] >= req.memory)
    storage_options = [p for p in PRODUCTS if p["category"] == "SSD" and p.get("capacity", 0) >= req.storage]
    storage = storage_options[0] if storage_options else next(p for p in PRODUCTS if p["category"] == "SSD")
    parts = [cpu, next(p for p in PRODUCTS if p["category"] == "CPU 쿨러"), board, ram, gpu,
             storage, next(p for p in PRODUCTS if p["category"] == "파워"), next(p for p in PRODUCTS if p["category"] == "케이스")]
    optional = []
    if "monitor" in req.include: optional.append({"category":"모니터","maker":"BuildMyPC","model":"24인치 FHD 100Hz 모니터","spec":"24인치 / 1920x1080 / 100Hz (예시 구성)","price":150000})
    if "keyboard" in req.include: optional.append({"category":"키보드·마우스","maker":"BuildMyPC","model":"기본 키보드·마우스 세트","spec":"유선 입력장치 세트 (예시 구성)","price":30000})
    total = sum(p["price"] for p in parts + optional)
    warnings = []
    if storage.get("capacity", 0) < req.storage: warnings.append(f"요청한 {req.storage}GB 저장장치 데이터가 없어 {storage.get('capacity', 0)}GB 참고 제품을 표시했습니다.")
    if total > req.budget: warnings.append("현재 제품 데이터 기준으로 예산을 초과합니다. GPU·메모리·주변기기 조건을 조정해 주세요.")
    return {"parts": parts + optional, "total": total, "budget": req.budget, "balance": req.budget-total,
            "compatibility": check_compatibility(parts),
            "warnings": warnings,
            "source_note": "가격은 2026-11-02 기준 기능 시연용 수동 관리 참고 가격이며 실시간 판매가가 아닙니다.",
            "reason": f"{req.resolution} 해상도와 {req.purpose} 목적을 기준으로 CPU·GPU 성능과 예산을 균형 있게 배분했습니다."}
