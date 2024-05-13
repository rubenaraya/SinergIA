// frontend\jsinergia\ApiLocal.js

import { AdaptadorApi } from './AdaptadorApi.js';

class ApiLocal extends AdaptadorApi {
    constructor() {
        super();
    }
    construirPeticion(datos={}) {
        const keyApi = this._obtenerKeyApi();
        const encabezados = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json',
            'Authorization': `Bearer ${keyApi}`,
            'X-Token': this.token,
            'X-UUID': this.uuid
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
        const { codigo='', tipo='', mensaje='', esquemas=null, resultado } = respuesta;
        return {
            codigo, tipo, esquemas, mensaje,
            caso: resultado?.caso || null,
            lista: resultado?.lista || null,
        };
    }
}
export const adaptador = new ApiLocal();
