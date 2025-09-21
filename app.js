const API_BASE = "http://127.0.0.1:8000";

let jwtToken = null, sse = null, countdownInterval = null;
const out = document.getElementById("output");
const statusEl = document.getElementById("status");
const walletInput = document.getElementById("wallet");
const paymentPreview = document.getElementById("paymentPreview");
const rentalCountdownContainer = document.getElementById("rentalCountdownContainer");
const rentalCountdown = document.getElementById("rentalCountdown");
const rentalBar = document.getElementById("rentalBar");

// --- Logging ---
function log(msg){
  const ts = new Date().toLocaleTimeString();
  out.textContent += `[${ts}] ${msg}\n`;
  out.scrollTop = out.scrollHeight;
}

function setStatus(text, color="#9aa4b2"){
  statusEl.textContent = text;
  statusEl.style.color = color;
}

// --- Payment Preview ---
function updatePaymentPreview() {
  const wallet = walletInput.value || "demo-wallet";
  const demoPayment = {
    reference: "preview-" + Math.random().toString(36).slice(2,8),
    to: "DemoReceiver1",
    amount: 0.01,
    currency: "SOL",
    message: `Rental for ${wallet}`
  };
  paymentPreview.textContent = JSON.stringify(demoPayment, null, 2);
}
walletInput.addEventListener("input", updatePaymentPreview);
updatePaymentPreview();

// --- Create Payment ---
document.getElementById("btnCreate").addEventListener("click", async () => {
  setStatus("Creating payment...");
  const wallet = walletInput.value || "demo-wallet";
  try {
    const res = await fetch(`${API_BASE}/create_payment`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({wallet_address: wallet, rental_hours:1, amount:0.01})
    });
    const data = await res.json();
    log("Payment created: " + JSON.stringify(data));
    setStatus("Payment created — verify to get token", "#f0ad4e");
  } catch(e){
    log("Create payment error: " + e);
    setStatus("Error creating payment", "red");
  }
});

// --- Verify Payment ---
document.getElementById("btnVerify").addEventListener("click", async () => {
  setStatus("Verifying...");
  const wallet = walletInput.value || "demo-wallet";
  try {
    const res = await fetch(`${API_BASE}/verify_dev?tx_signature=dev-ok&wallet_address=${encodeURIComponent(wallet)}`);
    const js = await res.json();
    if(js.token){
      jwtToken = js.token;
      document.getElementById("token").value = jwtToken;
      setStatus("Verified — token received", "#2ea043");
      connectSSE();

      // Show countdown and start timer
      rentalCountdownContainer.style.display = "block";
      startRentalCountdown(60*60); // 1 hour

      log("Received token (dev): " + jwtToken.slice(0,40) + "...");
    } else {
      log("Verify returned: " + JSON.stringify(js));
      setStatus("Verification failed", "red");
    }
  } catch(e){
    log("Verify error: " + e);
    setStatus("Verification error", "red");
  }
});

// --- Countdown ---
function startRentalCountdown(seconds=3600){
  if(countdownInterval) clearInterval(countdownInterval);
  const endTime = Date.now() + seconds*1000;

  countdownInterval = setInterval(()=>{
    const remaining = Math.max(0, endTime - Date.now());
    const hrs = Math.floor(remaining / 3600000);
    const mins = Math.floor((remaining % 3600000)/60000);
    const secs = Math.floor((remaining % 60000)/1000);
    rentalCountdown.textContent = `${hrs.toString().padStart(2,"0")}:${mins.toString().padStart(2,"0")}:${secs.toString().padStart(2,"0")}`;
    rentalBar.style.width = `${(remaining/(seconds*1000))*100}%`;

    if(remaining<=0){
      clearInterval(countdownInterval);
      rentalCountdown.textContent="Expired";
      setStatus("Rental expired", "red");
      if(sse) sse.close();
    }
  },1000);
}

// --- Upload Document ---
document.getElementById("btnUpload").addEventListener("click", async ()=>{
  const fileInput = document.getElementById("docInput");
  if(!jwtToken){ log("No JWT — verify first."); setStatus("No token","red"); return; }
  if(fileInput.files.length===0){ log("No file selected."); return; }
  const fd = new FormData();
  fd.append("file", fileInput.files[0]);
  setStatus("Uploading...");
  try{
    const res = await fetch(`${API_BASE}/upload_document`, {
      method:"POST",
      headers: { "Authorization": `Bearer ${jwtToken}` },
      body: fd
    });
    const js = await res.json();
    log("Upload result: "+JSON.stringify(js));
    setStatus("Upload complete", "#2ea043");
  } catch(e){
    log("Upload error: "+e);
    setStatus("Upload failed", "red");
  }
});

// --- SSE ---
function connectSSE(){
  if(sse) sse.close();
  log("Connecting SSE...");
  sse = new EventSource(`${API_BASE}/sse?agentId=web&agentDescription=frontend`);
  sse.onmessage = (ev)=>{
    try{
      const d = JSON.parse(ev.data);
      if(d.event==="heartbeat"){ log("[heartbeat]"); } else { log("SSE: "+JSON.stringify(d)); }
    }catch(e){ log("SSE raw: "+ev.data); }
  };
  sse.onerror = ()=>{ log("SSE error"); setStatus("SSE disconnected","red"); };
}
