// login
async function login(event) {
  event.preventDefault();

  let form = document.getElementById("loginForm");
  let data = {};
  for (let i = 0; i < form.elements.length; i++) {
    let element = form.elements[i];
    if (element.type !== "submit") {
      data[element.name] = element.value;
    }
  }

  try {
    let response = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    let result = await response.json();

    console.log("server replied with:", result);
    if (result.error) {
      alert(result.error);
    } else {
      sessionStorage.setItem("username", result.username);
      window.location.href = "/main";
    }
  } catch (error) {
    console.error("Network error:", error);
  }
}
// register
async function register(event) {
  event.preventDefault();

  let form = document.getElementById("registerForm");
  let data = {};
  console.log(form.elements);
  for (let i = 0; i < form.elements.length; i++) {
    let element = form.elements[i];
    if (element.type !== "submit") {
      data[element.name] = element.value;
    }
  }

  try {
    let response = await fetch("/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    let result = await response.json();

    console.log("server replied with:", result);
    if (result.error) {
      alert(result.error);
    } else {
      sessionStorage.setItem("username", result.username);
      window.location.href = "/main";
    }
  } catch (error) {
    console.error("Network error:", error);
  }
}

// add tasks
async function addTasks(event) {
  event.preventDefault();

  let form = document.getElementById("addTasksForm");
  let data = {};
  for (let i = 0; i < form.elements.length; i++) {
    let element = form.elements[i];
    if (element.type !== "submit") {
      data[element.name] = element.value;
    }
  }
  console.log(data);

  // data{ element.name i.e, the text from name field on input: the vlue of that input, }
  //
  //

  let response = await fetch("/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  let result = await response.json();
  if (result.error) {
    alert(result.error);
  } else {
    window.location.href = "/main";
  }
}

// delete
//
// get task_id from sesionStorage and return to python to process
async function deleteTask(task_id) {
  let response = await fetch("/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task_id: task_id }),
  });
  let result = await response.json();
  if (result.error) {
    alert(result.error);
  } else {
    location.reload();
  }
}

async function editTask() {
  console.log("editTask() runnning NOW!");
  try {
    let form = document.getElementById("editTasksForm");
    let data = {};
    for (let i = 0; i < form.elements.length; i++) {
      let element = form.elements[i];
      if (
        element.name &&
        element.type !== "submit" &&
        element.type !== "button"
      ) {
        data[element.name] = element.value;
      }
    }
    console.log("form data:", data);
    let taskId = data.id;
    console.log("Task id:", taskId);
    console.log("Fetch url:", `/edit/${taskId}`);

    let response = await fetch(`http://127.0.0.1:4000/edit/${taskId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    let result = await response.json();
    if (result.error) {
      alert(result.error);
    } else {
      window.location.href = "/main";
    }
  } catch (error) {
    console.error("error:", error);
  }
}
