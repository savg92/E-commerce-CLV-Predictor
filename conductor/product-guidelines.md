# Product Guidelines: E-commerce CLV Predictor

## Visual Style & Branding
- **Design Philosophy:** Clean, professional, and data-centric. Use a "Modern Fintech" aesthetic.
- **Color Palette:**
  - Primary: Deep Indigo or Slate Blue for trust and stability.
  - Secondary: Teal or Soft Gray for auxiliary data visualization.
  - Alert/Warning: Amber for uncertainty (OOD alerts) and Red for errors.
- **Typography:** Sans-serif fonts (e.g., Inter, Roboto) for maximum legibility in data tables and charts.

## Voice & Tone
- **Professional & Precise:** Avoid flowery language. Focus on clarity and accuracy.
- **Empowering:** Help the user feel in control of the data.
- **Transparent:** Be explicit about model limitations and uncertainty.

## User Experience (UX) Principles
- **Clarity Over Clutter:** Prioritize the most important prediction metrics (CLV, Confidence Score).
- **Interactive Feedback:** Provide real-time updates when users modify input features.
- **Progressive Disclosure:** Show high-level summaries first, with the option to drill down into RFM details.
- **Error Handling:** Use human-readable error messages and clear recovery paths.

## Specific UI Requirements
- **OOD Safety Mechanism:** When the model detects Out-of-Distribution data, the UI must display a prominent warning:
  > ⚠️ **"Warning: I am not sure about this [prediction]!"**
- **Data Visualization:** Use charts (e.g., line charts for historical trends, bar charts for RFM distribution) to make predictions intuitive.
