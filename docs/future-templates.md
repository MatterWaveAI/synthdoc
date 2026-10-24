# Additional Document Templates - Future Development

This document lists document template categories and specific templates that are NOT currently implemented in the `synthetic-document-dataset` project. Each entry includes a description of the document type and key fields that would be useful for a document understanding dataset.

---

## 1. Government & Tax Forms (IRS/SSA)

### Federal Tax Forms (Beyond Existing W-2, W-4, W-9)

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `form_1040_template` | US Individual Income Tax Return | Name, SSN, filing status, income, deductions, credits, tax liability |
| `form_1040_schedule_c` | Profit or Loss From Business | Business income, expenses, net profit |
| `form_1040_schedule_e` | Supplemental Income and Loss | Rental income, royalties, partnerships |
| `form_1065_template` | US Return of Partnership Income | Partner names, partnership income, deductions |
| `form_1120_template` | US Corporate Income Tax Return | Corporation name, EIN, gross receipts, deductions |
| `form_1120s_template` | S Corporation Income Tax Return | S-corp elections, shareholder info |
| `form_941_template` | Quarterly Federal Tax Return | Employer ID, employee wages, tax deposits |
| `form_940_template` | Annual FUTA Tax Return | Employer FUTA tax, state contributions |
| `form_1099_nec_template` | Nonemployee Compensation | Payer info, recipient info, nonemployee compensation |
| `form_1099_div_template` | Dividends and Distributions | Payer, recipient, total dividends, qualified dividends |
| `form_1099_int_template` | Interest Income | Financial institution, recipient, interest earned |
| `form_1098_template` | Mortgage Interest Statement | Lender, borrower, mortgage interest paid |
| `form_1098_e_template` | Student Loan Interest Statement | Lender, borrower, interest paid |
| `form_w2c_template` | Corrected Wage Statement | Original W-2 info, corrections |
| `form_8863_template` | Education Credits | Student info, qualified expenses, credit calculation |

### Social Security Forms

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `ssa_7001_template` | Request for Social Security Statement | Personal info, requestor signature |
| `ssa_1099_template` | Social Security Benefit Statement | Beneficiary info, benefits received, taxes withheld |

---

## 2. Immigration & Citizenship Documents

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `i9_form_template` | Employment Eligibility Verification (EXISTS) | Employee info, document references |
| `i485_template` | Application to Register Permanent Residence | Applicant info, eligibility category |
| `i864_template` | Affidavit of Support | Sponsor info, household size, income |
| `i589_template` | Application for Asylum | Applicant info, fear of persecution |
| `i130_template` | Petition for Alien Relative | Petitioner info, beneficiary relationship |
| `i765_template` | Application for Employment Authorization | Applicant info, category |
| `i131_template` | Application for Travel Document | Applicant info, travel reason |
| `ds11_template` | Passport Application | Applicant info, citizenship evidence |
| `n400_template` | Application for Naturalization | Applicant info, residency duration |
| `i751_template` | Petition to Remove Conditions | Conditional resident info, marriage evidence |

---

## 3. Legal Documents

### Contracts & Agreements

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `purchase_agreement_template` | Real Estate Purchase Agreement | Buyer, seller, property address, purchase price |
| `lease_agreement_template` | Residential Lease (EXISTS) | Landlord, tenant, property, rent terms |
| `service_contract_template` | General Service Agreement | Service provider, client, scope of work |
| `consulting_agreement_template` | Consulting Services Contract | Consultant, client, deliverables, compensation |
| `vendor_agreement_template` | Vendor Contract | Vendor, buyer, products/services, terms |
| `distribution_agreement_template` | Distribution Rights Agreement | Manufacturer, distributor, territory |
| `franchise_agreement_template` | Franchise Contract (EXISTS) | Franchisor, franchisee, terms |
| `joint_venture_template` | Joint Venture Agreement | Parties, venture purpose, contributions |
| `stock_purchase_template` | Stock Purchase Agreement | Buyer, seller, shares, price |
| `merger_agreement_template` | Merger Agreement | Merging companies, terms |

### Court & Legal Filings

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `complaint_template` | Civil Complaint | Plaintiff, defendant, claims |
| `motion_template` | Legal Motion | Moving party, case info, motion type |
| `summons_template` | Court Summons | Defendant, court, hearing date |
| `subpoena_template` | Subpoena (EXISTS) | Witness, case, required presence |
| `judgment_template` | Court Judgment | Case number, parties, ruling |
| `divorce_decree_template` | Divorce Decree (EXISTS) | Parties, custody, asset division |
| `child_support_order_template` | Child Support Order | Non-custodial parent, amount, terms |
| `restraining_order_template` | Restraining Order (EXISTS) | Protected party, restrained party |

### Corporate Formation

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `articles_of_incorporation_template` | Articles of Incorporation | Company name, registered agent, shares |
| `bylaws_template` | Corporate Bylaws | Company name, governance rules |
| `operating_agreement_template` | LLC Operating Agreement | Members, ownership, management |
| `partnership_agreement_template` | General Partnership | Partners, contributions, profit sharing |
| `shareholder_agreement_template` | Shareholder Agreement | Shareholders, rights, restrictions |
| `board_resolution_template` | Board Resolution | Company, date, resolution details |
| `minutes_of_meeting_template` | Meeting Minutes (EXISTS) | Date, attendees, agenda, votes |

---

## 4. Healthcare & Medical Documents

### Medical Forms

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `patient_intake_form_template` | Patient Registration | Patient info, insurance, medical history |
| `medical_history_form_template` | Medical History Questionnaire | Patient info, conditions, medications |
| `hipaa_form_template` | HIPAA Authorization (EXISTS) | Patient, authorized party, permissions |
| `patient_consent_form_template` | Treatment Consent | Patient, procedure, risks acknowledged |
| `surgical_consent_template` | Surgical Consent (EXISTS) | Patient, procedure details |
| `lab_order_form_template` | Lab Test Order | Patient, tests ordered, diagnosis |
| `referral_form_template` | Physician Referral | Referring doctor, patient, specialist |
| `discharge_instructions_template` | Discharge Instructions | Patient, discharge summary, follow-up |
| `advance_directive_template` | Advance Directive (EXISTS) | Patient, healthcare wishes |

### Insurance & Claims

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `prior_auth_request_template` | Prior Authorization Request | Patient, provider, procedure, insurance |
| `claim_submission_template` | Insurance Claim Form | Patient, provider, services, diagnosis codes |
| `appeal_letter_template` | Insurance Appeal | Patient, denial reason, appeal argument |
| `eoB_template` | Explanation of Benefits (EXISTS) | Claim details, covered amounts, patient responsibility |

---

## 5. Real Estate & Property Documents

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `property_deed_template` | Property Deed | Grantor, grantee, property description |
| `mortgage_template` | Mortgage Agreement | Borrower, lender, property, terms |
| `title_insurance_template` | Title Insurance Policy | Property, insured party, coverage |
| `property_tax_statement_template` | Property Tax Statement (EXISTS) | Owner, assessed value, tax due |
| `home_inspection_template` | Home Inspection Report | Inspector, property, findings |
| `appraisal_report_template` | Property Appraisal | Appraiser, property, value estimate |
| `hoa_covenant_template` | HOA Covenants & Restrictions | Property, association rules |
| `lease_addendum_template` | Lease Addendum | Lease reference, additional terms |
| `eviction_notice_template` | Eviction Notice (EXISTS) | Tenant, reason, vacate date |
| `quitclaim_deed_template` | Quitclaim Deed (EXISTS) | Grantor, grantee, property |

---

## 6. Financial Documents

### Banking

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `bank_reconciliation_template` | Bank Reconciliation | Account, statement period, adjustments |
| `check_template` | Business Check | Payor, payee, amount, memo |
| `money_order_template` | Money Order | Issuer, payee, amount |
| `wire_confirmation_template` | Wire Transfer Confirmation | From, to, amount, reference |

### Investment

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `brokerage_statement_template` | Brokerage Account Statement | Account holder, holdings, values |
| `mutual_fund_statement_template` | Mutual Fund Statement | Fund, shares, NAV, performance |
| `401k_statement_template` | 401(k) Account Statement | Participant, contributions, balance |
| `ira_statement_template` | IRA Statement | Account holder, contributions, value |
| `stock_certificate_template` | Stock Certificate (EXISTS) | Company, shareholder, shares |

### Credit & Lending

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `credit_report_template` | Credit Report (EXISTS) | Consumer, accounts, score, inquiries |
| `loan_modification_template` | Loan Modification Agreement | Lender, borrower, new terms |
| `foreclosure_notice_template` | Foreclosure Notice | Borrower, property, sale date |
| `debt_collection_letter_template` | Collection Letter | Debtor, creditor, amount, deadline |

---

## 7. Employment & HR Documents

### Hiring & Employment

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `job_application_template` | Job Application | Applicant info, employment history |
| `background_check_authorization_template` | Background Check Authorization | Applicant, employer, consent |
| `offer_letter_template` | Job Offer Letter (EXISTS) | Employer, candidate, position, salary |
| `employment_contract_template` | Employment Contract (EXISTS) | Terms of employment |
| `confidentiality_agreement_template` | Confidentiality Agreement | Employee, employer, confidential info |
| `non_compete_agreement_template` | Non-Compete Agreement | Employee, restrictions, duration |
| `independent_contractor_agreement_template` | Independent Contractor Agreement | Contractor, client, scope, payment |
| `employee_handbook_acknowledgment_template` | Handbook Receipt | Employee, acknowledgment date |

### Payroll & Benefits

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `pay_stub_template` | Pay Stub (EXISTS) | Employee, wages, deductions, taxes |
| `direct_deposit_form_template` | Direct Deposit Authorization | Employee, bank account, routing |
| `w4_form_template` | W-4 Withholding (EXISTS) | Employee withholding allowances |
| `i9_form_template` | I-9 Employment Eligibility (EXISTS) | Employee authorization |
| `benefits_enrollment_template` | Benefits Enrollment | Employee, selected plans, dependents |
| ` cobra_notice_template` | COBRA Election Notice | Qualified beneficiary, coverage, deadline |
| `termination_letter_template` | Termination Letter | Employee, reason, final pay |

### Performance & Policies

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `performance_evaluation_template` | Performance Review | Employee, manager, ratings, feedback |
| `written_warning_template` | Written Warning | Employee, violation, corrective action |
| `position_description_template` | Job Description | Position, duties, qualifications |
| `organization_chart_template` | Org Chart | Positions, reporting structure |

---

## 8. Transportation & Logistics

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `bill_of_lading_template` | Bill of Lading (EXISTS) | Shipper, consignee, goods, carrier |
| `packing_list_template` | Packing List (EXISTS) | Shipper, contents, weights, quantities |
| `freight_invoice_template` | Freight Invoice | Shipper, charges, terms |
| `customs_declaration_template` | Customs Declaration | Importer, goods, value, origin |
| `certificate_of_origin_template` | Certificate of Origin | Goods, country of origin |
| `shipping_label_template` | Shipping Label (EXISTS) | Shipper, recipient, tracking |
| `delivery_receipt_template` | Delivery Receipt | Package, recipient signature |
| `cargo_manifest_template` | Cargo Manifest | Vessel, cargo description |
| `transportation_agreement_template` | Carrier Agreement | Carrier, shipper, terms |

---

## 9. Education & Academic Documents

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `transcript_template` | Academic Transcript (EXISTS) | Student, courses, grades, GPA |
| `diploma_template` | Diploma/Certificate | Recipient, degree, date |
| `enrollment_verification_template` | Enrollment Verification | Student, enrollment status, dates |
| `degree_verification_template` | Degree Verification | Graduate, degree, conferral date |
| `student_loan_disclosure_template` | Student Loan Disclosure | Borrower, lender, terms |
| `fafsa_template` | FAFSA Application | Student, financial information |
| `scholarship_application_template` | Scholarship Application | Applicant, qualifications, essay |
| ` IEP_template` | Individualized Education Program (EXISTS) | Student, accommodations, goals |
| `report_card_template` | Report Card (EXISTS) | Student, courses, grades |

---

## 10. Insurance Documents

### Property & Auto

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `auto_insurance_card_template` | Auto Insurance ID Card | Policy holder, policy number, dates |
| `homeowners_policy_template` | Homeowners Insurance Policy | Insured, property, coverage |
| `renters_insurance_template` | Renters Insurance Policy | Tenant, personal property coverage |
| `claims_form_template` | Insurance Claim Form | Claimant, incident, damages |

### Health Insurance

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `health_insurance_card_template` | Insurance ID Card | Member, group, coverage dates |
| `enrollment_form_template` | Insurance Enrollment | Applicant, plan selection, dependents |
| `premium_invoice_template` | Premium Invoice | Member, amount due, due date |

---

## 11. Retail & E-Commerce

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `retail_receipt_template` | Retail Receipt (EXISTS) | Items, prices, tax, total |
| `gift_card_template` | Gift Card | Card number, value, terms |
| `price_tag_template` | Product Price Tag | Product, price, barcode |
| `return_authorization_template` | Return Authorization | Customer, item, return reason |
| `loyalty_card_application_template` | Loyalty Program Application | Customer, rewards level |
| `warranty_card_template` | Product Warranty Card | Product, serial number, registration |

---

## 12. Construction & Engineering

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `construction_contract_template` | Construction Contract | Contractor, owner, scope, price |
| `change_order_template` | Change Order (EXISTS) | Original contract, changes, cost |
| `request_for_proposal_template` | RFP Document | Owner, project description, requirements |
| `bid_proposal_template` | Bid Proposal | Contractor, bid amount, timeline |
| `inspection_report_template` | Building Inspection | Inspector, property, violations |
| `certificate_of_completion_template` | Certificate of Completion | Project, contractor, completion date |
| `mechanic_lien_template` | Mechanic's Lien (EXISTS) | Claimant, property, amount due |
| `payment_application_template` | AIA G702/G703 (EXISTS) | Contractor, completed work, payment request |

---

## 13. Technology & Software

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `software_license_template` | Software License | Licensor, licensee, usage rights |
| `terms_of_service_template` | Terms of Service | Company, user terms, liabilities |
| `privacy_policy_template` | Privacy Policy | Company, data practices |
| `end_user_agreement_template` | End User Agreement | Software, user rights |
| `saas_agreement_template` | SaaS Subscription | Provider, customer, service level |
| `api_documentation_template` | API Documentation | Endpoints, parameters, responses |
| `bug_report_template` | Bug Report | Reporter, environment, description |

---

## 14. Personal Documents

| Template Name | Description | Key Fields |
|--------------|-------------|------------|
| `birth_certificate_template` | Birth Certificate (EXISTS) | Name, date, place, parents |
| `marriage_certificate_template` | Marriage Certificate (EXISTS) | Spouses, date, location |
| `death_certificate_template` | Death Certificate | Decedent, date, cause |
| `divorce_certificate_template` | Divorce Decree | Parties, date, terms |
| `passport_template` | Passport (EXISTS) | Holder, nationality, expiration |
| `drivers_license_template` | Driver's License (EXISTS) | Holder, class, restrictions |
| `social_security_card_template` | Social Security Card (EXISTS) | Name, SSN |
| `travel_visa_template` | Visa | Holder, country, type, dates |
| `power_of_attorney_template` | Power of Attorney (EXISTS) | Principal, agent, powers |
| `will_template` | Last Will and Testament (EXISTS) | Testator, beneficiaries, executor |

---

## Priority Recommendations

Based on common use cases and dataset diversity, the following are recommended for initial implementation:

### High Priority

1. **Form 1040** - Core IRS form, highly relevant for financial document understanding
2. **I-9 Form** - Employment eligibility, common business document
3. **Bank Statement** (already exists - verify variations)
4. **Invoice** (already exists - verify variations)
5. **Rental Lease Agreement** - Common legal document
6. **Medical Insurance Claim** - Healthcare + insurance intersection
7. **Pay Stub** - Employment document
8. **Property Deed** - Real estate legal document
9. **Purchase Order** - Business transaction document
10. **Credit Report** - Financial document with structured data

### Medium Priority

1. **Immigration forms** (I-485, I-130, etc.)
2. **Corporate formation documents**
3. **Construction/contractor documents**
4. **More IRS tax forms** (1099 series, Schedules)
5. **Court documents** (complaints, motions)

### Lower Priority (Nice to Have)

1. **Technical documentation**
2. **E-commerce receipts**
3. **Educational credentials**
4. **Insurance policy documents**
