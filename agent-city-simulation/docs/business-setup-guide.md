# Agent City Business Setup Guide

## 💰 Money Handling & Banking

### **Do You Need a Business Bank Account?**

**YES, for several critical reasons:**

1. **Tax Nightmare Prevention**
   - Mixing personal/business = IRS audit red flag
   - Impossible to track expenses/revenue
   - Can't deduct business expenses properly
   - Tax accountant will hate you (and charge more)

2. **Legal Protection** (if LLC)
   - Mixing funds = "piercing the corporate veil"
   - Lose liability protection
   - Personal assets at risk

3. **Professional Credibility**
   - Accepting payments to "John Doe" vs "Agent City Labs LLC"
   - Stripe/payment processors prefer business accounts
   - Easier to work with contractors/vendors

4. **Financial Clarity**
   - Know exactly how much the business makes
   - Track which products are profitable
   - Make better investment decisions
   - Easier to get funding later

---

### **Business Structure Options**

```yaml
sole_proprietorship:
  setup: "Automatic (just start selling)"
  cost: "$0"
  taxes: "Personal income tax"
  liability: "UNLIMITED (personal assets at risk)"
  banking: "Can use personal account, but SHOULDN'T"
  recommended: "NO (too risky)"

llc_single_member:
  setup: "File with state (~1 hour)"
  cost: "$50-$500 (varies by state)"
  taxes: "Pass-through to personal (default)"
  liability: "LIMITED (personal assets protected)"
  banking: "REQUIRES business account"
  recommended: "YES (best for solo founders)"

llc_with_s_corp_election:
  setup: "LLC + IRS Form 2553"
  cost: "Same as LLC + accountant fees"
  taxes: "Can save on self-employment tax"
  liability: "LIMITED"
  banking: "REQUIRES business account"
  recommended: "LATER (when revenue > $60k/year)"
```

**Recommendation**: Start with **Single-Member LLC**
- Costs $50-$500 depending on state
- Takes 1-2 weeks to process
- Protects personal assets
- Professional appearance
- Easy to manage

---

### **Best Business Banks for You (2025)**

Since you're starting solo (likely sole prop or single-member LLC):

#### **Option 1: Relay** ⭐ **BEST FOR YOU**
```yaml
pros:
  - "Accepts sole proprietors AND LLCs"
  - "FREE (no monthly fees, no minimums)"
  - "Up to 20 checking accounts (separate products/departments!)"
  - "Integrates with QuickBooks, Xero"
  - "Physical + virtual debit cards"
  - "Good customer support"

cons:
  - "Less tech-focused than Mercury"
  - "No high-yield savings for small balances"

cost: "$0/month"
recommendation: "START HERE - easiest, free, accepts your structure"
```

#### **Option 2: Novo** (Alternative)
```yaml
pros:
  - "Accepts sole proprietors"
  - "FREE worldwide ATM access"
  - "No monthly fees, no minimums"
  - "Integrates with tons of software (Stripe, QuickBooks, etc.)"
  - "Good for online businesses"

cons:
  - "Limited features vs. Relay"
  - "Only 1 checking account (vs Relay's 20)"

cost: "$0/month"
recommendation: "Good alternative if Relay doesn't work"
```

#### **Option 3: Mercury** (If you form LLC)
```yaml
pros:
  - "Built for startups/tech companies"
  - "Excellent API access (good for automation!)"
  - "Free domestic + international wires"
  - "Beautiful interface"
  - "Developer-friendly"

cons:
  - "Does NOT accept sole proprietors (LLC required)"
  - "No interest unless you have $500k+"
  - "Sometimes picky about who they accept"

cost: "$0/month"
recommendation: "Form LLC first, then apply"
```

#### **Option 4: Found** (For Freelancers/Solopreneurs)
```yaml
pros:
  - "Accepts sole proprietors"
  - "Built-in tax withholding (automatically saves for taxes!)"
  - "Invoicing, expense tracking"
  - "Bookkeeping built-in"

cons:
  - "$25/month (not free)"
  - "More freelancer-focused than startup-focused"

cost: "$25/month"
recommendation: "Good if you want automatic tax savings"
```

#### **Traditional Banks** (Not Recommended)
```yaml
chase_business:
  pros: ["Physical branches", "Established name"]
  cons: ["$15/month fees", "Minimum balances", "Terrible online banking"]
  recommendation: "AVOID (you're 100% online)"

bank_of_america:
  pros: ["Nationwide", "Business credit cards"]
  cons: ["$16/month fees", "Poor customer service", "Slow"]
  recommendation: "AVOID"
```

---

### **My Recommendation**

**PHASE 1: Right Now (This Week)**
```yaml
action: "Open Relay account as sole proprietor"
why: "Free, fast, accepts your current structure"
timeline: "15 minutes online application"
cost: "$0"
```

**PHASE 2: After Weekend (When You Have Time)**
```yaml
action: "Form single-member LLC in your state"
resources:
  - "Northwest Registered Agent: $39 + state fees"
  - "LegalZoom: $79 + state fees (overkill)"
  - "DIY: File directly with state (cheapest)"
timeline: "1-2 weeks to process"
cost: "$50-$500 depending on state"
```

**PHASE 3: Once LLC is Approved**
```yaml
action: "Upgrade to Mercury or keep Relay"
why: "Mercury has better API access for automation"
decision: "Relay is fine to keep, Mercury is nice-to-have"
```

---

### **Payment Processing**

**How Customers Will Pay You**:

```yaml
gumroad:
  use_for: "Digital products (icon packs, templates)"
  fees: "10% + payment processing (2.9% + $0.30)"
  total_fee: "~13% of sale"
  pros: "Easiest, handles everything, instant setup"
  cons: "Higher fees than Stripe"
  payout: "Automatically to your bank account"

stripe:
  use_for: "SaaS subscriptions, custom storefront"
  fees: "2.9% + $0.30 per transaction"
  pros: "Lower fees, most flexibility, great API"
  cons: "Need to build checkout yourself"
  payout: "2-7 days to bank account"

paypal_business:
  use_for: "Backup option (some customers prefer it)"
  fees: "3.49% + $0.49 per transaction"
  pros: "Some people only use PayPal"
  cons: "Higher fees, freezes accounts randomly"
  recommendation: "Offer as backup only"

crypto:
  use_for: "Optional (some customers want it)"
  fees: "~1-2% (Coinbase Commerce)"
  pros: "No chargebacks, global"
  cons: "Volatile, small market"
  recommendation: "Add later if requested"
```

**Best Strategy**:
1. **Gumroad** for digital products (easiest, worth the 13%)
2. **Stripe** for SaaS products (lower fees, more control)
3. **PayPal** as backup option
4. All feed into your **Relay/Mercury** business account

---

### **Accounting & Taxes**

**Minimum Required**:
```yaml
bookkeeping:
  tool: "Wave (FREE) or QuickBooks ($30/month)"
  task: "Track income and expenses monthly"
  time: "15 minutes/week"

quarterly_taxes:
  what: "Estimated tax payments (if making > $1k/quarter)"
  when: "April 15, June 15, Sept 15, Jan 15"
  amount: "~25-30% of profit (federal + state)"
  tool: "IRS Form 1040-ES"

annual_taxes:
  sole_prop: "Schedule C (business income) on personal 1040"
  llc: "Same as sole prop (pass-through)"
  deadline: "April 15"
  recommendation: "Hire accountant ($300-800) for first year"

write_offs:
  allowable:
    - "Computer equipment"
    - "Software subscriptions (GCP, Anthropic API, etc.)"
    - "Internet (portion used for business)"
    - "Home office (if dedicated space)"
    - "Domain names, hosting"
    - "Education (courses, books)"
    - "Business bank fees"
    - "Marketing expenses"

  save_receipts: "Screenshot or save ALL receipts"
```

**Pro Tip**: Set aside **30% of every dollar** you make for taxes immediately. Put it in separate account (Relay lets you have 20 accounts - perfect for this!).

---

### **Money Flow Diagram**

```
Customer Purchase ($100 icon pack)
  ↓
Gumroad ($13 fee) → You receive $87
  ↓
Relay Business Checking Account
  ↓
Split automatically:
  - Operating Account: $61 (70%)
  - Tax Savings Account: $26 (30%)
  - Reinvestment Account: $0 (use operating for now)
  ↓
Monthly:
  - Pay yourself: $X (whatever you need to live)
  - Reinvest in business: Rest
  - Pay quarterly taxes: From tax savings account
```

**Why Multiple Accounts Matter** (Relay's 20 accounts feature):
```yaml
checking_accounts:
  operating: "Daily business expenses"
  tax_savings: "30% of revenue (don't touch!)"
  product_a: "Recipe optimizer revenue"
  product_b: "Icon pack revenue"
  product_c: "Template revenue"
  stockbrokers: "Trading capital (later)"
  payroll: "Paying yourself"
  emergency: "3-month runway"

benefit: "Know exactly where money is, can't accidentally spend tax money"
```

---

## **Action Items**

**This Week**:
- [ ] Open Relay business account (15 min)
- [ ] Connect to Stripe (for SaaS) and Gumroad (for digital products)
- [ ] Set up automatic 30% transfer to "Tax Savings" account

**Next Week**:
- [ ] Research LLC formation in your state
- [ ] Decide on business name
- [ ] File LLC paperwork (or hire Northwest Registered Agent for $39)

**Month 1**:
- [ ] Get EIN from IRS (free, 5 minutes online)
- [ ] Open Wave or QuickBooks for bookkeeping
- [ ] Set up monthly bookkeeping routine (15 min/week)

**Ongoing**:
- [ ] Track every expense (save receipts!)
- [ ] Pay quarterly estimated taxes (if making > $1k/quarter)
- [ ] Review financials monthly

---

## **Costs Summary**

**Immediate (This Month)**:
```yaml
domain_name: "$12/year" # yourcompany.com
relay_account: "$0" # Free
stripe_account: "$0" # Free (pay per transaction)
gumroad_account: "$0" # Free (pay per transaction)

total_month_1: "$12"
```

**Optional (Next Month)**:
```yaml
llc_formation: "$50-$500" # Depends on state
registered_agent: "$39-$125/year" # If needed
bookkeeping_software: "$0-$30/month" # Wave free, QuickBooks $30

total_optional: "$50-$655"
```

**Annual Costs**:
```yaml
llc_annual_fees: "$0-$800" # Varies by state
accountant_tax_prep: "$300-$800" # First year
bookkeeping: "$0-$360/year" # If using QuickBooks

total_annual: "$300-$1,960"
```

**Bottom Line**: You can start for **$12** (domain name). Everything else is optional or later.

---

**Next**: You asked about others trying this approach - let me document what I found about that.
