let userWalletAddress = null;

const walletAddressEl = document.getElementById("walletAddress");
const containerEl = document.querySelector(".container");
const connectBtnEl = document.getElementById("connectBtn");
const promptEl = document.getElementById("prompt");
const outputEl = document.getElementById("output");

async function connectWallet() {
    if (!window.ethereum) {
        alert("MetaMask is not installed. Please install it to use this app.");
        return;
    }

    try {
        const accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
        userWalletAddress = accounts[0];
        walletAddressEl.textContent = `Connected: ${userWalletAddress}`;
        containerEl.style.display = "block";
        connectBtnEl.style.display = "none";
    } catch (error) {
        console.error("User denied account access", error);
        alert("MetaMask connection is required to use this feature.");
    }
}

async function generateContract() {
    if (!userWalletAddress) {
        alert("Please connect your MetaMask wallet first.");
        return;
    }

    const prompt = promptEl.value.trim();
    if (!prompt) {
        outputEl.textContent = "Please enter a prompt.";
        return;
    }

    outputEl.textContent = "⏳ Generating contract...";

    try {
        const response = await fetch("http://127.0.0.1:8001/create-and-execute", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                prompt,
                wallet_address: userWalletAddress
            })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        outputEl.textContent = data.contract_code 
            ? data.contract_code 
            : data.error 
                ? `Error: ${data.error}` 
                : "Unexpected response from server.";
    } catch (error) {
        outputEl.textContent = `Error contacting backend: ${error.message}`;
    }
}

// Modern event listeners
connectBtnEl.addEventListener("click", connectWallet);
document.getElementById("generateBtn").addEventListener("click", generateContract);