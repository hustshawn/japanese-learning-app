# Japanese Grammar Learning App

A personal web application for learning Japanese grammar through random exposure and spaced practice.

## Features

- **Random Grammar Display**: Shows random grammar points with smart prioritization of non-mastered items
- **Romaji Support**: All Japanese text includes romaji (romanized pronunciation)
- **Examples**: Each grammar point includes 2-3 example sentences with translations
- **Mastery Tracking**: Mark grammar points as mastered; progress persists in browser
- **List View**: View all grammar points with mastery status indicators
- **Keyboard Shortcuts**:
  - `Space` - Show random grammar
  - `M` - Toggle mastery for current grammar
- **Responsive Design**: Works beautifully on desktop and mobile

## Usage

1. Open `index.html` in your web browser
2. Study the displayed grammar point
3. Click "Mark as Mastered" when you've learned it
4. Click "Show Random Grammar" for another point
5. Click "View All" to see the complete list

Your progress is automatically saved in your browser.

## Adding More Grammar Points

Edit `data/grammar.json` and add new entries following this format:

```json
{
  "id": "unique-id",
  "title": "Japanese Title",
  "titleRomaji": "romaji",
  "explanation": "Explanation in English",
  "examples": [
    {
      "japanese": "日本語の例",
      "romaji": "Nihongo no rei",
      "english": "English translation"
    }
  ]
}
```

## Tech Stack

- Pure HTML5, CSS3, JavaScript (ES6+)
- No frameworks or build tools required
- localStorage for data persistence

## Future Enhancements

- Practice exercises (fill-in-the-blank, multiple choice)
- Grammar categories and filtering
- Export/import progress
- Study statistics and streaks
- Spaced repetition algorithm

## License

Personal use project. Use and modify as you wish.
