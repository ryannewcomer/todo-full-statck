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
