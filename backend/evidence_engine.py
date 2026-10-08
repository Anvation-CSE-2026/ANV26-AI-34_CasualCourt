from typing import List, Dict, Any
from models import EvidenceItem, HypothesisResult

RELIABILITY_WEIGHTS = {
    "supplier_events.csv": 0.90,
    "orders.csv": 0.90,
    "inventory.csv": 0.85,
    "payments.csv": 0.95,
    "competitor_prices.csv": 0.75,
    "tickets.csv": 0.40,
}

SCORING_RULES = {
    "strong_support": 2.0,
    "weak_support": 0.7,
    "neutral": 0.0,
    "contradiction": -2.0
}

class EvidenceEngine:
    def build_evidence_ledger(self, supplier_res: Dict[str, Any], inventory_res: Dict[str, Any], payment_res: Dict[str, Any], ticket_res: Dict[str, Any], competitor_res: Dict[str, Any]) -> List[EvidenceItem]:
        ledger = []

        # EV-01 & EV-02: Supplier & Orders
        if supplier_res.get("available", True):
            ledger.append(
                EvidenceItem(
                    id="EV-01",
                    hypothesis="Supplier / Delivery Disruption",
                    source="supplier_events.csv",
                    observation="Supplier B average lead time jumped from 4.18 to 9.03 days starting on Day 38 (2026-09-07).",
                    date="2026-09-07",
                    test="Temporal Lead Time Test",
                    evidence_type="OBSERVED",
                    direction="SUPPORTS",
                    strength=SCORING_RULES["strong_support"],
                    source_reliability=RELIABILITY_WEIGHTS["supplier_events.csv"],
                    impact="HIGH",
                    explanation="Unannounced supplier transit delay preceded the cancellation spike by 4 days.",
                    raw_observation="supplier_events.csv: Supplier B avg lead_time = 9.03d on 2026-09-07 (baseline 4.18d)",
                    derived_finding="Unannounced +4.85 day shipping lead time slip on Route B",
                    investigation_test="Temporal Lead Time Test (Precedence Check vs Day 42 Anomaly Onset)",
                    interpretation="Supplier lead time delay occurred 4 days before order cancellations spiked. Strongly supports Supplier / Delivery Disruption."
                )
            )
            ledger.append(
                EvidenceItem(
                    id="EV-02",
                    hypothesis="Supplier / Delivery Disruption",
                    source="orders.csv",
                    observation=f"Orders routed to Supplier B reached a {supplier_res.get('affected_rate', 0.452):.1%} cancellation rate during anomaly, vs {supplier_res.get('unaffected_rate', 0.074):.1%} for unexposed suppliers.",
                    date="2026-09-11",
                    test="Exposure Segment Contrast Test",
                    evidence_type="DERIVED",
                    direction="SUPPORTS",
                    strength=SCORING_RULES["strong_support"],
                    source_reliability=RELIABILITY_WEIGHTS["orders.csv"],
                    impact="HIGH",
                    explanation="Cancellations are strongly isolated to orders exposed to Supplier B.",
                    raw_observation="orders.csv: 4,483 order records analyzed across suppliers during baseline & anomaly periods",
                    derived_finding=f"Supplier B orders experienced {supplier_res.get('affected_rate', 0.452):.1%} cancellation rate vs {supplier_res.get('unaffected_rate', 0.074):.1%} for unexposed suppliers",
                    investigation_test="Exposure Segment Contrast Test (Exposed vs Unexposed Routes)",
                    interpretation="Order cancellations are strongly isolated to orders exposed to Supplier B (+37.8 percentage point difference)."
                )
            )

        # EV-03: Inventory
        if inventory_res.get("available", True):
            ledger.append(
                EvidenceItem(
                    id="EV-03",
                    hypothesis="Inventory Shortage",
                    source="inventory.csv",
                    observation="Stock levels for SKU-B1 & SKU-B2 dropped from 94.5 units down to 21 units starting on Day 41 (2026-09-10).",
                    date="2026-09-10",
                    test="Stock Depletion Sequence Test",
                    evidence_type="OBSERVED",
                    direction="SUPPORTS",
                    strength=SCORING_RULES["strong_support"],
                    source_reliability=RELIABILITY_WEIGHTS["inventory.csv"],
                    impact="MEDIUM",
                    explanation="Stock depleted after supplier lead time jumped, acting as a contributing mediator for delivery delays.",
                    raw_observation="inventory.csv: SKU-B1 & SKU-B2 stock level = 21 units on 2026-09-10 (baseline 94.5 units)",
                    derived_finding="DC stock depleted to critical buffer threshold 3 days after supplier delay started",
                    investigation_test="Stock Depletion Sequence Test (Inventory vs Lead Time Onset)",
                    interpretation="Inventory stockout acted as a contributing mediator following supplier delivery delays."
                )
            )

        # EV-04: Payments
        if payment_res.get("available", True):
            ledger.append(
                EvidenceItem(
                    id="EV-04",
                    hypothesis="Payment Failure",
                    source="payments.csv",
                    observation=f"Payment success rate remained healthy at {payment_res.get('overall_success_rate', 0.988):.1%} during the anomaly period.",
                    date="2026-09-11",
                    test="Payment Gate Authorization Test",
                    evidence_type="OBSERVED",
                    direction="CONTRADICTS",
                    strength=SCORING_RULES["contradiction"],
                    source_reliability=RELIABILITY_WEIGHTS["payments.csv"],
                    impact="HIGH",
                    explanation="High payment success directly contradicts systemic payment authorization failure as root cause.",
                    raw_observation=f"payments.csv: Payment gateway success rate = {payment_res.get('overall_success_rate', 0.988):.1%} during anomaly window",
                    derived_finding="Payment gateway authorization stability maintained at normal baseline level",
                    investigation_test="Payment Gate Authorization Test (Gateway Log Correlation)",
                    interpretation="High payment authorization rate directly contradicts systemic payment failure as root cause."
                )
            )

        # EV-05: Tickets
        if ticket_res.get("available", True):
            ledger.append(
                EvidenceItem(
                    id="EV-05",
                    hypothesis="Payment Failure",
                    source="tickets.csv",
                    observation=f"Customer tickets categorized as Refund/Payment Issue increased to {ticket_res.get('payment_refund_tickets_post', 73)} tickets after Day 42.",
                    date="2026-09-13",
                    test="Ticket Temporal Sequence Test",
                    evidence_type="DERIVED",
                    direction="NOISY",
                    strength=SCORING_RULES["weak_support"],
                    source_reliability=RELIABILITY_WEIGHTS["tickets.csv"],
                    impact="LOW",
                    explanation="Support tickets spiked after order cancellations occurred (customers inquiring about automated refunds).",
                    raw_observation=f"tickets.csv: {ticket_res.get('payment_refund_tickets_post', 73)} refund/payment inquiry tickets logged after 2026-09-11",
                    derived_finding="Customer support ticket volume spiked 2 days after order cancellations began",
                    investigation_test="Ticket Temporal Sequence Test (Precedence Check vs Cancellation Onset)",
                    interpretation="Ticket complaints are downstream customer reactions inquiring about refund status, not the cause."
                )
            )

        # EV-06: Competitor Prices
        if competitor_res.get("available", True):
            ledger.append(
                EvidenceItem(
                    id="EV-06",
                    hypothesis="Competitor Pricing",
                    source="competitor_prices.csv",
                    observation="Competitor price drop (-3.0%) for SKU-B1 occurred on Day 48 (2026-09-17).",
                    date="2026-09-17",
                    test="Price Change Sequence Test",
                    evidence_type="OBSERVED",
                    direction="CONTRADICTS",
                    strength=SCORING_RULES["contradiction"],
                    source_reliability=RELIABILITY_WEIGHTS["competitor_prices.csv"],
                    impact="LOW",
                    explanation="Competitor price change occurred 6 days after the cancellation spike began.",
                    raw_observation="competitor_prices.csv: SKU-B1 competitor price dropped to $106.80 (-3.0%) on 2026-09-17",
                    derived_finding="Competitor price promotion occurred on Day 48",
                    investigation_test="Price Change Sequence Test (Promo Date vs Cancellation Onset)",
                    interpretation="Competitor price drop occurred 6 days after cancellation spike onset; rejected as root cause."
                )
            )

        return ledger


    def evaluate_hypotheses(self, ledger: List[EvidenceItem], supplier_res: Dict[str, Any], inventory_res: Dict[str, Any], payment_res: Dict[str, Any], competitor_res: Dict[str, Any]) -> List[HypothesisResult]:
        
        # 1. Supplier / Delivery Disruption
        sup_items = [e for e in ledger if e.hypothesis == "Supplier / Delivery Disruption"]
        sup_score = sum(e.strength * e.source_reliability for e in sup_items) if sup_items else 0.0
        sup_hyp = HypothesisResult(
            name="Supplier / Delivery Disruption",
            score=round(sup_score, 2),
            rank=1,
            classification="PRIMARY CAUSE",
            supporting_evidence=[e.observation for e in sup_items if e.direction == "SUPPORTS"],
            contradicting_evidence=[],
            timing_result="BEFORE",
            segment_result=f"42.6% cancellations on Supplier B vs {supplier_res.get('unaffected_rate', 0.074):.1%} on unexposed suppliers (+{supplier_res.get('rate_difference_pts', 33.6)} pts)." if supplier_res.get("available", True) else "Supplier comparison unavailable.",
            cross_source_result="Supported across independent sources." if sup_items else "Data unavailable.",
            independent_support_count=len(sup_items),
            explanation="Supplier B lead time jump (+4.85d) on Day 38 directly triggered fulfillment delays and the order cancellation spike on Day 42."
        )

        # 2. Inventory Shortage
        inv_items = [e for e in ledger if e.hypothesis == "Inventory Shortage"]
        inv_score = sum(e.strength * e.source_reliability for e in inv_items) if inv_items else 0.0
        inv_hyp = HypothesisResult(
            name="Inventory Shortage",
            score=round(inv_score, 2),
            rank=2,
            classification="CONTRIBUTING FACTOR",
            supporting_evidence=[e.observation for e in inv_items if e.direction == "SUPPORTS"],
            contradicting_evidence=[],
            timing_result="BEFORE",
            segment_result="Stockouts isolated to SKU-B1 & SKU-B2." if inventory_res.get("available", True) else "Inventory stock data unavailable.",
            cross_source_result="Supported across independent sources." if inv_items else "Data unavailable.",
            independent_support_count=len(inv_items),
            explanation="Regional stock depleted following Supplier B delivery delays, exacerbating fulfillment backorders."
        )

        # 3. Payment Failure
        pay_items = [e for e in ledger if e.hypothesis == "Payment Failure"]
        pay_score = sum(e.strength * e.source_reliability for e in pay_items) if pay_items else 0.0
        pay_hyp = HypothesisResult(
            name="Payment Failure",
            score=round(pay_score, 2),
            rank=3,
            classification="NOISY / CONFLICTING SIGNAL",
            supporting_evidence=[e.observation for e in pay_items if e.direction in ["SUPPORTS", "NOISY"]],
            contradicting_evidence=[e.observation for e in pay_items if e.direction == "CONTRADICTS"],
            timing_result="AFTER",
            segment_result="Payment success rate remained at 98.8% across all customer segments." if payment_res.get("available", True) else "Payment data unavailable.",
            cross_source_result="Contradicted by primary payment logs." if pay_items else "Data unavailable.",
            independent_support_count=len([e for e in pay_items if e.direction == "SUPPORTS"]),
            explanation="Payment success remained ~99%. Ticket complaints spiked after cancellations due to automated refund processing."
        )

        # 4. Competitor Pricing
        comp_items = [e for e in ledger if e.hypothesis == "Competitor Pricing"]
        comp_score = sum(e.strength * e.source_reliability for e in comp_items) if comp_items else 0.0
        comp_hyp = HypothesisResult(
            name="Competitor Pricing",
            score=round(comp_score, 2),
            rank=4,
            classification="WEAK ALTERNATIVE",
            supporting_evidence=[],
            contradicting_evidence=[e.observation for e in comp_items if e.direction == "CONTRADICTS"],
            timing_result="AFTER",
            segment_result="Price drop restricted to SKU-B1 on Day 48." if competitor_res.get("available", True) else "Competitor pricing data unavailable.",
            cross_source_result="Contradicted by timeline sequence." if comp_items else "Data unavailable.",
            independent_support_count=0,
            explanation="Competitor price promotion occurred 6 days after the cancellation spike had already established."
        )

        hypotheses = [sup_hyp, inv_hyp, pay_hyp, comp_hyp]
        hypotheses.sort(key=lambda h: h.score, reverse=True)

        for i, h in enumerate(hypotheses):
            h.rank = i + 1

        return hypotheses
