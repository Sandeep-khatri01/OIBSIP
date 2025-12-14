// Dark Mode Toggle Functionality
document.addEventListener('DOMContentLoaded', () => {
    // Check for saved theme preference or default to light mode
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);

    // Update toggle switch state
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.checked = currentTheme === 'dark';

        // Add event listener for theme toggle
        themeToggle.addEventListener('change', function () {
            const theme = this.checked ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
        });
    }

    // Add smooth fade-in animation for messages
    const observeMessages = () => {
        const messageContainer = document.querySelector('.messages');
        if (!messageContainer) return;

        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1 && node.classList.contains('message')) {
                        node.style.animation = 'fadeIn 0.3s ease-in';
                    }
                });
            });
        });

        observer.observe(messageContainer, { childList: true });
    };

    // Smooth scroll to bottom when new messages arrive
    const scrollToBottom = () => {
        const messageContainer = document.querySelector('.messages');
        if (messageContainer) {
            messageContainer.scrollTop = messageContainer.scrollHeight;
        }
    };

    // Initialize
    observeMessages();
    scrollToBottom();

    // Scroll to bottom when page loads
    window.addEventListener('load', scrollToBottom);
});
