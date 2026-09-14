import { useEffect, useState } from "react";

type Ciudad = {
  nombre: string;
  descripcion: string;
  lat: number;
  lng: number;
};

type CiudadesResponse = {
  provincia: string;
  pais: string;
  ciudades: Ciudad[];
};

function App() {
  const [data, setData] = useState<CiudadesResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/ciudades/")
      .then((res) => {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.json();
      })
      .then(setData)
      .catch((err: Error) => {
        setError(
          "No se pudo leer la API. ¿Están la red, Postgres, Django y Vite levantados? (" +
            err.message +
            ")",
        );
      });
  }, []);

  return (
    <main>
      <h1>Tierra del Fuego</h1>
      {!data && !error && <p className="status">Cargando ciudades…</p>}
      {error && (
        <p className="status" data-error="">
          {error}
        </p>
      )}
      {data && (
        <>
          <h1 className="lead">
            {data.provincia}, {data.pais}
          </h1>
          <table>
            <thead>
              <tr>
                <th>Ciudad</th>
                <th>Descripción</th>
                <th>Lat</th>
                <th>Lng</th>
              </tr>
            </thead>
            <tbody>
              {data.ciudades.map((ciudad) => (
                <tr key={ciudad.nombre}>
                  <td>{ciudad.nombre}</td>
                  <td>{ciudad.descripcion}</td>
                  <td className="coords">{ciudad.lat}</td>
                  <td className="coords">{ciudad.lng}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </main>
  );
}

export default App;
