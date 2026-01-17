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

        // Update button text
        this.viewAllBtn.innerHTML = '<span>📋</span> View All';

        // Update progress
        this.updateProgress();
    }

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
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new GrammarApp();
});
