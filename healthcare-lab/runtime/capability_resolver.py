"""Capability-first tool routing. Tool names are never treated as availability evidence."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

@dataclass
class ToolResult:
    capability: str
    tool_id: str
    ok: bool
    data: Any = None
    error: Optional[str] = None
    checked_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    degraded: bool = False
    confidence_penalty: str = "none"
    provenance: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ToolAdapter:
    tool_id: str
    capability: str
    priority: int
    executor: Callable[[Dict[str, Any]], Any]
    health_probe: Callable[[], Any]

class CapabilityRegistry:
    def __init__(self) -> None:
        self._adapters: Dict[str, List[ToolAdapter]] = {}
        self.status: Dict[str, ToolResult] = {}

    def register(self, adapter: ToolAdapter) -> None:
        self._adapters.setdefault(adapter.capability, []).append(adapter)
        self._adapters[adapter.capability].sort(key=lambda a: a.priority)

    def health_check(self, capability: str) -> List[ToolResult]:
        results = []
        for adapter in self._adapters.get(capability, []):
            try:
                value = adapter.health_probe()
                ok = bool(value)
                result = ToolResult(capability, adapter.tool_id, ok, data=value,
                                    degraded=not ok,
                                    confidence_penalty="none" if ok else "source_degradation")
            except Exception as exc:
                result = ToolResult(capability, adapter.tool_id, False,
                                    error=f"{type(exc).__name__}: {exc}", degraded=True,
                                    confidence_penalty="source_degradation")
            self.status[f"{capability}:{adapter.tool_id}"] = result
            results.append(result)
        return results

    def resolve(self, capability: str) -> Optional[ToolAdapter]:
        self.health_check(capability)
        for adapter in self._adapters.get(capability, []):
            state = self.status.get(f"{capability}:{adapter.tool_id}")
            if state and state.ok:
                return adapter
        return None

    def execute(self, capability: str, payload: Dict[str, Any]) -> ToolResult:
        adapter = self.resolve(capability)
        if adapter is None:
            return ToolResult(capability, "none", False, error="No verified available adapter",
                              degraded=True, confidence_penalty="source_degradation",
                              provenance={"availability": "not_verified"})
        try:
            data = adapter.executor(payload)
            return ToolResult(capability, adapter.tool_id, True, data=data,
                              provenance={"tool_id": adapter.tool_id, "capability": capability,
                                          "availability": "verified_live_call"})
        except Exception as exc:
            # A primary can fail after health check; route once to the next verified fallback.
            for fallback in self._adapters.get(capability, []):
                if fallback.tool_id == adapter.tool_id:
                    continue
                state = self.status.get(f"{capability}:{fallback.tool_id}")
                if state and state.ok:
                    try:
                        data = fallback.executor(payload)
                        return ToolResult(capability, fallback.tool_id, True, data=data,
                                          degraded=True, confidence_penalty="fallback",
                                          provenance={"primary_failed": adapter.tool_id,
                                                      "fallback": fallback.tool_id,
                                                      "availability": "verified_live_call"})
                    except Exception:
                        continue
            return ToolResult(capability, adapter.tool_id, False,
                              error=f"{type(exc).__name__}: {exc}", degraded=True,
                              confidence_penalty="source_degradation",
                              provenance={"availability": "verified_but_execution_failed"})
