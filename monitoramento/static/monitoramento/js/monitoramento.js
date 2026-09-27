document.addEventListener("DOMContentLoaded", function () {

    const campoBusca =
        document.getElementById("buscarMonitoramento");

    const cards =
        document.querySelectorAll(".monitor-card");

    const botaoTodas =
        document.getElementById("mostrarTodas");

    const semResultado =
        document.getElementById("semResultado");

    const horaAtual =
        document.getElementById("horaAtual");


    /* =========================
       RELÓGIO
    ========================== */

    function atualizarHora() {

        const agora = new Date();


        const horas =
            String(
                agora.getHours()
            ).padStart(2, "0");


        const minutos =
            String(
                agora.getMinutes()
            ).padStart(2, "0");


        const segundos =
            String(
                agora.getSeconds()
            ).padStart(2, "0");


        if (horaAtual) {

            horaAtual.textContent =
                horas + ":" +
                minutos + ":" +
                segundos;

        }

    }


    atualizarHora();

    setInterval(
        atualizarHora,
        1000
    );



    /* =========================
       BUSCA
    ========================== */

    function filtrarCisternas() {

        if (!campoBusca) {
            return;
        }


        const texto =
            campoBusca.value
                .toLowerCase()
                .trim();


        let encontrou = false;


        cards.forEach(function (card) {

            const dados =
                card
                    .getAttribute("data-search")
                    .toLowerCase();


            if (dados.includes(texto)) {

                card.style.display = "block";

                encontrou = true;

            } else {

                card.style.display = "none";

            }

        });


        if (semResultado) {

            if (texto === "" || encontrou) {

                semResultado.style.display =
                    "none";

            } else {

                semResultado.style.display =
                    "flex";

            }

        }

    }


    if (campoBusca) {

        campoBusca.addEventListener(
            "input",
            filtrarCisternas
        );

    }



    /* =========================
       MOSTRAR TODAS
    ========================== */

    if (botaoTodas) {

        botaoTodas.addEventListener(
            "click",
            function () {

                if (campoBusca) {

                    campoBusca.value = "";

                }


                cards.forEach(function (card) {

                    card.style.display =
                        "block";

                });


                if (semResultado) {

                    semResultado.style.display =
                        "none";

                }


                if (campoBusca) {

                    campoBusca.focus();

                }

            }
        );

    }



    /* =========================
       BARRAS DE NÍVEL
    ========================== */

    const barras =
        document.querySelectorAll(
            ".monitor-level-fill"
        );


    barras.forEach(function (barra) {

        let nivel =
            parseFloat(
                barra.getAttribute("data-nivel")
            );


        if (Number.isNaN(nivel)) {

            nivel = 0;

        }


        nivel = Math.max(
            0,
            Math.min(100, nivel)
        );


        barra.style.width = "0%";


        setTimeout(
            function () {

                barra.style.width =
                    nivel + "%";

            },
            150
        );

    });

});