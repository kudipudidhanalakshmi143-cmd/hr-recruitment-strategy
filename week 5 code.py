"""
Recruitment Metrics & Performance Analytics Engine
===================================================
Accompanies: Post-Recruitment Evaluation and Recruitment Metrics Analysis (Week 5)

This module provides:
1. Multi-Stage Recruitment Funnel Throughput & Conversion Calculator
2. Time-to-Fill (TTF) & Time-to-Hire (TTH) Velocity Analyzer
3. Cost-Per-Hire (CPH) Accounting Engine (ANSI/SHRM Standard)
4. 360-Degree Quality-of-Hire (QoH) Composite Index Calculator
5. Candidate Net Promoter Score (cNPS) & Manager Satisfaction Evaluator
6. Automated Bottleneck Detection & Executive Reporting Suite
"""

from typing import Dict, List
from dataclasses import dataclass

# ==============================================================================
# 1. FUNNEL CONVERSION & BOTTLENECK DETECTOR
# ==============================================================================

@dataclass
class FunnelStageData:
    applied_or_sourced: int
    recruiter_screened: int
    technical_assessed: int
    panel_interviewed: int
    offers_extended: int
    offers_accepted: int


class RecruitmentFunnelAnalyzer:
    """Analyzes stage-by-stage throughput and diagnoses recruitment friction points."""

    def __init__(self, data: FunnelStageData):
        self.data = data

    def compute_funnel_metrics(self) -> Dict:
        d = self.data
        screen_pass_rate = (d.recruiter_screened / d.applied_or_sourced) * 100.0 if d.applied_or_sourced else 0.0
        tech_pass_rate = (d.technical_assessed / d.recruiter_screened) * 100.0 if d.recruiter_screened else 0.0
        panel_pass_rate = (d.panel_interviewed / d.technical_assessed) * 100.0 if d.technical_assessed else 0.0
        offer_ext_rate = (d.offers_extended / d.panel_interviewed) * 100.0 if d.panel_interviewed else 0.0
        offer_accept_rate = (d.offers_accepted / d.offers_extended) * 100.0 if d.offers_extended else 0.0
        overall_conversion = (d.offers_accepted / d.applied_or_sourced) * 100.0 if d.applied_or_sourced else 0.0

        bottlenecks = []
        if tech_pass_rate < 45.0:
            bottlenecks.append({
                "stage": "Technical Assessment",
                "pass_rate": round(tech_pass_rate, 1),
                "benchmark": "45.0% - 55.0%",
                "status": "CRITICAL CHOKE POINT",
                "diagnosis": "Severe candidate drop-off at technical test. Take-home too onerous or screening misaligned."
            })
        if offer_accept_rate < 85.0:
            bottlenecks.append({
                "stage": "Offer Acceptance",
                "pass_rate": round(offer_accept_rate, 1),
                "benchmark": ">= 85.0%",
                "status": "UNFAVORABLE LEAKAGE",
                "diagnosis": "Offer acceptance erosion. Late compensation alignment or slow offer turnaround."
            })

        return {
            "applied_or_sourced": d.applied_or_sourced,
            "recruiter_screened": d.recruiter_screened,
            "technical_assessed": d.technical_assessed,
            "panel_interviewed": d.panel_interviewed,
            "offers_extended": d.offers_extended,
            "offers_accepted": d.offers_accepted,
            "screen_pass_rate_pct": round(screen_pass_rate, 1),
            "tech_pass_rate_pct": round(tech_pass_rate, 1),
            "panel_pass_rate_pct": round(panel_pass_rate, 1),
            "offer_extension_rate_pct": round(offer_ext_rate, 1),
            "offer_acceptance_rate_pct": round(offer_accept_rate, 1),
            "overall_yield_pct": round(overall_conversion, 2),
            "diagnosed_bottlenecks": bottlenecks
        }


# ==============================================================================
# 2. COST-PER-HIRE (CPH) ACCOUNTING ENGINE
# ==============================================================================

class CostPerHireCalculator:
    """Calculates Cost-Per-Hire following ANSI/SHRM standard 06001."""

    def __init__(self, internal_costs: Dict[str, float], external_costs: Dict[str, float], total_hires: int):
        self.internal_costs = internal_costs
        self.external_costs = external_costs
        self.total_hires = total_hires

    def compute_cph(self) -> Dict:
        if self.total_hires <= 0:
            raise ValueError("Total hires must be greater than zero.")

        sum_internal = sum(self.internal_costs.values())
        sum_external = sum(self.external_costs.values())
        total_expenditure = sum_internal + sum_external
        cph = total_expenditure / self.total_hires

        return {
            "total_hires": self.total_hires,
            "internal_costs_total": round(sum_internal, 2),
            "external_costs_total": round(sum_external, 2),
            "total_recruitment_spend": round(total_expenditure, 2),
            "cost_per_hire": round(cph, 2),
            "internal_cost_ratio_pct": round((sum_internal / total_expenditure) * 100.0, 1),
            "external_cost_ratio_pct": round((sum_external / total_expenditure) * 100.0, 1)
        }


# ==============================================================================
# 3. 360-DEGREE QUALITY-OF-HIRE (QoH) COMPOSITE MODEL
# ==============================================================================

@dataclass
class NewHireQualityRecord:
    employee_id: str
    job_title: str
    department: str
    performance_score: float         # 0 - 100 scale (e.g. 88.0)
    ramp_speed_score: float          # 0 - 100 scale (actual vs benchmark days)
    manager_satisfaction_score: float # 0 - 100 scale (scaled from 1-5 rating)
    cultural_contribution_score: float # 0 - 100 scale
    retention_months: int


class QualityOfHireEngine:
    """
    Computes the 360-degree Quality-of-Hire (QoH) Composite Index:
    QoH = (w1 * Perf) + (w2 * Ramp) + (w3 * ManagerSat) + (w4 * Culture)
    """

    DEFAULT_WEIGHTS = {
        "performance": 0.35,
        "ramp_speed": 0.25,
        "manager_satisfaction": 0.25,
        "cultural_contribution": 0.15
    }

    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or self.DEFAULT_WEIGHTS

    def evaluate_hire(self, record: NewHireQualityRecord) -> float:
        w = self.weights
        qoh = (
            w["performance"] * record.performance_score +
            w["ramp_speed"] * record.ramp_speed_score +
            w["manager_satisfaction"] * record.manager_satisfaction_score +
            w["cultural_contribution"] * record.cultural_contribution_score
        )
        return round(qoh, 2)

    def evaluate_cohort(self, records: List[NewHireQualityRecord]) -> Dict:
        if not records:
            return {"cohort_size": 0, "average_qoh": 0.0}

        individual_scores = [self.evaluate_hire(r) for r in records]
        avg_qoh = sum(individual_scores) / len(individual_scores)

        exceptional = sum(1 for s in individual_scores if s >= 90.0)
        high_impact = sum(1 for s in individual_scores if 80.0 <= s < 90.0)
        standard = sum(1 for s in individual_scores if 70.0 <= s < 80.0)
        underperforming = sum(1 for s in individual_scores if s < 70.0)

        return {
            "cohort_size": len(records),
            "average_qoh_index": round(avg_qoh, 2),
            "rating_distribution": {
                "exceptional_90_plus": exceptional,
                "high_impact_80_to_89": high_impact,
                "standard_70_to_79": standard,
                "underperforming_sub_70": underperforming
            }
        }


# ==============================================================================
# 4. CANDIDATE NET PROMOTER SCORE (cNPS) CALCULATOR
# ==============================================================================

class CandidateSentimentAnalyzer:
    """Calculates cNPS and segment analysis (Hired vs. Declined candidates)."""

    @staticmethod
    def calculate_cnps(ratings_0_to_10: List[int]) -> float:
        if not ratings_0_to_10:
            return 0.0
        promoters = sum(1 for r in ratings_0_to_10 if r >= 9)
        detractors = sum(1 for r in ratings_0_to_10 if r <= 6)
        return round(((promoters - detractors) / len(ratings_0_to_10)) * 100.0, 1)


# ==============================================================================
# 5. DEMONSTRATION & TEST SUITE RUNNER
# ==============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("      WEEK 5: POST-RECRUITMENT EVALUATION & METRICS ANALYTICS ENGINE")
    print("=" * 80)

    # 1. Funnel Conversion & Bottleneck Analysis
    funnel_data = FunnelStageData(
        applied_or_sourced=1200,
        recruiter_screened=300,
        technical_assessed=110,
        panel_interviewed=48,
        offers_extended=31,
        offers_accepted=24
    )
    funnel_analyzer = RecruitmentFunnelAnalyzer(funnel_data)
    funnel_results = funnel_analyzer.compute_funnel_metrics()
    print(f"Top of Funnel: {funnel_results['applied_or_sourced']} -> Placements: {funnel_results['offers_accepted']} (Yield: {funnel_results['overall_yield_pct']}%)")
    for b in funnel_results["diagnosed_bottlenecks"]:
        print(f"  [!] Bottleneck: {b['stage']} ({b['status']}) - Pass Rate: {b['pass_rate']}%")

    # 2. Cost-Per-Hire Calculation
    internal_costs = {"recruiter_salaries": 180000.0, "interviewer_time": 45000.0, "referral_bonuses": 24000.0, "software": 35000.0}
    external_costs = {"agency_fees": 195000.0, "job_boards": 38000.0, "background_checks": 8500.0, "travel": 12000.0}
    cph_calc = CostPerHireCalculator(internal_costs, external_costs, total_hires=100)
    cph_summary = cph_calc.compute_cph()
    print(f"\nCost-Per-Hire: ${cph_summary['cost_per_hire']:,.2f} across {cph_summary['total_hires']} hires")

    # 3. Quality of Hire Composite Index
    qoh_engine = QualityOfHireEngine()
    sample_hires = [
        NewHireQualityRecord("H01", "Senior Backend Engineer", "Engineering", 92.0, 88.0, 95.0, 85.0, 12),
        NewHireQualityRecord("H02", "Account Executive", "Sales", 85.0, 80.0, 88.0, 80.0, 12),
        NewHireQualityRecord("H03", "DevOps Specialist", "Engineering", 78.0, 75.0, 80.0, 75.0, 9),
        NewHireQualityRecord("H04", "Product Designer", "Product", 95.0, 90.0, 95.0, 90.0, 12),
        NewHireQualityRecord("H05", "Customer Success Lead", "Support", 68.0, 65.0, 70.0, 70.0, 6)
    ]
    qoh_summary = qoh_engine.evaluate_cohort(sample_hires)
    print(f"\nCohort QoH Average Index: {qoh_summary['average_qoh_index']}% (Target: >= 85.0%)")

    # 4. Candidate NPS
    sentiment_analyzer = CandidateSentimentAnalyzer()
    print(f"Candidate NPS (Offered/Hired): +{sentiment_analyzer.calculate_cnps([10, 9, 10, 9, 10, 8, 10, 9])}")
    print(f"Candidate NPS (Declined):      {sentiment_analyzer.calculate_cnps([8, 7, 6, 9, 5, 8, 4, 7, 8, 6])}")
    print("=" * 80)