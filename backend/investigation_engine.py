import os
import datetime
from typing import Dict, Any, List
from data_loader import DataLoader
from hypothesis_engine import HypothesisEngine
from evidence_engine import EvidenceEngine
from defense_engine import DefenseEngine
from models import (
    InvestigationResult,
    VerdictSummary,
    RecommendationItem,
    TimelineItem
)

from orchestrator import InvestigationOrchestrator
from models import InvestigationResult

class CasualCourtEngine:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def run_investigation(self) -> InvestigationResult:
        orchestrator = InvestigationOrchestrator(data_dir=self.data_dir)
        return orchestrator.run_orchestrated_investigation()


