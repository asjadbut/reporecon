fetch("data/repos.json")
.then(res => res.json())
.then(data => {

const table = document.querySelector("#repoTable tbody");

data.forEach(item => {

const row = document.createElement("tr");

row.innerHTML = `
<td>${item.platform}</td>
<td><a href="${item.program_url}" target="_blank">${item.program}</a></td>
<td><a href="${item.repo}" target="_blank">${item.repo}</a></td>
`;

table.appendChild(row);

});

});