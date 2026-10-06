document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultContainer = document.getElementById('result-container');
    const downloadBtn = document.getElementById('download-btn');

    // Navigation Logic
    const navLinks = document.querySelectorAll('#top-nav-links .nav-link[data-target]');
    const views = document.querySelectorAll('.view-section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(nav => nav.classList.remove('active'));
            
            // Add active class to clicked link
            link.classList.add('active');
            
            // Hide all views
            views.forEach(view => view.classList.add('hidden-view'));
            
            // Show targeted view
            const targetId = link.getAttribute('data-target');
            document.getElementById(targetId).classList.remove('hidden-view');
        });
    });

    let currentFile = null;

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropArea.classList.add('dragover');
    }

    function unhighlight(e) {
        dropArea.classList.remove('dragover');
    }

    // Handle dropped files
    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            currentFile = files[0];
            
            if (!currentFile.type.startsWith('image/') && !currentFile.type.startsWith('video/')) {
                alert('Please upload an image or video file.');
                currentFile = null;
                return;
            }

            fileInfo.textContent = currentFile.name;
            analyzeBtn.disabled = false;
        }
    }

    // Handle Analysis
    analyzeBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        // UI Loading state
        analyzeBtn.disabled = true;
        const originalBtnText = analyzeBtn.textContent;
        analyzeBtn.textContent = 'ANALYZING...';
        
        resultContainer.innerHTML = `
            <div class="loader-container">
                <div class="spinner-ring"></div>
                <span style="margin-top: 10px; display: block;">PROCESSING MODEL</span>
            </div>
        `;
        downloadBtn.classList.add('hidden');

        const formData = new FormData();
        formData.append('file', currentFile);

        const endpoint = currentFile.type.startsWith('image/') ? '/api/detect/image' : '/api/detect/video';

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Analysis failed');
            }

            const data = await response.json();
            displayResult(data.url, data.type);

        } catch (error) {
            console.error(error);
            resultContainer.innerHTML = `<div class="placeholder-content" style="color: #ef4444;">ERROR: ${error.message.toUpperCase()}</div>`;
        } finally {
            // Restore UI state
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = originalBtnText;
        }
    });

    function displayResult(url, type) {
        resultContainer.innerHTML = ''; 

        let mediaElement;
        
        if (type === 'image') {
            mediaElement = document.createElement('img');
            mediaElement.src = url;
            mediaElement.className = 'result-media';
            mediaElement.alt = 'Detection Result';
        } else if (type === 'video') {
            mediaElement = document.createElement('video');
            mediaElement.src = url;
            mediaElement.className = 'result-media';
            mediaElement.controls = true;
            mediaElement.autoplay = true;
            mediaElement.muted = true;
        }

        resultContainer.appendChild(mediaElement);

        downloadBtn.href = url;
        downloadBtn.download = `detected_${currentFile.name}`;
        downloadBtn.classList.remove('hidden');
    }
});

// Modal Logic
window.toggleAboutModal = function(e) {
    if (e) e.preventDefault();
    const modal = document.getElementById('about-modal');
    modal.classList.toggle('hidden');
}

window.closeAboutModal = function(e) {
    if (e) e.preventDefault();
    const modal = document.getElementById('about-modal');
    modal.classList.add('hidden');
}
