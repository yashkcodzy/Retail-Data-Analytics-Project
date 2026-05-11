# Dashboard Design System: "Eclipse Premium"

To make your Power BI dashboard look stunning and professional, follow this design system.

## 1. Color Palette (HEX Codes)
*   **Background**: `#0F172A` (Deep Slate)
*   **Card Background**: `#1E293B` (Mid Slate)
*   **Primary Accent**: `#3B82F6` (Electric Blue)
*   **Success (Profit)**: `#10B981` (Emerald)
*   **Warning (Loss)**: `#EF4444` (Coral Red)
*   **Text (Primary)**: `#F8FAFC` (Off-white)
*   **Text (Secondary)**: `#94A3B8` (Cool Grey)

## 2. Power BI Theme JSON
You can copy this into a file named `eclipse_theme.json` and import it into Power BI (**View > Themes > Browse for Themes**).

```json
{
    "name": "Eclipse Premium",
    "dataColors": ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#06B6D4"],
    "background": "#0F172A",
    "foreground": "#F8FAFC",
    "tableAccent": "#3B82F6",
    "visualStyles": {
        "*": {
            "*": {
                "background": [{ "show": true, "color": { "solid": { "color": "#1E293B" } }, "transparency": 10 }],
                "border": [{ "show": true, "color": { "solid": { "color": "#334155" } }, "radius": 10 }],
                "visualTooltip": [{ "type": "Default" }],
                "title": [{ "show": true, "fontFamily": "Segoe UI Semibold", "fontSize": 12, "fontColor": { "solid": { "color": "#F8FAFC" } } }]
            }
        },
        "card": {
            "*": {
                "labels": [{ "fontSize": 25, "fontFamily": "Segoe UI Semibold", "color": { "solid": { "color": "#3B82F6" } } }],
                "categoryLabels": [{ "fontSize": 10, "color": { "solid": { "color": "#94A3B8" } } }]
            }
        }
    }
}
```

## 3. Visual Styling Tips
*   **Shadows**: Enable "Shadow" on every visual. Set color to `#000000`, Transparency to 70%, and Blur to 10px.
*   **Glow Effect**: Use the "Emerald" color for positive trend lines and add a "Marker" with a halo effect if available.
*   **Typography**: Use **Segoe UI Semibold** for titles and **Segoe UI** for axis labels.
*   **Spacing**: Ensure there is at least 15px of "breathable" space between every chart.

## 4. Header Bar
Create a rectangle at the top with color `#1E293B`.
*   Place your title "RETAIL INSIGHTS | 2024" on the left.
*   Place slicers (Year, Region) on the right for a "toolbar" look.
