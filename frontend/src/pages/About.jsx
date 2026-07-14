export default function About() {
  return (
    <main className="min-h-screen bg-slate-950 text-white px-6 py-24">
      <div className="mx-auto flex max-w-6xl flex-col gap-12">
        <section className="rounded-3xl border border-slate-800 bg-slate-900/80 p-8 shadow-2xl shadow-black/20 md:p-12">
          <p className="mb-4 text-sm font-semibold uppercase tracking-[0.3em] text-blue-300">
            Sobre nós
          </p>
          <h1 className="text-4xl font-bold text-white sm:text-5xl">
            Conectamos pessoas e imóveis com confiança.
          </h1>
          <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-300">
            A GlassRoof nasceu para simplificar a forma como pessoas encontram o lugar ideal para viver ou investir.
            Com uma experiência moderna e intuitiva, reunimos oportunidades imóveis, avaliações e uma comunicação clara entre clientes e imobiliárias.
          </p>
        </section>

        <section className="grid gap-6 md:grid-cols-3">
          <article className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
            <h2 className="text-xl font-semibold text-white">Missão</h2>
            <p className="mt-3 text-sm leading-7 text-slate-300">
              Transformar a busca por imóveis em uma jornada simples, segura e transparente para todos.
            </p>
          </article>

          <article className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
            <h2 className="text-xl font-semibold text-white">Visão</h2>
            <p className="mt-3 text-sm leading-7 text-slate-300">
              Ser referência em soluções digitais para o mercado imobiliário, com foco em clareza e confiança.
            </p>
          </article>

          <article className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
            <h2 className="text-xl font-semibold text-white">Valores</h2>
            <p className="mt-3 text-sm leading-7 text-slate-300">
              Transparência, praticidade, inovação e respeito à experiência do cliente.
            </p>
          </article>
        </section>
      </div>
    </main>
  )
}
