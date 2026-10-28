---
name: PDF Local Engine
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#5c3f40'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#906f70'
  outline-variant: '#e5bdbe'
  surface-tint: '#be0037'
  primary: '#b80035'
  on-primary: '#ffffff'
  primary-container: '#e11d48'
  on-primary-container: '#fffaf9'
  inverse-primary: '#ffb3b6'
  secondary: '#006c49'
  on-secondary: '#ffffff'
  secondary-container: '#6cf8bb'
  on-secondary-container: '#00714d'
  tertiary: '#535b71'
  on-tertiary: '#ffffff'
  tertiary-container: '#6c738a'
  on-tertiary-container: '#fcfaff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdada'
  primary-fixed-dim: '#ffb3b6'
  on-primary-fixed: '#40000c'
  on-primary-fixed-variant: '#920028'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#dae2fd'
  tertiary-fixed-dim: '#bec6e0'
  on-tertiary-fixed: '#131b2e'
  on-tertiary-fixed-variant: '#3f465c'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.03em
  display-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.025em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.04em
  code-mono:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-mobile: 0.75rem
  margin: 1.5rem
  margin-mobile: 1rem
  space-2xs: 0.25rem
  space-xs: 0.5rem
  space-sm: 0.75rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 3rem
---

## Brand & Style

The design system is engineered around absolute trust, local-first performance, and utilitarian elegance. It targets security-conscious professionals, developers, and privacy-minded users who process sensitive documents without cloud dependencies. The interface merges the precision of a high-end desktop developer tool with the ergonomic tactility of a modern mobile operating system.

Visually, the style pairs **Modern Utilitarianism** with a tactile, layered card structure. It avoids frivolous ornamentation, opting instead for crisp vector borders, functional badge indicators, deep content contrast, and focused micro-interactions that communicate instant, on-device execution. The emotional response should be immediate reassurance: secure, zero-latency, and reliable under zero-network conditions.

## Colors

The palette leverages a crisp, modern visual hierarchy rooted in document utility and data safety:

- **Primary (`#E11D48`)**: A vivid crimson red providing clear visual lineage to traditional document and PDF tooling. Used deliberately for key actions, destructive warnings, processing states, and active tool glyphs.
- **Secondary (`#10B981`)**: An authoritative emerald green reserved for privacy affirmations, on-device verification badges, offline guarantees, and successful task completions.
- **Tertiary (`#0F172A`)**: Deep slate blue-black utilized for dominant high-contrast headlines, primary floating actions, and deep dark-mode base canvases.
- **Neutral (`#64748B`)**: Slate gray scale spanning `#0F172A` (surface dark), `#334155` (text secondary), `#94A3B8` (borders and dividers), `#F1F5F9` (card and pill fills), and `#F8FAFC` (canvas light), anchoring high legibility across variable lighting conditions.

## Typography

The type scale pairs the structural warmth of **Plus Jakarta Sans** for prominent UI markers and headers with the neutral, hyper-legible metrics of **Inter** for dense metadata and utility copy. 

- Use **Plus Jakarta Sans** with negative tracking across all heading levels to maintain a cohesive, compact mobile hierarchy.
- Use **Inter** for all file sizes, page tallies, settings configurations, and button labels to avoid visual fatigue during document audits.
- Use **JetBrains Mono** strictly for file hash strings (MD5/SHA-256), cryptographic key summaries, page ranges, and file extensions.

## Layout & Spacing

The layout operates on a standard 4-column fluid mobile grid upgrading to 8 columns on tablets, anchored by an 8pt base grid for all gaps and paddings:

- **Mobile Viewport**: 16px screen margins (`margin-mobile`), 12px horizontal gutters (`gutter-mobile`), ensuring maximal surface area for document previews and multi-file listings.
- **Utility Cards Grid**: A 2-column uniform square/rectangular aspect ratio grid for tool shortcuts (e.g., Merge, Split, Compress, Sign, Redact).
- **Rhythm Rules**: Keep internal card padding at 16px (`space-md`). Stack grouped tool panels with 12px gaps (`space-sm`) and section dividers with 24px margins (`space-lg`).

## Elevation & Depth

This system avoids heavy, disorienting drop shadows in favor of **low-contrast architectural outlines and subtle ambient light models**:

- **Canvas Base**: `#F8FAFC` (Light) and `#0F172A` (Dark).
- **Surface Elevation 1 (Cards, Modules)**: Flat white `#FFFFFF` layered over canvas, delimited by a 1px border of `#E2E8F0` and an ambient shadow: `0 1px 3px 0 rgba(15, 23, 42, 0.04), 0 1px 2px -1px rgba(15, 23, 42, 0.02)`.
- **Surface Elevation 2 (Active Sheets, Popovers)**: `#FFFFFF` bounded by `0 10px 15px -3px rgba(15, 23, 42, 0.06), 0 4px 6px -4px rgba(15, 23, 42, 0.03)` with a hairline outline `#CBD5E1`.
- **Privacy Surface Highlight**: Secure offline badge containers leverage a soft tinted background (`#ECFDF5`) surrounded by a translucent emerald keyline (`#A7F3D0`), conveying verified perimeter encapsulation without visual weight.

## Shapes

The geometry reflects soft, precision-tooled contours using systematic curves:

- **Cards & Modal Sheets**: Styled with `rounded-2xl` (1rem / 16px) to present an inviting, friendly utility aesthetic.
- **Tool Icon Containers**: Styled with `rounded-xl` (0.75rem / 12px) nested cleanly inside cards.
- **Status Pills & Chips**: Strictly pill-shaped (`rounded-full`) to differentiate reactive states from structural surfaces.
- **Form Inputs & Action Buttons**: Structured at `rounded-xl` (0.75rem / 12px) for thumb-friendly reach on mobile devices.

## Components

### Buttons
- **Primary Action**: Crimson background (`#E11D48`), white text (`#FFFFFF`), `rounded-xl`, 48px fixed height for optimal touch target. Slight active state scale down (`0.98`) with background shift to `#BE123C`.
- **Secondary Utility**: Slate background (`#F1F5F9`), text in `#0F172A`, 1px border in `#E2E8F0`.
- **Destructive/Clear**: Crimson text, background transparent, active state soft crimson tint (`#FFE4E6`).

### Offline & Security Badges (Chips)
- **Status Shield**: Pill-shaped container (`rounded-full`), padding `4px 10px`. Background `#ECFDF5`, border 1px solid `#A7F3D0`. Includes a static 6px emerald dot (`#10B981`) paired with `label-sm` text: "100% On-Device / Sandboxed".

### Utility Grid Cards
- **Structure**: Surface white, `rounded-2xl`, 16px padding, containing an upper badge housing the category icon (36x36px with tinted backgrounds, e.g., `#FFE4E6` for Crimson tools, `#EFF6FF` for organizing tools).
- **Typography Layout**: Upper-left icon alignment, bold tool title (`headline-sm`) positioned directly below, accompanied by single-line meta descriptor (`body-sm`, e.g., "Combine 2+ files").

### File Lists & Queue Items
- **File Row**: Row height 64px, separated by 1px border (`#F1F5F9`). Contains file type glyph, title truncated via ellipsis, size tag in `code-mono`, and an end-aligned contextual action icon (reorder handle or remove toggle).

### Input Fields & Sliders (Compression/DPI)
- **Text Inputs**: 44px height, `rounded-xl`, border 1px solid `#CBD5E1`, filled with `#FFFFFF`. Focus ring in `#E11D48` at 2px offset.
- **Range Controls**: Smooth crimson thumb with `#E2E8F0` track, displaying numerical compression output dynamically in `code-mono`.

### Checkboxes & Toggle Controls
- **Toggle Switch**: 28px height, 48px width pill. Active thumb rests in emerald `#10B981` (for privacy preferences) or crimson `#E11D48` (for action parameters).