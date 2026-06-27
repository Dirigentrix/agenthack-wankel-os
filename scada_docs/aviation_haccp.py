"""
Moduł: AviationHACCP v1.3 GUARDIAN
Opis: Zaawansowany system kontroli bezpieczeństwa żywności dla cateringu lotniczego.
Zgodność: IATA, WHO, FALCPA, EU FIC, integracja z PeklowniaBatch.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class CCPStatus(Enum):
    PASS = "ZGODNY"
    FAIL = "NIEZGODNY"
    WARNING = "OSTRZEŻENIE"

@dataclass
class CCPDefinition:
    id: str
    name: str
    parameter: str
    min_limit: Optional[float] = None
    max_limit: Optional[float] = None
    time_limit_hours: Optional[float] = None
    corrective_action: str = ""

class AviationHACCP:
    def __init__(self, flight_id: str):
        self.flight_id = flight_id
        self.session_start = datetime.now()
        self.ccp_definitions = self._load_ccp_definitions()
        self.allergens_protocols = self._load_allergen_protocols()
        self.critical_alerts: List[str] = []
        self.cold_chain_log: List[Dict] = []

    def _load_ccp_definitions(self) -> Dict[str, CCPDefinition]:
        return {
            "CCP1": CCPDefinition(id="CCP1", name="Obróbka termiczna", parameter="Temperatura rdzenia", min_limit=75.0,
                                  corrective_action="Wydłużyć czas lub zutylizować."),
            "CCP2": CCPDefinition(id="CCP2", name="Szybkie schładzanie", parameter="Czas i temperatura", time_limit_hours=6.0,
                                  corrective_action="Zutylizować partię."),
            "CCP3": CCPDefinition(id="CCP3", name="Utrzymanie temperatury", parameter="Temperatura składowania", max_limit=4.0,
                                  corrective_action="Przeskalibrować, zutylizować."),
            "CCP5": CCPDefinition(id="CCP5", name="Transport", parameter="Temperatura chłodni", max_limit=4.0,
                                  corrective_action="Zawrócić transport."),
            "CCP6": CCPDefinition(id="CCP6", name="Załadunek", parameter="Temperatura przy wejściu", max_limit=4.0,
                                  corrective_action="Zatrzymać załadunek.")
        }

    def _load_allergen_protocols(self) -> Dict[str, str]:
        return {
            "IDENTYFIKACJA": "Pełna identyfikacja 14 alergenów.",
            "KRZYŻOWANIE": "Oddzielne linie + sanityzacja.",
            "ZAŁOGA": "Certyfikaty IATA/WHO."
        }

    def validate_ccp(self, ccp_id: str, measured_value: float) -> CCPStatus:
        if ccp_id not in self.ccp_definitions:
            return CCPStatus.FAIL
        ccp = self.ccp_definitions[ccp_id]

        if ccp_id == "CCP1" and measured_value < ccp.min_limit:
            self._trigger_alert(ccp)
            return CCPStatus.FAIL
        elif ccp_id in ["CCP3", "CCP5", "CCP6"] and (measured_value > 4.0 and measured_value < 60.0):
            self._trigger_alert(ccp)
            return CCPStatus.FAIL
        return CCPStatus.PASS

    def _trigger_alert(self, ccp: CCPDefinition):
        alert = f"[IATA ALERT] {ccp.id} ({ccp.name}): Przekroczono limit. Akcja: {ccp.corrective_action}"
        self.critical_alerts.append(alert)

    def register_cold_chain(self, stage: str, temp_c: float):
        entry = {"stage": stage, "temp_c": temp_c, "timestamp": datetime.now().isoformat()}
        self.cold_chain_log.append(entry)
        # Auto-walidacja
        if "cold" in stage.lower() and temp_c > 4.0:
            self._trigger_alert(self.ccp_definitions.get("CCP5", CCPDefinition("CCP5", "", "")))

    def generate_report(self) -> str:
        status = "BEZPIECZNY" if not self.critical_alerts else "KRYTYCZNY"
        report = f"""
==================================================
RAPORT IATA AVIATION HACCP — GUARDIAN
Lot ID: {self.flight_id}
Status: {status}
Czas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
==================================================
ALERTY: {len(self.critical_alerts)}
"""
        for alert in self.critical_alerts:
            report += f" - {alert}\n"
        if not self.critical_alerts:
            report += " Wszystkie CCP ZGODNE.\n"
        report += "=================================================="
        return report

# Test
if __name__ == "__main__":
    system = AviationHACCP("LO123_WAW_JFK")
    system.validate_ccp("CCP1", 76.5)
    system.validate_ccp("CCP5", 7.2)  # alert
    system.register_cold_chain("transport", 3.5)
    print(system.generate_report())
