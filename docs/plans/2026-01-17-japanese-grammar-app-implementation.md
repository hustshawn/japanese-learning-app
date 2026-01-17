# Japanese Grammar Learning App Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a personal Japanese grammar learning web app with random display, mastery tracking, and romaji support.

**Architecture:** Pure client-side web app using HTML/CSS/JS with JSON data file for grammar content and localStorage for persistence. No build tools or frameworks - runs directly in browser.

**Tech Stack:** HTML5, CSS3, JavaScript (ES6+), localStorage API, JSON

---

## Task 1: Project Structure Setup

**Files:**
- Create: `data/grammar.json`
- Create: `index.html`
- Create: `styles.css`
- Create: `app.js`

**Step 1: Create data directory and initial grammar data**

Create the data directory:
```bash
mkdir -p data
```

**Step 2: Write grammar.json with sample content**

Create `data/grammar.json`:
```json
[
  {
    "id": "ga-particle",
    "title": "が (ga) - Subject Marker",
    "titleRomaji": "ga",
    "explanation": "Marks the grammatical subject of a sentence. Often used to introduce new information or emphasize what is doing the action.",
    "examples": [
      {
        "japanese": "猫が好きです。",
        "romaji": "Neko ga suki desu.",
        "english": "I like cats. (Literally: Cats are liked)"
      },
      {
        "japanese": "雨が降っています。",
        "romaji": "Ame ga futteimasu.",
        "english": "It is raining. (Literally: Rain is falling)"
      },
      {
        "japanese": "誰が来ましたか？",
        "romaji": "Dare ga kimashita ka?",
        "english": "Who came?"
      }
    ]
  },
  {
    "id": "wa-particle",
    "title": "は (wa) - Topic Marker",
    "titleRomaji": "wa",
    "explanation": "Marks the topic of a sentence (what you're talking about). Note: written as は but pronounced 'wa' when used as a particle.",
    "examples": [
      {
        "japanese": "私は学生です。",
        "romaji": "Watashi wa gakusei desu.",
        "english": "I am a student."
      },
      {
        "japanese": "これは本です。",
        "romaji": "Kore wa hon desu.",
        "english": "This is a book."
      },
      {
        "japanese": "今日は暑いです。",
        "romaji": "Kyou wa atsui desu.",
        "english": "Today is hot."
      }
    ]
  },
  {
    "id": "wo-particle",
    "title": "を (wo) - Object Marker",
    "titleRomaji": "wo/o",
    "explanation": "Marks the direct object of an action. Usually pronounced 'o' rather than 'wo' in modern Japanese.",
    "examples": [
      {
        "japanese": "りんごを食べます。",
        "romaji": "Ringo wo tabemasu.",
        "english": "I eat an apple."
      },
      {
        "japanese": "本を読みます。",
        "romaji": "Hon wo yomimasu.",
        "english": "I read a book."
      },
      {
        "japanese": "音楽を聞きます。",
        "romaji": "Ongaku wo kikimasu.",
        "english": "I listen to music."
      }
    ]
  },
  {
    "id": "ni-particle",
    "title": "に (ni) - Location/Time/Direction Marker",
    "titleRomaji": "ni",
    "explanation": "Indicates location of existence, time, direction, or target of an action. Very versatile particle with multiple uses.",
    "examples": [
      {
        "japanese": "東京に住んでいます。",
        "romaji": "Toukyou ni sundeimasu.",
        "english": "I live in Tokyo."
      },
      {
        "japanese": "９時に起きます。",
        "romaji": "Kuji ni okimasu.",
        "english": "I wake up at 9 o'clock."
      },
      {
        "japanese": "友達に会います。",
        "romaji": "Tomodachi ni aimasu.",
        "english": "I meet a friend."
      }
    ]
  },
  {
    "id": "de-particle",
    "title": "で (de) - Location/Means Marker",
    "titleRomaji": "de",
    "explanation": "Indicates the location where an action takes place or the means/method by which something is done.",
    "examples": [
      {
        "japanese": "図書館で勉強します。",
        "romaji": "Toshokan de benkyou shimasu.",
        "english": "I study at the library."
      },
      {
        "japanese": "バスで行きます。",
        "romaji": "Basu de ikimasu.",
        "english": "I go by bus."
      },
      {
        "japanese": "日本語で話します。",
        "romaji": "Nihongo de hanashimasu.",
        "english": "I speak in Japanese."
      }
    ]
  },
  {
    "id": "desu-copula",
    "title": "です (desu) - Copula",
    "titleRomaji": "desu",
    "explanation": "A copula that means 'to be' (for non-actions). Makes sentences polite and indicates state of being or equality.",
    "examples": [
      {
        "japanese": "これは机です。",
        "romaji": "Kore wa tsukue desu.",
        "english": "This is a desk."
      },
      {
        "japanese": "彼は先生です。",
        "romaji": "Kare wa sensei desu.",
        "english": "He is a teacher."
      },
      {
        "japanese": "きれいです。",
        "romaji": "Kirei desu.",
        "english": "It is beautiful."
      }
    ]
  },
  {
    "id": "masu-form",
    "title": "ます (masu) - Polite Verb Ending",
    "titleRomaji": "masu",
    "explanation": "Polite present/future tense verb ending. Attached to verb stems to make them formal and polite.",
    "examples": [
      {
        "japanese": "行きます。",
        "romaji": "Ikimasu.",
        "english": "I go. / I will go."
      },
      {
        "japanese": "食べます。",
        "romaji": "Tabemasu.",
        "english": "I eat. / I will eat."
      },
      {
        "japanese": "見ます。",
        "romaji": "Mimasu.",
        "english": "I see. / I will see."
      }
    ]
  },
  {
    "id": "te-form",
    "title": "て形 (te-form) - Connector Form",
    "titleRomaji": "te-kei",
    "explanation": "A verb form used to connect actions, make requests, or indicate ongoing actions. Very common and versatile grammatical structure.",
    "examples": [
      {
        "japanese": "起きて、顔を洗います。",
        "romaji": "Okite, kao wo araimasu.",
        "english": "I wake up and wash my face."
      },
      {
        "japanese": "座ってください。",
        "romaji": "Suwatte kudasai.",
        "english": "Please sit down."
      },
      {
        "japanese": "走っています。",
        "romaji": "Hashitteimasu.",
        "english": "I am running."
      }
    ]
  }
]
```

**Step 3: Verify JSON is valid**

Run:
```bash
cat data/grammar.json | python3 -m json.tool > /dev/null && echo "JSON is valid"
```

Expected output: "JSON is valid"

**Step 4: Commit data structure**

```bash
git add data/grammar.json
git commit -m "feat: add initial grammar data with 8 common grammar points

- Add particles: が、は、を、に、で
- Add basic structures: です、ます、て形
- Include romaji for all Japanese text
- 3 examples per grammar point

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 2: HTML Structure

**Files:**
- Create: `index.html`

**Step 1: Create basic HTML structure**

Create `index.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Japanese Grammar Learning</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>日本語文法 Japanese Grammar</h1>
            <p class="subtitle">にほんごぶんぽう (Nihongo Bunpou)</p>
        </header>

        <nav class="controls">
            <button id="randomBtn" class="btn btn-primary">
                <span>🎲</span> Show Random Grammar
            </button>
            <button id="viewAllBtn" class="btn btn-secondary">
                <span>📋</span> View All
            </button>
        </nav>

        <main id="mainContent">
            <!-- Grammar card or list will be inserted here -->
        </main>

        <footer id="progressFooter">
            <!-- Progress will be shown here -->
        </footer>
    </div>

    <script src="app.js"></script>
</body>
</html>
```

**Step 2: Test HTML in browser**

Open `index.html` in browser:
```bash
echo "Open file:///home/coder/jp-learning-app/index.html in your browser"
```

Expected: Page loads with header, two buttons, and empty main content area.

**Step 3: Commit HTML structure**

```bash
git add index.html
git commit -m "feat: add HTML structure with header and navigation

- Semantic HTML5 structure
- Header with Japanese and romaji title
- Navigation buttons for random and view all
- Main content area for dynamic content
- Footer for progress display

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 3: CSS Styling - Base Styles

**Files:**
- Create: `styles.css`

**Step 1: Add CSS reset and base styles**

Create `styles.css`:
```css
/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-color: #3b82f6;
    --primary-hover: #2563eb;
    --success-color: #10b981;
    --success-hover: #059669;
    --text-primary: #1f2937;
    --text-secondary: #6b7280;
    --text-light: #9ca3af;
    --bg-primary: #ffffff;
    --bg-secondary: #f9fafb;
    --border-color: #e5e7eb;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --radius: 12px;
    --transition: all 0.3s ease;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
    line-height: 1.6;
    color: var(--text-primary);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: var(--bg-primary);
    border-radius: var(--radius);
    box-shadow: var(--shadow-lg);
    overflow: hidden;
}
```

**Step 2: Add header styles**

Append to `styles.css`:
```css
/* Header */
header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    text-align: center;
}

header h1 {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.subtitle {
    font-size: 1rem;
    opacity: 0.9;
    font-weight: 300;
}
```

**Step 3: Test styling in browser**

Refresh browser at `file:///home/coder/jp-learning-app/index.html`

Expected: Beautiful gradient background, centered white card, gradient header with title.

**Step 4: Commit base CSS**

```bash
git add styles.css
git commit -m "feat: add base CSS styles and header design

- CSS custom properties for theming
- Gradient background and container card
- Beautiful header with gradient matching body
- Modern, clean typography

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 4: CSS Styling - Navigation and Buttons

**Files:**
- Modify: `styles.css`

**Step 1: Add navigation and button styles**

Append to `styles.css`:
```css
/* Navigation */
.controls {
    padding: 1.5rem;
    background: var(--bg-secondary);
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
    border-bottom: 1px solid var(--border-color);
}

/* Buttons */
.btn {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: var(--transition);
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    box-shadow: var(--shadow-sm);
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.btn:active {
    transform: translateY(0);
}

.btn-primary {
    background: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background: var(--primary-hover);
}

.btn-secondary {
    background: white;
    color: var(--text-primary);
    border: 2px solid var(--border-color);
}

.btn-secondary:hover {
    border-color: var(--primary-color);
    color: var(--primary-color);
}

.btn-success {
    background: var(--success-color);
    color: white;
}

.btn-success:hover {
    background: var(--success-hover);
}

.btn span {
    font-size: 1.2rem;
}
```

**Step 2: Test button styles in browser**

Refresh browser.

Expected: Two beautifully styled buttons with hover effects, centered below header.

**Step 3: Commit button styles**

```bash
git add styles.css
git commit -m "feat: add navigation and button styles

- Flexible navigation layout
- Modern button designs with hover effects
- Primary, secondary, and success button variants
- Smooth transitions and shadows

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 5: CSS Styling - Grammar Card

**Files:**
- Modify: `styles.css`

**Step 1: Add grammar card styles**

Append to `styles.css`:
```css
/* Main content */
main {
    padding: 2rem;
    min-height: 400px;
}

/* Grammar card */
.grammar-card {
    background: white;
    border: 2px solid var(--border-color);
    border-radius: var(--radius);
    padding: 2rem;
    animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.grammar-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.grammar-romaji {
    font-size: 1.2rem;
    color: var(--text-light);
    margin-bottom: 1.5rem;
}

.grammar-explanation {
    font-size: 1.1rem;
    line-height: 1.8;
    color: var(--text-secondary);
    margin-bottom: 2rem;
    padding: 1rem;
    background: var(--bg-secondary);
    border-radius: 8px;
    border-left: 4px solid var(--primary-color);
}

/* Examples section */
.examples-section {
    margin-top: 2rem;
}

.examples-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 1rem;
}

.example {
    margin-bottom: 1.5rem;
    padding: 1rem;
    background: var(--bg-secondary);
    border-radius: 8px;
    border-left: 3px solid var(--success-color);
}

.example-japanese {
    font-size: 1.4rem;
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 0.3rem;
}

.example-romaji {
    font-size: 1rem;
    color: var(--text-light);
    font-style: italic;
    margin-bottom: 0.5rem;
}

.example-english {
    font-size: 1rem;
    color: var(--text-secondary);
}

/* Mastery button */
.mastery-section {
    margin-top: 2rem;
    text-align: center;
    padding-top: 1.5rem;
    border-top: 2px solid var(--border-color);
}

.mastery-btn {
    padding: 1rem 2rem;
    font-size: 1.1rem;
}

.mastered .mastery-btn {
    background: var(--success-color);
}

.mastered .mastery-btn:hover {
    background: var(--success-hover);
}
```

**Step 2: Test grammar card styles in browser**

Refresh browser.

Expected: Styles are loaded (no visual change yet since no grammar card is rendered).

**Step 3: Commit grammar card styles**

```bash
git add styles.css
git commit -m "feat: add grammar card and example styles

- Card layout with fade-in animation
- Japanese text prominently displayed
- Romaji in subtle, lighter style
- Color-coded sections for explanation and examples
- Mastery button section with success color

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 6: CSS Styling - List View and Footer

**Files:**
- Modify: `styles.css`

**Step 1: Add list view and footer styles**

Append to `styles.css`:
```css
/* Grammar list view */
.grammar-list {
    display: grid;
    gap: 1rem;
}

.grammar-list-item {
    background: white;
    border: 2px solid var(--border-color);
    border-radius: 8px;
    padding: 1.25rem;
    cursor: pointer;
    transition: var(--transition);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.grammar-list-item:hover {
    border-color: var(--primary-color);
    transform: translateX(5px);
    box-shadow: var(--shadow-md);
}

.grammar-list-item.mastered {
    border-color: var(--success-color);
    background: rgba(16, 185, 129, 0.05);
}

.list-item-content h3 {
    font-size: 1.3rem;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
}

.list-item-romaji {
    font-size: 0.9rem;
    color: var(--text-light);
}

.list-item-status {
    font-size: 1.5rem;
}

/* Footer */
footer {
    padding: 1.5rem;
    background: var(--bg-secondary);
    border-top: 2px solid var(--border-color);
    text-align: center;
}

.progress-text {
    font-size: 1.1rem;
    color: var(--text-secondary);
    font-weight: 600;
}

.progress-bar-container {
    margin-top: 0.75rem;
    height: 10px;
    background: var(--border-color);
    border-radius: 5px;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--success-color), var(--primary-color));
    transition: width 0.5s ease;
    border-radius: 5px;
}

/* Responsive design */
@media (max-width: 640px) {
    body {
        padding: 10px;
    }

    header h1 {
        font-size: 1.5rem;
    }

    .controls {
        flex-direction: column;
    }

    .btn {
        width: 100%;
        justify-content: center;
    }

    main {
        padding: 1rem;
    }

    .grammar-title {
        font-size: 1.5rem;
    }

    .example-japanese {
        font-size: 1.2rem;
    }
}

/* Utility classes */
.hidden {
    display: none;
}

.fade-in {
    animation: fadeIn 0.5s ease;
}
```

**Step 2: Test responsive styles**

Refresh browser and resize window.

Expected: Styles adapt to smaller screens with stacked buttons and adjusted font sizes.

**Step 3: Commit list and footer styles**

```bash
git add styles.css
git commit -m "feat: add list view, footer, and responsive styles

- Grid layout for grammar list
- List items with hover effects and mastery indicators
- Progress bar with gradient
- Responsive design for mobile devices
- Utility classes for show/hide

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 7: JavaScript - App Structure and Data Loading

**Files:**
- Create: `app.js`

**Step 1: Create app initialization structure**

Create `app.js`:
```javascript
// Japanese Grammar Learning App
// Main application logic

class GrammarApp {
    constructor() {
        this.grammarData = [];
        this.masteredGrammar = new Set();
        this.currentView = 'card'; // 'card' or 'list'
        this.currentGrammarId = null;

        // DOM elements
        this.mainContent = document.getElementById('mainContent');
        this.progressFooter = document.getElementById('progressFooter');
        this.randomBtn = document.getElementById('randomBtn');
        this.viewAllBtn = document.getElementById('viewAllBtn');

        this.init();
    }

    async init() {
        // Load mastered grammar from localStorage
        this.loadMasteredFromStorage();

        // Load grammar data
        await this.loadGrammarData();

        // Set up event listeners
        this.setupEventListeners();

        // Show initial random grammar
        this.showRandomGrammar();

        // Update progress
        this.updateProgress();
    }

    loadMasteredFromStorage() {
        const stored = localStorage.getItem('masteredGrammar');
        if (stored) {
            try {
                const parsed = JSON.parse(stored);
                this.masteredGrammar = new Set(parsed);
            } catch (e) {
                console.error('Error loading mastered grammar:', e);
                this.masteredGrammar = new Set();
            }
        }
    }

    saveMasteredToStorage() {
        const array = Array.from(this.masteredGrammar);
        localStorage.setItem('masteredGrammar', JSON.stringify(array));
    }

    async loadGrammarData() {
        try {
            const response = await fetch('data/grammar.json');
            if (!response.ok) {
                throw new Error('Failed to load grammar data');
            }
            this.grammarData = await response.json();
            console.log(`Loaded ${this.grammarData.length} grammar points`);
        } catch (error) {
            console.error('Error loading grammar data:', error);
            this.showError('Failed to load grammar data. Please refresh the page.');
        }
    }

    setupEventListeners() {
        this.randomBtn.addEventListener('click', () => this.showRandomGrammar());
        this.viewAllBtn.addEventListener('click', () => this.toggleView());

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && e.target === document.body) {
                e.preventDefault();
                this.showRandomGrammar();
            }
            if (e.code === 'KeyM' && this.currentView === 'card' && this.currentGrammarId) {
                e.preventDefault();
                this.toggleMastery(this.currentGrammarId);
            }
        });
    }

    showError(message) {
        this.mainContent.innerHTML = `
            <div class="grammar-card">
                <p style="color: #ef4444; font-size: 1.2rem; text-align: center;">
                    ⚠️ ${message}
                </p>
            </div>
        `;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new GrammarApp();
});
```

**Step 2: Test app initialization**

Open browser console and refresh page.

Expected: Console shows "Loaded 8 grammar points" and no errors.

**Step 3: Commit app structure**

```bash
git add app.js
git commit -m "feat: add app structure and data loading

- GrammarApp class with initialization
- Load grammar data from JSON
- localStorage integration for mastery tracking
- Event listeners setup
- Keyboard shortcuts (Space, M)
- Error handling

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 8: JavaScript - Random Grammar Display

**Files:**
- Modify: `app.js`

**Step 1: Add random grammar selection method**

Add these methods to the `GrammarApp` class in `app.js`, before the closing brace:

```javascript
    showRandomGrammar() {
        if (this.grammarData.length === 0) {
            this.showError('No grammar data available');
            return;
        }

        // Smart randomization: 70% chance for non-mastered, 30% for any
        const nonMastered = this.grammarData.filter(g => !this.masteredGrammar.has(g.id));

        let grammar;
        if (nonMastered.length > 0 && Math.random() < 0.7) {
            // Pick from non-mastered
            grammar = nonMastered[Math.floor(Math.random() * nonMastered.length)];
        } else {
            // Pick from all
            grammar = this.grammarData[Math.floor(Math.random() * this.grammarData.length)];
        }

        this.showGrammarCard(grammar);
    }

    showGrammarCard(grammar) {
        this.currentView = 'card';
        this.currentGrammarId = grammar.id;
        const isMastered = this.masteredGrammar.has(grammar.id);

        // Build examples HTML
        const examplesHTML = grammar.examples.map(ex => `
            <div class="example">
                <div class="example-japanese">${ex.japanese}</div>
                <div class="example-romaji">${ex.romaji}</div>
                <div class="example-english">${ex.english}</div>
            </div>
        `).join('');

        // Build card HTML
        this.mainContent.innerHTML = `
            <div class="grammar-card ${isMastered ? 'mastered' : ''}">
                <div class="grammar-title">${grammar.title}</div>
                <div class="grammar-romaji">(${grammar.titleRomaji})</div>
                <div class="grammar-explanation">${grammar.explanation}</div>

                <div class="examples-section">
                    <div class="examples-title">📝 Examples</div>
                    ${examplesHTML}
                </div>

                <div class="mastery-section">
                    <button class="btn mastery-btn" data-grammar-id="${grammar.id}">
                        ${isMastered ? '✓ Mastered' : 'Mark as Mastered'}
                    </button>
                </div>
            </div>
        `;

        // Add mastery toggle event listener
        const masteryBtn = this.mainContent.querySelector('.mastery-btn');
        masteryBtn.addEventListener('click', () => this.toggleMastery(grammar.id));

        // Update progress
        this.updateProgress();
    }
```

**Step 2: Test random grammar display**

Refresh browser.

Expected: A random grammar point displays with Japanese, romaji, explanation, examples, and mastery button.

**Step 3: Commit random display**

```bash
git add app.js
git commit -m "feat: add random grammar display functionality

- Smart randomization (70% non-mastered, 30% any)
- Render grammar card with all details
- Display Japanese with romaji
- Show examples with translations
- Mastery button integration

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 9: JavaScript - Mastery Toggle and Progress

**Files:**
- Modify: `app.js`

**Step 1: Add mastery toggle method**

Add these methods to the `GrammarApp` class in `app.js`:

```javascript
    toggleMastery(grammarId) {
        if (this.masteredGrammar.has(grammarId)) {
            this.masteredGrammar.delete(grammarId);
        } else {
            this.masteredGrammar.add(grammarId);
        }

        // Save to localStorage
        this.saveMasteredToStorage();

        // Update UI
        if (this.currentView === 'card' && this.currentGrammarId === grammarId) {
            // Update button in card view
            const card = this.mainContent.querySelector('.grammar-card');
            const btn = this.mainContent.querySelector('.mastery-btn');
            const isMastered = this.masteredGrammar.has(grammarId);

            if (isMastered) {
                card.classList.add('mastered');
                btn.textContent = '✓ Mastered';
                btn.classList.add('btn-success');
            } else {
                card.classList.remove('mastered');
                btn.textContent = 'Mark as Mastered';
                btn.classList.remove('btn-success');
            }
        } else if (this.currentView === 'list') {
            // Refresh list view
            this.showAllGrammar();
        }

        // Update progress
        this.updateProgress();
    }

    updateProgress() {
        const total = this.grammarData.length;
        const mastered = this.masteredGrammar.size;
        const percentage = total > 0 ? Math.round((mastered / total) * 100) : 0;

        this.progressFooter.innerHTML = `
            <div class="progress-text">
                Progress: ${mastered} / ${total} mastered (${percentage}%)
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar" style="width: ${percentage}%"></div>
            </div>
        `;
    }
```

**Step 2: Test mastery toggle**

Refresh browser, click "Mark as Mastered".

Expected: Button changes to "✓ Mastered" with green background, progress updates.

**Step 3: Verify localStorage persistence**

Refresh page after marking items as mastered.

Expected: Mastery status persists after refresh.

**Step 4: Commit mastery toggle**

```bash
git add app.js
git commit -m "feat: add mastery toggle and progress tracking

- Toggle mastery status on/off
- Save to localStorage automatically
- Update button text and styling
- Progress bar with percentage
- Visual feedback for mastered items

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 10: JavaScript - List View

**Files:**
- Modify: `app.js`

**Step 1: Add list view methods**

Add these methods to the `GrammarApp` class in `app.js`:

```javascript
    toggleView() {
        if (this.currentView === 'card') {
            this.showAllGrammar();
        } else {
            this.showRandomGrammar();
        }
    }

    showAllGrammar() {
        this.currentView = 'list';
        this.currentGrammarId = null;

        // Sort: non-mastered first, then by title
        const sorted = [...this.grammarData].sort((a, b) => {
            const aMastered = this.masteredGrammar.has(a.id);
            const bMastered = this.masteredGrammar.has(b.id);

            if (aMastered === bMastered) {
                return a.title.localeCompare(b.title);
            }
            return aMastered ? 1 : -1;
        });

        const listHTML = sorted.map(grammar => {
            const isMastered = this.masteredGrammar.has(grammar.id);
            return `
                <div class="grammar-list-item ${isMastered ? 'mastered' : ''}" data-grammar-id="${grammar.id}">
                    <div class="list-item-content">
                        <h3>${grammar.title}</h3>
                        <div class="list-item-romaji">${grammar.titleRomaji}</div>
                    </div>
                    <div class="list-item-status">
                        ${isMastered ? '✓' : '○'}
                    </div>
                </div>
            `;
        }).join('');

        this.mainContent.innerHTML = `
            <div class="grammar-list">
                ${listHTML}
            </div>
        `;

        // Add click listeners to list items
        this.mainContent.querySelectorAll('.grammar-list-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const grammarId = e.currentTarget.dataset.grammarId;
                const grammar = this.grammarData.find(g => g.id === grammarId);
                if (grammar) {
                    this.showGrammarCard(grammar);
                }
            });
        });

        // Update button text
        this.viewAllBtn.innerHTML = '<span>🎲</span> Show Random';
    }
```

**Step 2: Update button text when switching views**

Modify the `showGrammarCard` method to update the view button. Add this line at the end of the method:

```javascript
        // Update button text
        this.viewAllBtn.innerHTML = '<span>📋</span> View All';
```

**Step 3: Test list view**

Refresh browser, click "View All".

Expected: Shows list of all grammar points, mastered items at bottom with checkmarks.

**Step 4: Test clicking list items**

Click a grammar item in the list.

Expected: Returns to card view showing that grammar point.

**Step 5: Commit list view**

```bash
git add app.js
git commit -m "feat: add list view for all grammar points

- Toggle between card and list view
- Sort list: non-mastered first
- Visual indicators for mastery status
- Click items to view details
- Dynamic button text updates

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 11: Testing and Polish

**Files:**
- Modify: `app.js` (if needed)
- Modify: `styles.css` (if needed)

**Step 1: Manual testing checklist**

Open browser and test:

1. ✓ Page loads and shows random grammar
2. ✓ Japanese text displays correctly
3. ✓ Romaji displays below Japanese
4. ✓ Examples show all three languages
5. ✓ Click "Mark as Mastered" - button changes
6. ✓ Progress bar updates
7. ✓ Click "Show Random Grammar" - new grammar appears
8. ✓ Refresh page - mastery persists
9. ✓ Click "View All" - shows list
10. ✓ Click list item - shows that grammar
11. ✓ Press Space key - random grammar
12. ✓ Press M key - toggle mastery
13. ✓ Resize window - responsive design works
14. ✓ Test on mobile device (or mobile emulation)

**Step 2: Fix any issues found**

If issues are found during testing, fix them now.

**Step 3: Add favicon (optional polish)**

Create a simple favicon by adding to `index.html` in the `<head>` section:

```html
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🇯🇵</text></svg>">
```

**Step 4: Test final version**

Complete full testing checklist again.

Expected: All features work smoothly, no errors in console.

**Step 5: Commit polish and testing**

```bash
git add index.html
git commit -m "feat: add favicon and complete testing

- Add Japanese flag emoji favicon
- Verify all features working
- Confirm responsive design
- Test keyboard shortcuts

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 12: Documentation

**Files:**
- Create: `README.md`

**Step 1: Create README documentation**

Create `README.md`:
```markdown
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
```

**Step 2: Commit README**

```bash
git add README.md
git commit -m "docs: add README with usage instructions

- Feature overview
- Usage guide
- Instructions for adding grammar points
- Tech stack documentation
- Future enhancement ideas

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**Step 3: Final verification**

List all project files:
```bash
find . -type f ! -path './.git/*' ! -path './.claude/*' | sort
```

Expected output:
```
./README.md
./app.js
./data/grammar.json
./docs/plans/2026-01-17-japanese-grammar-app-design.md
./docs/plans/2026-01-17-japanese-grammar-app-implementation.md
./index.html
./styles.css
```

**Step 4: Create final commit**

```bash
git add -A
git commit -m "chore: finalize Japanese grammar learning app MVP

Complete implementation includes:
- 8 grammar points with romaji
- Random display with smart prioritization
- Mastery tracking with localStorage
- List view with sorting
- Beautiful, responsive UI
- Keyboard shortcuts
- Complete documentation

Ready for personal use and future enhancements.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Implementation Complete

The MVP is now complete with all core features:

✅ Random grammar display with romaji
✅ Mastery tracking with localStorage persistence
✅ Beautiful, modern UI with animations
✅ List view with all grammar points
✅ Progress tracking with visual bar
✅ Responsive design for mobile
✅ Keyboard shortcuts (Space, M)
✅ 8 initial grammar points
✅ Easy content expansion via JSON
✅ Complete documentation

**To use:** Open `index.html` in any modern web browser.

**To extend:** Add more grammar points to `data/grammar.json`.
