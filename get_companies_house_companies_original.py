"""Companies house Search for Companies.

GOAL: We want to have an interface in python where we can search for companies in Companies House. The results need to be returned in a typing dataclass so
we can easily use this in the application.

Feel free to use any library or api (if available) to do the job, but it should be as simple and light as possible.

The interface below are the minimum requirement, for example enums are not complete and can be filled completely with the values.
If you feel motivated to go the extra mile by improving the interfaces then that is a bonus.

Companies House can always give errors, it would be nice to have those handled like making too much requests or connection failures.

Example URL: https://find-and-update.company-information.service.gov.uk/advanced-search/get-results?companyNameIncludes=Atradius&companyNameExcludes=&registeredOfficeAddress=&incorporationFromDay=&incorporationFromMonth=&incorporationFromYear=&incorporationToDay=&incorporationToMonth=&incorporationToYear=&sicCodes=&dissolvedFromDay=&dissolvedFromMonth=&dissolvedFromYear=&dissolvedToDay=&dissolvedToMonth=&dissolvedToYear=
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum


@dataclass
class IndustryCode:
    """SIC Industry Code Classification."""
    code: int
    description: str


@dataclass
class PreviousCompanyName:
    """Previous (legacy) company names.."""
    name: str
    start_period: datetime
    end_period: datetime


class CompanyType(Enum):
    """Types Of Companies."""
    PRIVATE_LIMITED_COMPANY = "private_limited_company"


class CompanyStatus(Enum):
    """Current status of Company."""
    ACTIVE = "active"


@dataclass
class Company:
    """Company Information."""
    # Primary Name of the company.
    primary_name: str

    # Local registration number
    local_registration_number: str

    # Flag indicating if the company is still active
    status: CompanyStatus

    company_type: CompanyType

    # Date of incorporation, None when cannot identify from website.
    incorporation_date: datetime

    # Optional date when the company was dissolved
    dissolved_date: Optional[datetime]

    # Information about the next reports will be published
    next_statement_date: Optional[datetime]
    last_statement_date: Optional[datetime]
    next_accounts_date: Optional[datetime]
    last_accounts_date: Optional[datetime]

    industry_codes: List[IndustryCode]

    previous_company_names: List[PreviousCompanyName]


def search_companies(
    name: Optional[str] = None,
    registration_number: Optional[str] = None,
    status: Optional[CompanyStatus] = CompanyStatus.ACTIVE
) -> List[Company]:
    """Search for companies in Companies House."""
    # For example using: https://find-and-update.company-information.service.gov.uk/advanced-search or smarter way if available
    return []


if __name__ == "__main__":
    search_companies(
        name="Atradius"
    )
