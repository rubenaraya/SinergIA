// frontend\prueba\inicio.js

/* FUNCION PARA INICIALIZAR LA APLICACION */
let coordinador;
window.onload = async () => {
    try {
        window.addEventListener('beforeinstallprompt', (evento) => {
            evento.preventDefault();
            window.promptInstalacion = evento;
        });
        if (!window.aplicacionIniciada) {
            const interfazUsuario = InterfazUsuario.obtenerInstancia(bootstrap);
            const operadorDatos = OperadorDatos.obtenerInstancia();
            coordinador = CoordinadorGeneral.obtenerInstancia(operadorDatos, interfazUsuario);
            window.aplicacionIniciada = await coordinador.coordinarInicio('./manifest.json', './errores.php', GestorEstado.obtenerInstancia());
            if (window.aplicacionIniciada) {
                await coordinador.ejecutarServicio('./frontend/servicios/base/servicio.js');
            }
        }
    } catch (error) {
        console.error(error);
    }
};
let nivel_trazado = 4;
let filtro_trazado = [];
