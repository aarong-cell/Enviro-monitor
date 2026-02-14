// Global state
let allBids = [];
let filteredBids = [];

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadBids();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Search
    document.getElementById('search-input').addEventListener('input', (e) => {
        filterBids();
    });

    // Type filter
    document.getElementById('filter-type').addEventListener('change', () => {
        filterBids();
    });

    // Refresh button
    document.getElementById('btn-refresh').addEventListener('click', () => {
        refreshBids();
    });

    // Export button
    document.getElementById('btn-export').addEventListener('click', () => {
        exportToCSV();
    });
}

// Load bids from API
async function loadBids() {
    try {
        const response = await fetch('/api/bids');
        const data = await response.json();

        if (data.success) {
            allBids = data.bids;
            filteredBids = allBids;
            updateStats(data);
            renderBids();
        }
    } catch (error) {
        console.error('Error loading bids:', error);
        document.getElementById('bids-container').innerHTML = 
            '<div class="no-results">❌ Error loading bids. Please try again.</div>';
    }
}

// Update statistics
function updateStats(data) {
    document.getElementById('total-bids').textContent = data.count || 0;
    
    const municipal = data.bids.filter(b => b.type === 'Municipal').length;
    const county = data.bids.filter(b => b.type === 'County').length;
    const state = data.bids.filter(b => b.type === 'State').length;
    
    document.getElementById('municipal-bids').textContent = municipal;
    document.getElementById('county-bids').textContent = county;
    document.getElementById('state-bids').textContent = state;
    
    if (data.last_update) {
        const date = new Date(data.last_update);
        document.getElementById('last-update').textContent = date.toLocaleString();
    }
}

// Filter bids
function filterBids() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const typeFilter = document.getElementById('filter-type').value;

    filteredBids = allBids.filter(bid => {
        // Type filter
        if (typeFilter !== 'all' && bid.type !== typeFilter) {
            return false;
        }

        // Search filter
        if (searchTerm) {
            const searchableText = `
                ${bid.title || ''} 
                ${bid.description || ''} 
                ${bid.location || ''} 
                ${bid.bid_number || ''}
            `.toLowerCase();
            
            if (!searchableText.includes(searchTerm)) {
                return false;
            }
        }

        return true;
    });

    renderBids();
}

// Render bids
function renderBids() {
    const container = document.getElementById('bids-container');

    if (filteredBids.length === 0) {
        container.innerHTML = '<div class="no-results">No bids found matching your criteria.</div>';
        return;
    }

    container.innerHTML = filteredBids.map(bid => `
        <div class="bid-card">
            <div class="bid-header">
                <div class="bid-title">${bid.title}</div>
            </div>
            
            <div class="bid-badges">
                <span class="badge badge-${bid.type.toLowerCase()}">${bid.type}</span>
                <span class="badge badge-location">📍 ${bid.location}</span>
                ${bid.deadline ? `<span class="badge badge-deadline">⏰ Due: ${formatDate(bid.deadline)}</span>` : ''}
                ${bid.bid_number ? `<span class="badge">🔢 ${bid.bid_number}</span>` : ''}
            </div>

            ${bid.description ? `
                <div class="bid-description">
                    ${bid.description}
                </div>
            ` : ''}

            <div class="bid-meta">
                <div class="bid-meta-item">
                    <strong>📅 Posted:</strong> ${formatDate(bid.posted_date)}
                </div>
            </div>

            <div class="bid-footer">
                <div class="bid-source">
                    <strong>Source:</strong> ${bid.source}
                </div>
                <a href="${bid.url}" target="_blank" class="btn-view">
                    View Opportunity →
                </a>
            </div>
        </div>
    `).join('');
}

// Format date
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

// Refresh bids
async function refreshBids() {
    const btn = document.getElementById('btn-refresh');
    btn.textContent = '⏳ Refreshing...';
    btn.disabled = true;

    try {
        const response = await fetch('/api/refresh', { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            await loadBids();
            btn.textContent = '✅ Refreshed!';
            setTimeout(() => {
                btn.textContent = '🔄 Refresh';
                btn.disabled = false;
            }, 2000);
        }
    } catch (error) {
        console.error('Error refreshing:', error);
        btn.textContent = '❌ Error';
        setTimeout(() => {
            btn.textContent = '🔄 Refresh';
            btn.disabled = false;
        }, 2000);
    }
}

// Export to CSV
function exportToCSV() {
    if (filteredBids.length === 0) {
        alert('No bids to export');
        return;
    }

    const headers = ['Title', 'Type', 'Location', 'Source', 'Posted Date', 'Deadline', 'Bid Number', 'URL', 'Description'];
    
    const csvContent = [
        headers.join(','),
        ...filteredBids.map(bid => [
            `"${(bid.title || '').replace(/"/g, '""')}"`,
            bid.type || '',
            `"${(bid.location || '').replace(/"/g, '""')}"`,
            `"${(bid.source || '').replace(/"/g, '""')}"`,
            bid.posted_date || '',
            bid.deadline || '',
            bid.bid_number || '',
            bid.url || '',
            `"${(bid.description || '').replace(/"/g, '""')}"`
        ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `bids_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}
