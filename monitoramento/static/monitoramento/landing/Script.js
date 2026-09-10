const secoes = document.querySelectorAll('main section[id]');
const linksMenu = document.querySelectorAll('.menu a');

document.addEventListener('wheel', (event) => {
  if (event.ctrlKey) event.preventDefault();
}, { passive: false });

document.addEventListener('keydown', (event) => {
  if (event.ctrlKey && ['+', '-', '=', '0'].includes(event.key)) event.preventDefault();
});

document.addEventListener('gesturestart', (event) => event.preventDefault());
document.addEventListener('dblclick', (event) => event.preventDefault());

function atualizarProgresso() {
  const altura = document.documentElement.scrollHeight - window.innerHeight;
  document.documentElement.style.setProperty('--scroll', `${altura ? (window.scrollY / altura) * 100 : 0}%`);
}

window.addEventListener('scroll', atualizarProgresso, { passive: true });
atualizarProgresso();

const observadorRevelar = new IntersectionObserver((entradas) => {
  entradas.forEach((entrada) => {
    entrada.target.classList.toggle('visivel', entrada.isIntersecting);
  });
}, { threshold: 0.16 });

document.querySelectorAll('.revelar').forEach((elemento) => observadorRevelar.observe(elemento));

const observadorSecao = new IntersectionObserver((entradas) => {
  entradas.forEach((entrada) => {
    if (!entrada.isIntersecting) return;
    linksMenu.forEach((link) => link.classList.toggle('ativo', link.getAttribute('href') === `#${entrada.target.id}`));
  });
}, { rootMargin: '-35% 0px -55% 0px' });

secoes.forEach((secao) => observadorSecao.observe(secao));

const nivelAgua = document.querySelector('.nivel-agua');
const barrasAgua = document.querySelector('.barras-agua');

if (nivelAgua) {
  const inicio = Number(nivelAgua.dataset.start);
  const alvo = Number(nivelAgua.dataset.target);
  const duracao = 9400;
  const reduzirMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const definirNivel = (valor) => {
    nivelAgua.innerHTML = `${valor}<sup>%</sup>`;
  };

  const animarNivel = (timestamp) => {
    const tempoInicial = timestamp;

    const passo = (agora) => {
      const progresso = Math.min((agora - tempoInicial) / duracao, 1);
      const progressoSuave = 1 - Math.pow(1 - progresso, 3);
      const nivelAtual = inicio + (alvo - inicio) * progressoSuave;

      definirNivel(Math.round(nivelAtual));
      if (barrasAgua) barrasAgua.style.setProperty('--nivel-agua', nivelAtual / 100);

      if (progresso < 1) requestAnimationFrame(passo);
    };

    requestAnimationFrame(passo);
  };

  if (reduzirMovimento) {
    definirNivel(alvo);
    if (barrasAgua) barrasAgua.style.setProperty('--nivel-agua', alvo / 100);
  } else {
    requestAnimationFrame(animarNivel);
  }
}
