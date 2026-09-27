document.addEventListener("DOMContentLoaded", function () {

    /* =========================
       CAMPOS
    ========================= */

    const campoImagem = document.getElementById("id_imagem");
    const campoSituacao = document.getElementById("id_situacao");

    const campoLatitude = document.getElementById("id_latitude");
    const campoLongitude = document.getElementById("id_longitude");

    const formulario = document.getElementById("cisternaForm");

    const imagemPreview = document.getElementById("imagePreview");
    const imagemVazia = document.getElementById("imageEmpty");
    const removerImagem = document.getElementById("removeImage");

    const situacaoPreview = document.getElementById("situacaoPreview");

    const marcador = document.getElementById("mapMarker");
    const mensagemMapa = document.getElementById("mapMessage");


    /* =========================
       PRÉVIA DA IMAGEM
    ========================= */

    if (campoImagem) {

        campoImagem.addEventListener("change", function () {

            const arquivo = this.files[0];

            if (!arquivo) {
                return;
            }

            if (!arquivo.type.startsWith("image/")) {

                alert("Selecione uma imagem válida.");

                this.value = "";

                return;
            }

            const leitor = new FileReader();

            leitor.onload = function (evento) {

                if (imagemPreview) {
                    imagemPreview.src = evento.target.result;
                    imagemPreview.style.display = "block";
                }

                if (imagemVazia) {
                    imagemVazia.style.display = "none";
                }

            };

            leitor.readAsDataURL(arquivo);

        });

    }


    /* =========================
       REMOVER IMAGEM
    ========================= */

    if (removerImagem) {

        removerImagem.addEventListener("click", function () {

            if (campoImagem) {
                campoImagem.value = "";
            }

            if (imagemPreview) {
                imagemPreview.src = "";
                imagemPreview.style.display = "none";
            }

            if (imagemVazia) {
                imagemVazia.style.display = "flex";
            }

        });

    }


    /* =========================
       SITUAÇÃO
    ========================= */

    function atualizarSituacao() {

        if (!campoSituacao || !situacaoPreview) {
            return;
        }

        const valor = campoSituacao.value;

        const nomes = {
            normal: "Normal",
            atencao: "Atenção",
            critico: "Crítico",
            sem_dados: "Sem dados"
        };

        const nome = nomes[valor] || "Sem dados";

        situacaoPreview.className =
            "situacao-preview " + valor;

        const texto = situacaoPreview.querySelector("strong");

        if (texto) {
            texto.textContent = nome;
        }

    }


    if (campoSituacao) {

        campoSituacao.addEventListener(
            "change",
            atualizarSituacao
        );

        atualizarSituacao();

    }


    /* =========================
       MAPA
    ========================= */

    function atualizarMapa() {

        if (
            !campoLatitude ||
            !campoLongitude ||
            !marcador ||
            !mensagemMapa
        ) {
            return;
        }

        const latitude = parseFloat(
            campoLatitude.value
        );

        const longitude = parseFloat(
            campoLongitude.value
        );


        if (
            Number.isNaN(latitude) ||
            Number.isNaN(longitude)
        ) {

            marcador.style.display = "none";

            mensagemMapa.style.display = "flex";

            return;
        }


        let esquerda =
            ((longitude + 180) / 360) * 100;

        let topo =
            ((90 - latitude) / 180) * 100;


        esquerda = Math.max(
            5,
            Math.min(95, esquerda)
        );

        topo = Math.max(
            8,
            Math.min(88, topo)
        );


        marcador.style.left =
            esquerda + "%";

        marcador.style.top =
            topo + "%";

        marcador.style.display =
            "flex";

        mensagemMapa.style.display =
            "none";

    }


    if (campoLatitude) {

        campoLatitude.addEventListener(
            "input",
            atualizarMapa
        );

    }


    if (campoLongitude) {

        campoLongitude.addEventListener(
            "input",
            atualizarMapa
        );

    }


    atualizarMapa();


    /* =========================
       VALIDAÇÃO
    ========================= */

    if (formulario) {

        formulario.addEventListener(
            "submit",
            function (evento) {

                const identificacao =
                    document.getElementById(
                        "id_identificacao"
                    );


                if (
                    identificacao &&
                    !identificacao.value.trim()
                ) {

                    evento.preventDefault();

                    alert(
                        "Informe a identificação da cisterna."
                    );

                    identificacao.focus();

                    return;
                }


                if (
                    campoSituacao &&
                    !campoSituacao.value
                ) {

                    evento.preventDefault();

                    alert(
                        "Selecione a situação da cisterna."
                    );

                    campoSituacao.focus();

                }

            }
        );

    }

});