// Tab switching
function openTab(evt, tabName) {
    // Hide all tab contents
    const tabContents = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove("active");
    }
    
    // Remove active class from all tab buttons
    const tabButtons = document.getElementsByClassName("tab-btn");
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove("active");
    }
    
    // Show the current tab and add active class to the button
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

// Task completion
function completeTask(button) {
    const taskCard = button.closest('.task-card');
    const taskName = taskCard.querySelector('h4').textContent;
    
    // Update counters
    const completedElem = document.getElementById('completed');
    const totalTasksElem = document.getElementById('total-tasks');
    const highPriorityElem = document.getElementById('high-priority');
    
    let completed = parseInt(completedElem.textContent);
    let totalTasks = parseInt(totalTasksElem.textContent);
    let highPriority = parseInt(highPriorityElem.textContent);
    
    completedElem.textContent = completed + 1;
    
    // Remove from high priority if needed
    if (taskCard.classList.contains('task-high')) {
        highPriorityElem.textContent = highPriority - 1;
    }
    
    // Visual feedback
    taskCard.style.opacity = '0.6';
    taskCard.style.textDecoration = 'line-through';
    button.disabled = true;
    button.textContent = '✅ تکمیل شده';
    
    // Show success message
    showNotification(`کار "${taskName}" تکمیل شد!`, 'success');
}

// Add new task
function addTask() {
    const title = document.getElementById('task-title').value;
    const course = document.getElementById('task-course').value;
    const deadline = document.getElementById('task-deadline').value;
    const time = document.getElementById('task-time').value;
    
    if (!title || !course) {
        showNotification('لطفا عنوان و درس را وارد کنید', 'error');
        return;
    }
    
    // Calculate priority (simplified)
    const priority = calculatePriority(time, deadline);
    
    // Update counters
    const totalTasksElem = document.getElementById('total-tasks');
    const highPriorityElem = document.getElementById('high-priority');
    const activeCoursesElem = document.getElementById('active-courses');
    
    let totalTasks = parseInt(totalTasksElem.textContent);
    let highPriority = parseInt(highPriorityElem.textContent);
    let activeCourses = parseInt(activeCoursesElem.textContent);
    
    totalTasksElem.textContent = totalTasks + 1;
    
    if (priority >= 7) {
        highPriorityElem.textContent = highPriority + 1;
    }
    
    // Show success message
    showNotification(`کار "${title}" با موفقیت اضافه شد! اولویت: ${priority}`, 'success');
    
    // Reset form
    document.getElementById('task-form').reset();
    document.getElementById('time-value').textContent = '۲ ساعت';
    document.getElementById('preview-details').textContent = 'اطلاعات کار را وارد کنید';
    document.getElementById('priority-display').textContent = 'اولویت: --';
    
    // Update preview
    updatePreview();
}

// Calculate task priority
function calculatePriority(time, deadline) {
    let score = 0;
    
    // Based on time
    if (time >= 5) score += 3;
    else if (time >= 3) score += 2;
    else score += 1;
    
    // Based on deadline (simplified)
    const today = new Date();
    const deadlineDate = new Date(deadline);
    const daysLeft = Math.ceil((deadlineDate - today) / (1000 * 60 * 60 * 24));
    
    if (daysLeft <= 1) score += 7;
    else if (daysLeft <= 3) score += 5;
    else if (daysLeft <= 7) score += 3;
    else score += 1;
    
    // Random factor for demo
    score += Math.random() * 2;
    
    return Math.min(Math.round(score * 10) / 10, 10);
}

// Update time value display
document.getElementById('task-time').addEventListener('input', function() {
    document.getElementById('time-value').textContent = this.value + ' ساعت';
    updatePreview();
});

// Update deadline display
document.getElementById('task-deadline').addEventListener('change', updatePreview);

// Update form inputs
document.getElementById('task-title').addEventListener('input', updatePreview);
document.getElementById('task-course').addEventListener('input', updatePreview);

// Update preview card
function updatePreview() {
    const title = document.getElementById('task-title').value;
    const course = document.getElementById('task-course').value;
    const deadline = document.getElementById('task-deadline').value;
    const time = document.getElementById('task-time').value;
    
    if (title && course && deadline) {
        const priority = calculatePriority(time, deadline);
        
        document.getElementById('preview-details').innerHTML = `
            <strong>عنوان:</strong> ${title}<br>
            <strong>درس:</strong> ${course}<br>
            <strong>مهلت:</strong> ${formatDate(deadline)}<br>
            <strong>زمان تخمینی:</strong> ${time} ساعت
        `;
        
        document.getElementById('priority-display').textContent = `اولویت: ${priority}`;
        
        // Color based on priority
        const priorityDisplay = document.getElementById('priority-display');
        priorityDisplay.style.background = priority >= 7 ? '#E17055' : 
                                         priority >= 4 ? '#00CEC9' : '#00B894';
    }
}

// Format date to Persian
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('fa-IR', options);
}

// Generate new schedule
function generateSchedule() {
    showNotification('برنامه روزانه جدید تولید شد!', 'success');
    
    // Animate schedule items
    const timeSlots = document.querySelectorAll('.time-slot');
    timeSlots.forEach((slot, index) => {
        slot.style.animation = 'none';
        setTimeout(() => {
            slot.style.animation = 'pulse 0.5s';
        }, index * 100);
    });
}

// Show notification
function showNotification(message, type) {
    // Remove existing notification
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'}"></i>
        ${message}
    `;
    
    // Style notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        left: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#00B894' : '#E17055'};
        color: white;
        border-radius: 10px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: slideIn 0.3s ease-out;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 3000);
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Set minimum date for deadline
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('task-deadline').min = today;
    
    // Set default deadline to tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    document.getElementById('task-deadline').value = tomorrow.toISOString().split('T')[0];
    
    // Initialize preview
    updatePreview();
    
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(-100%); opacity: 0; }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        
        .notification {
            font-family: 'Vazirmatn', sans-serif;
        }
    `;
    document.head.appendChild(style);
});
