// frontend\prueba\base\DefinicionModulo.js

import { DefinicionModulo } from './DefinicionModulo.js';

/* ************************************************************************
MODULO: Base
VERSION: 0.0.1 */

/* Clase: DefinicionModuloBase (subclase)
PROPOSITO: Es una subclase de "DefinicionModulo" que actúa como un contenedor de funcionalidad para el "Servicio Base" de la aplicación. Esta clase encapsula los fragmentos de código JavaScript necesarios para implementar este servicio y extender con ello las clases principales de la aplicación.
RESPONSABILIDADES:
1. Contención de Funciones de Extensión: Encapsula el código JavaScript de las funciones que se inyectarán en las clases principales para ampliar su funcionalidad y adaptarla a las necesidades del servicio.
2. Facilitación de Transferencia de Funciones: Provee una estructura que facilita la recuperación y transferencia de las funciones al "ConfiguradorServicios", permitiendo una configuración dinámica del servicio, por demanda y en tiempo de ejecución.
3. Integración con la Arquitectura de la Aplicación: Trabaja en conjunto con el "ConfiguradorServicios" y con el "esquema de servicio" para activar las configuraciones necesarias e implementar las funciones del servicio.
NOTAS:
Esta subclase hereda de la superclase "DefinicionModulo" para la estructura base de un servicio.
Interactúa con la clase "ConfiguradorServicios" para la importación e inyección de las funciones y extensiones del servicio en las clases principales de la aplicación.
Requiere la existencia de un archivo JSON de "esquema de servicio" que contenga los parámetros y datos de las configuraciones del servicio correspondiente en formato JSON.
*/
class DefinicionModuloBase extends DefinicionModulo {
    constructor() {
        super();
    }
    // FUNCIONES PARA DEFINIR / AMPLIAR LA FUNCIONALIDAD DEL SERVICIO
    manejadoresInteracciones() {
        // Funciones para manejar Interacciones de la UI del servicio (callbacks). Se inyectan en "InterfazUsuario".
        return {
        manejarNuevoCaso: function(evento) {
            this.enrutarInteraccion('.nuevo-caso', {'nuevo-caso': this.accionNuevoCaso}, evento);
        },
        manejarEnviarNuevoCaso: function(evento) {
            this.enrutarInteraccion('.enviar-nuevo-caso', {'enviar-nuevo-caso': this.accionEnviarNuevoCaso}, evento);
        },
        manejarEnviarEdicionCaso: function(evento) {
            this.enrutarInteraccion('.enviar-edicion-caso', {'enviar-edicion-caso': this.accionEnviarEdicionCaso}, evento);
        },
        manejarSolicitarListaCasos: function(evento) {
            this.enrutarInteraccion('.solicitar-lista-casos', {'solicitar-lista-casos': this.accionSolicitarListaCasos}, evento);
        },
        manejarAbrirServicio: function(evento) {
            this.enrutarInteraccion('.abrir-servicio', {'abrir-servicio': this.accionAbrirServicio}, evento);
        },
        manejarCambiarIdioma: function(evento) {
            this.enrutarInteraccion('.cambiar-idioma', {'cambiar-idioma': this.accionCambiarIdioma}, evento);
        },
        manejarAccionesParaCasos: function(evento) {
            const mapeoAcciones = {
                'solicitar-eliminacion-caso': this.accionSolicitarEliminacionCaso,
                'solicitar-detalle-caso': this.accionSolicitarDetalleCaso,
            };
            this.enrutarInteraccion('.caso', mapeoAcciones, evento);
        },
        manejarAccionesParaNavegacion: function(evento) {
            const mapeoAcciones = {
                'abrir-servicio': this.accionAbrirServicio,
            };
            this.enrutarInteraccion('.navegacion', mapeoAcciones, evento);
        },
        manejarEnterInput: function(evento) {
            let keycode = (evento.keyCode ? evento.keyCode : evento.which);
            if (keycode === 13) {
                evento.preventDefault();
                this.enrutarInteraccion('.enter-input', {'enter-input': this.accionEnviarNuevoInput}, evento);
            }
        },
        manejarTextosCopiables: function(evento) {
            if (evento.target.classList.contains('copiar-texto')) {
                this.enrutarInteraccion('.copiar-texto', {'copiar-texto': this.accionCopiarTexto}, evento);
            }
        },
        manejarCamposAjustables: function(evento) {
            if (evento.target.classList.contains('ajustar-campo')) {
                this.enrutarInteraccion('.ajustar-campo', {'ajustar-campo': this.accionAjustarCampo}, evento);
            }
        }
        };
    }
    accionesCoordinador() {
        // Funciones para "acciones" que otorgan funcionalidad al servicio. Se inyectan en "CoordinadorGeneral".
        return {
        accionSolicitarListaCasos: async function(contexto) {
            const accion = 'accionSolicitarListaCasos';
            Base.trazarFlujo(this.constructor.name, accion, 2, '[A]');
            try {
                const { recurso, esquema, operacion, servicio, plantilla } = contexto;
                const detalleInteraccion = this.controlarAcceso(accion, servicio);
                if (!detalleInteraccion) { return this.rechazarAcceso(accion, detalleInteraccion); }
                this.interfazUsuario.alternarEsperando(true);
                const parametros = this.interfazUsuario.receptorUI.obtenerDatosFormulario(`form_${esquema}`);
                const portadorInformacion = new PortadorInformacion(this.gestorEstados);
                portadorInformacion.prepararPeticion(operacion, {
                    recurso: recurso,
                    servicio: servicio,
                    informe: esquema,
                    parametros: parametros,
                    plantilla: plantilla
                });
                await this.procesarEsquemas(portadorInformacion);
                await this.operadorDatos.efectuarOperacion(portadorInformacion);
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error, {accion: accion}));
            } finally {
                this.interfazUsuario.alternarEsperando(false);
            }
        },
        accionSolicitarEliminacionCaso: async function(contexto) {
            const accion = 'accionSolicitarEliminacionCaso';
            Base.trazarFlujo(this.constructor.name, accion, 2, '[A]');
            try {
                const { uid, recurso, esquema, operacion, servicio } = contexto;
                const detalleInteraccion = this.controlarAcceso(accion, servicio);
                if (!detalleInteraccion) { return this.rechazarAcceso(accion, detalleInteraccion); }
                const portadorInformacion = new PortadorInformacion(this.gestorEstados);
                portadorInformacion.prepararPeticion(operacion, {
                    uid: uid,
                    recurso: recurso,
                    servicio: servicio,
                    formulario: esquema
                });
                await this.operadorDatos.efectuarOperacion(portadorInformacion);
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error, {accion: accion}));
            }
        },
        accionSolicitarDetalleCaso: async function(contexto) {
            const accion = 'accionSolicitarDetalleCaso';
            Base.trazarFlujo(this.constructor.name, accion, 2, '[A]');
            try {
                const { uid, recurso, esquema, operacion, servicio, plantilla } = contexto;
                const detalleInteraccion = this.controlarAcceso(accion, servicio);
                if (!detalleInteraccion) { return this.rechazarAcceso(accion, detalleInteraccion); }
                const portadorInformacion = new PortadorInformacion(this.gestorEstados);
                portadorInformacion.prepararPeticion(operacion, {
                    uid: uid,
                    recurso: recurso,
                    servicio: servicio,
                    formulario: esquema,
                    plantilla: plantilla
                });
                await this.procesarEsquemas(portadorInformacion);
                await this.operadorDatos.efectuarOperacion(portadorInformacion);
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error, {accion: accion}));
            }
        },
        accionEnviarEdicionCaso: async function(contexto) {
            const accion = 'accionEnviarEdicionCaso';
            Base.trazarFlujo(this.constructor.name, accion, 2, '[A]');
            try {
                const { uid, recurso, esquema, operacion, servicio } = contexto;
                const detalleInteraccion = this.controlarAcceso(accion, servicio);
                if (!detalleInteraccion) { return this.rechazarAcceso(accion, detalleInteraccion); }
                const valores = this.interfazUsuario.receptorUI.obtenerDatosFormulario(`form_${esquema}`);
                const portadorInformacion = new PortadorInformacion(this.gestorEstados);
                portadorInformacion.prepararPeticion(operacion, {
                    uid: uid,
                    recurso: recurso,
                    servicio: servicio,
                    valores: valores,
                    formulario: esquema
                });
                await this.procesarEsquemas(portadorInformacion);
                if (this.operadorDatos.comprobarDatosEnviados(portadorInformacion)) {
                    await this.operadorDatos.efectuarOperacion(portadorInformacion);
                }
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error, {accion: accion}));
            }
        },
        accionEnviarNuevoCaso: async function(contexto) {
            const accion = 'accionEnviarNuevoCaso';
            Base.trazarFlujo(this.constructor.name, accion, 2, '[A]');
            try {
                const { recurso, esquema, operacion, servicio } = contexto;
                const detalleInteraccion = this.controlarAcceso(accion, servicio);
                if (!detalleInteraccion) { return this.rechazarAcceso(accion, detalleInteraccion); }
                const valores = this.interfazUsuario.receptorUI.obtenerDatosFormulario(`form_${esquema}`);
                const portadorInformacion = new PortadorInformacion(this.gestorEstados);
                portadorInformacion.prepararPeticion(operacion, {
                    recurso: recurso,
                    servicio: servicio,
                    valores: valores,
                    formulario: esquema
                });
                await this.procesarEsquemas(portadorInformacion);
                if (this.operadorDatos.comprobarDatosEnviados(portadorInformacion)) {
                    await this.operadorDatos.efectuarOperacion(portadorInformacion);
                }
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error, {accion: accion}));
            }
        },
        accionAbrirServicio: async function(contexto) {
            const accion = 'accionAbrirServicio';
            Base.trazarFlujo(this.constructor.name, accion, 2, '[A]');
            try {
                const { recurso, esquema, operacion, servicio, plantilla } = contexto;
                const detalleInteraccion = this.controlarAcceso(accion, servicio);
                if (!detalleInteraccion) { return this.rechazarAcceso(accion, detalleInteraccion); }
                this.gestorEstados.emitirEventoInformacion('ENVIANDO_PETICION', contexto);
                const portadorInformacion = new PortadorInformacion(this.gestorEstados);
                portadorInformacion.prepararPeticion(operacion, {
                    informe: esquema,
                    recurso: recurso,
                    servicio: servicio,
                    plantilla: plantilla
                });
                await this.procesarEsquemas(portadorInformacion);
                await this.operadorDatos.efectuarOperacion(portadorInformacion);
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error, {accion: accion}));
            }
        },
        accionNuevoCaso: async function(contexto) {
            const accion = 'accionNuevoCaso';
            Base.trazarFlujo(this.constructor.name, accion, 2, '[A]');
            try {
                const { esquema, servicio, plantilla } = contexto;
                const detalleInteraccion = this.controlarAcceso(accion, servicio);
                if (!detalleInteraccion) { return this.rechazarAcceso(accion, detalleInteraccion); }
                const portadorInformacion = new PortadorInformacion(this.gestorEstados);
                portadorInformacion.prepararPeticion(operacion, {
                    servicio: servicio,
                    formulario: esquema,
                });
                const esquemas = await this.procesarEsquemas(portadorInformacion);
                const datos = { caso: {} };
                if (esquemas.formulario) {
                    const contenido = this.interfazUsuario.generarFormularioCaso(datos, esquemas, plantilla);
                    this.interfazUsuario.abrirVentanaModal(contenido);
                } else {
                    this.interfazUsuario.mostrarInformacion(
                        this.interfazUsuario.traductorIdiomas._('ERROR_EN_DATOS_O_ESQUEMAS'),
                        Base.Mensajes.ERROR
                    );
                }
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error, {accion: accion}));
            }
        },
        accionCambiarIdioma: async function(contexto) {
            Base.trazarFlujo(this.constructor.name, 'accionCambiarIdioma', 2, '[A]');
            try {
                const { idioma } = contexto;
                await this.interfazUsuario.traductorIdiomas.cambiarIdioma(idioma);
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error));
            }
        },
        accionEnviarNuevoInput: async function(contexto) {
            Base.trazarFlujo(this.constructor.name, 'accionEnviarNuevoInput', 2, '[A]');
            try {
                const { recurso, operacion, selector, servicio } = contexto;
                const contenido = this.interfazUsuario.receptorUI.obtenerValorCampo(selector);
                if (contenido) {
                    const portadorInformacion = new PortadorInformacion(this.gestorEstados);
                    portadorInformacion.prepararPeticion(operacion, {
                        recurso: recurso,
                        servicio: servicio,
                        selector: selector,
                        valores: { 'contenido': contenido }
                    });
                    await this.operadorDatos.efectuarOperacion(portadorInformacion);
                }
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error));
            }
        },
        accionCopiarTexto: function(contexto) {
            Base.trazarFlujo(this.constructor.name, 'accionCopiarTexto', 2, '[A]');
            try {
                const { selector } = contexto;
                const contenido = this.interfazUsuario.receptorUI.obtenerTextoElemento(selector);
                if (contenido) {
                    this.interfazUsuario.manipuladorUI.copiarContenido(contenido);
                }
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error));
            }
        },
        accionAjustarCampo: function(contexto) {
            Base.trazarFlujo(this.constructor.name, 'accionAjustarCampo', 2, '[A]');
            try {
                const { selector } = contexto;
                this.interfazUsuario.manipuladorUI.ajustarAlturaCampo(selector);
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error));
            }
        },
        accionProbar: async function() {
            Base.trazarFlujo(this.constructor.name, 'accionProbar', 2, '[A]');
            const contenido = 'CONTENIDO';
            this.interfazUsuario.abrirVentanaModal(contenido);
        },
        guardarEnHistorial: async function(interaccion) {
        },
        navegarHaciaInteraccion: async function(opcion, interaccion) {
        }
        };
    }
    reaccionesCoordinador() {
        // Funciones para "reacciones" que otorgan funcionalidad al servicio. Se inyectan en "CoordinadorGeneral".
        return {
        reaccionCasoAgregado: async function(informacion) {
            Base.trazarFlujo(this.constructor.name, 'reaccionCasoAgregado', 2, '[R]');
            try {
                if (informacion.tipo && informacion.mensaje) {
                    this.interfazUsuario.mostrarInformacion(informacion.mensaje, informacion.tipo);
                }
                await this.lanzarInteraccion('accionSolicitarListaCasos', informacion.servicio);
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error, {}));
            }
        },
        reaccionCasoEditado: async function(informacion) {
            Base.trazarFlujo(this.constructor.name, 'reaccionCasoEditado', 2, '[R]');
            try {
                if (informacion.tipo && informacion.mensaje) {
                    this.interfazUsuario.mostrarInformacion(informacion.mensaje, informacion.tipo);
                }
                await this.lanzarInteraccion('accionSolicitarListaCasos', informacion.servicio);
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error, {}));
            }
        },
        reaccionCasoEliminado: async function(informacion) {
            Base.trazarFlujo(this.constructor.name, 'reaccionCasoEliminado', 2, '[R]');
            try {
                if (informacion.tipo && informacion.mensaje) {
                    this.interfazUsuario.mostrarInformacion(informacion.mensaje, informacion.tipo);
                }
                await this.lanzarInteraccion('accionSolicitarListaCasos', informacion.servicio);
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error, {}));
            }
        },
        reaccionListaRecibida: async function(informacion) {
            Base.trazarFlujo(this.constructor.name, 'reaccionListaRecibida', 2, '[R]');
            try {
                if (informacion.datos && informacion.esquemas) {
                    this.interfazUsuario.actualizarListaCasos(informacion.datos, informacion.esquemas, informacion.plantilla);
                } else {
                    this.interfazUsuario.mostrarInformacion(
                        this.interfazUsuario.traductorIdiomas._('ERROR_EN_DATOS_O_ESQUEMAS'),
                        Base.Mensajes.ERROR
                    );
                }
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error, {}));
            }
        },
        reaccionCasoRecibido: async function(informacion) {
            Base.trazarFlujo(this.constructor.name, 'reaccionCasoRecibido', 2, '[R]');
            try {
                if (informacion.datos && informacion.esquemas.formulario) {
                    const contenido = this.interfazUsuario.generarFormularioCaso(datos, esquemas, plantilla);
                    this.interfazUsuario.abrirVentanaModal(contenido);
                } else {
                    this.interfazUsuario.mostrarInformacion(
                        this.interfazUsuario.traductorIdiomas._('ERROR_EN_DATOS_O_ESQUEMAS'),
                        Base.Mensajes.ERROR
                    );
                }
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error, {}));
            }
        },
        reaccionServicioAbierto: async function(informacion) {
            Base.trazarFlujo(this.constructor.name, 'reaccionServicioAbierto', 2, '[R]');
            try {
                if (informacion.datos && informacion.esquemas) {
                    this.interfazUsuario.actualizarPanelContenidos(informacion.datos, informacion.esquemas, informacion.plantilla);
                } else {
                    this.interfazUsuario.mostrarInformacion(
                        this.interfazUsuario.traductorIdiomas._('ERROR_EN_DATOS_O_ESQUEMAS'),
                        Base.Mensajes.ERROR
                    );
                }
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error, {}));
            } finally {
                this.gestorEstados.emitirEventoInformacion('RESPUESTA_RECIBIDA', {});
            }
        },
        reaccionResultadoNuevoInput: function(informacion) {
            Base.trazarFlujo(this.constructor.name, 'reaccionResultadoNuevoInput', 2, '[R]');
            //TODO: Pendiente
            try {
            } catch (error) {
                this.informarErrorServicio(this.manejadorErrores.procesarError(error, {}));
            }
        },
        reaccionRespuestaRecibidaCoordinador: function() {
            //console.warn('reaccionRespuestaRecibidaCoordinador');
        }
        };
    }
    extenderInterfazUsuario() {
        return {
        actualizarListaCasos: function(datos, esquemas, plantilla='plantillaLista', selector='lista_casos') {
            Base.trazarFlujo(this.constructor.name, 'actualizarListaCasos', 1, selector);
            if (!datos.lista?.casos || !Array.isArray(datos.lista.casos)) { return; }
            const elemento = this.ELEMENTOS.get(selector);
            if (!elemento) { return; }
            let contenido = this.procesadorPlantillas.representarListaCasos(
                datos, esquemas, plantilla
            );
            contenido = this.traductorIdiomas.aplicarTraduccion(contenido);
            this.manipuladorUI.actualizarContenido(elemento, contenido);
            this.manipuladorUI.cambiarVisibilidad(elemento, true);
        },
        generarFormularioCaso: function(datos, esquemas, plantilla='plantillaCaso') {
            Base.trazarFlujo(this.constructor.name, 'generarFormularioCaso', 1);
            if (!datos.caso || !Array.isArray(datos.caso)) { return; }
            let contenido = this.procesadorPlantillas.representarFormularioCaso(
                datos, esquemas, plantilla
            );
            contenido = this.procesadorPlantillas.reemplazarDatos(contenido, datos);
            contenido = this.procesadorPlantillas.sustituirFechaHora(contenido);
            contenido = this.traductorIdiomas.aplicarTraduccion(contenido);
            return contenido;
        },
        actualizarPanelContenidos: function(datos, esquemas, plantilla='plantillaPanel') {
            Base.trazarFlujo(this.constructor.name, 'actualizarPanelContenidos', 1);
            let contenido = this.procesadorPlantillas.representarContenido(plantilla, {});
            const elemento = this.ELEMENTOS.get('area_cuerpo');
            if (elemento && contenido) {
                contenido = this.procesadorPlantillas.reemplazarDatos(contenido, datos);
                contenido = this.procesadorPlantillas.sustituirFechaHora(contenido);
                contenido = this.traductorIdiomas.aplicarTraduccion(contenido);
                this.manipuladorUI.actualizarContenido(elemento, contenido);
                this.manipuladorUI.cambiarVisibilidad(elemento, true);
            }
        },
        reaccionEnviandoPeticion: function() {
            this.alternarEsperando(true);
            this.cerrarMenusAbiertos();
        },
        reaccionRespuestaRecibidaInterfaz: function() {
            //console.warn('reaccionRespuestaRecibidaInterfaz');
            this.alternarEsperando(false, '');
        },
        mostrarErroresValidacion: function(errores) {
            Base.trazarFlujo(this.constructor.name, 'mostrarErroresValidacion', 1, errores);
            if (!errores) return;
            Object.entries(errores).forEach(([campo, mensaje]) => {
                const areaMensaje = this.manipuladorUI.seleccionar(`.campo-${campo} .invalid-feedback`);
                const campoFormulario = this.manipuladorUI.seleccionar(`.campo-${campo} [name="${campo}"]`);
                if (campoFormulario) {
                    this.manipuladorUI.manejarClasesElemento('quitar', `is-valid`, campoFormulario);
                    this.manipuladorUI.manejarClasesElemento('agregar', `is-invalid`, campoFormulario);
                }
                this.manipuladorUI.actualizarContenido(areaMensaje, mensaje);
                this.manipuladorUI.resaltarSeleccionados(`.campo-${campo}`, true);
            });
        },
        quitarErroresValidacion: function(selector) {
            Base.trazarFlujo(this.constructor.name, 'quitarErroresValidacion', 1, selector);
            this.manipuladorUI.resaltarSeleccionados(`#${selector} .area-campo`, false);
            const camposFormulario = this.manipuladorUI.seleccionar(`#${selector} .form-control, #${selector} .form-select`, 'todos');
            camposFormulario.forEach(campo => {
                this.manipuladorUI.manejarClasesElemento('quitar', `is-valid, is-invalid`, campo);
            });
        }
        };
    }
    extenderProcesadorPlantillas() {
        return {
        representarListaCasos: function(datos, esquemas, plantilla) {
            Base.trazarFlujo(this.constructor.name, 'representarListaCasos', 2, plantilla);
            //TODO: falta que use esquemas de INFORME + DICCIONARIO para hacer dinámicas las plantillas. Corregir  elemento y conjunto
            if (!this.plantillas.has(plantilla) || !datos?.lista) {
                return '';
            }
            const elemento = this.plantillas.get(plantilla);
            const conjunto = this.plantillas.get(plantilla);
            let contenido = datos.lista.casos.map(caso => {
                let baseCaso = elemento.innerHTML;
                //TODO: evaluar si los reemplazos (()) en "baseCaso" se cambian por {{}} con sustituirClaves
                /* Object.entries(caso).forEach(([clave, valor]) => {
                    baseCaso = baseCaso.replace(new RegExp(`\\(\\(${clave}\\)\\)`, 'g'), String(valor));
                }); */
                baseCaso = this.sustituirClaves(baseCaso, caso);
                return `<div class="caso" data-id="${caso.id}" data-recurso="${caso.recurso}">${baseCaso}</div>`;
            }).join('');
            const baseLista = conjunto.innerHTML;
            if (baseLista.includes('((ListaCasos))')) {
                contenido = baseLista.replace('((ListaCasos))', contenido);
            }
            return this.traductorIdiomas.aplicarTraduccion(contenido);
        },
        representarFormularioCaso: function(datos, esquemas, plantilla) {
            Base.trazarFlujo(this.constructor.name, 'representarFormularioCaso', 2, plantilla);
            let contenido = '';
            if (this.plantillas.has(plantilla)) {
                const elemento = this.plantillas.get(plantilla);
                if (elemento && datos) {
                    //TODO: pendiente de implementar usando esquemas de FORMULARIO + DICCIONARIO para hacer dinámica la plantilla
                    contenido = this.traductorIdiomas.aplicarTraduccion(contenido);
                }
            }
            return contenido;
        }
        };
    }
    extenderOperadorDatos() {
        return {
        reaccionRespuestaRecibidaOperador: function() {
            //console.warn('reaccionRespuestaRecibidaOperador');
        }
        };
    }
    validadoresDatos() {
        return {};
    }
}
export const modulo = new DefinicionModuloBase();
