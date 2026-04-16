function CreateProperty() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100 px-4 py-10">
      <div className="w-full max-w-2xl bg-white rounded-2xl shadow-md p-8">
        <h1 className="text-3xl font-bold mb-2">Cadastro de Imóvel</h1>
        <p className="text-gray-500 mb-6">
          Preencha as informações abaixo para cadastrar um novo imóvel.
        </p>

        <form className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Título do imóvel"
            className="p-3 border border-gray-300 rounded-lg"
          />

          <input
            type="text"
            placeholder="Endereço"
            className="p-3 border border-gray-300 rounded-lg"
          />

          <input
            type="text"
            placeholder="Cidade"
            className="p-3 border border-gray-300 rounded-lg"
          />

          <input
            type="text"
            placeholder="Estado"
            className="p-3 border border-gray-300 rounded-lg"
          />

          <textarea
            placeholder="Descrição do imóvel"
            rows="5"
            className="p-3 border border-gray-300 rounded-lg"
          ></textarea>

          <button
            type="submit"
            className="bg-black text-white p-3 rounded-lg hover:opacity-90 transition"
          >
            Cadastrar Imóvel
          </button>
        </form>
      </div>
    </main>
  );
}

export default CreateProperty;