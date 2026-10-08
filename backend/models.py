from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class DataQualityMetrics(BaseModel):
    total_order_rows: int
    unique_order_count: int
    duplicate_count: int
    data_quality_notes: List[str]

class AnomalyMetrics(BaseModel):
    baseline_cancellation_rate: float
    current_cancellation_rate: float
    change_percentage_points: float
    anomaly_start_date: str
    anomaly_end_date: str
    anomaly_start_day: int
    total_affected_orders: int
    estimated_value_at_risk: float

class TimelineItem(BaseModel):
    date: str
    day_number: int
    source: str
    event: str
    importance: str  # HIGH, MEDIUM, LOW

class EvidenceItem(BaseModel):
    id: str
    hypothesis: str
    source: str
    observation: str
    date: Optional[str] = None
    test: str
    evidence_type: str  # OBSERVED, DERIVED, INFERENCE, HYPOTHESIS
    direction: str      # SUPPORTS, CONTRADICTS, NEUTRAL, NOISY
    strength: float
    source_reliability: float
    impact: str
    explanation: str
    raw_observation: Optional[str] = None
    derived_finding: Optional[str] = None
    investigation_test: Optional[str] = None
    interpretation: Optional[str] = None


class ChallengeTestResult(BaseModel):
    id: str
    test_name: str
    question: str
    result: str  # PASSED, REJECTED_ALTERNATIVE, NO_CONTRADICTION, FAILED
    details: str
    passed: bool

class HypothesisResult(BaseModel):
    name: str
    score: float
    rank: int
    classification: str  # PRIMARY CAUSE, CONTRIBUTING FACTOR, NOISY / CONFLICTING SIGNAL, WEAK ALTERNATIVE, EFFECT
    supporting_evidence: List[str]
    contradicting_evidence: List[str]
    timing_result: str   # BEFORE, DURING, AFTER, UNCLEAR
    segment_result: str
    cross_source_result: str
    independent_support_count: int
    explanation: str

class VerdictSummary(BaseModel):
    primary_cause: str
    contributing_factor: str
    noisy_signal: str
    weak_alternative: str
    investigation_confidence: str
    case_challenge_status: str  # CASE SURVIVED, CASE CHALLENGED, CASE FAILED

class RecommendationItem(BaseModel):
    step: int
    title: str
    description: str

class DefenseResult(BaseModel):
    status: str                         # CASE SURVIVED, CASE CHALLENGED, CASE FAILED
    leading_hypothesis: str
    falsification_question: str
    tests: List[ChallengeTestResult]
    passed_tests: List[str]
    failed_tests: List[str]
    contradictions: List[str]
    what_would_change_our_mind: List[str]
    summary: str

class InvestigationTraceStep(BaseModel):
    step_number: int
    stage: str
    action: str
    decision: str
    next_action: str
    status: str

class InvestigationResult(BaseModel):
    case_id: str
    scenario: str
    timestamp: str
    data_quality: DataQualityMetrics
    anomaly: AnomalyMetrics
    timeline: List[TimelineItem]
    hypotheses: List[HypothesisResult]
    evidence_ledger: List[EvidenceItem]
    challenge: List[ChallengeTestResult]
    defense: DefenseResult
    verdict: VerdictSummary
    recommendations: List[RecommendationItem]
    investigation_trace: List[InvestigationTraceStep]


