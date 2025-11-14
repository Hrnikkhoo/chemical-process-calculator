// Theme Management
const themeManager = {
  init() {
    this.html = document.documentElement;
    this.themeToggleBtn = document.getElementById('themeToggle');
    this.themeIcon = this.themeToggleBtn?.querySelector('i');
    this.prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    if (this.themeToggleBtn) {
      this.initTheme();
      this.bindEvents();
    }
  },

  initTheme() {
    const savedTheme = localStorage.getItem('theme') || 
                      (this.prefersDarkScheme.matches ? 'dark' : 'light');
    this.setTheme(savedTheme);
  },

  setTheme(theme) {
    this.html.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    if (this.themeIcon) {
      this.themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
  },

  bindEvents() {
    // Theme toggle
    this.themeToggleBtn.addEventListener('click', () => {
      const currentTheme = this.html.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      this.setTheme(newTheme);
    });

    // System theme changes
    this.prefersDarkScheme.addEventListener('change', (e) => {
      if (!localStorage.getItem('theme')) {
        this.setTheme(e.matches ? 'dark' : 'light');
      }
    });
  }
};

// Form Handling
const formManager = {
  init() {
    this.forms = document.querySelectorAll('form');
    this.loadingOverlay = document.querySelector('.loading-overlay');
    
    if (this.forms.length && this.loadingOverlay) {
      this.bindEvents();
    }
  },

  bindEvents() {
    this.forms.forEach(form => {
      form.addEventListener('submit', () => {
        this.loadingOverlay.style.display = 'flex';
      });
    });
  }
};

// Input Validation
const inputManager = {
  init() {
    this.inputs = document.querySelectorAll('input[type="number"]');
    if (this.inputs.length) {
      this.bindEvents();
    }
  },

  bindEvents() {
    this.inputs.forEach(input => {
      input.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);
        if (isNaN(value)) {
          e.target.value = '';
        }
      });
    });
  }
};

// Image Fallback Handler
const imageFallback = {
  init() {
    const images = document.querySelectorAll('img[data-fallback]');
    images.forEach(img => {
      img.addEventListener('error', function() {
        const fallback = this.getAttribute('data-fallback');
        if (fallback && this.src !== fallback) {
          this.src = fallback;
        }
      });
    });
  }
};

// Initialize all managers when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  themeManager.init();
  formManager.init();
  inputManager.init();
  imageFallback.init();

  // Search functionality
  const searchInput = document.getElementById("calculatorSearch");
  const calculatorCards = document.querySelectorAll(".calculator-card");
  const searchSpinner = document.getElementById("searchSpinner");

  if (searchInput && calculatorCards.length > 0 && searchSpinner) {
    searchInput.addEventListener("input", function () {
      const searchTerm = this.value.trim().toLowerCase();

      // Show spinner and hide cards initially
      searchSpinner.classList.remove("d-none");
      calculatorCards.forEach((card) => {
        card.style.display = "none";
      });

      setTimeout(() => {
        calculatorCards.forEach((card) => {
          const cardName = card.getAttribute("data-name")?.toLowerCase() || "";
          const cardTitle = card.querySelector(".card-title")?.textContent.toLowerCase() || "";
          const cardTags = card.querySelector(".card-tags")?.textContent.toLowerCase() || "";

          if (
            cardName.includes(searchTerm) ||
            cardTitle.includes(searchTerm) ||
            cardTags.includes(searchTerm)
          ) {
            card.style.display = "";
          }
        });
        // Hide spinner after search is complete
        searchSpinner.classList.add("d-none");
      }, 300);
    });
  }
}); 