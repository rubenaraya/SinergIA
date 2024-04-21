// frontend\jsinergia\ApiOpenAI.jsv

import { AdaptadorApi } from './AdaptadorApi.js';

/* CLASE: AdaptadorApiOpenAI (subclase)
PROPOSITO: es una subclase específica de "AdaptadorApi" diseñada para interactuar con la API de OpenAI, particularmente con el modelo GPT-4. Se encarga de formatear las peticiones y adaptar las respuestas para su uso en la aplicación, cumpliendo con los requisitos y restricciones específicos de la API de OpenAI.
RESPONSABILIDADES:
1. Formatear las peticiones para cumplir con los formatos y limitaciones de la API de OpenAI, incluyendo el manejo de parámetros como prompt, temperature, max_tokens, entre otros.
2. Validar los datos de entrada para garantizar que cumplen con los requisitos de la API de OpenAI, como la longitud máxima del prompt y los rangos permitidos para los parámetros.
3. Adaptar las respuestas recibidas de la API de OpenAI a un formato que pueda ser utilizado eficazmente por la aplicación.
4. Implementar métodos específicos para la construcción de peticiones y la adaptación de respuestas, según las necesidades de interacción con la API de OpenAI.
NOTAS:
Hereda de la superclase "AdaptadorApi", aprovechando sus funcionalidades generales para adaptadores de API y extendiéndolas para cumplir con las especificidades de la API de OpenAI.
Depende de la configuración de la API de OpenAI, incluyendo URL base, claves de acceso y otros parámetros específicos.
*/
export class AdaptadorApiOpenAI extends AdaptadorApi {
    constructor() {
        super();
    }
    // Funciones privadas
    _formatearCuerpoPeticion(datos) {
        // Valores predeterminados y límites
        const MAX_LENGTH_PROMPT = 2048;
        const MAX_TOKENS = 512;
        const TEMPERATURE_MIN = 0;
        const TEMPERATURE_MAX = 1;
        // Validaciones y extracción de datos
        const prompt = datos.get('prompt');
        if (!prompt || prompt.length === 0) {
            throw new Error('El campo "prompt" no puede estar vacío.');
        }
        if (prompt.length > MAX_LENGTH_PROMPT) {
            throw new Error('El "prompt" excede el tamaño máximo permitido.');
        }
        const temperature = parseFloat(datos.get('temperature')) || 0.7;
        if (temperature < TEMPERATURE_MIN || temperature > TEMPERATURE_MAX) {
            throw new Error('La "temperature" debe estar en el rango de 0 a 1.');
        }
        const maxTokens = parseInt(datos.get('max_tokens')) || 100;
        if (maxTokens < 1 || maxTokens > MAX_TOKENS) {
            throw new Error('El valor de "max_tokens" excede el límite permitido.');
        }
        // Construcción del cuerpo de la petición
        let cuerpo = {
            model: datos.get('model') || 'gpt-4',
            messages: [
                {
                    role: "system",
                    content: datos.get('message_system') || ''
                },{
                    role: "user",
                    content: prompt
                }
            ],
            temperature,
            max_tokens: maxTokens,
            top_p: parseFloat(datos.get('top_p')) || 1,
            frequency_penalty: parseFloat(datos.get('frequency_penalty')) || 0,
            presence_penalty: parseFloat(datos.get('presence_penalty')) || 0
        };
        // Filtrar mensajes vacíos
        cuerpo.messages = cuerpo.messages.filter(msg => msg.content.trim() !== '');
        return JSON.stringify(cuerpo);
    }
    // Funciones públicas
    construirPeticion(datos={}) {
        const encabezados = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this._obtenerKeyApi()}`
        };
        const cuerpo = this._formatearCuerpoPeticion(datos);
        return { "encabezados": encabezados, "cuerpo": cuerpo };
    }
    adaptarRespuesta(respuesta) {
        //TODO: Pendiente
        return respuesta.choices[0].text;
    }
}
export const adaptador = new AdaptadorApiOpenAI();
