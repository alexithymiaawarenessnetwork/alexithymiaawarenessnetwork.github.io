/**
 * Citation Hover Box System
 * Handles citation links and displays rich citation information in hover boxes
 */

class CitationManager {
    constructor() {
        this.citationsData = null;
        this.currentHoverBox = null;
        this.init();
    }

    async init() {
        // Load citations data
        await this.loadCitationsData();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Create hover box container
        this.createHoverBoxContainer();
    }

    async loadCitationsData() {
        try {
            // Determine the correct path to citations.json based on current location
            const currentPath = window.location.pathname;
            const basePath = currentPath.endsWith('/') ? '../' : './';
            const citationsPath = basePath + 'citations.json';
            
            const response = await fetch(citationsPath);
            if (!response.ok) {
                throw new Error(`Failed to load citations: ${response.status}`);
            }
            
            const data = await response.json();
            this.citationsData = data.citations;
            console.log('Citations data loaded successfully');
        } catch (error) {
            console.error('Error loading citations data:', error);
            this.citationsData = [];
        }
    }

    setupEventListeners() {
        // Handle clicks on citation links
        document.addEventListener('click', (event) => {
            const link = event.target.closest('a[href*="citations.json#"]');
            if (link) {
                event.preventDefault();
                this.handleCitationClick(link, event);
            }
        });

        // Close hover box when clicking outside
        document.addEventListener('click', (event) => {
            if (this.currentHoverBox && !this.currentHoverBox.contains(event.target) && 
                !event.target.closest('a[href*="citations.json#"]')) {
                this.closeHoverBox();
            }
        });

        // Close hover box on escape key
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && this.currentHoverBox) {
                this.closeHoverBox();
            }
        });
    }

    createHoverBoxContainer() {
        const container = document.createElement('div');
        container.id = 'citation-hover-container';
        container.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
        `;
        document.body.appendChild(container);
    }

    handleCitationClick(link, event) {
        const href = link.getAttribute('href');
        const citationId = href.split('#')[1];
        
        if (!citationId) {
            console.error('No citation ID found in link');
            return;
        }

        const citation = this.findCitation(citationId);
        if (!citation) {
            console.error(`Citation not found: ${citationId}`);
            // Fallback to original behavior
            window.open(href, '_blank');
            return;
        }

        this.showHoverBox(citation, event);
    }

    findCitation(citationId) {
        return this.citationsData.find(citation => citation.id === citationId);
    }

    showHoverBox(citation, event) {
        // Close existing hover box
        this.closeHoverBox();

        // Create hover box
        const hoverBox = this.createHoverBox(citation);
        
        // Position the hover box
        this.positionHoverBox(hoverBox, event);
        
        // Add to container
        const container = document.getElementById('citation-hover-container');
        container.appendChild(hoverBox);
        container.style.pointerEvents = 'auto';
        
        this.currentHoverBox = hoverBox;

        // Animate in
        setTimeout(() => {
            hoverBox.classList.add('citation-hover-visible');
        }, 10);
    }

    createHoverBox(citation) {
        const hoverBox = document.createElement('div');
        hoverBox.className = 'citation-hover-box';
        
        // Build citation content
        const content = this.buildCitationContent(citation);
        hoverBox.innerHTML = content;

        return hoverBox;
    }

    buildCitationContent(citation) {
        const authors = Array.isArray(citation.authors) ? citation.authors.join(', ') : citation.authors;
        const year = citation.year || 'Unknown year';
        const title = citation.title || 'Untitled';
        const description = citation.description || '';
        
        let publicationInfo = '';
        if (citation.journal) {
            publicationInfo = `<em>${citation.journal}</em>`;
            if (citation.volume) publicationInfo += `, ${citation.volume}`;
            if (citation.issue) publicationInfo += `(${citation.issue})`;
            if (citation.pages) publicationInfo += `, ${citation.pages}`;
        } else if (citation.publisher) {
            publicationInfo = citation.publisher;
        }

        let accessLinks = '';
        const links = [];
        
        if (citation.doi) {
            links.push(`<a href="https://doi.org/${citation.doi}" target="_blank" rel="noopener">DOI</a>`);
        }
        
        if (citation.url) {
            links.push(`<a href="${citation.url}" target="_blank" rel="noopener">View Source</a>`);
        }

        if (citation.retailers) {
            if (citation.retailers.bookshop_org?.url) {
                links.push(`<a href="${citation.retailers.bookshop_org.url}" target="_blank" rel="noopener">Bookshop.org</a>`);
            }
            if (citation.retailers.amazon?.asin) {
                const amazonUrl = `https://amazon.com/dp/${citation.retailers.amazon.asin}`;
                links.push(`<a href="${amazonUrl}" target="_blank" rel="noopener">Amazon</a>`);
            }
        }

        if (citation.free_sources) {
            Object.entries(citation.free_sources).forEach(([source, url]) => {
                const sourceName = source.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                links.push(`<a href="${url}" target="_blank" rel="noopener">${sourceName}</a>`);
            });
        }

        if (links.length > 0) {
            accessLinks = `<div class="citation-access-links">
                <strong>Access:</strong> ${links.join(' • ')}
            </div>`;
        }

        const citationDataLink = `citations.json#${citation.id}`;

        return `
            <div class="citation-header">
                <h3 class="citation-title">${title}</h3>
                <div class="citation-authors">${authors} (${year})</div>
                <button class="citation-close" aria-label="Close citation">&times;</button>
            </div>
            
            ${publicationInfo ? `<div class="citation-publication">${publicationInfo}</div>` : ''}
            
            ${description ? `<div class="citation-description">${description}</div>` : ''}
            
            ${accessLinks}
            
            <div class="citation-footer">
                <a href="${citationDataLink}" target="_blank" class="citation-data-link">View Citation Data</a>
            </div>
        `;
    }

    positionHoverBox(hoverBox, event) {
        const container = document.getElementById('citation-hover-container');
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;
        
        // Initial positioning to measure dimensions
        hoverBox.style.cssText = `
            position: absolute;
            visibility: hidden;
            max-width: min(500px, 90vw);
            width: max-content;
        `;
        container.appendChild(hoverBox);
        
        const rect = hoverBox.getBoundingClientRect();
        const boxWidth = rect.width;
        const boxHeight = rect.height;
        
        // Calculate position
        let left = event.clientX + 10;
        let top = event.clientY + 10;
        
        // Adjust if box would go off screen
        if (left + boxWidth > viewportWidth - 20) {
            left = event.clientX - boxWidth - 10;
        }
        
        if (top + boxHeight > viewportHeight - 20) {
            top = event.clientY - boxHeight - 10;
        }
        
        // Ensure minimum margins
        left = Math.max(10, Math.min(left, viewportWidth - boxWidth - 10));
        top = Math.max(10, Math.min(top, viewportHeight - boxHeight - 10));
        
        // Apply final positioning
        hoverBox.style.cssText = `
            position: absolute;
            left: ${left}px;
            top: ${top}px;
            max-width: min(500px, 90vw);
            visibility: visible;
        `;
        
        // Remove from container temporarily (will be re-added by caller)
        container.removeChild(hoverBox);
    }

    closeHoverBox() {
        if (this.currentHoverBox) {
            this.currentHoverBox.classList.remove('citation-hover-visible');
            
            setTimeout(() => {
                const container = document.getElementById('citation-hover-container');
                if (container && this.currentHoverBox) {
                    container.removeChild(this.currentHoverBox);
                    container.style.pointerEvents = 'none';
                }
                this.currentHoverBox = null;
            }, 200);
        }
    }
}

// Initialize when DOM is ready
console.log('Citations.js loaded, document ready state:', document.readyState);

if (document.readyState === 'loading') {
    console.log('Document still loading, adding DOMContentLoaded listener');
    document.addEventListener('DOMContentLoaded', () => {
        console.log('DOMContentLoaded fired, initializing CitationManager');
        new CitationManager();
    });
} else {
    console.log('Document already ready, initializing CitationManager immediately');
    new CitationManager();
}

// Handle close button clicks
document.addEventListener('click', (event) => {
    if (event.target.classList.contains('citation-close')) {
        const hoverBox = event.target.closest('.citation-hover-box');
        if (hoverBox) {
            hoverBox.classList.remove('citation-hover-visible');
            setTimeout(() => {
                const container = document.getElementById('citation-hover-container');
                if (container && hoverBox.parentNode === container) {
                    container.removeChild(hoverBox);
                    container.style.pointerEvents = 'none';
                }
            }, 200);
        }
    }
});
