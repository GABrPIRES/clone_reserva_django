var url = new URL(document.URL);
var itens = document.getElementsByClassName("item-ordenar");

console.log("Chamou")

for (i = 0; i < itens.length; i++) {
    console.log("Chamou 1")
    url.searchParams.set("ordem", itens[i].value)
    itens[i].value = url.href
}