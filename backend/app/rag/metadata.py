from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class DocumentSpec:
    """
    Specification and verified metadata for institutional documents.
    """
    file_name: str
    document_name: str
    document_category: str  # academics, examinations, schedule, disclosure, placement, research, policy
    program: str            # B.E./B.Tech, M.E./M.Tech, MBA, All
    regulation: str         # R2022, R2026, R2021, R2024, General, None
    academic_year: Optional[str]
    document_status: str    # current, historical, amendment, reference, unknown
    source_type: str        # official_regulation, official_schedule, official_disclosure, competitive_guideline, national_policy
    is_included_in_primary_rag: bool
    exclusion_reason: Optional[str] = None


# Registry of all 16 PDFs based on comprehensive dataset inspection
DATASET_REGISTRY: Dict[str, DocumentSpec] = {
    # 1. UG Regulations R2022
    "B.E.-B.Tech-Regulations-2022-Version-1_-18.09.2026.pdf": DocumentSpec(
        file_name="B.E.-B.Tech-Regulations-2022-Version-1_-18.09.2026.pdf",
        document_name="B.E./B.Tech Academic Rules and Regulations 2022",
        document_category="academics",
        program="B.E./B.Tech",
        regulation="R2022",
        academic_year="2022-2026",
        document_status="current",
        source_type="official_regulation",
        is_included_in_primary_rag=True
    ),
    # 2. UG Regulations R2026
    "R2026_Regulation-Updated-as-on-09.09.2026_Approved.pdf": DocumentSpec(
        file_name="R2026_Regulation-Updated-as-on-09.09.2026_Approved.pdf",
        document_name="B.E./B.Tech CBCS Regulations 2026",
        document_category="academics",
        program="B.E./B.Tech",
        regulation="R2026",
        academic_year="2026-2030",
        document_status="current",
        source_type="official_regulation",
        is_included_in_primary_rag=True
    ),
    # 3. Amendments R2018/R2022
    "Amendments-of-the-Revised-R2018-and-Regulations-2022-approved-V3.pdf": DocumentSpec(
        file_name="Amendments-of-the-Revised-R2018-and-Regulations-2022-approved-V3.pdf",
        document_name="Amendments to Regulations 2018 (Revised) and 2022",
        document_category="academics",
        program="B.E./B.Tech",
        regulation="R2018-R2022-Amendments",
        academic_year="2022-2024",
        document_status="amendment",
        source_type="official_regulation",
        is_included_in_primary_rag=True
    ),
    # 4. ACM 32nd Relative Grading Amendment
    "Amendments_R2022_32-ACM.pdf": DocumentSpec(
        file_name="Amendments_R2022_32-ACM.pdf",
        document_name="Regulations 2022 Relative Grading Amendment (32nd ACM)",
        document_category="examinations",
        program="B.E./B.Tech",
        regulation="R2022",
        academic_year="2022-2026",
        document_status="amendment",
        source_type="official_regulation",
        is_included_in_primary_rag=True
    ),
    # 5. PG Regulations R2024
    "R2024-ME-MTech-Regulations-V1.pdf": DocumentSpec(
        file_name="R2024-ME-MTech-Regulations-V1.pdf",
        document_name="M.E./M.Tech Regulations 2024 CBCS",
        document_category="academics",
        program="M.E./M.Tech",
        regulation="R2024",
        academic_year="2024-2026",
        document_status="current",
        source_type="official_regulation",
        is_included_in_primary_rag=True
    ),
    # 6. PG Amendments R2021
    "Amendment-Regulations-2021-PG-V3.pdf": DocumentSpec(
        file_name="Amendment-Regulations-2021-PG-V3.pdf",
        document_name="M.E./M.Tech Rules & Regulations 2021 Amendments (27th ACM)",
        document_category="academics",
        program="M.E./M.Tech",
        regulation="R2021",
        academic_year="2021-2023",
        document_status="amendment",
        source_type="official_regulation",
        is_included_in_primary_rag=True
    ),
    # 7. MBA Regulations R2024
    "MBA-Regulations-2024.V5.pdf": DocumentSpec(
        file_name="MBA-Regulations-2024.V5.pdf",
        document_name="MBA Degree Programme Regulations 2024 (102 Credits CBCS)",
        document_category="academics",
        program="MBA",
        regulation="R2024",
        academic_year="2024-2026",
        document_status="current",
        source_type="official_regulation",
        is_included_in_primary_rag=True
    ),
    # 8. AICTE Mandatory Disclosure (Campus, Hostel, Fees, Facilities)
    "aicte-mandatory-disclosure.pdf": DocumentSpec(
        file_name="aicte-mandatory-disclosure.pdf",
        document_name="AICTE Mandatory Institutional Disclosure (BIT Sathyamangalam)",
        document_category="disclosure",
        program="All",
        regulation="institutional",
        academic_year="2026-2027",
        document_status="current",
        source_type="official_disclosure",
        is_included_in_primary_rag=True
    ),
    # 9. Even Semester Academic Schedule 2025-2026
    "2025-2026-EVEN-SEMESTER-ACADEMIC-SCHEDULE.pdf": DocumentSpec(
        file_name="2025-2026-EVEN-SEMESTER-ACADEMIC-SCHEDULE.pdf",
        document_name="Academic Schedule Even Semester 2025-2026",
        document_category="schedule",
        program="All",
        regulation="institutional",
        academic_year="2025-2026",
        document_status="current",
        source_type="official_schedule",
        is_included_in_primary_rag=True
    ),
    # 10. Odd Semester Academic Calendar 2025-2026
    "Academic-Calendar-2025-2026-Odd-Semester.pdf": DocumentSpec(
        file_name="Academic-Calendar-2025-2026-Odd-Semester.pdf",
        document_name="Academic Calendar Odd Semester 2025-2026",
        document_category="schedule",
        program="All",
        regulation="institutional",
        academic_year="2025-2026",
        document_status="current",
        source_type="official_schedule",
        is_included_in_primary_rag=True
    ),
    # 11. Tata Imagination Challenge TAS Pre-Placement Guidelines
    "c6f54aea-dfa7-4a77-a3a2-bee19c038660 tata.pdf": DocumentSpec(
        file_name="c6f54aea-dfa7-4a77-a3a2-bee19c038660 tata.pdf",
        document_name="Tata Imagination Challenge 2026 TAS Pre-Placement Opportunity Guidelines",
        document_category="placement",
        program="All",
        regulation="placement",
        academic_year="2026",
        document_status="current",
        source_type="competitive_guideline",
        is_included_in_primary_rag=True
    ),
    # 12. Tata Imagination Challenge 2026 Idea Guide Book
    "54c13c1a-f901-47c5-ab98-d0441d6633ea tata.pdf": DocumentSpec(
        file_name="54c13c1a-f901-47c5-ab98-d0441d6633ea tata.pdf",
        document_name="Tata Imagination Challenge 2026 Idea Guide Book",
        document_category="placement",
        program="All",
        regulation="placement",
        academic_year="2026",
        document_status="current",
        source_type="competitive_guideline",
        is_included_in_primary_rag=True
    ),
    # 13. AICTE Productization Fellowship FAQ
    "FAQ_APL _22052025.pdf": DocumentSpec(
        file_name="FAQ_APL _22052025.pdf",
        document_name="AICTE Productization Fellowship (APF) FAQs",
        document_category="research",
        program="All",
        regulation="fellowship",
        academic_year="2025",
        document_status="current",
        source_type="official_disclosure",
        is_included_in_primary_rag=True
    ),
    # 14. Excluded: 11th Five Year Plan Education
    "eleventh_five_year_plan_education_2007_12.pdf": DocumentSpec(
        file_name="eleventh_five_year_plan_education_2007_12.pdf",
        document_name="Eleventh Five Year Plan Education 2007-2012",
        document_category="policy",
        program="National",
        regulation="unknown",
        academic_year="2007-2012",
        document_status="reference",
        source_type="national_policy",
        is_included_in_primary_rag=False,
        exclusion_reason="External national macro-policy document from 2007-2012 Planning Commission; not relevant for institutional college student FAQ."
    ),
    # 15. Excluded: Engendering 11th Plan
    "engendering_XI_five_year_plan.pdf": DocumentSpec(
        file_name="engendering_XI_five_year_plan.pdf",
        document_name="Engendering the Eleventh Five-Year Plan 2007-2012",
        document_category="policy",
        program="National",
        regulation="unknown",
        academic_year="2007-2012",
        document_status="reference",
        source_type="national_policy",
        is_included_in_primary_rag=False,
        exclusion_reason="External national policy advocacy report; not relevant for institutional college student FAQ."
    ),
    # 16. Excluded: Higher Education 11th Plan Working Group
    "higher_education_XIplan.pdf": DocumentSpec(
        file_name="higher_education_XIplan.pdf",
        document_name="Report of Working Group on Higher Education 11th Plan",
        document_category="policy",
        program="National",
        regulation="unknown",
        academic_year="2007-2012",
        document_status="reference",
        source_type="national_policy",
        is_included_in_primary_rag=False,
        exclusion_reason="122-page external macro-policy working group report from Government of India Planning Commission; contains no college-specific operational FAQs."
    ),
}


def get_document_spec(file_name: str) -> DocumentSpec:
    """
    Lookup document specification from verified registry.
    If unknown file, return safe fallback without guessing.
    """
    if file_name in DATASET_REGISTRY:
        return DATASET_REGISTRY[file_name]

    return DocumentSpec(
        file_name=file_name,
        document_name=file_name.replace(".pdf", ""),
        document_category="unknown",
        program="unknown",
        regulation="unknown",
        academic_year=None,
        document_status="unknown",
        source_type="unknown",
        is_included_in_primary_rag=False,
        exclusion_reason="Unregistered document file in dataset directory."
    )
