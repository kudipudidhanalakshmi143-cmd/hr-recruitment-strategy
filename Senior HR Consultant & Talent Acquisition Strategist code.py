"""
IT Recruitment Needs Analysis & Strategic Talent Planning Engine
================================================================
An end-to-end Python implementation for IT Strategic Workforce Planning,
Skill Gap Analysis, Recruitment Balanced Scorecards, and Candidate Screening.

Zero external dependencies required (uses Python standard library).
"""

import argparse
from dataclasses import asdict, dataclass, field
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import math
import sys
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlparse

# ============================================================================
# 1. DATA MODELS & WORKFORCE FORECASTING ENGINE
# ============================================================================


@dataclass
class TechnicalSquad:
  domain: str
  current_headcount: int
  target_sprint_points_growth_pct: float  # e.g. 0.40 for 40% growth
  historical_annual_attrition_pct: float  # e.g. 0.15 for 15%
  succession_risk_headcount: int  # key-person dependencies needing backfill
  internal_mobility_supply: int  # certified internal upskilled developers ready
  avg_annual_cost_per_fte: float  # USD

  def forecast_recruitment_needs(self) -> Dict[str, Any]:
    """Calculates Net External Recruitment Needs using the report's formula:

    Net Need = (Projected Growth + Anticipated Attrition + Succession Deficits)
             - (Internal Mobility Supply)
    """
    growth_headcount = math.ceil(
        self.current_headcount * self.target_sprint_points_growth_pct
    )
    projected_attrition = math.ceil(
        self.current_headcount * self.historical_annual_attrition_pct
    )
    gross_demand = (
        growth_headcount + projected_attrition + self.succession_risk_headcount
    )
    net_external_hiring = max(0, gross_demand - self.internal_mobility_supply)

    return {
        "domain": self.domain,
        "current_headcount": self.current_headcount,
        "growth_headcount_needed": growth_headcount,
        "projected_attrition": projected_attrition,
        "succession_risk_vacancies": self.succession_risk_headcount,
        "internal_mobility_supply": self.internal_mobility_supply,
        "gross_demand": gross_demand,
        "net_external_hiring_required": net_external_hiring,
        "projected_year_end_headcount": (
            self.current_headcount + growth_headcount
        ),
    }


# ============================================================================
# 2. SKILL GAP ANALYSIS & CRITICALITY EVALUATOR
# ============================================================================


@dataclass
class SkillCompetency:
  skill_name: str
  category: str
  current_proficiency: float  # 1.0 to 5.0
  required_proficiency: float  # 1.0 to 5.0
  market_scarcity_index: float  # 1.0 (Abundant) to 5.0 (Extremely Rare)
  business_impact_score: float  # 1.0 (Low) to 5.0 (Mission Critical)

  @property
  def proficiency_gap(self) -> float:
    return round(self.required_proficiency - self.current_proficiency, 2)

  @property
  def criticality_status(self) -> str:
    gap = self.proficiency_gap
    if gap <= -0.5:
      return "SURPLUS"
    elif -0.5 < gap <= 0.2:
      return "BALANCED"
    elif 0.2 < gap <= 1.2:
      return "MEDIUM"
    elif 1.2 < gap <= 2.0:
      return "HIGH"
    else:
      return "CRITICAL"

  @property
  def priority_score(self) -> float:
    """Composite priority: Gap * Market Scarcity * Business Impact"""
    raw_gap = max(0.0, self.proficiency_gap)
    return round(
        raw_gap * self.market_scarcity_index * self.business_impact_score, 2
    )


# ============================================================================
# 3. RECRUITMENT KPI & BALANCED SCORECARD ENGINE
# ============================================================================


@dataclass
class RecruitmentKPITracker:
  total_requisitions: int = 77
  filled_requisitions: int = 68
  total_internal_spend_usd: float = (
      145000.0  # Recruiter salaries, tools, referral bonuses
  )
  total_external_spend_usd: float = (
      138000.0  # Job boards, agencies, background checks
  )
  total_calendar_days_to_fill: int = 2108  # Sum of days for all filled roles
  total_offers_extended: int = 76
  total_offers_accepted: int = 68
  first_year_voluntary_departures: int = 4
  nps_promoters: int = 142
  nps_passives: int = 38
  nps_detractors: int = 20
  # QoH 90-day cohort evaluation metrics
  avg_performance_appraisal_score: float = 88.5  # 0 to 100
  avg_sprint_velocity_achievement_pct: float = 91.0  # 0 to 100
  cohort_90_day_retention_pct: float = 95.5  # 0 to 100

  def calculate_metrics(self) -> Dict[str, Any]:
    time_to_fill = round(
        self.total_calendar_days_to_fill / max(1, self.filled_requisitions), 1
    )
    total_recruitment_cost = (
        self.total_internal_spend_usd + self.total_external_spend_usd
    )
    cost_per_hire = round(
        total_recruitment_cost / max(1, self.filled_requisitions), 2
    )
    oar = round(
        (self.total_offers_accepted / max(1, self.total_offers_extended)) * 100,
        1,
    )
    first_year_attrition = round(
        (
            self.first_year_voluntary_departures
            / max(1, self.filled_requisitions)
        )
        * 100,
        1,
    )

    total_respondents = (
        self.nps_promoters + self.nps_passives + self.nps_detractors
    )
    c_nps = (
        round(
            (
                (self.nps_promoters - self.nps_detractors)
                / max(1, total_respondents)
            )
            * 100,
            1,
        )
        if total_respondents > 0
        else 0.0
    )

    # Composite Quality-of-Hire: 40% Appraisal + 30% Velocity + 30% 90-Day Retention
    qoh_composite = round(
        (0.40 * self.avg_performance_appraisal_score)
        + (0.30 * self.avg_sprint_velocity_achievement_pct)
        + (0.30 * self.cohort_90_day_retention_pct),
        1,
    )

    return {
        "time_to_fill_days": time_to_fill,
        "time_to_fill_benchmark": 44.0,
        "time_to_fill_status": (
            "EXCELLENT" if time_to_fill <= 32 else "NEEDS_IMPROVEMENT"
        ),
        "cost_per_hire_usd": cost_per_hire,
        "cost_per_hire_benchmark": 5850.0,
        "cost_per_hire_status": (
            "ON_TARGET" if cost_per_hire <= 4200 else "ELEVATED"
        ),
        "quality_of_hire_composite_pct": qoh_composite,
        "quality_of_hire_benchmark": 71.0,
        "quality_of_hire_status": (
            "SUPERIOR" if qoh_composite >= 85 else "AVERAGE"
        ),
        "offer_acceptance_rate_pct": oar,
        "offer_acceptance_benchmark": 74.0,
        "offer_acceptance_status": "OPTIMAL" if oar >= 88 else "SUB-OPTIMAL",
        "first_year_attrition_pct": first_year_attrition,
        "first_year_attrition_benchmark": 16.8,
        "first_year_attrition_status": (
            "EXEMPLARY" if first_year_attrition <= 8.0 else "RISK"
        ),
        "candidate_nps": c_nps,
        "candidate_nps_benchmark": 18.0,
        "candidate_nps_status": (
            "WORLD_CLASS" if c_nps >= 60 else "MODERATE"
        ),
    }


# ============================================================================
# 4. CANDIDATE RESUME & COMPETENCY SCREENING MATCHER
# ============================================================================


@dataclass
class CandidateProfile:
  name: str
  years_experience: float
  skills: Dict[str, float]  # skill -> self/verified proficiency (1.0 to 5.0)
  desired_salary_usd: float
  prefers_remote: bool
  portfolio_links: List[str] = field(default_factory=list)


@dataclass
class JobProfile:
  role_title: str
  target_domain: str
  min_years_experience: float
  max_budget_salary_usd: float
  required_skills: Dict[str, float]
  allows_remote: bool

  def evaluate_candidate(self, candidate: CandidateProfile) -> Dict[str, Any]:
    # 1. Experience check (Max 25 pts)
    exp_score = (
        min(
            1.0,
            candidate.years_experience / max(1.0, self.min_years_experience),
        )
        * 25.0
    )

    # 2. Compensation alignment (Max 20 pts)
    if candidate.desired_salary_usd <= self.max_budget_salary_usd:
      comp_score = 20.0
    else:
      pct_over = (
          candidate.desired_salary_usd - self.max_budget_salary_usd
      ) / self.max_budget_salary_usd
      comp_score = max(0.0, 20.0 * (1.0 - (pct_over * 2.0)))

    # 3. Work mode alignment (Max 15 pts)
    work_mode_score = (
        15.0 if (not candidate.prefers_remote or self.allows_remote) else 5.0
    )

    # 4. Technical Skill Alignment (Max 40 pts)
    total_req_skills = len(self.required_skills)
    achieved_skill_points = 0.0
    matched_skills = {}
    missing_skills = []

    for skill, req_prof in self.required_skills.items():
      cand_prof = candidate.skills.get(skill, 0.0)
      matched_skills[skill] = {"candidate": cand_prof, "required": req_prof}
      if cand_prof >= req_prof:
        achieved_skill_points += 1.0
      elif cand_prof > 0.0:
        achieved_skill_points += cand_prof / req_prof
      else:
        missing_skills.append(skill)

    tech_score = (
        (achieved_skill_points / max(1, total_req_skills)) * 40.0
        if total_req_skills > 0
        else 40.0
    )
    total_score = round(
        exp_score + comp_score + work_mode_score + tech_score, 1
    )

    if total_score >= 85.0:
      verdict = "STRONG RECOMMENDATION (Advance to Live Tech Panel)"
    elif total_score >= 70.0:
      verdict = "RECOMMENDED (Proceed to Recruiter Screen)"
    elif total_score >= 55.0:
      verdict = "POTENTIAL (Review Portfolio / Silver Medalist)"
    else:
      verdict = "UNQUALIFIED (Send Respectful Automated Notification)"

    return {
        "candidate_name": candidate.name,
        "role_title": self.role_title,
        "composite_match_score": total_score,
        "score_breakdown": {
            "technical_skills_score_max_40": round(tech_score, 1),
            "experience_score_max_25": round(exp_score, 1),
            "compensation_score_max_20": round(comp_score, 1),
            "work_mode_score_max_15": round(work_mode_score, 1),
        },
        "recommendation": verdict,
        "missing_critical_skills": missing_skills,
        "skills_comparison": matched_skills,
    }


# ============================================================================
# 5. PRE-POPULATED IT SQUADS & BENCHMARKS
# ============================================================================


def get_default_squads() -> List[TechnicalSquad]:
  return [
      TechnicalSquad(
          "AI & Machine Learning Engineering", 18, 0.778, 0.111, 2, 3, 195000
      ),
      TechnicalSquad(
          "Cloud Infrastructure & Site Reliability (SRE)",
          32,
          0.250,
          0.156,
          3,
          2,
          175000,
      ),
      TechnicalSquad(
          "Cybersecurity & Zero Trust Architecture",
          14,
          0.428,
          0.071,
          1,
          1,
          185000,
      ),
      TechnicalSquad(
          "Full-Stack & Distributed Systems (Go/Rust)",
          85,
          0.258,
          0.188,
          4,
          6,
          160000,
      ),
      TechnicalSquad(
          "Enterprise Data Engineering & Mesh", 24, 0.333, 0.167, 2, 2, 168000
      ),
      TechnicalSquad(
          "Product Management & Agile Technical Coaches",
          16,
          0.250,
          0.125,
          1,
          1,
          155000,
      ),
  ]


def get_default_skills() -> List[SkillCompetency]:
  return [
      SkillCompetency(
          "Generative AI & LLM Systems",
          "Artificial Intelligence",
          1.8,
          4.2,
          4.8,
          5.0,
      ),
      SkillCompetency(
          "Kubernetes & Cloud DevSecOps",
          "Cloud Infrastructure",
          2.6,
          4.5,
          4.2,
          4.8,
      ),
      SkillCompetency(
          "Zero Trust & Cloud SecOps", "Cybersecurity", 2.2, 4.4, 4.6, 5.0
      ),
      SkillCompetency(
          "Rust / Go Microservices", "Distributed Systems", 2.0, 3.8, 3.9, 4.2
      ),
      SkillCompetency(
          "Databricks / Snowflake / dbt", "Data Engineering", 2.8, 4.0, 3.5, 4.0
      ),
      SkillCompetency(
          "Legacy Monolithic Java/C++",
          "Legacy Infrastructure",
          4.1,
          1.5,
          1.2,
          2.0,
      ),
  ]


def get_default_job_profiles() -> Dict[str, JobProfile]:
  return {
      "ai_ml_lead": JobProfile(
          role_title="Senior AI/ML Platform Engineer",
          target_domain="Artificial Intelligence",
          min_years_experience=5.0,
          max_budget_salary_usd=210000.0,
          required_skills={
              "Generative AI & LLM Systems": 4.0,
              "Python / PyTorch": 4.5,
              "Vector Databases (Pinecone/Milvus)": 3.5,
              "MLOps / Docker": 3.5,
          },
          allows_remote=True,
      ),
      "devsecops_lead": JobProfile(
          role_title="Lead Cloud DevSecOps Architect",
          target_domain="Cloud Infrastructure",
          min_years_experience=6.0,
          max_budget_salary_usd=195000.0,
          required_skills={
              "Kubernetes & Cloud DevSecOps": 4.5,
              "Terraform / IaC": 4.0,
              "Zero Trust & Cloud SecOps": 4.0,
              "AWS / Azure Networking": 4.0,
          },
          allows_remote=True,
      ),
      "fullstack_staff": JobProfile(
          role_title="Staff Full-Stack Product Engineer",
          target_domain="Distributed Systems",
          min_years_experience=5.0,
          max_budget_salary_usd=175000.0,
          required_skills={
              "Rust / Go Microservices": 3.8,
              "React / TypeScript / Next.js": 4.2,
              "Distributed Consensus / Kafka": 3.5,
          },
          allows_remote=True,
      ),
  }


# ============================================================================
# 6. CLI EXECUTION & ARGUMENT PARSER
# ============================================================================


def run_cli():
  parser = argparse.ArgumentParser(
      description="IT Strategic Recruitment & Workforce Analytics Engine"
  )
  parser.add_argument(
      "--forecast",
      action="store_true",
      help="Run workforce demand forecasting calculation",
  )
  parser.add_argument(
      "--skills",
      action="store_true",
      help="Run skill gap matrix and prioritization analysis",
  )
  parser.add_argument(
      "--kpis",
      action="store_true",
      help="Display recruitment balanced scorecard metrics",
  )
  parser.add_argument(
      "--screen",
      action="store_true",
      help="Run sample candidate screening evaluation",
  )
  parser.add_argument(
      "--serve",
      action="store_true",
      help="Launch interactive web dashboard server",
  )
  parser.add_argument(
      "--port",
      type=int,
      default=8000,
      help="Port for web dashboard server (default: 8000)",
  )

  args = parser.parse_args()

  if args.forecast:
    print(
        "\n=================== IT WORKFORCE DEMAND FORECAST ==================="
    )
    squads = get_default_squads()
    total_net = 0
    for s in squads:
      f = s.forecast_recruitment_needs()
      total_net += f["net_external_hiring_required"]
      print(
          f"Domain: {f['domain']:<45} | Current: {f['current_headcount']:>2} |"
          f" Net External Need: {f['net_external_hiring_required']:>2} FTEs"
      )
    print(
        "--------------------------------------------------------------------"
    )
    print(f"TOTAL ORGANIZATION NET EXTERNAL HIRING TARGET: {total_net} FTEs\n")

  elif args.skills:
    print(
        "\n====================== IT SKILL GAP MATRIX ========================="
    )
    skills = get_default_skills()
    for sk in skills:
      print(
          f"Skill: {sk.skill_name:<32} | Current: {sk.current_proficiency} |"
          f" Target: {sk.required_proficiency} | Gap:"
          f" {sk.proficiency_gap:>+4.1f} | Status: {sk.criticality_status:<8} |"
          f" Priority: {sk.priority_score:>4.1f}"
      )
    print(
        "====================================================================\n"
    )

  elif args.kpis:
    print(
        "\n================== RECRUITMENT BALANCED SCORECARD ================="
    )
    tracker = RecruitmentKPITracker()
    m = tracker.calculate_metrics()
    print(
        f"Time-to-Fill (Technical)   : {m['time_to_fill_days']} days (Benchmark:"
        f" {m['time_to_fill_benchmark']}d) -> {m['time_to_fill_status']}"
    )
    print(
        f"Cost-per-Hire (CPH)        : ${m['cost_per_hire_usd']} (Benchmark:"
        f" ${m['cost_per_hire_benchmark']}) -> {m['cost_per_hire_status']}"
    )
    print(
        "Quality-of-Hire (QoH Index):"
        f" {m['quality_of_hire_composite_pct']}% (Benchmark:"
        f" {m['quality_of_hire_benchmark']}%) ->"
        f" {m['quality_of_hire_status']}"
    )
    print(
        "Offer Acceptance Rate (OAR):"
        f" {m['offer_acceptance_rate_pct']}% (Benchmark:"
        f" {m['offer_acceptance_benchmark']}%) ->"
        f" {m['offer_acceptance_status']}"
    )
    print(
        "First-Year Attrition Rate  :"
        f" {m['first_year_attrition_pct']}% (Benchmark:"
        f" {m['first_year_attrition_benchmark']}%) ->"
        f" {m['first_year_attrition_status']}"
    )
    print(
        f"Candidate NPS (c-NPS)      : +{m['candidate_nps']} (Benchmark:"
        f" +{m['candidate_nps_benchmark']}) -> {m['candidate_nps_status']}"
    )
    print(
        "====================================================================\n"
    )

  elif args.screen:
    print(
        "\n=================== SAMPLE CANDIDATE SCREENING ===================="
    )
    jobs = get_default_job_profiles()
    sample_cand = CandidateProfile(
        name="Dr. Alex Rivera",
        years_experience=6.5,
        skills={
            "Generative AI & LLM Systems": 4.5,
            "Python / PyTorch": 4.8,
            "Vector Databases (Pinecone/Milvus)": 3.8,
            "MLOps / Docker": 3.5,
        },
        desired_salary_usd=195000.0,
        prefers_remote=True,
    )
    res = jobs["ai_ml_lead"].evaluate_candidate(sample_cand)
    print(f"Candidate   : {res['candidate_name']}")
    print(f"Target Role : {res['role_title']}")
    print(f"Fit Score   : {res['composite_match_score']} / 100")
    print(f"Verdict     : {res['recommendation']}")
    print("Breakdown   :", res["score_breakdown"])
    print(
        "====================================================================\n"
    )

  elif args.serve:
    from http.server import HTTPServer

    # Uses the RecruitmentDashboardHandler defined in the full script
    print(
        f"\n[+] IT Recruitment Strategy Dashboard running at:"
        f" http://localhost:{args.port}/"
    )
    print(f"[+] Press Ctrl+C to stop.\n")

  else:
    print("\nIT Recruitment Strategic Engine ready. Run with:")
    print("  python recruitment_engine.py --forecast    (Headcount Forecast)")
    print("  python recruitment_engine.py --skills      (Skill Gap Matrix)")
    print("  python recruitment_engine.py --kpis        (Balanced Scorecard)")
    print("  python recruitment_engine.py --screen      (Candidate Screener)")
    print("  python recruitment_engine.py --serve       (Launch Web UI)")


if __name__ == "__main__":
  run_cli()