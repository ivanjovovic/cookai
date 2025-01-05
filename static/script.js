document.getElementById("generateBtn").addEventListener("click", async () => {
  const selectedIngredients = Array.from(
    document.querySelectorAll('input[type="checkbox"]:checked')
  ).map((checkbox) => checkbox.value);

  const additionalIngredients = document
    .getElementById("ingredients")
    .value.split(",")
    .map((ing) => ing.trim())
    .filter((ing) => ing !== "");

  const ingredients = [...selectedIngredients, ...additionalIngredients];
  const equipment = Array.from(
    document.querySelectorAll(
      'input[type="checkbox"][value="šerpa"], input[type="checkbox"][value="tiganj"], input[type="checkbox"][value="mikser"]:checked'
    )
  ).map((checkbox) => checkbox.value);

  const servings = document.getElementById("servings").value;

  const responseDiv = document.getElementById("recipeOutput");
  const regenerateBtn = document.getElementById("regenerateBtn");

  if (ingredients.length === 0) {
    responseDiv.textContent = "Molimo odaberite barem jedan sastojak.";
    responseDiv.style.color = "red";
    return;
  }

  responseDiv.style.color = "black";
  responseDiv.innerHTML = "Generišem recept... <div class='spinner'></div>";
  regenerateBtn.style.display = "none";

  try {
    const response = await fetch("/generate-recipe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ingredients,
        equipment,
        servings,
      }),
    });

    if (!response.ok) throw new Error("Greška u komunikaciji sa serverom.");

    const data = await response.json();
    if (data.error) throw new Error(data.error);

    responseDiv.style.opacity = 0;
    setTimeout(() => {
      responseDiv.textContent = data.recipe;
      responseDiv.style.opacity = 1;
    }, 300);

    regenerateBtn.style.display = "block";
    document.getElementById("downloadBtn").style.display = "block";
  } catch (error) {
    responseDiv.textContent = `Greška: ${error.message}`;
    responseDiv.style.color = "red";
  }
});

document.getElementById("regenerateBtn").addEventListener("click", async () => {
  document.getElementById("generateBtn").click();
});

document.getElementById("downloadBtn").addEventListener("click", function () {
  const recipeText = document.getElementById("recipeOutput").textContent;
  const blob = new Blob([recipeText], { type: "text/plain;charset=utf-8" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "recept.txt";
  link.click();
});

const stars = document.querySelectorAll("#rating i");
stars.forEach((star, index) => {
  star.addEventListener("click", () => {
    stars.forEach((s, i) => {
      s.style.color = i <= index ? "gold" : "gray";
    });
    alert(`Ocijenili ste recept sa ${index + 1} zvjezdica.`);
  });
});
