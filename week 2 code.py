"""
Candidate Sourcing & Talent Pipeline Development Toolkit
=========================================================
Automates Boolean/X-Ray query construction, capacity planning,
and personalized candidate engagement sequences.
"""

from typing import List, Dict, Any

class BooleanQueryBuilder:
    """Generates precise Boolean and Google X-Ray search strings across platforms."""

    @staticmethod
    def build_linkedin_xray(job_title: str, required_skills: List[str], 
                             optional_skills: List[str] = None, 
                             locations: List[str] = None, 
                             exclude_terms: List[str] = None) -> str:
        query_parts = ['site:linkedin.com/in']
        
        # Target Job Title
        query_parts.append(f'("{job_title}")')
        
        # Mandatory Skills (AND)
        if required_skills:
            req_str = " ".join([f'"{skill}"' for skill in required_skills])
            query_parts.append(f"({req_str})")
            
        # Optional Skills (OR)
        if optional_skills:
            opt_str = " OR ".join([f'"{skill}"' for skill in optional_skills])
            query_parts.append(f"({opt_str})")
            
        # Target Locations (OR)
        if locations:
            loc_str = " OR ".join([f'"{loc}"' for loc in locations])
            query_parts.append(f"({loc_str})")
            
        # Standard Exclusions
        exclusions = ["jobs", "recruiter", "careers", "intern"]
        if exclude_terms:
            exclusions.extend(exclude_terms)
        for term in set(exclusions):
            query_parts.append(f"-intitle:{term}")
            
        return " ".join(query_parts)

    @staticmethod
    def build_github_search(language: str, location: str, min_repos: int = 5, min_followers: int = 10) -> str:
        return f"language:{language} location:{location} repos:>{min_repos} followers:>{min_followers}"


class SourcingFunnelCalculator:
    """Calculates reverse-funnel volume and recruiter capacity required to hit target hires."""

    DEFAULT_CONVERSIONS = {
        "sourced_to_response": 0.35,      # 35% response rate
        "response_to_screen": 0.50,       # 50% qualified & agree to call
        "screen_to_technical": 0.40,      # 40% pass recruiter screen
        "technical_to_final": 0.50,       # 50% pass technical assessment
        "final_to_offer": 0.75,           # 75% pass final panel & receive offer
        "offer_to_accept": 0.85           # 85% offer acceptance rate
    }

    def __init__(self, conversion_rates: Dict[str, float] = None):
        self.conversions = conversion_rates or self.DEFAULT_CONVERSIONS

    def calculate_pipeline_requirements(self, target_hires: int) -> Dict[str, Any]:
        """Calculates stage-by-stage candidate volumes needed to secure target_hires."""
        offers_accepted = target_hires
        offers_extended = round(offers_accepted / self.conversions["offer_to_accept"])
        final_panels = round(offers_extended / self.conversions["final_to_offer"])
        technical_tests = round(final_panels / self.conversions["technical_to_final"])
        recruiter_screens = round(technical_tests / self.conversions["screen_to_technical"])
        responding_candidates = round(recruiter_screens / self.conversions["response_to_screen"])
        profiles_to_source = round(responding_candidates / self.conversions["sourced_to_response"])

        return {
            "target_hires": target_hires,
            "profiles_to_source": profiles_to_source,
            "expected_responses": responding_candidates,
            "recruiter_screens_needed": recruiter_screens,
            "technical_assessments": technical_tests,
            "final_panel_interviews": final_panels,
            "offers_to_extend": offers_extended
        }


class CandidateEngagementGenerator:
    """Generates hyper-personalized multi-touch email drip sequences."""

    @staticmethod
    def generate_sequence(candidate_name: str, current_company: str, 
                          specific_project: str, primary_skill: str, 
                          company_name: str, recruiter_name: str, 
                          blog_link: str) -> Dict[str, str]:
        
        touch_1 = f"""Subject: Your work on {specific_project} + {company_name}

Hi {candidate_name},

I came across your recent work on {specific_project}—specifically your approach to {primary_skill}. It immediately caught our engineering team's attention because we are currently solving a very similar scaling challenge at {company_name}.

We are scaling our core engineering team and seeking someone with deep expertise in {primary_skill}. Given your background at {current_company}, I thought your perspective would be invaluable.

I'd love to share what our leadership is building over the next 12 months. Would you be open to an informal 15-minute conversation this Thursday or Friday?

Best regards,
{recruiter_name} | Senior Technical Talent Partner
{company_name}"""

        touch_2 = f"""Subject: Re: Your work on {specific_project}

Hi {candidate_name},

I know you're heads-down, so I wanted to share a quick piece of context rather than follow up empty-handed.

Our team recently published an architectural teardown on how we optimized our data pipelines for high throughput: {blog_link}.

Given your work with {primary_skill}, I thought you might appreciate the approach we took. If this sparks any curiosity, I'd still welcome the chance to connect briefly.

Cheers,
{recruiter_name}"""

        touch_3 = f"""Subject: Closing the loop / Staying in touch

Hi {candidate_name},

I haven't heard back, which usually means one of two things: you're fully engaged in meaningful work at {current_company}, or my timing is completely off!

Either way, I promise not to keep cluttering your inbox. I think your work in {primary_skill} is exceptional, and I'd love to stay connected for whenever the timing makes sense down the road.

Wishing you and the team at {current_company} continued success.

Warm regards,
{recruiter_name}"""

        return {
            "Day_1_Initial_Hook": touch_1,
            "Day_4_Value_Add": touch_2,
            "Day_14_Graceful_Breakup": touch_3
        }


if __name__ == "__main__":
    builder = BooleanQueryBuilder()
    query = builder.build_linkedin_xray(
        job_title="Senior Backend Engineer",
        required_skills=["Python", "Distributed Systems"],
        optional_skills=["Golang", "Kubernetes"],
        locations=["San Francisco", "Remote"]
    )
    print("GENERATED GOOGLE X-RAY SEARCH QUERY:\n", query)

    calculator = SourcingFunnelCalculator()
    print("\nREVERSE FUNNEL CAPACITY (TARGET: 3 HIRES):\n", 
          calculator.calculate_pipeline_requirements(target_hires=3))