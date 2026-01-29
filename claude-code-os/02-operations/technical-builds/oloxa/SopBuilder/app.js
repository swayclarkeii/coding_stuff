/* ============================================
   SOP Builder - Application Logic
   ============================================ */

// Configuration
const CONFIG = {
    // Update this to your n8n webhook URL once the workflow is deployed
    webhookUrl: 'https://n8n.oloxa.ai/webhook/sop-builder',
    maxFileSize: 25 * 1024 * 1024, // 25MB
    allowedTypes: ['audio/mpeg', 'audio/mp4', 'audio/wav', 'audio/x-m4a', 'audio/m4a', 'video/mp4']
};

// State
let currentStep = 0;
const totalSteps = 5;
let selectedFile = null;
let inputMethod = 'text';

// Form data
const formData = {
    email: '',
    name: '',
    goal: '',
    improvement_type: '',
    department: '',
    end_user: '',
    process_steps: '',
    lead_id: ''
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeUploadZone();
    handleResubmitParams();
    updateProgress();
});

// Handle resubmit URL parameters (?lead=xxx&email=xxx&name=xxx&score=60&wins=[...])
function handleResubmitParams() {
    const params = new URLSearchParams(window.location.search);
    const leadId = params.get('lead');
    const email = params.get('email');
    const name = params.get('name');
    const score = params.get('score');
    const winsEncoded = params.get('wins');

    if (!leadId) return;

    formData.lead_id = leadId;

    // Parse quick wins
    let quickWins = [];
    if (winsEncoded) {
        try {
            quickWins = JSON.parse(decodeURIComponent(winsEncoded));
        } catch (e) {
            console.error('Failed to parse quick wins:', e);
        }
    }

    // Replace Step 0 content with welcome-back summary
    const stepContent = document.querySelector('#step-0 .step-content');

    // Build quick wins HTML
    let quickWinsHtml = '';
    for (let i = 0; i < Math.min(3, quickWins.length); i++) {
        const win = quickWins[i];
        quickWinsHtml += `
            <div style="margin: 12px 0; padding: 12px; background: #2a2a2a; border-radius: 6px; display: flex;">
                <div style="font-size: 24px; font-weight: bold; color: #d4af37; margin-right: 15px;">${i + 1}</div>
                <div>
                    <strong>${win.title || 'Quick Win'}</strong>
                    <p style="margin: 4px 0 0; color: #ccc; font-size: 14px;">${win.action || 'Action needed'}</p>
                </div>
            </div>
        `;
    }

    stepContent.innerHTML = `
        <h1>Welcome back, ${name || 'there'}! Here's where you're at:</h1>

        <div style="font-size: 64px; font-weight: bold; color: #F26B5D; text-align: center; margin: 30px 0;">${score || '0'}%</div>

        <div style="margin: 30px 0; padding: 25px; background: #1a1a1a; border-left: 4px solid #F26B5D; border-radius: 4px;">
            <h2 style="color: #F26B5D; font-size: 20px; margin-top: 0;">3 Quick Wins to Improve Your Score</h2>
            ${quickWinsHtml || '<p>Quick wins will be provided after analysis.</p>'}
        </div>

        <div class="btn-center">
            <button type="button" class="btn btn-primary btn-large" onclick="goToStep(3)">
                Update My SOP
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
            </button>
        </div>
    `;

    // Pre-fill email/name on step 4 when it loads
    if (email) {
        formData.email = email;
    }
    if (name) {
        formData.name = name;
    }

    // Set up pre-fill for when step 4 becomes active
    const observer = new MutationObserver(() => {
        const emailInput = document.getElementById('email');
        const nameInput = document.getElementById('name');
        if (emailInput && formData.email) {
            emailInput.value = formData.email;
            emailInput.readOnly = true;
            emailInput.style.opacity = '0.7';
        }
        if (nameInput && formData.name) {
            nameInput.value = formData.name;
            nameInput.readOnly = true;
            nameInput.style.opacity = '0.7';
        }
    });
    observer.observe(document.querySelector('.form-container'), { childList: true, subtree: true, attributes: true });
}

// Step Navigation
function nextStep() {
    if (!validateCurrentStep()) return;

    saveCurrentStepData();

    if (currentStep < totalSteps - 1) {
        goToStep(currentStep + 1);
    }
}

function prevStep() {
    if (currentStep > 0) {
        goToStep(currentStep - 1);
    }
}

function goToStep(step) {
    // Hide current step
    document.getElementById(`step-${currentStep}`).classList.remove('active');

    // Show new step
    currentStep = step;
    document.getElementById(`step-${currentStep}`).classList.add('active');

    updateProgress();
}

function updateProgress() {
    // Update progress bar
    const progress = (currentStep / (totalSteps - 1)) * 100;
    document.getElementById('progress-fill').style.width = `${progress}%`;

    // Update step dots
    document.querySelectorAll('.step-dot').forEach((dot, index) => {
        dot.classList.remove('active', 'completed');
        if (index === currentStep) {
            dot.classList.add('active');
        } else if (index < currentStep) {
            dot.classList.add('completed');
        }
    });
}

// Validation
function validateCurrentStep() {
    switch (currentStep) {
        case 0: // Landing page - no validation needed
            return true;

        case 1: // Goal
            const goal = document.getElementById('goal').value.trim();
            if (!goal || goal.length < 20) {
                shakeInput('goal');
                document.getElementById('goal').focus();
                return false;
            }
            return true;

        case 2: // Improvement type + department
            const selected = document.querySelector('input[name="improvement_type"]:checked');
            if (!selected) {
                document.querySelector('.option-cards').classList.add('shake');
                setTimeout(() => {
                    document.querySelector('.option-cards').classList.remove('shake');
                }, 500);
                return false;
            }
            const department = document.getElementById('department').value;
            if (!department) {
                shakeInput('department');
                document.getElementById('department').focus();
                return false;
            }
            return true;

        case 3: // Process steps
            if (inputMethod === 'text') {
                const steps = document.getElementById('process_steps').value.trim();
                if (!steps || steps.length < 50) {
                    shakeInput('process_steps');
                    document.getElementById('process_steps').focus();
                    return false;
                }
            } else {
                if (!selectedFile) {
                    document.getElementById('upload-zone').classList.add('shake');
                    setTimeout(() => {
                        document.getElementById('upload-zone').classList.remove('shake');
                    }, 500);
                    return false;
                }
            }
            return true;

        case 4: // Email capture
            const email = document.getElementById('email').value.trim();
            const name = document.getElementById('name').value.trim();

            if (!email || !isValidEmail(email)) {
                shakeInput('email');
                document.getElementById('email').focus();
                return false;
            }
            if (!name) {
                shakeInput('name');
                document.getElementById('name').focus();
                return false;
            }
            return true;

        default:
            return true;
    }
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function shakeInput(id) {
    const el = document.getElementById(id);
    el.classList.add('shake');
    setTimeout(() => el.classList.remove('shake'), 500);
}

// Save step data
function saveCurrentStepData() {
    switch (currentStep) {
        case 0: // Landing - nothing to save
            break;
        case 1:
            formData.goal = document.getElementById('goal').value.trim();
            break;
        case 2:
            const selected = document.querySelector('input[name="improvement_type"]:checked');
            formData.improvement_type = selected ? selected.value : '';
            formData.department = document.getElementById('department').value;
            formData.end_user = document.getElementById('end_user').value.trim();
            break;
        case 3:
            if (inputMethod === 'text') {
                formData.process_steps = document.getElementById('process_steps').value.trim();
            }
            break;
        case 4:
            formData.email = document.getElementById('email').value.trim();
            formData.name = document.getElementById('name').value.trim();
            break;
    }
}

// Input Method Toggle
function setInputMethod(method) {
    inputMethod = method;

    // Update toggle buttons
    document.querySelectorAll('.method-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.method === method);
    });

    // Show/hide input areas
    document.getElementById('text-input').classList.toggle('hidden', method !== 'text');
    document.getElementById('voice-input').classList.toggle('hidden', method !== 'voice');
}

// File Upload
function initializeUploadZone() {
    const uploadZone = document.getElementById('upload-zone');
    const fileInput = document.getElementById('audio-file');

    // Click to upload
    uploadZone.addEventListener('click', () => fileInput.click());

    // Drag and drop
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });
}

function handleFile(file) {
    // Validate file type
    const isValidType = CONFIG.allowedTypes.some(type =>
        file.type === type || file.name.match(/\.(mp3|m4a|wav|mp4)$/i)
    );

    if (!isValidType) {
        alert('Please upload an audio file (MP3, M4A, WAV, or MP4)');
        return;
    }

    // Validate file size
    if (file.size > CONFIG.maxFileSize) {
        alert('File is too large. Maximum size is 25MB.');
        return;
    }

    selectedFile = file;

    // Update UI
    document.getElementById('upload-zone').classList.add('hidden');
    document.getElementById('file-preview').classList.remove('hidden');
    document.getElementById('file-name').textContent = file.name;
}

function removeFile() {
    selectedFile = null;
    document.getElementById('audio-file').value = '';
    document.getElementById('upload-zone').classList.remove('hidden');
    document.getElementById('file-preview').classList.add('hidden');
}

// Form Submission
async function submitForm() {
    if (!validateCurrentStep()) return;
    saveCurrentStepData();

    const submitBtn = document.querySelector('.btn-submit');
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;

    try {
        // Prepare form data
        const payload = new FormData();
        payload.append('email', formData.email);
        payload.append('name', formData.name);
        payload.append('goal', formData.goal);
        payload.append('improvement_type', formData.improvement_type);
        payload.append('department', formData.department);
        payload.append('end_user', formData.end_user);
        if (formData.lead_id) {
            payload.append('lead_id', formData.lead_id);
        }

        if (inputMethod === 'text') {
            payload.append('process_steps', formData.process_steps);
            payload.append('input_method', 'text');
        } else if (selectedFile) {
            payload.append('audio_file', selectedFile);
            payload.append('input_method', 'voice');
        }

        // Submit to n8n webhook
        const response = await fetch(CONFIG.webhookUrl, {
            method: 'POST',
            body: payload
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        if (result.success) {
            showSuccess();
        } else {
            throw new Error(result.message || 'Something went wrong');
        }

    } catch (error) {
        console.error('Submission error:', error);
        showError(error.message);
    } finally {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
}

function showSuccess() {
    // Hide all steps
    document.querySelectorAll('.step').forEach(step => step.classList.remove('active'));

    // Show success
    document.getElementById('step-success').classList.add('active');

    // Hide progress
    document.querySelector('.progress-container').style.display = 'none';
}

function showError(message) {
    // Hide all steps
    document.querySelectorAll('.step').forEach(step => step.classList.remove('active'));

    // Show error
    document.getElementById('step-error').classList.add('active');
    document.getElementById('error-message').textContent = message || 'We couldn\'t process your request. Please try again.';

    // Hide progress
    document.querySelector('.progress-container').style.display = 'none';
}

function resetForm() {
    // Reset state
    currentStep = 0;
    selectedFile = null;
    inputMethod = 'text';

    // Reset form fields
    document.getElementById('email').value = '';
    document.getElementById('name').value = '';
    document.getElementById('goal').value = '';
    document.querySelectorAll('input[name="improvement_type"]').forEach(r => r.checked = false);
    document.getElementById('department').value = '';
    document.getElementById('end_user').value = '';
    document.getElementById('process_steps').value = '';

    // Reset UI
    removeFile();
    setInputMethod('text');
    document.querySelector('.progress-container').style.display = 'block';

    // Hide all steps, show first
    document.querySelectorAll('.step').forEach(step => step.classList.remove('active'));
    document.getElementById('step-0').classList.add('active');

    updateProgress();
}

// Add shake animation
const style = document.createElement('style');
style.textContent = `
    .shake {
        animation: shake 0.5s ease;
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-5px); }
        40%, 80% { transform: translateX(5px); }
    }
`;
document.head.appendChild(style);
