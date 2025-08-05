document.getElementById("armorForm").addEventListener("submit", async function(e) {
  e.preventDefault();
  const formData = new FormData(this);
  const json = Object.fromEntries(formData.entries());

  const response = await fetch("/calculate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(json)
  });

  const result = await response.json();
  console.log("Server response:", result); // Debugging output

  // Render build table
  const buildTable = document.getElementById("buildTable");
  buildTable.innerHTML = "";

  if (result.columns && result.build) {
    let headerRow = "<tr>";
    result.columns.forEach(col => {
      headerRow += `<th>${col}</th>`;
    });
    headerRow += "</tr>";
    buildTable.innerHTML += headerRow;

    result.build.forEach(row => {
      let rowHTML = "<tr>";
      result.columns.forEach(col => {
        rowHTML += `<td>${row[col]}</td>`;
      });
      rowHTML += "</tr>";
      buildTable.innerHTML += rowHTML;
    });
  } else {
    buildTable.innerHTML = "<tr><td colspan='99'>No data returned from server.</td></tr>";
  }

  // Display total stats
  const statList = document.getElementById("statList");
  statList.innerHTML = "";
  for (const [key, value] of Object.entries(result.total_stats)) {
    statList.innerHTML += `<li>${key}: ${value}</li>`;
  }

  // Display armor
  document.getElementById("armorResult").textContent = result.effective_armor;
});
