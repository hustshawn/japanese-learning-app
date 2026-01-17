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
