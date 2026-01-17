# Japanese Grammar Learning App - Design Document

**Date:** 2026-01-17
**Type:** Personal learning tool
**Stack:** Pure HTML/CSS/JavaScript (no build tools)

## Overview

A simple, personal web application for learning Japanese grammar through random exposure and mastery tracking. The app displays random grammar points with examples (all Japanese text includes romaji), allows marking items as mastered, and stores progress locally.

## Architecture

### File Structure
```
jp-learning-app/
├── index.html          # Main application page
├── styles.css          # Styling
├── app.js              # Application logic
└── data/
    └── grammar.json    # Grammar points database
```

### Technology Stack
- **Frontend:** Pure HTML5, CSS3, JavaScript (ES6+)
- **Storage:** Browser localStorage for mastery tracking
- **Content:** JSON file for easy editing and expansion
- **Deployment:** File system - open index.html directly in browser

## Core Features (MVP)

### 1. Random Grammar Display
- Shows a random grammar point on page load or button click
- Each point includes:
  - Japanese title with romaji
  - English explanation
  - 2-3 example sentences with Japanese, romaji, and English

### 2. Mastery Tracking
- Toggle button to mark grammar points as mastered/unmastered
- Visual indicator (color, checkmark) for mastered status
- Status persists in browser localStorage
- Progress counter shows mastered/total ratio

### 3. View All Grammar Points
- List view showing all available grammar points
- Visual indicators for mastery status
- Click to view specific grammar point

## Data Structure

### Grammar Point Schema (grammar.json)
```json
[
  {
    "id": "ga-particle",
    "title": "が (ga) - Subject Marker",
    "titleRomaji": "ga",
    "explanation": "Marks the grammatical subject of a sentence. Often used to introduce new information or emphasize the subject.",
    "examples": [
      {
        "japanese": "猫が好きです。",
        "romaji": "Neko ga suki desu.",
        "english": "I like cats."
      },
      {
        "japanese": "雨が降っています。",
        "romaji": "Ame ga futteimasu.",
        "english": "It is raining."
      }
    ]
  }
]
```

### localStorage Format
```javascript
{
  "masteredGrammar": ["ga-particle", "te-form"],
  "lastViewed": "wa-particle"
}
```

### Initial Content
Start with 5-10 common grammar points:
- Basic particles (が, は, を, に, で)
- Common sentence structures
- Easily expandable by editing JSON

## User Interface

### Layout
```
┌─────────────────────────────────────┐
│   Japanese Grammar Learning App     │
├─────────────────────────────────────┤
│                                     │
│   [Show Random Grammar] [View All]  │
│                                     │
│   ┌───────────────────────────────┐ │
│   │ が (ga) - Subject Marker      │ │
│   │ (ga)                          │ │
│   │                               │ │
│   │ Marks the grammatical subject │ │
│   │ of a sentence...              │ │
│   │                               │ │
│   │ Examples:                     │ │
│   │ • 猫が好きです。              │ │
│   │   Neko ga suki desu.          │ │
│   │   I like cats.                │ │
│   │                               │ │
│   │ [✓ Mark as Mastered]          │ │
│   └───────────────────────────────┘ │
│                                     │
│   Progress: 3/10 mastered          │
└─────────────────────────────────────┘
```

### User Flow
1. Page loads → displays random grammar point
2. User reads and studies the content
3. User clicks "Mark as Mastered" → button updates to "✓ Mastered" (green)
4. User clicks "Show Random Grammar" → displays another random point
5. User clicks "View All" → shows complete list with mastery indicators

## Design Principles

### Visual Polish
- **Typography:** Large, clear Japanese text with subtle romaji below
- **Modern Style:** Card-based layout, rounded corners, subtle shadows
- **Color Scheme:** Clean whites/grays with green (success) and blue (primary) accents
- **Animations:** Smooth transitions for grammar switching and button interactions

### User Experience
- **Touch-friendly:** Large buttons suitable for mobile
- **Visual Feedback:** Hover states, click animations, loading transitions
- **Reversible Actions:** Click "Mastered" again to unmark
- **Keyboard Shortcuts:** Space for random grammar, M to toggle mastered
- **Smart Randomization:** Prioritize non-mastered items (70% probability)

### Responsive Design
- Single column layout works on all screen sizes
- Comfortable padding and margins
- Mobile-optimized typography and touch targets

## Future Enhancements

### Practice Exercises (Phase 2)
When ready to expand, add exercise functionality:

**Exercise Types:**
- Fill-in-the-blank: Complete sentences with correct particles/forms
- Multiple choice: Select correct grammar option
- Sentence construction: Rearrange words into correct order

**Data Structure Addition:**
```json
{
  "id": "ga-particle",
  "title": "が (ga)",
  "exercises": [
    {
      "type": "fill-blank",
      "sentence": "猫___好きです。",
      "sentenceRomaji": "Neko ___ suki desu.",
      "answer": "が",
      "answerRomaji": "ga"
    }
  ]
}
```

### Other Potential Features
- Grammar categories/tags (particles, verb forms, adjectives)
- Search and filter functionality
- Export/import progress for backup
- Study statistics (streaks, most reviewed items)
- Spaced repetition algorithm

## Technical Implementation Notes

### Why This Architecture
- **No build tools:** Instant setup, just open in browser
- **JSON for content:** Easy to edit, add, and maintain grammar points
- **localStorage:** Automatic persistence without backend
- **Separation of concerns:** Clean split between data, logic, and presentation

### Extensibility
The design supports future growth:
- JSON structure can accommodate new fields (exercises, categories, difficulty)
- localStorage can store additional tracking data
- Modular JS structure allows adding new UI sections
- Can migrate to framework (React/Vue) later if complexity grows

## Success Criteria

MVP is successful when:
1. Can display random grammar points with romaji
2. Examples render clearly with all three languages
3. Mastery tracking persists across browser sessions
4. UI is clean, readable, and pleasant to use
5. Adding new grammar points requires only JSON editing
