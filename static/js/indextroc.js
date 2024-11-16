function acceptTrade(messageElement) {
    console.log("troc accepté");
    alert("Troc accepté !");
    messageElement.style.display = "none"; // Cache le message
    messageElement.status = "accepté";
}

function declineTrade(messageElement) {
    console.log("troc refusé");
    alert("Troc refusé !");
    messageElement.style.display = "none"; // Cache le message
    messageElement.status = "refusé";
}
