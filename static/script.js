document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const promptInput = document.getElementById('prompt-input');
    const imageGallery = document.getElementById('image-gallery');

    if (!generateBtn || !promptInput || !imageGallery) {
        console.error('One or more elements not found. Check your HTML.');
        return;
    }

    generateBtn.addEventListener('click', async () => {
        const prompt = promptInput.value;
        if (!prompt) {
            alert('Please enter a prompt');
            return;
        }

        console.log('Sending prompt:', prompt);

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt })
            });

            if (!response.ok) {
                throw new Error('Failed to generate image');
            }

            const blob = await response.blob();
            const imgUrl = URL.createObjectURL(blob);

            console.log('Image generated successfully:', imgUrl);

            const img = document.createElement('img');
            img.src = imgUrl;
            img.alt = 'Generated Image';
            imageGallery.appendChild(img);
        } catch (error) {
            console.error('Error:', error);
            alert('Error generating image: ' + error.message);
        }
    });
});
