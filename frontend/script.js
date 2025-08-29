document.getElementById("resumeForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append("resume", document.getElementById("resume").files[0]);
    formData.append("job_description", document.getElementById("job_description").value);

    const resultBox = document.getElementById("result");
    resultBox.classList.remove("hidden");
    resultBox.innerHTML = "<p>⏳ Analyzing resume... Please wait.</p>";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.status === "success") {
            const result = data.data;

            // Build result UI
            let output = `
              <h2>✅ Match Score</h2>
              <div class="score-bar">
                <div class="score-fill" style="width: ${parseInt(result.match_score)}%"></div>
              </div>
              <p><strong>${result.match_score}</strong></p><br><br>

              <h3>📊 Score Breakdown</h3>
              <ul>
                ${Object.entries(result.score_breakdown).map(([k,v]) => `<li><b>${k}</b>: ${v}</li>`).join("")}
              </ul><br><br>

              <h3>❌ Missing Skills</h3>
              <ul>
                ${result.missing_skills.map(s => `<li>${s}</li>`).join("")}
              </ul><br><br>

              <h3>💡 Suggestions</h3>
              <ul>
                ${result.suggestions.map(s => `<li>${s}</li>`).join("")}
              </ul><br><br>

              <h3>🏢 Company Alignment</h3>
              <p><b>Service-based:</b> ${result.company_alignment.service_based}</p>
              <p><b>Product-based:</b> ${result.company_alignment.product_based}</p><br><br>

              <h3>📝 Summary</h3>
              <p>${result.summary}</p><br><br>

              <h3>📋 Skills Comparison Table</h3>
              <table class="skills-table">
                <tr><th>Category</th><th>Existing Skills</th><th>Missing Skills</th></tr>
                ${result.skills_table.map(row => `
                  <tr>
                    <td>${row.category}</td>
                    <td>${row.existing.join(", ") || "-"}</td>
                    <td>${row.missing.join(", ") || "-"}</td>
                  </tr>
                `).join("")}
              </table>
            `;

            resultBox.innerHTML = output;
        } else {
            resultBox.innerHTML = "<p>❌ Error: " + data.message + "</p>";
        }

    } catch (error) {
        resultBox.innerHTML = "<p>⚠️ Failed to connect to backend: " + error + "</p>";
    }
});
