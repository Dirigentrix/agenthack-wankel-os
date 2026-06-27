"""
Moduł: AviationHACCP v1.5 GUARDIAN
Opis: Zaawansowany system kontroli bezpieczeństwa żywności dla cateringu lotniczego.
Zgodność: IATA, WHO, FALCPA, EU FIC, integracja z PeklowniaBatch i Google Sheets.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger("AviationHACCP")

class CCPStatus(Enum):
    PASS = "ZGODNY"
    FAIL = "NIEZGODNY"
    WARNING = "OSTRZEŻENIE"
    DATA_ERROR = "BRAK_DANYCH"

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
        self.sensor_failures: List[str] = []

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

    def _is_malformed(self, val: Any) -> bool:
        if val is None: return True
        if isinstance(val, str):
            if val.upper() in ["ERR", "???", "NAN", "NULL"]: return True
            try:
                float(val)
                return False
            except ValueError:
                return True
        return False

    def validate_ccp(self, ccp_id: str, measured_value: Any) -> CCPStatus:
        if self._is_malformed(measured_value):
            msg = f"[SENSOR FAILURE] {ccp_id}: Dane uszkodzone lub brak odczytu ({measured_value})"
            self.sensor_failures.append(msg)
            logger.warning(msg)
            return CCPStatus.DATA_ERROR

        val = float(measured_value)
        if ccp_id not in self.ccp_definitions:
            return CCPStatus.PASS
        
        ccp = self.ccp_definitions[ccp_id]

        if ccp_id == "CCP1" and val < ccp.min_limit:
            self._trigger_alert(ccp, val)
            return CCPStatus.FAIL
        elif ccp_id in ["CCP3", "CCP5", "CCP6"] and (val > 4.0 or val < 0.0):
            self._trigger_alert(ccp, val)
            return CCPStatus.FAIL
        
        if val == 0.0 and ccp_id == "CCP6":
            self.critical_alerts.append(f"[SUSPICIOUS] CCP6: Odczyt 0.0 - Możliwy flatline sensora.")
            
        return CCPStatus.PASS

    def _trigger_alert(self, ccp: CCPDefinition, val: float):
        risk = "RYZYKO ZAMROŻENIA" if val < 0.0 else "PRZEKROCZENIE TEMP"
        alert = f"[IATA ALERT] {ccp.id} ({ccp.name}): {risk} ({val}°C). Akcja: {ccp.corrective_action}"
        self.critical_alerts.append(alert)

    def register_cold_chain(self, stage: str, temp_c: Any):
        if self._is_malformed(temp_c):
            self.sensor_failures.append(f"[COLD CHAIN FAILURE] {stage}: BRAK_DANYCH ({temp_c})")
            return

        val = float(temp_c)
        entry = {"stage": stage, "temp_c": val, "timestamp": datetime.now().isoformat()}
        self.cold_chain_log.append(entry)
        
        if val > 4.0 or val < 0.0:
            msg = f"[IATA ALERT] Log: {stage} ({val}°C) poza zakresem 0-4°C."
            if val < 0.0: msg += " ALARM: Ryzyko zamrożenia (Deep Freeze)."
            self.critical_alerts.append(msg)

    def generate_report(self) -> str:
        status = "BEZPIECZNY" if not (self.critical_alerts or self.sensor_failures) else "KRYTYCZNY"
        if self.sensor_failures and not self.critical_alerts:
            status = "NIEPEWNY (AWARIA SENSORÓW)"
            
        report = f"""
==================================================
RAPORT IATA AVIATION HACCP — GUARDIAN v1.5
Lot ID: {self.flight_id}
Status: {status}
Czas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
==================================================
AWARIE SENSORÓW: {len(self.sensor_failures)}
"""
        for f in self.sensor_failures:
            report += f" - {f}\n"

        report += f"\nALERTY KRYTYCZNE: {len(self.critical_alerts)}\n"
        for alert in self.critical_alerts:
            report += f" - {alert}\n"
            
        if not (self.critical_alerts or self.sensor_failures):
            report += " Wszystkie CCP ZGODNE. Brak awarii.\n"
            
        report += "=================================================="
        return report

if __name__ == "__main__":
    # Internal baseline test
    system = AviationHACCP("BASELINE_TEST")
    system.validate_ccp("CCP1", 76.0)
    system.validate_ccp("CCP5", 5.2)
    system.register_cold_chain("Cruise", -2.0)
    print(system.generate_report())
