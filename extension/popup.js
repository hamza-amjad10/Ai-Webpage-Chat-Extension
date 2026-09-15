let send_button = document.getElementById("send_btn");
let user_input = document.getElementById("input_value");

function addMessage(text, sender) {
    let messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.classList.add(sender === "user" ? "user-message" : "ai-message");
    messageDiv.textContent = text;

    let messagesContainer = document.getElementById("messages_container");
    messagesContainer.appendChild(messageDiv);

    return messageDiv;  
}

user_input.addEventListener("keypress",(e)=>{
    if(e.key ==="Enter"){
        send_button.click();
    }
});

send_button.addEventListener("click", async () => {
    let question = user_input.value;
    addMessage(question, "user");
    user_input.value = "";

    let tabs = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    let loadingDiv = addMessage("Thinking...", "ai");  

    let response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            url: tabs[0].url,
            question: question
        })
    });

    let data = await response.json();
    loadingDiv.textContent = data.answer;  
});



