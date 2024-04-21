// frontend\jsinergia\ApiLocal.js

import { AdaptadorApi } from './AdaptadorApi.js';

class AdaptadorApiLocal extends AdaptadorApi {
    constructor() {
        super();
    }
    construirPeticion(datos={}) {
        const keyApi = this._obtenerKeyApi();
        const encabezados = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json',
            'Authorization': `Bearer ${keyApi}`,
            'token': this.token,
            'uuid': this.uuid
        };
        let cuerpo = JSON.stringify(datos, (clave, valor) => {
            if (valor === null || valor === undefined) {
                return '';
            }
            return valor;
        });
        return { "encabezados": encabezados, "cuerpo": cuerpo };
    }
    adaptarRespuesta(respuesta) {
        const { codigo='', tipo='', texto='', esquemas=null, resultado } = respuesta;
        return {
            codigo, tipo, esquemas,
            mensaje: texto,
            caso: resultado?.caso || null,
            lista: resultado?.lista || null,
        };
    }
}
export const adaptador = new AdaptadorApiLocal();
