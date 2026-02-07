// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Helper function to make API requests
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const requestOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, requestOptions);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Ticket API functions

/**
 * Get all tickets with optional filters
 * @param {Object} filters - Filter parameters (status, category, priority, search, etc.)
 * @returns {Promise<Array>} Array of tickets
 */
async function getTickets(filters = {}) {
    // Build query string from filters
    const queryParams = new URLSearchParams();
    
    Object.keys(filters).forEach(key => {
        if (filters[key]) {
            queryParams.append(key, filters[key]);
        }
    });
    
    const queryString = queryParams.toString();
    const endpoint = queryString ? `/tickets?${queryString}` : '/tickets';
    
    const result = await apiRequest(endpoint);
    return result.tickets || [];
}

/**
 * Get a specific ticket by ID
 * @param {number} ticketId - Ticket ID
 * @returns {Promise<Object>} Ticket object with comments
 */
async function getTicketById(ticketId) {
    return await apiRequest(`/tickets/${ticketId}`);
}

/**
 * Create a new ticket
 * @param {Object} ticketData - Ticket data
 * @returns {Promise<Object>} Created ticket
 */
async function createTicket(ticketData) {
    return await apiRequest('/tickets', {
        method: 'POST',
        body: JSON.stringify(ticketData),
    });
}

/**
 * Update an existing ticket
 * @param {number} ticketId - Ticket ID
 * @param {Object} updateData - Data to update
 * @returns {Promise<Object>} Updated ticket
 */
async function updateTicket(ticketId, updateData) {
    return await apiRequest(`/tickets/${ticketId}`, {
        method: 'PUT',
        body: JSON.stringify(updateData),
    });
}

/**
 * Delete a ticket
 * @param {number} ticketId - Ticket ID
 * @returns {Promise<Object>} Success message
 */
async function deleteTicket(ticketId) {
    return await apiRequest(`/tickets/${ticketId}`, {
        method: 'DELETE',
    });
}

// Comment API functions

/**
 * Get all comments for a ticket
 * @param {number} ticketId - Ticket ID
 * @returns {Promise<Array>} Array of comments
 */
async function getComments(ticketId) {
    const result = await apiRequest(`/tickets/${ticketId}/comments`);
    return result.comments || [];
}

/**
 * Add a comment to a ticket
 * @param {number} ticketId - Ticket ID
 * @param {Object} commentData - Comment data (author, comment_text)
 * @returns {Promise<Object>} Created comment
 */
async function addComment(ticketId, commentData) {
    return await apiRequest(`/tickets/${ticketId}/comments`, {
        method: 'POST',
        body: JSON.stringify(commentData),
    });
}

// Stats API function

/**
 * Get ticket statistics
 * @returns {Promise<Object>} Statistics object
 */
async function getStats() {
    const result = await apiRequest('/stats');
    return result.stats || {};
}

// Utility functions

/**
 * Format date to readable string
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (days === 0) {
        return 'Today at ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    } else if (days === 1) {
        return 'Yesterday at ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    } else if (days < 7) {
        return `${days} days ago`;
    } else {
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    }
}

/**
 * Get priority color class
 * @param {string} priority - Priority level
 * @returns {string} CSS class name
 */
function getPriorityClass(priority) {
    const priorityMap = {
        'Low': 'badge-priority-low',
        'Medium': 'badge-priority-medium',
        'High': 'badge-priority-high',
        'Urgent': 'badge-priority-urgent'
    };
    return priorityMap[priority] || 'badge-priority-medium';
}

/**
 * Get status color class
 * @param {string} status - Status
 * @returns {string} CSS class name
 */
function getStatusClass(status) {
    const statusMap = {
        'Open': 'badge-status-open',
        'In Progress': 'badge-status-in-progress',
        'Resolved': 'badge-status-resolved',
        'Closed': 'badge-status-closed'
    };
    return statusMap[status] || 'badge-status-open';
}

/**
 * Escape HTML to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Show notification message
 * @param {string} message - Message to display
 * @param {string} type - Message type (success, error, info)
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add to body
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

/**
 * Debounce function for search inputs
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait = 300) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getTickets,
        getTicketById,
        createTicket,
        updateTicket,
        deleteTicket,
        getComments,
        addComment,
        getStats,
        formatDate,
        getPriorityClass,
        getStatusClass,
        escapeHtml,
        showNotification,
        debounce
    };
}
