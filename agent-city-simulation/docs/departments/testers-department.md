# Testers Department - The Quality Gatekeepers
*"Where working code becomes certified, launch-ready products."*

## Core Concept
Receives working code from Builders → Performs comprehensive QA → Certifies product ready for launch

## Team Composition (4 Roles)

**1. QA Engineer / Test Lead** (Required, 1 per project)
- Functional testing, integration testing, test automation
- Example: Sofia Rodriguez (risk_tolerance: 0.18, analytical: 0.89, assertiveness: 0.77)
- Low risk_tolerance → Blocks releases for ANY critical/high bugs (strict standards)

**2. Security Auditor** (0.5-1 per project)
- OWASP Top 10, penetration testing, vulnerability scanning
- Example: Aisha Okonkwo (risk_tolerance: 0.12, analytical: 0.95, assertiveness: 0.86)
- Extremely low risk_tolerance → Paranoid security testing (catches XSS, auth bypass)

**3. Performance Tester** (0.5-1 per project)
- Load testing, database optimization, API response times
- Example: Kenji Yamamoto (analytical: 0.94, patience: 0.91)
- Target: p95 API response < 200ms

**4. Accessibility Specialist** (0.25 per project, optional)
- WCAG 2.1 compliance, screen reader testing
- Example: Rachel Kim (empathy: 0.91, patience: 0.84)
- Ensures product accessible to all users

## Quality Gates (Must Pass ALL)
✅ 100% of critical features working  
✅ Zero critical/high security vulnerabilities  
✅ Performance targets met (p95 < 200ms)  
✅ WCAG 2.1 AA compliant  

## Testing Workflow (3 days typical)

**Day 1-2: Functional & Security Testing**
- QA tests all features, finds bugs
- Security auditor scans for vulnerabilities
- Bugs sent back to Builders if critical

**Day 2-3: Performance & Accessibility**
- Load testing, database optimization
- Accessibility audit with screen readers
- Final fixes applied

**Day 3: Certification**
- All tests pass → Issue certification report
- Hand off to Salesmen Department

## Personality Impact Examples

**Sofia (risk_tolerance: 0.18)** finds session persistence bug:
- Higher tolerance QA might call it "minor" → ship with known issue
- Sofia blocks release → Builders fix → Zero production bugs ✅

**Aisha (risk_tolerance: 0.12)** finds XSS vulnerability:
- Builder: "It's only medium severity, ship and fix later?"
- Aisha (assertiveness: 0.86): "NO. Fix before launch."
- Result: Users protected from session hijacking

## Recursive Learning

**Pattern Learned**: "QA with risk_tolerance < 0.30 find 42% more bugs, resulting in 75% fewer production bugs"

**Feedback Loop**:
- Bugs found → Update Builder checklists
- Common issues (XSS in 60% of projects) → Add to prevention checklist
- Tester reputation tracked by production bugs vs testing bugs

## Success Metrics
- Production bugs Week 1: <3 (target)
- Bug detection rate: 95%+ (bugs found in testing / total bugs)
- Security posture: 100% of launches with 0 critical vulns

**Key Insight**: Low-risk-tolerance testers add time but dramatically reduce production issues.
