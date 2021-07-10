document.addEventListener("DOMContentLoaded", function (event) {

    const showNavbar = (toggleId, navId, bodyId, headerId) => {
        const toggle = document.getElementById(toggleId),
            nav = document.getElementById(navId),
            bodypd = document.getElementById(bodyId),
            headerpd = document.getElementById(headerId)

        // Valida si las varianles existen
        if (toggle && nav && bodypd && headerpd) {
            toggle.addEventListener('click', () => {
                // muestra navbar
                nav.classList.toggle('show')
                // cambia icon
                toggle.classList.toggle('header_toggle_rot90')
                // agrega padding al body
                bodypd.classList.toggle('body-pd')
                // agregar padding al header
                headerpd.classList.toggle('body-pd')
            })
        }
    }

    showNavbar('header-toggle', 'nav-bar', 'body-pd', 'header')

    /* Cambia el estedo el link activo (Active) */
    const linkColor = document.querySelectorAll('.nav_link')

    function colorLink() {
        if (linkColor) {
            linkColor.forEach(l => l.classList.remove('active'))
            this.classList.add('active')
            /* Obtiene el selector al cual apunta para buscar el ID*/
            const sectionSend = this.href.substring(this.href.indexOf('#') + 1);
            /* Busca todos los elementos de la clase xxxx */
            let noneDisplay = document.querySelectorAll('.section_display')
            if (noneDisplay) {
                noneDisplay.forEach(l => l.classList.add('section_diplay_none'))
                document.getElementById(sectionSend).classList.remove("section_diplay_none")
            }
        }
    }
    linkColor.forEach(l => l.addEventListener('click', colorLink))
});