
document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll(".monitor-card");

    cards.forEach(function (card) {
        const barra = card.querySelector(".level-fill");
        const status = card.querySelector(".status-badge");

        if (!barra) return;

        const textoNivel = barra.getAttribute("data-nivel");

        if (
            textoNivel === null ||
            textoNivel.trim() === "" ||
            !Number.isFinite(Number(textoNivel.replace(",", ".")))
        ) {
            barra.style.width = "0%";

            if (status) {
                status.textContent = "Sem leitura";
                status.className = "status-badge sem-dados";
            }

            return;
        }

        const nivel = Math.max(
            0,
            Math.min(100, Number(textoNivel.replace(",", ".")))
        );

        barra.style.width = nivel + "%";

        const trilha = barra.closest(".level-bar");

        if (trilha) {
            trilha.setAttribute("aria-valuenow", nivel);
        }

        if (nivel >= 70) {
            barra.style.backgroundColor = "#22c55e";

            if (status) {
                status.textContent = "Normal";
                status.className = "status-badge normal";
            }
        } else if (nivel >= 30) {
            barra.style.backgroundColor = "#f59e0b";

            if (status) {
                status.textContent = "Atenção";
                status.className = "status-badge atencao";
            }
        } else {
            barra.style.backgroundColor = "#ef4444";

            if (status) {
                status.textContent = "Crítico";
                status.className = "status-badge critico";
            }
        }
    });

    const busca = document.getElementById("buscarMonitoramento");
    const semResultados = document.getElementById("semResultados");

    if (busca) {
        busca.addEventListener("input", function () {
            const termo = busca.value.toLocaleLowerCase("pt-BR").trim();
            let encontrados = 0;

            cards.forEach(function (card) {
                const texto = (
                    (card.dataset.busca || "") + " " + card.textContent
                ).toLocaleLowerCase("pt-BR");

                const corresponde = texto.includes(termo);

                card.style.display = corresponde ? "" : "none";

                if (corresponde) encontrados++;
            });

            if (semResultados) {
                semResultados.style.display =
                    encontrados === 0 && cards.length > 0 ? "block" : "none";
            }
        });
    }
});

