// frontend\jsinergia\AdaptadorApi.js

export class AdaptadorApi {
    constructor() {
        this.gestorEstados = null;
        this.urlApi = null;
        this.keyApi = null;
        this.token = null;
        this.uuid = null;
    }
    // Funciones privadas compartidas por todos los Adaptadores API
    _obtenerKeyApi() {
        return Base.desencriptarTexto(([...this.keyApi]).reverse().join(''), Base.cadenaUrl(this.urlApi));
    }
    // Funciones compartidas por todos los Adaptadores API (se pueden sobreescribir)
    crearUrlCompleta(puntofinal, parametros={}) {
        Base.trazarFlujo(this.constructor.name, 'crearUrlCompleta', 3, puntofinal);
        if (!puntofinal) {
            throw new ErrorPersonalizado('ERROR_URL_NO_VALIDA');
        }
        const url = new URL(`${this.urlApi}${puntofinal}`);
        Object.keys(parametros).forEach(key => url.searchParams.append(key, parametros[key]));
        return url.toString();
    }
    validarMetodoEnvio(metodo) {
        Base.trazarFlujo(this.constructor.name, 'validarMetodoEnvio', 3, metodo);
        const metodosPermitidos = ['GET', 'POST', 'PUT', 'DELETE'];
        if (!metodosPermitidos.includes(metodo.toUpperCase())) {
            throw new ErrorPersonalizado('ERROR_METODO_NO_PERMITIDO');
        }
    }
    // Funciones que deben implementar obligatoriamente todos los Adaptadores API
    construirPeticion(datos={}) {
        throw new Error("No implementado");
    }
    adaptarRespuesta(respuesta) {
        throw new Error("No implementado");
    }
}
