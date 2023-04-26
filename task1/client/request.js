async function getBotResponse(message) {
  if (message.trim() === "") {
    return;
  }
  const requestData = { "message": message };
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json"},
    body: JSON.stringify(requestData)
  };
  try {
    const response = await fetch("http://127.0.0.1:5000/chatbot", requestOptions);
    const data = await response.json();
    const botMessage = data["bot-message"];
    return botMessage;
  } catch (error) {
    console.log(error);
  }
}
