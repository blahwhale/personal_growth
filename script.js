// Update date
function updateDate() {
    const dateElement = document.querySelector('.date');
    const options = { 
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    const today = new Date();
    dateElement.textContent = today.toLocaleDateString('en-US', options).toUpperCase();
}

// Pomodoro Timer
class PomodoroTimer {
    constructor() {
        this.timeLeft = 25 * 60; // 25 minutes in seconds
        this.isRunning = false;
        this.pomodorosCompleted = 0;
        this.totalPomodoros = 4;
        this.timerInterval = null;
        this.mode = 'work';

        // DOM elements
        this.timeDisplay = document.querySelector('.time');
        this.playButton = document.querySelector('.play');
        this.pauseButton = document.querySelector('.pause');
        this.resetButton = document.querySelector('.reset');
        this.pomodoroCount = document.querySelector('.pomodoro-count span');
        
        // Mode buttons
        this.workButton = document.querySelector('.work');
        this.breakButton = document.querySelector('.break');
        this.longBreakButton = document.querySelector('.long-break');

        this.initializeEventListeners();
        this.updateDisplay();
    }

    initializeEventListeners() {
        this.playButton.addEventListener('click', () => this.start());
        this.pauseButton.addEventListener('click', () => this.pause());
        this.resetButton.addEventListener('click', () => this.reset());
        
        this.workButton.addEventListener('click', () => this.setMode('work', 25));
        this.breakButton.addEventListener('click', () => this.setMode('break', 5));
        this.longBreakButton.addEventListener('click', () => this.setMode('longBreak', 15));
    }

    setMode(mode, minutes) {
        this.mode = mode;
        this.timeLeft = minutes * 60;
        this.pause();
        this.updateDisplay();
    }

    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
    }

    updateDisplay() {
        this.timeDisplay.textContent = this.formatTime(this.timeLeft);
        this.pomodoroCount.textContent = `${this.pomodorosCompleted} / ${this.totalPomodoros}`;
    }

    start() {
        if (!this.isRunning) {
            this.isRunning = true;
            this.timerInterval = setInterval(() => {
                this.timeLeft--;
                this.updateDisplay();

                if (this.timeLeft <= 0) {
                    this.completePomodoro();
                }
            }, 1000);
        }
    }

    pause() {
        this.isRunning = false;
        clearInterval(this.timerInterval);
    }

    reset() {
        this.pause();
        this.timeLeft = 25 * 60;
        this.updateDisplay();
    }

    completePomodoro() {
        this.pause();
        if (this.mode === 'work') {
            this.pomodorosCompleted++;
            this.updateDisplay();
            
            // Play notification sound
            const audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');
            audio.play();
            
            // Show notification
            if (Notification.permission === 'granted') {
                new Notification('Pomodoro Complete!', {
                    body: 'Time for a break!',
                    icon: '🍅'
                });
            }
        }
        this.reset();
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateDate();
    const pomodoro = new PomodoroTimer();
    
    // Request notification permission
    if (Notification.permission !== 'granted') {
        Notification.requestPermission();
    }
});

// Update weather (mock data for now)
function updateWeather() {
    const weatherTemp = document.querySelector('.temp');
    const weatherCondition = document.querySelector('.condition');
    
    // In a real application, you would fetch this data from a weather API
    weatherTemp.textContent = '72°F';
    weatherCondition.textContent = 'Clear';
} 