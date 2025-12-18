---
name: web-accessibility-contrast-fix
description: Diagnoses and fixes PageSpeed Insights accessibility "!" errors caused by color-contrast audit failures. Use when PageSpeed Insights shows "!" instead of Accessibility score, color-contrast audit reports errors, need to fix getImageData canvas errors, or improving WCAG 2.1 compliance.
---

# Web Accessibility - Contrast Audit Fix

Diagnoses and fixes PageSpeed Insights accessibility errors caused by color-contrast audit failures.

## When to Use This Skill

This skill should be triggered when:
- PageSpeed Insights shows "!" instead of Accessibility score
- color-contrast audit reports errors or incomplete
- Need to fix getImageData canvas errors
- Improving WCAG 2.1 compliance
- User mentions: "accessibility score", "color contrast", "PageSpeed Insights error", "WCAG"

## Problem Overview

**Symptom**: PageSpeed Insights (PSI) Accessibility shows **"!"** instead of a numeric score.

**Root Cause**: Not a low score, but a **measurement failure**!
- `color-contrast` audit errors during execution
- Canvas `getImageData()` call fails
- Cannot calculate color contrast → No score available

## Quick Diagnostic Commands

```bash
# 1. Check color spaces (OKLCH/OKLAB)
grep -r "oklch\|oklab" app/ components/ styles/

# 2. Check low opacity (< 0.4)
grep -r "/10\|/20\|/30\|opacity-25\|opacity-0" components/ app/

# 3. Check CSS Filters (Critical!)
grep -r "backdrop-blur\|filter:\|mix-blend-mode" components/ app/

# 4. Check gradient text
grep -r "background-clip.*text\|color.*transparent" components/ app/
```

## Fix Workflow

### Phase 1: Remove CSS Filters (Priority: Critical)

CSS filters are the main cause of `getImageData` errors.

```tsx
// ❌ BEFORE: Triggers getImageData error
<div className="bg-card/50 backdrop-blur-sm">
  <h2>Content</h2>
</div>

// ✅ AFTER: Use solid background instead
<div className="bg-card/80">
  <h2>Content</h2>
</div>
```

**Remove These Properties**:
- `backdrop-blur-*` → Remove completely
- `filter: brightness()` → Remove or use opacity instead
- `filter: contrast()` → Remove
- `mix-blend-mode` → Remove

### Phase 2: Convert Color Space (Priority: High)

OKLCH/OKLAB color spaces cause contrast calculation errors.

```css
/* ❌ BEFORE: OKLCH color space */
:root {
  --background: oklch(0.99 0 0);
  --foreground: oklch(0.15 0.01 270);
}

/* ✅ AFTER: Stable HSL color space */
:root {
  --background: hsl(0, 0%, 99%);
  --foreground: hsl(270, 5%, 15%);
}
```

### Phase 3: Increase Opacity Thresholds (Priority: Medium)

Opacity < 0.4 causes unstable canvas sampling.

```tsx
// ❌ BEFORE: Too low opacity
className="bg-muted/20"           // 20%

// ✅ AFTER: Safe opacity threshold
className="bg-muted/40"           // 40% (min safe)
className="bg-muted/60"           // 60% (recommended)
```

### Phase 4: Handle Gradient Text (Priority: Low)

```css
/* ✅ SOLUTION: Solid color fallback */
.title {
  color: #0a0a0a;  /* Default: solid color (accessible) */
}

@media (prefers-contrast: no-preference) {
  .title.with-gradient {
    background: linear-gradient(90deg, #0ea5e9, #6366f1);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }
}
```

### Phase 5: Add Overlay for Image Backgrounds (Priority: Medium)

```tsx
// ✅ Add opaque overlay (≥ 0.6)
<div className="relative">
  <img src="/hero.jpg" alt="Hero" />
  <div className="absolute inset-0 bg-black/60"></div>
  <h1 className="relative top-1/2 left-1/2 text-white">
    Title
  </h1>
</div>
```

## Verification Checklist

```markdown
## Color Space
- [ ] All colors use `hsl()` or `rgb()` (no `oklch` or `oklab`)

## Opacity
- [ ] All background opacity ≥ 0.4 (prefer ≥ 0.6)
- [ ] No Tailwind classes: `/10`, `/20`, `/30` in backgrounds

## CSS Filters
- [ ] No `backdrop-blur-*` classes
- [ ] No `filter: brightness()` or `filter: contrast()`
- [ ] No `mix-blend-mode`

## Image Backgrounds
- [ ] Text over images has opaque overlay (≥ 0.6 opacity)
- [ ] Contrast ratio ≥ 4.5:1 (small text) or ≥ 3:1 (large text)
```

## Quick 5-Minute Emergency Fix

```bash
# Step 1: Remove backdrop-blur (CRITICAL!)
grep -r "backdrop-blur" components/ app/
# Replace: backdrop-blur-sm → (delete)

# Step 2: Increase low opacity
grep -r "/10\|/20\|/30" components/
# Replace: /10 → /40, /20 → /40, /30 → /60

# Step 3: Build & verify
npm run build

# Step 4: Deploy
git add .
git commit -m "Fix accessibility contrast audit errors"
git push
```

## Expected Outcomes

### Before Fix
- ❌ Accessibility score: **"!" (error)**
- ❌ color-contrast audit: **Error/Incomplete**

### After Fix
- ✅ Accessibility score: **85-100** (numeric score)
- ✅ color-contrast audit: **Pass**
- ✅ Improved SEO rankings
- ✅ Better user experience
- ✅ Legal compliance (ADA, WCAG 2.1)

## Tools & Resources

- [PageSpeed Insights](https://pagespeed.web.dev/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [axe DevTools](https://www.deque.com/axe/devtools/)

## WCAG 2.1 Contrast Standards

| Text Size | Min Contrast | Example |
|-----------|--------------|---------|
| Small (< 18pt) | 4.5:1 | Body text, buttons |
| Large (≥ 18pt) | 3.0:1 | Headings, hero text |
| Large bold (≥ 14pt) | 3.0:1 | Bold headings |

For detailed information, see the [README.md](README.md) file in this skill directory.
