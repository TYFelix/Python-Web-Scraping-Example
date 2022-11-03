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
import requests
from bs4 import BeautifulSoup


@dataclass
class IndustryCode:
    """SIC Industry Code Classification."""

    code: int
    description: str


@dataclass
class PreviousCompanyName:
    """Previous (legacy) company names."""

    name: str
    start_period: datetime
    end_period: datetime


class CompanyType(Enum):
    """Types Of Companies."""

    ASSURANCE_COMPANY = "Assurance company"
    CHARITABLE_INCORPORATED_ORGANISATION = "Charitable incorporated organisation"
    CONVERTED_CLOSED = "Converted / closed"
    CREDIT_UNION_NORTHERN_IRELAND = "Credit union (Northern Ireland)"
    EUROPEAN_ECONOMIC_INTEREST_GROUPING = "European Economic Interest Grouping (EEIG)"
    EUROPEAN_PUBLIC_LIMITED_LIABILITY_COMPANY = "European public limited liability company (SE)"
    FURTHER_EDUCATION_OR_SIXTH_FORM_COLLEGE_CORPORATION = "Further education or sixth form college corporation"
    INDUSTRIAL_AND_PROVIDENT_SOCIETY = "Industrial and Provident society"
    INVESTMENT_COMPANY_WITH_VARIABLE_CAPITAL = "Investment company with variable capital"
    LIMITED_LIABILITY_PARTNERSHIP = "Limited liability partnership"
    LIMITED_PARTNERSHIP = "Limited partnership"
    NORTHERN_IRELAND_COMPANY = "Northern Ireland company"
    OLD_PUBLIC_COMPANY = "Old public company"
    OVERSEAS_COMPANY = "Overseas company"
    OVERSEAS_ENTITY = "Overseas entity"
    PRIVATE_LIMITED_BY_GUARANTEE_WITHOUT_SHARE_CAPITAL = "Private limited by guarantee without share capital"
    PRIVATE_LIMITED_COMPANY = "Private limited company"
    PRIVATE_LIMITED_COMPANY_BY_GUARANTEE_WITHOUT_SHARE_CAPITAL = "Private Limited Company by guarantee without share capital, use of 'Limited' exemption"
    PRIVATE_LIMITED_COMPANY_EXEMPTION = "Private Limited Company, use of 'Limited' exemption"
    PRIVATE_UNLIMITED_COMPANY = "Private unlimited company"
    PRIVATE_UNLIMITED_COMPANY_WITHOUT_SHARE_CAPITAL = "Private unlimited company without share capital"
    PROTECTED_CELL_COMPANY = "Protected cell company"
    PUBLIC_LIMITED_COMPANY = "Public limited company"
    REGISTERED_SOCIETY = "Registered society"
    ROYAL_CHARTER_COMPANY = "Royal charter company"
    SCOTTISH_CHARITABLE_INCORPORATED_ORGANISATION = "Scottish charitable incorporated organisation"
    SCOTTISH_QUALIFYING_PARTNERSHIP = "Scottish qualifying partnership"
    UK_ESTABLISHMENT_COMPANY = "UK establishment company"
    UNREGISTERED_COMPANY = "Unregistered company"


class CompanySubType(Enum):
    """Sub Types Of Companies."""
    COMMUNITY_INTEREST_COMPANY = "Community Interest Company (CIC)"
    PRIVATE_FUND_LIMITED_PARTNERSHIP = "Private Fund Limited Partnership (PFLP)"


class CompanyStatus(Enum):
    """Current status of Company."""

    ACTIVE = "active"
    DISSOLVED = "dissolved"
    OPEN = "open"
    CLOSED = "closed"
    CONVERTED_CLOSED = "converted-closed"
    RECEIVERSHIP = "receivership"
    LIQUIDATION = "liquidation"
    ADMINISTRATION = "administration"
    INSOLVENCY_PROCEEDINGS = "insolvency-proceedings"
    VOLUNTARY_ARRAGEMENT = "voluntary-arrangement"


@dataclass
class Company:
    """Company Information."""

    # Primary Name of the company.
    primary_name: str

    # Local registration number
    local_registration_number: str

    # registered offce address
    registered_office_address: str

    # Flag indicating if the company is still active
    status: CompanyStatus

    company_type: CompanyType

    company_sub_type: CompanySubType

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
    status: Optional[CompanyStatus] = CompanyStatus.ACTIVE,
) -> List[Company]:
    """Search for companies in Companies House."""
    # For example using: https://find-and-update.company-information.service.gov.uk/advanced-search or smarter way if available

    companies = []

    url = "https://find-and-update.company-information.service.gov.uk/advanced-search/get-results?companyNameIncludes="

    if name:
        url += name.replace(" ", "+")

    url += "&status=" + status.value

    page = requests.get(url)
    soup = BeautifulSoup(
        page.content, features="html.parser"
    )  # BeautifulSoup which has search results

    url = "https://resources.companieshouse.gov.uk/sic/"
    page = requests.get(url)
    soup1 = BeautifulSoup(
        page.content, features="html.parser"
    )  # BeautifulSoup which has SIC codes

    sic_code_list = []
    sic_desc_list = []
    for tr_data in soup1.findAll("tr"):
        td_data = tr_data.findAll("td")
        if td_data:
            sic_code_list.append(td_data[0].text)
            sic_desc_list.append(td_data[1].text)

    for tr_data in soup.findAll("tr", attrs={"class": "govuk-table__row"}):

        a_data = tr_data.find("a", attrs={"class": "govuk-link"})
        ul_data = tr_data.find("ul", attrs={"class": "govuk-list"})
        
        """ Company Information
        <ul class="govuk-list govuk-!-font-size-16">
            <li>Private limited by guarantee without share capital</li>     company_type
            <li>Community Interest Company (CIC)</li>                       company_sub_type
            <li>07850377 - Incorporated on 16 November 2011</li>            local_registration_number, incorporation_date
            <li>Dissolved on 11 September 2018<br></li>                     dissolved_date
            <li>12 New Street, Huddersfield, England HD1 2AR</li>           registered_office_address
            <li>SIC codes - 78109, 88100</li>                               industry_codes
        </ul>
        """

        local_registration_number = ul_data.select("li:nth-child(3)")[0].text.split(" - ")[0]

        if (
            registration_number is not None
            and registration_number in local_registration_number
            or registration_number is None
        ):
            primary_name = a_data.text.split("(")[0]

            company_type_name = CompanyType(ul_data.select("li:nth-child(1)")[0].text).name
            company_type = CompanyType[company_type_name]

            if ul_data.select("li:nth-child(2)")[0].text:
                company_sub_type_name = CompanySubType(ul_data.select("li:nth-child(2)")[0].text).name
                company_sub_type = CompanySubType[company_sub_type_name]
            else:
                company_sub_type = None

            if " on " in ul_data.select("li:nth-child(3)")[0].text:
                incorporation_date = datetime.strptime(
                    ul_data.select("li:nth-child(3)")[0].text.split(" on ")[1], "%d %B %Y"
                ).date()
            else:
                incorporation_date = None

            if " on " in ul_data.select("li:nth-child(4)")[0].text:
                dissolved_date = datetime.strptime(
                    ul_data.select("li:nth-child(4)")[0].text.split(" on ")[1], "%d %B %Y"
                ).date()
            else:
                dissolved_date = None

            registered_office_address = ul_data.select("li:nth-child(5)")[0].text
            
            if ul_data.select("li:nth-child(6)")[0].text:
                industry_codes = []
                sic_codes = ul_data.select("li:nth-child(6)")[0].text.split(" - ")[1].split(", ")
                for sic_code in sic_codes:
                    desc = ""
                    if sic_code in sic_code_list:
                        id = sic_code_list.index(sic_code)
                        desc = sic_desc_list[id]

                    industry_code = IndustryCode(sic_code, desc)
                    industry_codes.append(industry_code)

                industry_codes = industry_codes
            else:
                industry_codes = None
            
            companies.append(Company(
                primary_name, local_registration_number, registered_office_address, status, company_type, company_sub_type, incorporation_date, dissolved_date, None, None, None, None, industry_codes, None
            ))

    return companies


if __name__ == "__main__":

    search_companies(
        name="Atradius"
    )


