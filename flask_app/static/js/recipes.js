document.addEventListener("DOMContentLoaded", function() {
    var addRecipeDiv = document.getElementById("addRecipe");
    var url = addRecipeDiv.dataset.url;

    addRecipeDiv.addEventListener("click", function() {
    window.location.href = url;
    });
});
