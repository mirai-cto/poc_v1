let machineSelect = document.getElementById("machine-select");
let materialSelect = document.getElementById("material-select");
let toolsBody = document.getElementById("tools-body");
let toolListSelect = document.getElementById("tool-list");

let selectedTools = []; // Combined tool list: recommended + manually added

window.onload = async () => {
  await loadDropdowns();
};

async function loadDropdowns() {
  const machines = await axios.get("/machines");
  machines.data.forEach(m => {
    let opt = document.createElement("option");
    opt.value = m.id;
    opt.text = m.title;
    machineSelect.add(opt);
  });

  const materials = await axios.get("/materials");
  materials.data.forEach(m => {
    let opt = document.createElement("option");
    opt.value = m.id;
    opt.text = m.name;
    materialSelect.add(opt);
  });

  const tools = await axios.get("/tools");
  tools.data.forEach(t => {
    let opt = document.createElement("option");
    opt.value = t.name;
    opt.text = t.name;
    toolListSelect.add(opt);
  });
}

async function uploadCAD() {
  const fileInput = document.getElementById("cad-file");
  if (!fileInput.files.length) return alert("Upload a CAD file first!");

  // upload fake CAD to trigger feature extraction (simulated)
  let formData = new FormData();
  formData.append("file", fileInput.files[0]);
  const featuresRes = await axios.post("/upload_cad", formData);
  const features = featuresRes.data.features;

  // recommend tools
  const machineId = machineSelect.value;
  const materialId = materialSelect.value;
  const recRes = await axios.post("/recommend_tools", {
    machine_id: parseInt(machineId),
    material_id: parseInt(materialId),
  });

  selectedTools = recRes.data.recommended_tools.map(t => ({
    feature: t.feature,
    tool: t.tool,
    rpm: t.suggested_rpm,
    wear_score: 0.0
  }));

  renderToolTable();
}

function renderToolTable() {
  toolsBody.innerHTML = "";
  selectedTools.forEach((tool, idx) => {
    const row = `<tr>
      <td>${tool.feature || "-"}</td>
      <td>${tool.tool}</td>
      <td>${tool.rpm}</td>
      <td>${tool.wear_score}</td>
      <td><button onclick="calcSpeedFeed(${idx})">Calc S/F</button></td>
    </tr>`;
    toolsBody.insertAdjacentHTML("beforeend", row);
  });
}

function showAddTool() {
  document.getElementById("manual-tool-section").style.display = "block";
}

function addToolManually() {
  const toolName = toolListSelect.value;
  const wearScore = parseFloat(document.getElementById("wear-score").value);
  if (!toolName || isNaN(wearScore)) return alert("Enter valid tool and wear score");

  selectedTools.push({
    feature: "manual",
    tool: toolName,
    rpm: "N/A",
    wear_score: wearScore
  });

  renderToolTable();
}

async function calcSpeedFeed(index) {
  const tool = selectedTools[index];
  const res = await axios.post("/calculate_speeds_feeds", {
    tool_name: tool.tool,
    wear_score: tool.wear_score
  });

  tool.rpm = res.data.rpm;
  tool.feed = res.data.feed;
  renderToolTable();
}
