/**
 * Insurance AI Agent - Main JavaScript
 * Handles all frontend functionality for the Insurance AI Agent
 */

// ========================================
// Global Variables
// ========================================
let chatSessionId = null;
let currentAnalysis = null;
let uploadedImage = null;

// ========================================
// DOM Ready
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initUploadArea();
    initChat();
    initTransparencySection();
    initModal();
    initSmoothScroll();
});

// ========================================
// Navigation
// ========================================
function initNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Mobile menu toggle
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }
    
    // Close menu on link click
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            
            // Update active state
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });
    
    // Navbar background on scroll
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.boxShadow = '0 1px 2px 0 rgba(0, 0, 0, 0.05)';
        }
    });
}

// ========================================
// Smooth Scroll
// ========================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ========================================
// Upload Area
// ========================================
function initUploadArea() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('damageImage');
    const previewArea = document.getElementById('previewArea');
    const removeBtn = document.getElementById('removeImage');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const newAnalysisBtn = document.getElementById('newAnalysis');
    const saveClaimBtn = document.getElementById('saveClaim');
    
    if (!uploadArea || !fileInput) return;

    // 1. SILENCE THE HTML BUTTON: Find the button with the inline onclick and kill it
    const inlineBtn = uploadArea.querySelector('button[onclick]');
    if (inlineBtn) {
        inlineBtn.removeAttribute('onclick');
    }

    // 2. THE MASTER CLICK HANDLER
    uploadArea.addEventListener('click', (e) => {
        // Only trigger if the click didn't come directly from the input itself
        if (e.target !== fileInput) {
            fileInput.click();
        }
    });

    // 3. STOP BUBBLING: Prevent the input from telling the parent it was clicked
    fileInput.addEventListener('click', (e) => {
        e.stopPropagation();
    });

    // Drag and drop events
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
    
    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation(); 
        resetUpload();
    });
    
    if (analyzeBtn) analyzeBtn.addEventListener('click', analyzeDamage);
    if (newAnalysisBtn) newAnalysisBtn.addEventListener('click', resetUpload);
    if (saveClaimBtn) {
        saveClaimBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            document.getElementById('claimModal').style.display = 'flex';
        });
    }
}

function handleFileUpload(file) {
    if (!file.type.startsWith('image/')) {
        showToast('Please upload an image file', 'error');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
        showToast('File size should be less than 10MB', 'error');
        return;
    }
    
    uploadedImage = file;
    
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('previewImage').src = e.target.result;
        document.getElementById('uploadArea').style.display = 'none';
        document.getElementById('previewArea').style.display = 'block';
        document.getElementById('analysisResults').style.display = 'none';
    };
    reader.readAsDataURL(file);
}

function resetUpload() {
    uploadedImage = null;
    currentAnalysis = null;
    document.getElementById('damageImage').value = '';
    document.getElementById('uploadArea').style.display = 'block';
    document.getElementById('previewArea').style.display = 'none';
    document.getElementById('analysisResults').style.display = 'none';
    document.getElementById('loadingState').style.display = 'none';
}

async function analyzeDamage() {
    if (!uploadedImage) {
        showToast('Please upload an image first', 'error');
        return;
    }
    
    const previewArea = document.getElementById('previewArea');
    const loadingState = document.getElementById('loadingState');
    const analysisResults = document.getElementById('analysisResults');
    
    previewArea.style.display = 'none';
    loadingState.style.display = 'block';
    
    const formData = new FormData();
    formData.append('image', uploadedImage);
    
    try {
        const response = await fetch('/api/claims/analyze/', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentAnalysis = data;
            displayAnalysisResults(data);
            loadingState.style.display = 'none';
            analysisResults.style.display = 'block';
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
    } catch (error) {
        showToast(error.message, 'error');
        loadingState.style.display = 'none';
        previewArea.style.display = 'block';
    }
}

function displayAnalysisResults(data) {
    const { analysis, relevant_clauses, eligibility, repair_estimate, required_documents } = data;
    
    // Damage Detection
    const damageHtml = `
        <div class="damage-result">
            <div class="damage-icon">
                <i class="fas fa-car-crash"></i>
            </div>
            <div class="damage-info">
                <h4>${analysis.detected_damage}</h4>
                <div class="damage-meta">
                    <span class="severity">${formatSeverity(analysis.severity)}</span>
                    <span class="confidence">${analysis.confidence}% Confidence</span>
                </div>
            </div>
        </div>
    `;
    document.getElementById('damageDetection').innerHTML = damageHtml;
    
    // Eligibility
    const eligibilityClass = eligibility.eligible === true ? 'eligible' : 
                            eligibility.eligible === false ? 'not-eligible' : 'maybe';
    const eligibilityIcon = eligibility.eligible === true ? 'fa-check-circle' : 
                           eligibility.eligible === false ? 'fa-times-circle' : 'fa-question-circle';
    const eligibilityText = eligibility.eligible === true ? 'Likely Covered' : 
                           eligibility.eligible === false ? 'Not Covered' : 'Review Needed';
    
    const eligibilityHtml = `
        <div class="eligibility-result">
            <div class="eligibility-icon ${eligibilityClass}">
                <i class="fas ${eligibilityIcon}"></i>
            </div>
            <div class="eligibility-content">
                <h4 class="${eligibilityClass}">${eligibilityText}</h4>
                <p>${eligibility.reason}</p>
            </div>
        </div>
    `;
    document.getElementById('eligibilityResult').innerHTML = eligibilityHtml;
    
    // Policy Clauses
    const clausesHtml = relevant_clauses.map(clause => `
        <div class="clause-item">
            <h5>Clause ${clause.number}: ${clause.title}</h5>
            <p>${clause.description}</p>
        </div>
    `).join('');
    document.getElementById('policyClauses').innerHTML = `<div class="clauses-list">${clausesHtml}</div>`;
    
    // Repair Estimate
    const estimateHtml = `
        <div class="estimate-result">
            <div class="estimate-amount">${repair_estimate.currency} ${repair_estimate.estimated_cost.toLocaleString()}</div>
            <p class="estimate-note">${repair_estimate.note}</p>
        </div>
    `;
    document.getElementById('repairEstimate').innerHTML = estimateHtml;
    
    // Required Documents
    const documentsHtml = required_documents.map(doc => `
        <div class="document-item">
            <i class="fas fa-check-circle"></i>
            <span>${doc}</span>
        </div>
    `).join('');
    document.getElementById('requiredDocuments').innerHTML = `<div class="documents-list">${documentsHtml}</div>`;
}

function formatSeverity(severity) {
    return severity.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

// ========================================
// Chat Functionality
// ========================================
function initChat() {
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendMessage');
    const clearBtn = document.getElementById('clearChat');
    const chatMessages = document.getElementById('chatMessages');
    const suggestionBtns = document.querySelectorAll('.suggestion-btn');
    
    if (!chatInput) return;
    
    // Send message on button click
    sendBtn.addEventListener('click', sendMessage);
    
    // Send message on Enter key
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Clear chat
    clearBtn.addEventListener('click', clearChat);
    
    // Suggested questions
    suggestionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const question = btn.getAttribute('data-question');
            chatInput.value = question;
            sendMessage();
        });
    });
}

async function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Add user message
    addMessageToChat('user', message);
    chatInput.value = '';
    
    // Show typing indicator
    const typingIndicator = addTypingIndicator();
    
    try {
        const response = await fetch('/api/chat/message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: chatSessionId,
                message: message
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        typingIndicator.remove();
        
        if (data.success) {
            chatSessionId = data.session_id;
            addMessageToChat('bot', data.response);
        } else {
            throw new Error(data.error || 'Failed to get response');
        }
    } catch (error) {
        typingIndicator.remove();
        addMessageToChat('bot', 'Sorry, I encountered an error. Please try again later.');
        console.error('Chat error:', error);
    }
}

function addMessageToChat(type, content) {
    const chatMessages = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.innerHTML = `<i class="fas ${type === 'bot' ? 'fa-robot' : 'fa-user'}"></i>`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Convert newlines to HTML
    const formattedContent = content
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
    
    contentDiv.innerHTML = `<p>${formattedContent}</p>`;
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <p><i class="fas fa-spinner fa-spin"></i> Thinking...</p>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return typingDiv;
}

async function clearChat() {
    const chatMessages = document.getElementById('chatMessages');
    
    try {
        const response = await fetch('/api/chat/clear/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: chatSessionId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            chatSessionId = data.session_id;
            chatMessages.innerHTML = `
                <div class="message bot-message">
                    <div class="message-avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="message-content">
                        <p>Namaste! I'm your Insurance AI Assistant. I can help you with:</p>
                        <ul>
                            <li>Understanding claim processes</li>
                            <li>Required documents</li>
                            <li>Coverage details</li>
                            <li>Claim rejection reasons</li>
                            <li>Premium information</li>
                        </ul>
                        <p>What would you like to know?</p>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Clear chat error:', error);
    }
}

// ========================================
// Transparency Section
// ========================================
async function initTransparencySection() {
    const rejectionContainer = document.getElementById('rejectionReasons');
    
    if (!rejectionContainer) return;
    
    try {
        const response = await fetch('/api/claims/rejection-reasons/');
        const data = await response.json();
        
        if (data.rejection_reasons) {
            const icons = ['fa-file-alt', 'fa-clock', 'fa-folder-open', 'fa-history', 'fa-tools', 'fa-wine-glass'];
            
            const html = data.rejection_reasons.map((reason, index) => `
                <div class="rejection-card">
                    <div class="rejection-icon">
                        <i class="fas ${icons[index % icons.length]}"></i>
                    </div>
                    <div class="rejection-content">
                        <h4>${reason.reason}</h4>
                        <p>${reason.description}</p>
                    </div>
                    <div class="rejection-tip">
                        <span>How to Avoid</span>
                        <p>${reason.how_to_avoid}</p>
                    </div>
                </div>
            `).join('');
            
            rejectionContainer.innerHTML = html;
        }
    } catch (error) {
        console.error('Failed to load rejection reasons:', error);
    }
}

// ========================================
// Modal Functionality
// ========================================
function initModal() {
    const modal = document.getElementById('claimModal');
    const closeBtn = document.getElementById('closeModal');
    const cancelBtn = document.getElementById('cancelClaim');
    const submitBtn = document.getElementById('submitClaim');
    
    if (!modal) return;
    
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    cancelBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    submitBtn.addEventListener('click', submitClaim);
    
    // Close on outside click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
}

async function submitClaim() {
    const form = document.getElementById('claimForm');
    const formData = new FormData(form);
    
    // Validate required fields
    const requiredFields = ['full_name', 'email', 'phone', 'vehicle_number'];
    for (const field of requiredFields) {
        if (!formData.get(field)) {
            showToast('Please fill in all required fields', 'error');
            return;
        }
    }
    
    // Build claim data
    const claimData = {
        full_name: formData.get('full_name'),
        email: formData.get('email'),
        phone: formData.get('phone'),
        vehicle_type: formData.get('vehicle_type'),
        vehicle_number: formData.get('vehicle_number'),
        insurance_policy_number: formData.get('insurance_policy_number'),
        damage_description: formData.get('damage_description'),
    };
    
    // Add analysis data if available
    if (currentAnalysis) {
        claimData.detected_damage_type = currentAnalysis.analysis.detected_damage;
        claimData.damage_severity = currentAnalysis.analysis.severity;
        claimData.ai_analysis = currentAnalysis.analysis;
        claimData.matched_clauses = currentAnalysis.relevant_clauses;
        claimData.eligibility_reason = currentAnalysis.eligibility.reason;
        claimData.status = currentAnalysis.eligibility.eligible === true ? 'eligible' : 
                          currentAnalysis.eligibility.eligible === false ? 'not_eligible' : 'needs_info';
    }
    
    try {
        const response = await fetch('/api/claims/submit/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(claimData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast(`Claim #${data.claim_id} submitted successfully!`);
            document.getElementById('claimModal').style.display = 'none';
            form.reset();
        } else {
            throw new Error(data.error || 'Failed to submit claim');
        }
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// ========================================
// Toast Notification
// ========================================
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    
    toastMessage.textContent = message;
    
    // Update icon based on type
    const icon = toast.querySelector('i');
    icon.className = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle';
    toast.style.background = type === 'success' ? 'var(--success-color)' : 'var(--danger-color)';
    
    toast.style.display = 'flex';
    
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

// ========================================
// Utility Functions
// ========================================
function debounce(func, wait) {
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

function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Intersection Observer for animations
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, observerOptions);

// Observe elements with animation class
document.querySelectorAll('.problem-card, .feature-card, .tip-card').forEach(el => {
    observer.observe(el);
});
