## Business Context

A mid-size retail bank wants to digitise its loan approval process.

Currently, loan approvals are processed manually by risk officers which causes:

* Slow decision times
* High operational costs
* Poor customer experience

The bank wants to introduce an automated **Loan Decisioning Platform** that:

* Accepts loan applications via API
* Performs automated risk scoring
* Approves or rejects loans instantly
* Stores decisions in an auditable record

The system must integrate with existing banking systems and meet strict regulatory and security requirements.

## Functional Requirements

### FR1 – Submit Loan Application
Customers or front-end systems must be able to submit loan applications via an API.

### FR2 – Validate Application Data
The system must validate submitted application data before processing.

### FR3 – Risk Scoring
Applications must be evaluated using a risk scoring algorithm.

### FR4 – Rules Engine
Business rules should determine whether the loan is approved, rejected, or flagged for manual review.

### FR5 – Store Decision
The system must store loan decisions and application details.

### FR6 – Retrieve Decision
Customers/Employees must be able to retrieve loan decisions via API.

### FR7 – Audit Logging
All actions and decisions must be recorded for compliance and auditing.

## Non-Functional Requirements

### Availability
The system must maintain 99.9% uptime.

### Performance
Loan decisions should be returned within 2 seconds.

### Security
All sensitive data must be encrypted in transit and at rest.

### Scalability
The system must support up to 1000 loan applications per minute.

### Auditability
All loan decisions must be traceable with full historical records.

### Compliance
The system must comply with financial regulations and data protection laws (e.g. GDPR).

### Observability
The platform must provide monitoring, logging, and alerting.

<!-- ## Non-Fuctional Requirements 

### FR1 - Customer Frontend

### FR2 - Loan Application API

### FR3 - Flask/FastAPI BackEnd

### FR4 - Database Layer for customer information

### FR5 - IAC

### FR6 - AWS/Azure Cost Analysis

### FR7 - Risk Scoring Algorithm -->
