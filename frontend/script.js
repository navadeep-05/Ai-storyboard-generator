async function generateStoryboard() {
    const script = document.getElementById("script").value;
    const storyboardDiv = document.getElementById("storyboard");
    storyboardDiv.innerHTML = "Generating...";

    try {
        const response = await fetch("https://ai-storyboard-generator.onrender.com", {
            method: "POST",
            body: JSON.stringify({ script }),
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) throw new Error("Backend error");

        const data = await response.json();
        storyboardDiv.innerHTML = data.images.map((url, i) => 
            `<img src="${url}" alt="Scene ${i+1}">`
        ).join("");
    } catch (error) {
        storyboardDiv.innerHTML = `Error: ${error.message}`;
    }
}
