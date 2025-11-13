# Updated Department Structure - Important Changes

## Overview
Based on user feedback, the department structure has been reorganized for better modularity and clearer separation of concerns.

## Key Changes

### 1. NEW: Designers Department
- **Extracted from**: Original Builders Department
- **Responsibility**: Create detailed technical blueprints
- **Roles**: System Architect, UI/UX Designer, Database Designer, API Designer, Technical Writer
- **Output**: Complete specifications that Builders implement without design decisions

### 2. REFACTORED: Builders Department
- **Original design** (builder-department.md): Included design work (Tech Lead making architecture decisions)
- **New approach**: Builders now ONLY implement based on Designers' blueprints
- **Simplified roles**: Frontend Engineer, Backend Engineer, DevOps Engineer
- **Key change**: NO architecture decisions during build phase

**Note**: The original `builder-department.md` file represents the OLD approach. The new pipeline is:
```
Evaluation Committee → Designers (NEW) → Builders (simplified) → Testers (NEW) → Salesmen (NEW) → Lawyers (NEW)
```

### 3. NEW: Testers Department
- **Extracted from**: Original Builders Department (QA was embedded)
- **Responsibility**: Independent quality assurance
- **Roles**: QA Engineer, Security Auditor, Performance Tester, Accessibility Specialist
- **Quality Gates**: Must pass ALL before launch

### 4. NEW: Salesmen Department
- **Responsibility**: Go-to-market, launch, user acquisition
- **Roles**: Marketing Strategist, Growth Hacker, Content Creator, Launch Specialist, Customer Success

### 5. NEW: Lawyers & Compliance Department
- **Activation**: When product hits 1,000+ users or $10k+ revenue
- **Responsibility**: Legal compliance (GDPR, CCPA, ToS)
- **Roles**: Privacy Lawyer, Terms Specialist, IP Lawyer, Compliance Auditor

### 6. NEW: Department of Good Taste
- **Special**: Reviews ANY department at ANY stage
- **Advisory only**: Provides feedback, doesn't block progress
- **Reputation-based influence**: Good reviewers' feedback carries more weight over time
- **Roles**: Design Critic, Code Aesthete, Copy Editor, Ethics Reviewer

### 7. UPDATED: Stockbrokers Department
- **Activation**: When products generate $5k+ revenue (not just bootstrap capital)
- **New investments**: Can reinvest in scaling successful products (not just public markets)
- **Modular**: Fires up only when money starts flowing

## Complete Pipeline (Updated)

```
1. Idea Factory (Huginn & Muninn)
   ↓
2. Idea Evaluation Committee (11 experts)
   ↓
3. Designers Department (NEW)
   ↓
4. Builders Department (REFACTORED - simpler)
   ↓
5. Testers Department (NEW)
   ↓
6. Salesmen Department (NEW)
   ↓
7. Lawyers & Compliance (NEW - activates at scale)
   ↓
8. Stockbrokers Department (UPDATED - modular activation)

   Department of Good Taste (NEW - reviews any stage)
```

## Configuration Changes

```yaml
# OLD (original design)
departments:
  builders:
    roles: ["tech_lead", "frontend", "backend", "devops", "qa"]  # Monolithic

# NEW (modular design)
departments:
  designers:
    enabled: false  # Activate when ready to build
    roles: ["system_architect", "ui_ux_designer", "database_designer", "api_designer"]
  
  builders:
    enabled: false
    roles: ["frontend_engineer", "backend_engineer", "devops_engineer"]  # Simplified
  
  testers:
    enabled: false
    roles: ["qa_engineer", "security_auditor", "performance_tester"]
  
  salesmen:
    enabled: false
    roles: ["marketing_strategist", "growth_hacker", "launch_specialist"]
  
  lawyers_compliance:
    enabled: false
    activation_trigger: {min_users: 1000, min_revenue: 10000}
  
  department_of_good_taste:
    enabled: true  # Always active, advisory only
  
  stockbrokers:
    enabled: false
    activation_trigger: {min_revenue: 5000}
```

## Benefits of New Structure

1. **Clearer separation of concerns**: Design vs. Build vs. Test vs. Launch
2. **Modular activation**: Fire up departments only when needed
3. **Better quality gates**: Independent testing prevents bad launches
4. **Scalable compliance**: Lawyers activate only when legally required
5. **Advisory quality review**: Department of Good Taste improves everything without blocking

## Migration Notes

- **Existing builder-department.md**: Represents old monolithic approach
- **New approach**: Use updated-department-pipeline.md and individual department docs
- **For implementation**: Start with new modular structure, not old monolithic design

---

**Summary**: User feedback led to breaking apart the monolithic Builders department into specialized, modular departments that activate as needed. This creates a clearer pipeline with better quality gates.
