function searchProjects() {
    const input = document.getElementById('searchProjects');
    const filter = input.value.toUpperCase();
    const projContainer = document.getElementById('project-container')
    const projRows = document.getElementsByClassName('project-row')
    const titles = projContainer.getElementsByClassName('project-title')
    const headlines = projContainer.getElementsByClassName('project-headline')
    const descs = projContainer.getElementsByClassName('project-description')

    for (let i = 0; i < titles.length; i++) {
        let val = titles[i].innerText + headlines[i].innerText
         // + descs[i].innerText
        if (val.toUpperCase().indexOf(filter) > -1) {
            projRows[i].style.display = ""
        } else {
            projRows[i].style.display = "none"
        }
    }
}
