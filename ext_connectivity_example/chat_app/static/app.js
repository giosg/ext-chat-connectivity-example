const STATE = {
  lastChatListUpdate: new Date(),
  lastMessageUpdate: new Date(),
  currentChatId: undefined,
};

/**
 * Super simple vanillajs app to poll api's and show results in html page.
 */
const startApp = () => {
  setupClickHandlers();
  refreshChatList(true);
  setInterval(refreshChatList, 500);
};

const setupClickHandlers = () => {
  // Start chat button, creates new visitor and chat
  const startBtn = document.getElementById("start-chat");
  startBtn.addEventListener("click", async () => {
    const visitorNameEl = document.getElementById("visitor-name");
    const chatResponse = await fetch("/api/chats/", {
      method: "POST",
      body: JSON.stringify({
        visitor_name: visitorNameEl.value,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    visitorNameEl.value = "";
    const createdChat = await chatResponse.json();
    console.log("Created chat", createdChat);
    setTimeout(() => {
      refreshChatList(true);
    }, 1000);
  });

  // Send button, sends a chat message.
  const sendButton = document.getElementById("send-message");
  sendButton.addEventListener("click", async () => {
    const messageEl = document.getElementById("message");
    const response = await fetch(
      `/api/chats/${STATE.currentChatId}/messages/`,
      {
        method: "POST",
        body: JSON.stringify({
          message: messageEl.value,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    messageEl.value = "";
    const createdMsg = await response.json();
    console.log(createdMsg);
    await refreshMessageList(true);
  });

  const backButton = document.getElementById("back");
  backButton.addEventListener("click", async () => {
    window.location.reload();
  });
};

const refreshChatList = async (force) => {
  if (force || new Date() - STATE.lastChatListUpdate > 1000) {
    console.log("fetching chats..");
    const response = await fetch("/api/chats");
    const chatList = await response.json();
    console.log(chatList);

    const chatListEl = document.getElementById("chat-list");
    chatListEl.innerHTML = "";
    chatList.forEach((chat) => {
      const chatRow = document.createElement("a");
      chatRow.href = "#";
      chatRow.className = "list-group-item list-group-item-action";
      chatRow.innerText = `Chat of "${chat.visitor_name}"`;
      chatListEl.appendChild(chatRow);
      chatRow.addEventListener("click", async () => {
        showChat(chat.id);
      });
    });
    STATE.lastChatListUpdate = new Date();
  }
};

const refreshVisitorList = async () => {
  console.log("fetching visitors..");
  const response = await fetch("/api/visitors");
  const visitorList = await response.json();
  console.log(visitorList);

  const visitorListEl = document.getElementById("visitor-list");
  visitorListEl.innerHTML = "";
  visitorList.forEach((chat) => {
    const row = document.createElement("a");
    row.href = "#";
    row.className = "list-group-item list-group-item-action";
    row.innerText = `"${chat.visitor_name}"`;
    visitorListEl.appendChild(row);
    row.addEventListener("click", async () => {
      showChat(chat.id);
    });
  });
};

const showChat = async (chatId) => {
  STATE.currentChatId = chatId;
  const conversations = document.getElementById("conversation-list");
  conversations.style.display = "none";
  const chatHistory = document.getElementById("chat-history");
  chatHistory.style.display = "block";
  await refreshMessageList(true);
  setInterval(refreshMessageList, 500);
};

const refreshMessageList = async (force) => {
  if (force || new Date() - STATE.lastMessageUpdate > 1000) {
    console.log("fetching messages..");
    const response = await fetch(`/api/chats/${STATE.currentChatId}/messages`);
    const messageList = await response.json();
    console.log("Messages", messageList);

    const messageListEl = document.getElementById("message-list");
    messageListEl.innerHTML = "";
    messageList.forEach((message) => {
      const messageRow = document.createElement("a");
      messageRow.href = "#";
      messageRow.className = "list-group-item";
      messageRow.innerText = `${message.sender_name}: "${message.message}"`;
      messageListEl.appendChild(messageRow);
    });
    STATE.lastMessageUpdate = new Date();
  }
};

// Start our simple chat app
startApp();
