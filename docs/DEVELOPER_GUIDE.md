# KVM1 Astrology Engine - Developer Guide

## Developer Quickstart

### Environment Setup

```bash
# 1. Clone repository
git clone https://github.com/krishnaravi/KVM1_ASTROLOGY_ENGINE.git
cd KVM1_ASTROLOGY_ENGINE

# 2. Run unit tests
python -m unittest discover -s tests -v

# 3. Start local development server
uvicorn main:app --reload --port 8000
```

---

## Code Architecture Conventions

1. **Domain Models**: Place new domain entity models under `domain/models/`. Use `@dataclass(frozen=True)` for immutability. Do NOT import FastAPI, Pydantic, or ORMs inside `domain/`.
2. **Interface Contracts**: Place interface definitions under `core/interfaces/`. Interfaces must subclass `abc.ABC` with `@abstractmethod` decorators.
3. **Services**: Implement pipeline stages under `services/`. Each stage must implement `IPipelineStage`.
4. **Engines**: Implement new engines under `engines/` and register them in `EngineRegistry`.
5. **Vargas**: Implement new divisional chart calculators under `vargas/` and register them in `VargaRegistry`.
6. **Rules**: Implement new rules under `rules/<category>/` inheriting from `IRule`.
