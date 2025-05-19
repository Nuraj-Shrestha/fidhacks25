// ========== GOAL TRACKING (localStorage) ==========

const goalInput = document.querySelector('input[placeholder="Add a goal..."]');
const goalList = document.getElementById('goal-list');

function loadGoals() {
  const saved = JSON.parse(localStorage.getItem('goals')) || [];
  goalList.innerHTML = '';
  saved.forEach((goal, index) => {
    const li = document.createElement('li');
    li.textContent = goal;
    li.onclick = () => removeGoal(index);
    goalList.appendChild(li);
  });
}

function addGoal() {
  const value = goalInput.value.trim();
  if (!value) return;

  const current = JSON.parse(localStorage.getItem('goals')) || [];
  if (current.length >= 3) {
    alert("You can only set 3 main goals.");
    return;
  }

  current.push(value);
  localStorage.setItem('goals', JSON.stringify(current));
  goalInput.value = '';
  loadGoals();
}

function removeGoal(index) {
  const current = JSON.parse(localStorage.getItem('goals')) || [];
  current.splice(index, 1);
  localStorage.setItem('goals', JSON.stringify(current));
  loadGoals();
}

// Bind enter key to goal input
if (goalInput) {
  goalInput.addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      addGoal();
    }
  });
  window.addEventListener("load", loadGoals);
}


// ========== OPTIONAL: REMEMBER NAME (localStorage) ==========

const nameInput = document.querySelector('input[name="name"]');
if (nameInput) {
  // Autofill if name previously entered
  const storedName = localStorage.getItem('username');
  if (storedName) nameInput.value = storedName;

  nameInput.addEventListener('input', () => {
    localStorage.setItem('username', nameInput.value);
  });
}
