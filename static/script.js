document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const navItems = document.querySelectorAll('.nav-item');
    const modeTitle = document.getElementById('current-mode-title');
    const statusText = document.getElementById('system-status');

    let currentMode = 'chat'; // chat, image, video

    // Mode Switching
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            currentMode = item.dataset.mode;
            
            // Update Title
            if(currentMode === 'chat') modeTitle.textContent = 'Conversational AI';
            else if(currentMode === 'image') modeTitle.textContent = 'Image Generation (Stable Diffusion)';
            else if(currentMode === 'video') modeTitle.textContent = 'Video Generation (ModelScope)';
        });
    });

    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Send Message
    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // Add User Message
        appendMessage('user', text);
        userInput.value = '';
        userInput.style.height = 'auto';
        sendBtn.disabled = true;

        statusText.textContent = `Generating ${currentMode}...`;
        const startTime = Date.now();

        try {
            let endpoint = '/chat';
            let body = { message: text };

            if (currentMode === 'image') {
                endpoint = '/generate_image';
                body = { prompt: text };
            } else if (currentMode === 'video') {
                endpoint = '/generate_video';
                body = { prompt: text };
            }

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });

            const data = await response.json();
            const duration = ((Date.now() - startTime) / 1000).toFixed(1);

            if (data.error) {
                appendMessage('system', `Error: ${data.error}`);
            } else {
                if (currentMode === 'chat') {
                    appendMessage('system', data.response);
                } else {
                    appendMedia('system', data.url, data.type);
                }
            }
            
            document.getElementById('processing-time').textContent = `Last generation: ${duration}s`;

        } catch (error) {
            appendMessage('system', `Network Error: ${error.message}`);
        } finally {
            sendBtn.disabled = false;
            statusText.textContent = 'System Ready';
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'content';
        content.innerHTML = `<p>${text}</p>`;
        
        msgDiv.appendChild(avatar);
        msgDiv.appendChild(content);
        chatContainer.appendChild(msgDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function appendMedia(sender, url, type) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.innerHTML = '<i class="fa-solid fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'content';
        
        if (type === 'image') {
            content.innerHTML = `<p>Generated Image:</p><img src="${url}" alt="Generated Image">`;
        } else {
            content.innerHTML = `<p>Generated Video:</p><video controls src="${url}"></video>`;
        }
        
        msgDiv.appendChild(avatar);
        msgDiv.appendChild(content);
        chatContainer.appendChild(msgDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});
